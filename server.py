#!/usr/bin/env python
import redis
import serial
from time import sleep

REDIS_HOST = '192.168.42.10'
REDIS_PORT = 6379

class Listener():
  def __init__(self, r, u, channels):
    self.redis = r
    self.usb = u
    self.pubsub = self.redis.pubsub()
    self.pubsub.subscribe(channels)

  def work(self, item):
    item = int(item['data'])

    if item >= 0 && item <= 255:
      byte = bytearray([int(item['data'])])
      self.usb.write(byte)

  def run(self):
    for item in self.pubsub.listen():
      self.work(item)
 
if __name__ == "__main__":
  r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
  u = serial.Serial("/dev/ttyUSB0", baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
  
  client = Listener(r, u, ['infinity-mirror'])
  client.run()
