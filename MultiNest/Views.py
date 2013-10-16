# -*- coding: utf-8 -*-

import json
from flask import render_template, flash, redirect, request, url_for, jsonify,\
        Response
from MultiNest import app, Server
from Forms import SubmitForm

"""
Definition of views - functions handling rendering of specific URLs.
"""

@app.route('/') # Defines URL that will call this function
def index():
    """Main service page."""
    _state = Server.status() # Ask the AppGateway for job state
    # Render HTML template, pass the job state to the renderer
    return render_template('index.html', state=_state)

@app.route('/submit', methods = ['GET', 'POST'])
def submit():
    """Submit form."""
    _state = Server.status()
    # Instantiate the form
    form = SubmitForm()
    # If the input validates pass it to the AppGateway for submission
    if form.validate_on_submit():
        return Server.submit(form.data)
    # No input data recieved yet or data did not validate.
    # Render the form with errors if any.
    return render_template('submit.html',
        title = 'Test Title',
        form = form,
        state = _state)

@app.route('/progress')
def progress():
    """
    Return jobs progress in JSON format.

    Used by AJAX to update the info in real time.
    """
    _result = Server.progress()
    # jsonify does not like our string :/
    return Response(json.dumps(_result), mimetype='application/json')

@app.route('/monitor')
def monitor():
    """Display job status."""
    _state = Server.status()
    _progress = Server.progress() # Extract job progress data from AppGateway
    # No jobs yet. Render the main page with error info
    if _progress['job_output'] == 'Empty Session':
        return redirect(url_for('index'))
    # Handle new line characters
    _progress['job_output'] = _progress['job_output'].replace('\n', '<br/>')
    # Render the HTML template passing state and progress info
    return render_template("monitor.html", state=_state, progress=_progress)

@app.route('/status')
def status():
    """
    Return job status in JSON format.

    Used by AJAX to update the info in real time.
    """
    return jsonify(Server.status())

@app.route('/output')
def output():
    """Return output data URL."""
    return Server.output()

@app.route('/kill')
def kill():
    """Kill current running job."""
    return Server.kill()
