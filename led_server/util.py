#!/usr/bin/python3

import numpy as np
import math

colors = { 
    'white': (255,255,255),
    'red': (255,0,0),
    'green': (0,255,0),
    'blue': (0,0,255),
    'cyan': (0,255,255),
    'magenta': (255,0,255),
    'yellow': (255,255,0)
}

def transform_brightness(rgb, br):
    r,g,b = rgb
    return (br if r > 0 else 0, br if g > 0 else 0, br if b > 0 else 0) 

def fft(data=None,trimBy=10,logScale=False,divBy=100,fs=32000,chunk=2048):
        left,right=np.split(np.abs(np.fft.fft(data)),2)
        ys=np.add(left,right[::-1])
        if logScale:
            ys=np.multiply(20,np.log10(ys))
        xs=np.arange(chunk/2,dtype=float)
        if trimBy:
            i=int((chunk/2)/trimBy)
            ys=ys[:i]
            xs=xs[:i]*fs/chunk
        if divBy:
            ys=ys/float(divBy)
        return xs,ys

def get_rgb_vol(vol, rgb):
    vol -= 800
    if vol <= 0:
        return (0,0,0)
    br = min(int(255*vol/10000),255)
    return transform_brightness(rgb, br)

def get_rgb_freq_vol(vol, freq):
    vol -= 800
    if vol <= 0:
        return (0,0,0)
    vol = min(int(255*vol/10000),255)
    freq -= 200
    if freq > 800:
        freq = 800
    if freq < 0: 
        freq = 0
    blue = int(vol*freq/800)
    red = int(vol*(1-freq/800))
    return (red,vol,blue)
