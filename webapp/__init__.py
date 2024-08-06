import os
from flask import Flask

import detect
import register
import respond

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'webapp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # default
    @app.route('/status')
    def index():
        return ''

    # Request memory analysis
    @app.route('/detect',methods = ['POST'])
    def detect():
        ip = request.form['ip']
        hostname = request.form['hostname']
        datetime = request.form['datetime']

        # dump analysis
        is_detected = dump_analysis.analysis(ip, datetime)

        # record on big query the analysis
        register.on_bigquery(hostname, ip, datetime, is_detected)

        # if a malware is detected, respond to host
        if is_detected:
            respond.disable_host_network(ip)

        return


    return app
