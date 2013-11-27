# -*- coding: UTF-8 -*-

import requests
import flask
import logging
import json

from logging import debug, error, warning

from MultiNest.Config import conf

logging.basicConfig(level=logging.DEBUG)


def submit(payload):
    """
    Submit MultiNest job to the AppGateway.

    :param payload: dict with job parameters to be passed in JSON format to
                    AppGateway.
    """

    # Rewrite payload data required for array variables
    req_data = {
        'service': "MultiNest",  # Service name
        'api': 1.0,  # API level
        'input': payload
    }
    # User requested a predefined set
    if payload['use_sets']:
        # One of predefined sets
        if payload['sets'] != 'user_set':
            req_data['input'][payload['sets']] = 1
        # User defined set - rewrite list of points into 4 lists of coordinates
        else:
            try:
                _user_data = json.loads(payload['user_set'])
            except Exception as e:
                flask.flash(u"Błędny format danych wejściowych: %s" % e,
                            "error")
                return flask.redirect(flask.url_for('submit'))

            _x = []
            _y = []
            _xsig = []
            _ysig = []

            for _v in _user_data:
                if len(_v) < 2:
                    flask.flash(u"Błędny format danych wejściowych. Każdy "
                                u"punkt musi mieć określone minimum "
                                u"współrzędne x i y.", "error")
                    return flask.redirect(flask.url_for('submit'))
                _x.append(_v[0])
                _y.append(_v[1])
                # Allow for point definitions that consist of coordinates only.
                # The sigmas will be set to a deafoult of 3.0.
                if len(_v) < 3:
                    _xsig.append(3.0)
                else:
                    _xsig.append(_v[2])
                if len(_v) < 4:
                    _ysig.append(3.0)
                else:
                    _ysig.append(_v[3])

            req_data['input']['node_list_x'] = _x
            req_data['input']['node_list_y'] = _y
            req_data['input']['node_list_xsigma'] = _xsig
            req_data['input']['node_list_ysigma'] = _ysig

    if 'use_sets' in req_data['input'].keys():
        del req_data['input']['use_sets']
    if 'sets' in req_data['input'].keys():
        del req_data['input']['sets']
    if 'user_set' in req_data['input'].keys():
        del req_data['input']['user_set']

    debug("Will submit request: %s" % req_data)
    url = conf.gw_url + "/submit"
    # Header has to define payload data type "application/json"
    headers = {'content-type': 'application/json'}
    try:
        # Set verify=False as we use self signed cert. With CA signed cert add
        # cafile as value of the verify attribute
        r = requests.post(url, data=json.dumps(req_data), headers=headers,
                          verify=False)
    except Exception as e:
        # Flash an error message
        flask.flash(u"Brak połączenia z serwerem aplikacji: %s" % e, "error")
        # Render main page
        return flask.redirect(flask.url_for('index'))

    # AppGateway should return job ID which starts with service name
    if r.text.startswith('MultiNest'):
        flask.flash(u"Zadanie wysłane pomyślnie", "success")
        # Lets set a cookie with the job ID. For that we have to generate the
        # resopnse by hand. While at it lets redirect user to the monitor page.
        resp = flask.make_response(flask.redirect(flask.url_for('monitor')))
        resp.set_cookie('CISMultiNestJobID', r.text)
        return resp

    # We did not recieve job ID. Flash the AppGateway response as an error to
    # the user on the main page.
    flask.flash(r.text, "error")
    return flask.redirect(flask.url_for('index'))


def status():
    """Query the AppGateway for the job status."""
    # Polish state names
    _states = (
        u'Oczekuję na zadania',
        u'Zadanie oczekuje w kolejce',
        u'Obliczenia w toku',
        u'Finalizacja obliczeń',
        u'Obliczenia zakończone',
        u'Błąd',
    )
    # Job ID should be stored in the users browser as a cookie. Retrive it.
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    # Job ID recieved
    if _jid is not None:
        # Query the AppGateway
        url = conf.gw_url + "/status/" + _jid
        # Set verify to false for now as AppGateway is running with self-signed
        # certificate
        r = requests.get(url, verify=False)
        if r.text.startswith('Waiting') or \
           r.text.startswith('Queued'):
            _st = 2
            _type = 'queued'
        elif r.text.startswith('Running'):
            _st = 3
            _type = 'running'
        elif r.text.startswith('Closing') or \
             r.text.startswith('Cleanup'):
            _st = 4
            _type = 'cleanup'
        elif r.text.startswith('Done'):
            _st = 5
            _type = 'done'
        else:
            _st = 6
            _type = 'error'

        # Build a result dictionary that will be parsed by client JavaScript
        # state - defines numeric types of the state - used javascript to
        #         identify active and finished states
        # type - defines text types of the state - used by CSS for visual id
        # desc - state description
        # msg - message from AppGateway
        _result = {
            'state': _st, 'type': _type, 'desc': _states[_st-1], 'msg': r.text
        }
        return _result

    _result = {'state': 1, 'type': 'ready', 'desc': _states[0], 'msg': ''}
    return _result


def progress():
    """Query AppGateway for job progress."""
    # Standard output when progress is not ready
    _result = {'job_output': 'Waiting ...'}
    # Get job ID from browser cookie
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        # Query AppGateway
        url = conf.gw_url + "/progress/" + _jid
        r = requests.get(url, verify=False)
        # We got an error flash it to the user
        if r.text.startswith('Error'):
            flask.flash(r.text, 'error')
        # No error - update the output
        _result['job_output'] = r.text
    else:
        flask.flash(u"Brak aktywnego zadania: nie mogę wyświetlić stanu "
                    u"obliczeń", "error")
        # Send "Empty Session" if no job ID is stored in the user browser
        _result['job_output'] = 'Empty Session'

    return _result


def output():
    """Query AppGateway for the job results"""
    # Get job ID from browser cookie
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        # Query AppGateway
        url = conf.gw_url + "/output/" + _jid
        r = requests.get(url, verify=False)
        # We got an error flash it to the user
        if r.text.startswith('Error'):
            flask.flash(r.text)
            return flask.redirect(flask.url_for('index'))
        else:
        # No error render the output results
            debug(r.text)
            _state = status()
            return flask.render_template("output.html",
                                         url=r.text,
                                         state=_state)

    flask.flash(u"Brak zakończonego zadania: nie mogę wyświetlić wyników",
                "error")
    return flask.redirect(flask.url_for('index'))


def kill():
    """Ask AppGateway to kill the job"""
    # Get job ID from browser cookie
    _jid = flask.request.cookies.get('CISMultiNestJobID')
    if _jid is not None:
        # Query AppGateway
        url = conf.gw_url + "/kill/" + _jid
        r = requests.get(url, verify=False)
        # We got an error flash it to the user
        if r.text.startswith('Error'):
            flask.flash(r.text)
            return flask.redirect(flask.url_for('index'))
        else:
        # No error render the output results
            debug(r.text)
            flask.flash(r.text)
            flask.flash("Zadanie zarzymane")
            return flask.redirect(flask.url_for('index'))

    flask.flash(u"Brak aktualnego zadania: nie mogę wysłać komendy kill",
                "error")
    return flask.redirect(flask.url_for('index'))
