#Code to calculate the delay using railway API

import urllib2
import json
import pylab as pl
api = urllib2.urlopen("http://api.railwayapi.com/live/train/12675/doj/20160603/apikey/dnsdx7015/")

data = json.load(api)