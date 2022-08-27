@@ -0,0 +1,167 @@
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 14:36:50 2020

@author: Danny
"""

import pyaudio
import numpy as np
import keyboard
from pynput.keyboard import Listener
import math

SAMPLE_RATE = 15000
CHANNELS = 1

## SoundMachine class to create thread for sound output, send sound signals
class SoundMachine(object):
    
    ## sample_rate = 44100, channel_num = 1 (mono audio)
    def __init__(self, sample_rate, channel_num):
        self.sample_rate = sample_rate
        self.channel_num = channel_num
    
    ## Initialise SoundMachine with PyAudio, start streaming thread
    def startSoundMachine(self):
        self.p = pyaudio.PyAudio()
    
        ## Streaming thread - sets bit depth (format), channel, rate, and sets output
        self.stream = self.p.open(format = pyaudio.paFloat32,
                    channels = self.channel_num,
                    rate = self.sample_rate,
                    output = True)

    ## Write given sound wave sample to streaming thread, play sound
    def makeSound(self, sample):
        self.stream.write(sample)
    
    ## Stop audio stream and close the PyAudio object
    def closeMachine(self):
        self.stream.close()
        self.p.terminate()
      
        
class EnvelopeADSR(object):
    def __init__(self, attack_time, decay_time, release_time, max_amp, sus_amp,
                 on_time, off_time):
        
        self.attack_time = attack_time
        self.decay_time = decay_time
        self.release_time = release_time
        
        self.max_amp = max_amp
        self.sus_amp = sus_amp
        
        self.on_time = on_time
        self.off_time = off_time
        self.note_on = False

    def getAmp(self, time):
        
        current_time = time-self.on_time
        
        if self.note_on:
            
            ## Attack
            if current_time >= self.attack_time:
                return (current_time/self.attack_time) * self.max_amp
            
            ## Decay
            elif current_time > self.attack_time and current_time < (self.attack_time + self.decay_time):
                return ((current_time-self.attack_time)/self.decay_time) * (self.sus_amp-self.max_amp) + self.max_amp
            
            ## Sustain
            elif current_time >= (self.attack_time + self.decay_time):
                return self.sus_amp

        ## Release          
        else:
            return ((current_time-self.off_time)/self.release_time) * (-self.sus_amp)
    
    def noteOn(self, time):
        self.note_on = True
        self.on_time = time
        
    def noteOff(self, time):
        self.note_on = False
        self.off_time = time
    

## Generates sine wave, and np array of values
def oscillator(freq, amp, osc_type):
    
    def sawtoothApprox(ar):
        return (0.2 * (freq*np.pi * ((ar%(1/freq))-(np.pi/2)))) #+ freq
        
    def sawtooth(ar):
        
        nums = np.arange(len(ar))
        
        
        a = -np.sin(freq*2*np.pi*ar*nums)/nums
        
        return a
        #return np.sum(a)
    
    adsr = EnvelopeADSR(attack_time=0.075,
                        decay_time=0.05,
                        release_time=0.1,
                        max_amp=amp+0.3,
                        sus_amp=amp,
                        on_time=0,
                        off_time=0
                        )
    
    adsr.noteOn(0)
    
    ## Creates array of numbers to use as 'time'
    sample_nums = np.arange(SAMPLE_RATE)
    
   # amps = getAmp
    
    ## y=A*sin(2pi * freq/rate * t)
    ## Generates audio samples using formula, converts all values to floats
    
    ## Sine wave
    if osc_type == 0:
        samples = (amp * np.sin(2*np.pi * sample_nums * freq/SAMPLE_RATE))
    
    ## Square wave
    elif osc_type == 1:
        samples = (amp * np.sin(2*np.pi * sample_nums * freq/SAMPLE_RATE))
        for i in range(len(samples)):
            if samples[i] > 0:
                samples[i] = amp
            else:
                samples[i] = -amp
    
    ## Triangle wave
    elif osc_type == 2:
        samples = amp * np.arcsin((np.sin(2*np.pi * sample_nums * freq/SAMPLE_RATE))) * 4/np.pi
        
    ## Good sawtooth but slow
    elif osc_type == 3:
        samples = sawtooth(sample_nums)
        print (samples)        

        
    ## Bad sawtooth approximation but faster
    elif osc_type == 4:
        samples = sawtoothApprox(sample_nums) + freq
        samples = np.interp(samples, (samples.min(), samples.max()), (-1, +1))
        print (samples)
        
    samples = samples.astype(np.float32)

        
    
    
    ## Start audio stream, play sound
    sm1.makeSound(samples)
    
## Create SoundMachine object
sm1 = SoundMachine(SAMPLE_RATE, CHANNELS)

## Initialise with PyAudio
sm1.startSoundMachine()