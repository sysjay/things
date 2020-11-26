'''
MIT License

Copyright (c) 2020 Jay Cornell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Created on Jun 28, 2020

@author: Jay Cornell
'''

#
# This is the MQTT publisher/sensor driver
# this reoutine subscribes to the topics and deals with the payloads
#


from machine import Pin, I2C, RTC, Timer
import machine
import sys
import time
from time import sleep
import ntptime
import BME280
from umqtt.robust import MQTTClient
import ujson
import micropython
import esp32

alert = "001"
initalert = "001"

# SECONDS webcam will work before sleeping unless motion reset
webcam = 15
# MINUTES webcam will sleep
webcamsleep = 15

BROKER_ADDRESS = "fd9a:6f5b:21d1::ee1"


def tsstr(ts):
    return '{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}.{:06d}'. \
            format(ts[0], ts[1], ts[2], ts[4], ts[5], ts[6], ts[7])


class EVENTS:
    def mqtt_sub_cb(topic, msg):
        print((topic, msg))

    def __init__(self, client, broker, id):
        self.uid = '{:02x}{:02x}{:02x}{:02x}'. \
                    format(id[0], id[1], id[2], id[3])
        self.client = MQTTClient(client, broker)
        self.client.set_callback(self.mqtt_sub_cb)
        print('attempt to %s MQTT broker' % (broker))
        try:
            self.client.connect()
            print('Connected to %s MQTT broker' % (broker))
        except:
            print("error connecting to MQTT broker")
            pass

    def logit(self,ts,temp, pressure,humidity,device="",delimiter=","):
        payload = {"uid":str(self.uid),
                   "device:":str(device),
                   "ts":str(ts),
                   "ts2":'{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}.{:06d}'. \
                          format(ts[0],ts[1],ts[2],ts[4],ts[5],ts[6],ts[7]),
                   "temp":str(temp),
                   "pressure":'{:3.2f}'.format(pressure),
                   "humidity":str(humidity)}
        d = ujson.dumps(payload)
        try:
            self.client.publish("sensors/",d)
            self.client.publish("sensorsd/id",str(self.uid),qos=1)
            self.client.publish("sensorsd/id/ts",str(ts),qos=1)
            self.client.publish("sensorsd/id/ts/temp",str(temp),qos=1)
            self.client.publish("sensorsd/id/ts/pressure",str(pressure),qos=1)
            self.client.publish("sensorsd/id/ts/humidity",str(humidity),qos=1)
        except:
            print("error publishing passing")
            pass
        #TODO: build store and forward
        #OSError: [Errno 113] EHOSTUNREACH
        #OSError: [Errno 110] ETIMEDOUT



micropython.alloc_emergency_exception_buf(100)
class Foo(object):
    def __init__(self, timer, led):
        self.led = led
        timer.callback(self.cb)
    def cb(self, tim):
        self.led.toggle()

#tim = Timer(-1)

#red = Foo(Timer(4, freq=1), LED(1))
#green = Foo(Timer(2, freq=0.8), LED(2))


interruptCounter = 0
totalInterruptsCounter = 0

timer = machine.Timer(0)
timer1 = machine.Timer(1)
p18 = Pin(18, Pin.OUT)
p19 = Pin(19, Pin.OUT)

def handleInterrupt(timer):
  global interruptCounter
  interruptCounter = interruptCounter+1
  p18.value(not p18.value())

def handleInterrupt2(timer):
  global interruptCounter
  interruptCounter = interruptCounter+1
  p19.value(not p19.value())


def i2c_init():
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
    return i2c

def i2c_scan(i2c):
    """Scan the I2C bus"""
    devices = i2c.scan()

    for dev in devices:
        print("*** Device found at address %s" % dev)

    return devices


motion = False
motion_led = Pin(26, Pin.OUT)
motion_pir = Pin(27, Pin.IN)
motiontmr = time.time()
motiontm = False

def handleInterrupt3(pin):
    global motion
    motion = True
    global motiontm
    motiontm = False
    global interrupt_pin
    interrupt_pin = pin
    motion_led.value(1)

def handleInterrupt4(pin):
    global motion
    motion = False
    global motiontmr
    motiontmr = time.time()
    global interrupt_pin
    interrupt_pin = pin
    motion_led.value(0)


motion_pir.irq(trigger=Pin.IRQ_RISING, handler=handleInterrupt3)
#otion_pir.irq(trigger=Pin.IRQ_HIGH_LEVEL, handler=handleInterrupt3)

#motion_pir.irq(trigger=Pin.IRQ_FALLING,handler=handleInterrupt4)

if __name__ == '__main__':
    ## setup RTC and sychronize with NTP servers
    rtc = machine.RTC()
    ntptime.host = '192.168.1.118'
    try:
        ntptime.settime()
        flg = True
        print("time set with ntp sync")

    except:
        print("error with ntp sync")
        flg = False
        pass

    #OSError: [Errno 110] ETIMEDOUT
    js = rtc.datetime
    print("starting jthings")
    print("WakeUP Reason: ", machine.wake_reason())
    print("wakeup PIN: ", machine.PIN_WAKE)
    print (sys.implementation.name, sys.implementation.version)
    ts = rtc.datetime()
    print(tsstr(rtc.datetime()))
    id = machine.unique_id()
    esp32.wake_on_ext0(motion_pir,esp32.WAKEUP_ANY_HIGH)

    ## setup i2c
    i2c = i2c_init()
    i2c_scan(i2c)
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
    devices = i2c.scan()
    b=BME280.BME280(i2c=i2c,fmt=False)



    #evnts = EVENTS("Sensors","fd9a:6f5b:21d1::ee1")
    evnts = EVENTS("Sensors1","192.168.1.118",id)
    evnts.logit(ts,0,0,0,device=500)



    #Due to limitations of the ESP8266 chip the internal real-time clock (RTC) will overflow every 7:45h.
    #If a long-term working RTC time is required then time() or localtime() must be called at least once within 7 hours.
    #MicroPython will then handle the overflow.
    led2 = machine.PWM(machine.Pin(2), freq=1000)
    print("PWM.duty=",led2.duty())
    print("Byte Order=",sys.byteorder)
    print("Implementation: ",sys.implementation.name,sys.implementation.version)
    print("Sensor Starting:",rtc.datetime())

#  set alert off to save amps
    if initalert == "001":
        time.sleep(.1)
        led2.duty(0)
        time.sleep(.2)
        led2.duty(200)
        time.sleep(.2)
        led2.duty(512)
        time.sleep(.2)
        led2.duty(826)
        time.sleep(.2)
        led2.duty(1023)
        time.sleep(.2)
        led2.duty(826)
        time.sleep(.2)
        led2.duty(512)
        time.sleep(.2)
        led2.duty(200)
        time.sleep(.2)
        led2.duty(0)
        time.sleep(.2)

    i = 0
#    timer.init(period=500, mode=machine.Timer.PERIODIC, callback=handleInterrupt)
#    timer1.init(period=350, mode=machine.Timer.PERIODIC, callback=handleInterrupt2)


#    while interruptCounter<200:
    while True:
        ts = rtc.datetime()

        pres = b.pressure
        temp = b.temperature
        hum = b.humidity
        evnts.logit(ts,temp,eval(pres),hum,device=118)

        sleep(2)

        print("now:      ",rtc.datetime())
        print("pressure: ",pres);
        print("temp:     ",temp)
        print("hum:      ",hum)
        led2.duty(i)



        if alert == "001":
            if motion:
                if not motiontm:
                   print('motion detected',interrupt_pin)
                   print(tsstr(rtc.datetime()))
                   motiontmr = time.time()
                   print('motion timer:',motiontmr)
                   motiontm = True
    #              HC-SR501 PIR Motion Sensor
                   evnts.logit(ts,temp,eval(pres),hum,device=501)
                   motion_led.value(1)
                else:
                    print('motion detected during motiontm lock',tsstr(rtc.datetime()))
        #    else:
                # print('going into sleep')
                # check if the device woke from a deep sleep
                # if machine.reset_cause() == machine.DEEPSLEEP_RESET:
                #    print('woke from a deep sleep')

                    # put the device to sleep for 10 seconds
                # machine.deepsleep(15000)
        print('motion check:::::::::::::')
        print(tsstr(rtc.datetime()), "motiontm time duration: ", time.time() - motiontmr)
        if ((time.time() - motiontmr) > webcam):
            print("motion time completed")
            motion = False
            motiontm = False
            rgct = 5
            for i in range(rgct):
                motion_led.value(not motion_led.value())
                sleep(0000000000 + rgct - i)
            print('starting deepsleep')
            print(tsstr(rtc.datetime()))
            evnts.logit(ts,temp,eval(pres),hum,device=509)
            #machine.deepsleep(60000*webcamsleep)
            machine.deepsleep()

        if alert == "001":
            for i in range(1023):
                #print("i=",i),
                led2.duty(i)
                #print("PWM.duty=",led2.duty())
                time.sleep(0.001)
            time.sleep(1)
            led2.duty(1023)
            time.sleep(1)
            led2.duty(0)
            time.sleep(1)
            led2.duty(1023)
            time.sleep(1)
