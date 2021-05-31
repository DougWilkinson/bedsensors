from sensorclass import Sensor
from machine import Pin
import time
from hx import HX711

# lbed sensor derived from cats (food weight sensor)
# Started 3/28/2020

hxmin = Sensor("hxmin", initval=0)
hxmax = Sensor("hxmax", initval=10000) 
status = Sensor("status", initval="Init") 
#hx = HX711(5,4) # clock, data
hx = HX711(14,12)

# callback that is polled by checklevel sensor
def hxread(x):
    lasthx = rawhx.value
    newhx = hx.raw_read()
    if (newhx < hxmin.value) or (newhx > hxmax.value):
        status.setvalue("MinMax")
        return
    if status.value != "Ok":
        status.setvalue("Ok")
    if abs(lasthx - newhx) > rawhx.diff:
        rawhx.setvalue(newhx)

# Sensor to poll for readings only

rawhx = Sensor("rawhx", initval=0.0, diff=5, poll=1000, callback=hxread)
print(rawhx.value)
time.sleep(2)
print(rawhx.value)

statusled = Sensor("led", "OUT", 2)
statusled.setstate(True)


def main():
    Sensor.MQTTSetup("lbed")
    while True:
        Sensor.Spin()
            
