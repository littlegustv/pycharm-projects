__author__ = 'littlegustv'

#comment

import urllib
from xml.etree.ElementTree import parse
import webbrowser

lostlat = 41.980262
lostlon = -87.668452

u = urllib.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
data = u.read()
f = open('rt22.xml', 'wb')
f.write(data)
f.close()
doc = parse('rt22.xml')

for bus in doc.findall('bus'):
    d = bus.findtext('d')
    lat = float(bus.findtext('lat'))
    lon = float(bus.findtext('lon'))
    if lat > lostlat and d.startswith("North"):
        print "lat: ", lat, "id", bus.findtext('id')
        webbrowser.open('http://maps.google.com/maps/@' + str(lat) + ',' + str(lon) + ',20z')

