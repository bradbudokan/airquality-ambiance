#!/usr/bin/python2
# pip install yeelight
from yeelight import discover_bulbs
from yeelight import Bulb
import json
import requests
import time
import argparse

sensor = '60019'
# Check the URI of your selected sensor on www.purpleair.com
# https://www.purpleair.com/map?opt=1/mAQI/a10/cC0&select=60019#18.4/37.791815/-122.393065
parser = argparse.ArgumentParser()
parser.add_argument('--sensor', default='60019',
                    help='PurpleAir Sensor (default: 60019, San Francisco, CA)')
args = parser.parse_args()

data = discover_bulbs()
# This assumes you only have one yeelight bulb
mybulb = Bulb(data[0]['ip'])
mybulb.turn_on()

green = "\033[0;32m"
yellow = "\033[1;33m"
orange = "\033[1;31m"
red = "\033[0;31m"
purple = "\033[0;35m"
orange = "\033[1;31m"

def compute_aqi():
    # based on https://en.wikipedia.org/wiki/Air_quality_index#Computing_the_AQI
    # green
    if (pm25 <= 12):
        print(round((((50-0)/(12-0))*(pm25-0))+0))
    # yellow
    elif (pm25 > 12) and (pm25 <= 35):
        print(round((((100-51)/(35-12))*(pm25-12))+51))
    # orange
    elif (pm25 > 35) and (pm25 <= 55):
        print(round((((150-101)/(55-35))*(pm25-35))+101))
    # red
    elif (pm25 > 55) and (pm25 <= 150):
        print(round((((200-151)/(150-55))*(pm25-55))+151))
    # purple
    elif (pm25 > 150) and (pm25 <= 250):
        print(round((((300-201)/(250-150))*(pm25-150))+201))
    # purple+
    elif (pm25 > 250) and (pm25 <= 350):
        print(round((((400-301)/(350-250))*(pm25-250))+301))
    # purple++
    else:
        print(round((((500-401)/(500-350))*(pm25-350))+401))
        
def get_data():
  while True:
    try:
      r = requests.get('https://www.purpleair.com/json?show='+args.sensor)
    except:
      time.sleep(10)
    if(r.ok):
      y = json.loads(r.content.decode('utf-8'))
      pm25 = float(y["results"][0]["PM2_5Value"])
      compute_aqi():
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
  mybulb.turn_on()
finally:
  mybulb.turn_off()
