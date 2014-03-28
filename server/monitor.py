#!/usr/bin/env python
import os
import json
import sqlite3
import sys
import socket
import urllib

from flask import Flask, Response, render_template, request

from settings import (DATABASE_NAME, FILES_TABLE_NAME, CLIENTS_TABLE_NAME,
                      CRITICAL_SETTINGS_FILE, RSYNC_BASE_DIR, CLIENT_NAME,
                      CONTROL_SIGNAL_RECEIVER_PORT, BACKUP_PATH)
from user_settings import HEARTBEAT_TIMING
from persistent_store import PersistentStore, set_critical_settings
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.debug = True
app.config['PORT'] = 5000


@app.route('/')
def index():
    values_to_page = { 'heartbeat_timing': HEARTBEAT_TIMING,
                       'backup_path': BACKUP_PATH }
    return render_template('landing.html', **values_to_page)


@app.route('/heartbeat')
def check_heartbeat():
    with open('heartbeat_record.record') as f:
        last_record = f.readlines()[-1]
    if "OK" in last_record:
        return "ALIVE"
    elif "DEAD" in last_record:
        return "DEAD"
    elif "TAMPERED" in last_record:
        return last_record
    return "UNKNOWN"

@app.route('/settings', methods=['POST', 'GET'])
def settings():
    storage = PersistentStore(DATABASE_NAME)

    if request.method == 'POST':
        # Extract all values from the POST request. Also check if they are
        # given. Otherwise, don't set the corresponding variables. Doing so
        # will cause to return an error to the frontend
        values_to_ui = {}
        if request.values['paths']:
            paths = request.values['paths'].split(',')
            try:
                sock = socket.socket()
                sock.connect((CLIENT_NAME, CONTROL_SIGNAL_RECEIVER_PORT))
                sock.send(json.dumps({'paths': {'client': CLIENT_NAME,
                                                'paths': json.dumps({'paths': paths}),
                                                'target_table': FILES_TABLE_NAME }
                                     }))
                sock.close()
            except:
                pass
            values_to_ui['paths'] = ','.join(paths)
        if request.values['client_ip']:
            client_ip = request.values['client_ip']
            values_to_ui['client_ip'] = client_ip
        if request.values['client_username']:
            client_username = request.values['client_username']
            values_to_ui['client_username'] = client_username
        if request.values['server_port']:
            server_port = request.values['server_port']
            values_to_ui['server_port'] = server_port
        if request.values['log_collection_timing']:
            log_collection_timing = request.values['log_collection_timing']
            values_to_ui['log_collection_timing'] = log_collection_timing
        if request.values['heartbeat_timing']:
            heartbeat_timing = request.values['heartbeat_timing']
            values_to_ui['heartbeat_timing'] = heartbeat_timing

        # Set all values in the database and settings file
        try:
            storage.set_paths(FILES_TABLE_NAME, client_ip, paths)
            storage.set_client_and_username(CLIENTS_TABLE_NAME, client_ip,
                                            client_username)
            set_critical_settings(CRITICAL_SETTINGS_FILE,
                                  SERVER_PORT=server_port,
                                  LOG_COLLECT_INTERVAL=log_collection_timing,
                                  HEARTBEAT_TIMING=heartbeat_timing)
            values_to_ui['saved'] = True
        except:
            print sys.exc_info()
            values_to_ui['error_message'] = "Error in saving. Check if "\
              "all fields are properly filled"
            values_to_ui['saved'] = False
            return render_templae('settings.html', **values_to_ui)
        return render_template('settings.html', **values_to_ui)

    client_ip, username = storage.get_clients_and_usernames(CLIENTS_TABLE_NAME)[0]
    paths = ','.join(storage.get_paths(FILES_TABLE_NAME, client_ip))
    server_port = getattr(__import__(CRITICAL_SETTINGS_FILE), 'SERVER_PORT')
    log_collection_timing = getattr(__import__(CRITICAL_SETTINGS_FILE),
                                    'LOG_COLLECT_INTERVAL')
    heartbeat_timing = getattr(__import__(CRITICAL_SETTINGS_FILE),
                               'HEARTBEAT_TIMING')

    values_to_ui = {'paths': paths, 'client_ip': client_ip,
                    'client_username': username,
                    'server_port': server_port,
                    'log_collection_timing': log_collection_timing,
                    'heartbeat_timing': heartbeat_timing }

    values_to_ui['saved'] = None
    return render_template('settings.html', **values_to_ui)

@app.route('/filesystem', methods=['POST'])
def filesystem():
    r=['<ul class="jqueryFileTree" style="display: none;">']
    try:
        r=['<ul class="jqueryFileTree" style="display: none;">']
        d=urllib.unquote(request.values.get('dir', BACKUP_PATH))
        for f in os.listdir(d):
            ff=os.path.join(d,f)
            if os.path.isdir(ff):
                r.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
            else:
                e=os.path.splitext(f)[1][1:] # get .ext and remove dot
                r.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (e,ff,f))
        r.append('</ul>')
    except Exception,e:
        r.append('Could not load directory: %s' % str(e))
    r.append('</ul>')
    return ''.join(r)
   
app.wsgi_app = ProxyFix(app.wsgi_app)
    
if __name__ == '__main__':
   app.run()

