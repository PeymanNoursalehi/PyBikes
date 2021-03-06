# -*- coding: utf-8 -*-
from station import Station

import re
import urllib,urllib2
from datetime import datetime
import demjson


PREFIX = "melbourne"
URL = "http://www.melbournebikeshare.com.au/stationmap/data"

def str2bool(v):
  return v.lower() in ["yes", "true", "t", "1"]
  
  
def get_all():
  usock = urllib2.urlopen(URL)
  data = usock.read()
  usock.close()
  raw = demjson.decode(data)
  stations = []
  for index, raw_station in enumerate(raw):
    station = MelbourneStation(index)
    station.from_json(raw_station)
    stations.append(station)
  return stations
    

class MelbourneStation(Station):
  prefix = PREFIX
  main_url = URL
  installed = False
  locked = False
  temporary = False
  
  def from_json(self, obj):
    self.number = int(obj["id"])
    self.name = obj["name"]
    self.lat = int(float(obj["lat"])*1E6)
    self.lng = int(float(obj["long"])*1E6)
    self.coordinates = obj["lat"]+","+obj["long"]
    self.bikes = int(obj["nbBikes"])
    self.free = int(obj["nbEmptyDocks"])
    self.installed = str2bool(obj["installed"])
    self.locked = str2bool(obj["locked"])
    self.temporary = str2bool(obj["temporary"])
    return self
    
  def update(self):
    self.timestamp = datetime.now()  
    return self
    
  def to_json(self):
    text =  '{"id":"%s", "name":"%s", "lat":"%s", "lng":"%s", "timestamp":"%s", "bikes":%s, "free":%s, "installed":"%s", "locked":"%s", "temporary":"%s", "coordinates":"%s"}' % \
    (self.idx, self.name, self.lat, self.lng, self.timestamp, self.bikes, self.free, self.installed, self.locked, self.temporary, self.coordinates)
    print text.encode('utf-8'),
    return text.encode('utf-8')