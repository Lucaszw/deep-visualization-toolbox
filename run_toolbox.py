#! /usr/bin/env python

import os
from live_vis import LiveVis
from bindings import bindings

from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import threading
import base64

import json
from settings import Settings
from pprint import pprint

#
# try:
#     import settings
# except:
#     print '\nError importing settings.py. Check the error message below for more information.'
#     print "If you haven't already, you'll want to copy one of the settings_local.template-*.py files"
#     print 'to settings_local.py and edit it to point to your caffe checkout. E.g. via:'
#     print
#     print '  $ cp models/caffenet-yos/settings_local.template-caffenet-yos.py settings_local.py'
#     print '  $ < edit settings_local.py >\n'
#     raise

# if not os.path.exists(settings.caffevis_caffe_root):
#     raise Exception('ERROR: Set caffevis_caffe_root in settings.py first.')

webapp = Flask(__name__)
webapp.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(webapp)
lv = None
td = None

def forget_lv():
    global lv
    del(lv)
    lv = None

def setup_lv(settings=None,onChange=None):
    print("SETTINGS:")
    print(settings.caffevis_caffe_root)
    global lv
    lv = LiveVis(settings=settings,onChange=onChange)


def main():
    global td

    @webapp.route('/')
    def index():
        return render_template('index.html')

    # Handler sent to LivVis and expets base64 image data:
    def change_handler(data):
        socketio.emit('re-draw panel', {'data': data })

    # Called when help button, or new image is called
    @socketio.on('mode changed')
    def mode_was_changed(message):
        # message['data'] contains a tag for the
        # assoicated key shortcut used for this action
        lv.handle_key_pre_apps(tag=message['data'])

        # For help, you cannot just alert the app that a key
        # has been pressed but you also have to change the help_mode variable
        # (which the app reads when it tries to re-draw)
        if message['data'] == 'help':
            if lv.help_mode == False:
                lv.help_mode = True
            else:
                lv.help_mode = False
            lv.state.drawing_stale = True

    # Handles key methods for keys whos listeners are in caffevis
    # All these keys behave the same way as in that you send a tag, and
    # call for a re-paint
    @socketio.on('key pressed')
    def key_was_pressed(message):
        key = message['data']
        lv.state.handle_key(tag=message['data'])
        lv.state.drawing_stale = True

    # When connection is established, send the default settings as json
    # data (so that the user doesn't have to set every variable each time
    # they want to run the app)
    @socketio.on('connect')
    def connection_established(message={}):
        with open('settings.json') as data_file:
            data = json.load(data_file)
        emit('has connected', {'data': data }, broadcast=True)


    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')


    def run(message={}):
        # Run the actual app in a separate thread. Send in the change_handler
        # to communicate between LV, and the webapp
        print("MESSAGER")
        print(message)

        settings = Settings(message)
        setup_lv(settings=settings,onChange=change_handler)
        help_keys, _ = bindings.get_key_help('help_mode')
        quit_keys, _ = bindings.get_key_help('quit')
        print '\n\nRunning toolbox. Push %s for help or %s to quit.\n\n' % (help_keys[0], quit_keys[0])
        lv.run_loop()

    # When the start button is pressed in the webapp, start the thread
    @socketio.on('start toolbox')
    def start_requested(message={}):
        stop_requested()
        kwargs = {"message": message}
        td = threading.Thread(target=run,kwargs=kwargs)
        td.start()

    # This method is used for ending the App Thread (not WebApp)
    @socketio.on('stop toolbox')
    def stop_requested(message={}):
        if lv != None:
            lv.quit = True
            lv.state.drawing_stale = True
            for app_name, app_class in lv.app_classes.iteritems():
                lv.apps[app_name].quit()
                del(lv.apps[app_name])
            forget_lv()

    @webapp.route('/stop')
    def stop():
        stop_requested()
        socketio.server.stop()

    socketio.run(webapp,host='0.0.0.0',port=8083)


if __name__ == '__main__':
    main()
