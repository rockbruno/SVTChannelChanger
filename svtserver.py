from big_red import BigRedButton
import socket
import serial
import time
import threading
import sys
import signal
import os
import ctypes

class KeyPresser:
    stop = False

    def start(self):
        thread = threading.Thread(target=self.fullscreen_procedure, args=())
        thread.start()

    def fullscreen_procedure(self):
        print 'Initiating procedure'
        os.system('sleep 15')
        if self.stop:
            print 'Killing ~some~ procedure because it was marked to stop'
            return
        os.system('xdotool key ctrl+shift+j')
        javascript_prefix = 'document.getElementsByClassName('
        javascript_middle = "VideoPlayerNew__fullscreen-button___P3G0L VideoPlayerNew__icon-defaults___2CUBE VideoPlayerNew__icon-spacing___3fSIa VideoPlayerNew__icon-sizing___Aalj7 VideoPlayerNew__icon-coloring___2-57r"
        javascript_suffix = ")[0].click()"
        os.system('sleep 5')
        if self.stop:
            print 'Killing ~some~ procedure because it was marked to stop'
            return
        os.system('xdotool type "' + javascript_prefix + '"')
        os.system('xdotool key quotedbl')
        os.system('xdotool type "' + javascript_middle + '"')
        os.system('xdotool key quotedbl')
        os.system('xdotool type "' + javascript_suffix + '"')
        os.system('sleep 10')
        if self.stop:
            print 'Killing ~some~ procedure because it was marked to stop'
            return
        os.system('xdotool key KP_Enter')
        os.system('sleep 10')
        if self.stop:
            print 'Killing ~some~ procedure because it was marked to stop'
            return
        os.system('xdotool key ctrl+shift+j')

class Button(BigRedButton):
    
    channels = ["svt1", "svt2", "svtbarn", "kunskapskanalen"]
    curr_channel = 0;
    url_prefix = "https://www.svtplay.se/kanaler/"
    url_suffix = "?start=auto"
    key_presser = 0

    def start(self):
        self.key_presser = KeyPresser()

    def on_unknown(self):
        print 'The button is in an unknown state'

    def on_cover_open(self):
        print 'The cover is now open'
        self.close_all()
        self.open_browser()

    def on_cover_close(self):
        print 'The cover has been closed'
        self.close_all()

    def on_button_release(self):
        print 'The button has been released'
        self.advance_channel_id()
        self.open_browser()

    def on_button_press(self):
        print 'The button has been pressed'
        self.close_all()
        
    def close_all(self):
        self.key_presser.stop = True;
        os.system('killall chromium-browser')
        
    def advance_channel_id(self):
        chan = self.channels[self.curr_channel]
        self.curr_channel = (self.curr_channel + 1) % len(self.channels)

    def open_browser(self):
        new_url = self.url_prefix + self.channels[self.curr_channel] + self.url_suffix
        os.system('lxterminal --command chromium-browser ' + new_url)
        self.key_presser = KeyPresser()
        self.key_presser.start()

print 'Nenezudo\'s channel server started'
button = Button()
button.start()
while True:
    try:
        button.run()
    except Exception as e:
        print "Exception raised: {}".format(e)
        print 'Avoided USB exception'
