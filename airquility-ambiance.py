#!/usr/bin/python2
# pip install yeelight
from yeelight import discover_bulbs
from yeelight import Bulb
import json
import requests
import time
import argparse

sensor = '5188'
# Check the URI of your selected sensor on www.purpleair.com
# https://www.purpleair.com/map?opt=1/mAQI/a10/cC0&select=5188#9.37/38.0552/-121.8958
parser = argparse.ArgumentParser()
parser.add_argument('--sensor', default='5188',
                    help='PurpleAir Sensor (default: 5188, near Hercules, CA)')
args = parser.parse_args()

data = discover_bulbs()
# This assumes you only have one yeelight bulb
mybulb = Bulb(data[0]['ip'])
mybulb.turn_on()

def get_data():
  while True:
    try:
      r = requests.get('https://www.purpleair.com/json?show='+args.sensor)
    except:
      time.sleep(10)
    if(r.ok):
      y = json.loads(r.content.decode('utf-8'))
      pm25 = float(y["results"][0]["PM2_5Value"])
      print(pm25)
      if (pm25 <= 12):
        print("green")
        mybulb.set_hsv(70, 75, 1)
      elif (pm25 > 12) and (pm25 <= 23):
        print("yellow/green")
        mybulb.set_hsv(60, 75, 1)
      elif (pm25 > 23) and (pm25 <= 35):
        print("yellow")
        mybulb.set_hsv(50, 75, 1)
      elif (pm25 > 35) and (pm25 <= 43):
        print("yellow/orange")
        mybulb.set_hsv(40, 75, 1)
      elif (pm25 > 43) and (pm25 <= 55):
        print("orange")
        mybulb.set_hsv(30, 75, 1)
      elif (pm25 > 55) and (pm25 <= 150):
        print("red")
        mybulb.set_hsv(10, 75, 1)
      else:
        print("purple")
        mybulb.set_hsv(290, 75, 1)
      time.sleep(92)
    else:
      print("connect error")
      time.sleep(10)

try:
  mybulb.turn_on()
  get_data()
except:
  mybulb.turn_off()
finally:
  mybulb.turn_off()
