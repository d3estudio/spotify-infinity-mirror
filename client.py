#!/usr/bin/env python
import alsaaudio
import numpy
import redis
from time import sleep
from struct import unpack

# Audio Capture Constants
CHANNELS = 1
INFORMAT = alsaaudio.PCM_FORMAT_S16_LE
SAMPLE_RATE = 44100
CHUNK = 1024

# Animation Constants
EASING_IN_FACTOR = 25
EASING_OUT_FACTOR = 15

# Redis Server Constants
REDIS_HOST = '192.168.42.10'
REDIS_PORT = 6379

class Publisher():
  def __init__(self, r, a):
    self.redis = r
    self.alsa = a
    
    self.alsa.setchannels(CHANNELS)
    self.alsa.setrate(SAMPLE_RATE)
    self.alsa.setformat(INFORMAT)
    self.alsa.setperiodsize(CHUNK)
    
    # Initialize the FFT matrix
    self.matrix    = [0, 0, 0, 0, 0, 0, 0, 0]
    self.weighting = [512, 512, 1024, 1024, 2048, 2048, 4096, 4096]

    # Precalculate weighting matrix
    self.weighting = numpy.true_divide(self.weighting, 1000000)
    
  # Return power array index corresponding to a particular frequency
  def piff(self, value):
    return int(2 * CHUNK * value / SAMPLE_RATE)

  def calculate_levels(self, data):
    # Convert raw data (ASCII string) to numpy array
    data = unpack("%dh"%(len(data)/2),data)
    data = numpy.array(data, dtype='h') 

    # Apply FFT - real data
    fourier = numpy.fft.rfft(data)
      
    # Remove last element in array to make it the same size as chunk
    fourier = numpy.delete(fourier, len(fourier) - 1)
      
    # Find average 'amplitude' for specific frequency ranges in Hz
    power = numpy.abs(fourier)
      
    lower_bound = 0
    upper_bound = 32

    for i in range(len(self.matrix)):
      mean = numpy.mean(power[self.piff(lower_bound) : self.piff(upper_bound):1])
      self.matrix[i] = int(mean) if numpy.isnan(mean) == False else 0       
      
      lower_bound = upper_bound
      upper_bound = upper_bound << 1
      
    # Tidy up column values for the LED matrix
    self.matrix = numpy.multiply(self.matrix, self.weighting)
      
    # Set all values smaller than first argument to 0, all greater than second argument to 4095
    self.matrix = self.matrix.clip(0, 4095) 

    return self.matrix

  def map(self, x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

  def run(self):
    l, data = self.alsa.read()
    a = 0
    while data != '':
      tmp = int(a)
      l, data = self.alsa.read()
      a = self.calculate_levels(data)
      a = self.map(int(a[0]), 0, 2600, 145, 0)
      
      if a < 0:
        a = 0
      
      if a > tmp:
        r = range(tmp, a, EASING_IN_FACTOR)
      else:
        r = range(tmp, a, EASING_OUT_FACTOR * -1)
      
      for x in r:
        self.redis.publish('infinity-mirror', x)
        l, data = self.alsa.read()
        
if __name__ == "__main__":
  r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
  a = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, 'sysdefault:CARD=1')
  
  publisher = Publisher(r, a)  
  publisher.run()
