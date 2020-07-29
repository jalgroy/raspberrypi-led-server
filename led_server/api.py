#!/usr/bin/python3

import time
import pyaudio
import audioop
import pigpio
import numpy as np
import math
import threading
from flask import Flask

from util import fft, get_rgb_vol, get_rgb_freq_vol, colors, transform_brightness

R = 17
G = 22
B = 24

fs = 32000
sample_format = pyaudio.paInt16
chunk = 2048
channels = 1

pi = pigpio.pi()

p = pyaudio.PyAudio()

app = Flask(__name__)

led_thread = None

def set_rgb(rgb):
    r,g,b = rgb
    pi.set_PWM_dutycycle(R, r)
    pi.set_PWM_dutycycle(G, g)
    pi.set_PWM_dutycycle(B, b)

def music_loop(rgb):
    t = threading.currentThread()
    mic_stream = p.open(format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True)

    while getattr(t,'do_run',True):
        # Read data from microphone
        data = np.fromstring(mic_stream.read(chunk), np.int16)
        xs,ys = fft(data, fs=fs, chunk=chunk)
        freq = np.average(ys, weights=xs)
        vol = audioop.max(data,2)
        set_rgb(get_rgb_vol(vol, rgb))
    mic_stream.close()
    print('Stopping audio loop')

def pulse_loop(rgb):
    t = threading.currentThread()
    i = 0
    up = True
    while getattr(t,'do_run',True):
        set_rgb(transform_brightness(rgb,i))
        if up:
            i += 1
            if i == 255:
                up = False
        else:
            i -= 1
            if i == 0:
                up = True
        time.sleep(0.01)
                

@app.route('/pulse/<color>')
def pulse(color):
    global led_thread
    if led_thread != None:
        led_thread.do_run = False
        led_thread.join()
        led_thread = None
    if color in colors:
        led_thread = threading.Thread(target=pulse_loop, args=(colors[color],))
        led_thread.start()
        return 'Started pulsing ' + color
    else:
        return 'Invalid color ' + color

@app.route('/music/<color>')
def music(color):
    global led_thread
    if led_thread != None:
        led_thread.do_run = False
        led_thread.join()
        led_thread = None
    if color in colors:
        led_thread = threading.Thread(target=music_loop, args=(colors[color],))
        led_thread.start()
        return 'Music mode started with color ' + color
    else:
        return 'Invalid color' + color

@app.route('/color/<color>')
def color(color):
    global led_thread
    if led_thread != None:
        led_thread.do_run = False
        led_thread.join()
        led_thread = None
    if color in colors:
        set_rgb(colors[color])
    else:
        return 'Unknown color'
    return 'Set color to ' + color

@app.route('/off')
def off():
    global led_thread
    if led_thread != None:
        led_thread.do_run = False
        led_thread.join()
        led_thread = None
    set_rgb((0,0,0))
    return 'Leds off'

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
