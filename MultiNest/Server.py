# -*- coding: UTF-8 -*-

import requests
import flask
import logging
import json

from logging import debug, error, warning

from MultiNest.Config import conf

logging.basicConfig(level=logging.DEBUG)


def submit(payload):
    req_data = {
        'service': "MultiNest",
        'xsize': payload['xsize'],
        'ysize': payload['ysize'],
        'nodes_min': payload['nodes_min'],
        'nodes_max': payload['nodes_max'],
        'sigma_min': payload['sigma_min'],
        'sigma_max': payload['sigma_max'],
        'n_live_points': payload['n_live_points'],
        'max_modes': payload['max_modes'],
        'sampling_efficiency': payload['sampling_efficiency'],
        'evidence_tolerance': payload['evidence_tolerance'],
    }
    if payload['use_sets'] == True:
        if payload['sets'] != 'user_set':
            req_data[payload['sets']] = 1
        else:
            try:
                _user_data = json.loads(payload['user_set'])
            except Exception as e:
                flask.flash(u"Błędny format danych wejściowych: %s" % e, "error")
                return flask.redirect(flask.url_for('submit'))

            _x = []
            _y = []
            _xsig = []
            _ysig = []

            for _v in _user_data:
                if len(_v) < 2:
                    flask.flash(u"Błędny format danych wejściowych. Każdy punkt musi mieć określone minimum współrzędne x i y.", "error")
                    return flask.redirect(flask.url_for('submit'))
                _x.append(_v[0])
                _y.append(_v[1])
                if len(_v) < 3:
                    _xsig.append(3)
                else:
                    _xsig.append(_v[2])
                if len(_v) < 4:
                    _ysig.append(3)
                else:
                    _ysig.append(_v[3])

            req_data['node_list_x'] = _x
            req_data['node_list_y'] = _y
            req_data['node_list_xsigma'] = _xsig
            req_data['node_list_ysigma'] = _ysig

    debug("Will submit request: %s" % req_data)
    url = conf.gw_url + "/submit"
    headers = {'content-type': 'application/json'}
    try:
        # Set verify=False as we use self signed cert. With CA signed cert add
        # cafile as value of the verify attribute
        r = requests.post(url, data=json.dumps(req_data), headers=headers,
                          verify=False)
    except Exception as e:
        flask.flash(u"Brak połączenia z serwerem aplikacji: %s" % e, "error")
        return flask.redirect(flask.url_for('index'))

    if r.text.startswith('MultiNest'):
        flask.flash(u"Zadanie wysłane pomyślnie", "success")
        resp = flask.make_response(flask.redirect(flask.url_for('monitor')))
        resp.set_cookie('CISMultiNestJobID', r.text)
        return resp

    flask.flash(r.text, "error")
    return flask.redirect(flask.url_for('index'))


def status():
    _states = (
        u'Oczekuję na zadania',
        u'Zadanie oczekuje w kolejce',
        u'Obliczenia w toku',
        u'Obliczenia zakończone',
        u'Błąd',
    )
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        url = conf.gw_url + "/status/" + _jid
        r = requests.get(url, verify=False)
        if r.text.startswith('Waiting') or \
           r.text.startswith('Queued'):
            _st = 2
            _type = 'queued'
        elif r.text.startswith('Running'):
            _st = 3
            _type = 'running'
        elif r.text.startswith('Done'):
            _st = 4
            _type = 'done'
        else:
            _st = 5
            _type = 'error'

        _result = {
            'state': _st, 'type': _type, 'desc': _states[_st-1], 'msg': r.text
        }
        return _result

    _result = {'state': 1, 'type': 'ready', 'desc': _states[0], 'msg': ''}
    return _result


def progress():
    _result = {'job_output': 'Waiting ...'}
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        url = conf.gw_url + "/progress/" + _jid
        r = requests.get(url, verify=False)
        if r.text.startswith('Error'):
            flask.flash(r.text, 'error')
        _result['job_output'] = r.text
    else:
        flask.flash(u"Brak aktywnego zadania: nie mogę wyświetlić stanu "
                    u"obliczeń", "error")
        _result['job_output'] = 'Empty Session'

    return _result


def output():
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        url = conf.gw_url + "/output/" + _jid
        r = requests.get(url, verify=False)
        if r.text.startswith('Error'):
            flask.flash(r.text)
            return flask.redirect(flask.url_for('index'))
        else:
            debug(r.text)
            _state = status()
            return flask.render_template("output.html",
                                         url=r.text,
                                         state=_state)

    flask.flash(u"Brak zakończonego zadania: nie mogę wyświetlić wyników",
                "error")
    return flask.redirect(flask.url_for('index'))
