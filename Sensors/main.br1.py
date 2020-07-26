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

BROKER_ADDRESS="fd9a:6f5b:21d1::ee1"
initalert = "001"
alert = "001"








class EVENTS:
    def mqtt_sub_cb(topic, msg):
        print((topic, msg))

    def __init__(self,client,broker,id):
        self.uid = '{:02x}{:02x}{:02x}{:02x}'.format(id[0], id[1], id[2], id[3])
        self.client = MQTTClient(client, broker)
        self.client.set_callback(self.mqtt_sub_cb)
        print('attempt to %s MQTT broker' % (broker))
        try:
            self.client.connect()
            print('Connected to %s MQTT broker' % (broker))
        except:
            print ("error connecting to MQTT broker")
            pass

    def logit(self,ts,temp, pressure,humidity,device="",delimiter=","):
        print ("ts=", ts)
        payload = {"uid":str(self.uid),
                   "device:":str(device),
                   "ts":str(ts),
                   "ts2":'{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}.{:06d}'.format(ts[0],ts[1],ts[2],ts[4],ts[5],ts[6],ts[7]),
                   "temp":str(temp),
#                   "pressure":str(pressure),
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
#             self.client.publish("sensorsd/ts",str(timestamp),qos=1)
#             self.client.publish("sensorsd/temp",str(temp),qos=1)
#             self.client.publish("sensorsd/pressure",str(pressure),qos=1)
#             self.client.publish("sensorsd/humidity",str(humidity),qos=1)
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

def handleInterrupt3(pin):
    global motion
    motion = True
    global interrupt_pin
    interrupt_pin = pin

motion_led = Pin(26, Pin.OUT)
motion_pir = Pin(27, Pin.IN)

motion_pir.irq(trigger=Pin.IRQ_RISING, handler=handleInterrupt3)


if __name__ == '__main__':
    print (sys.implementation.name, sys.implementation.version)
    id = machine.unique_id()

    ## setup i2c
    i2c = i2c_init()
    i2c_scan(i2c)
    i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
    devices = i2c.scan()
    b=BME280.BME280(i2c=i2c,fmt=False)

    ## setup RTC and sychronize with NTP servers
    rtc = machine.RTC()
    rtc.datetime((2020,06,06,07,48,0,0,0)) ## b-day of code :-)
    rtc.datetime()
    ntptime.host = '192.168.1.118'
    #flg = False
    #while not flg:
    try:
        ntptime.settime()
        flg = True
        print("time set with ntp sync")

    except:
        print("error with ntp sync")
        flg = False
        pass

    #OSError: [Errno 110] ETIMEDOUT
    rtc.datetime()


    #evnts = EVENTS("Sensors","fd9a:6f5b:21d1::ee1")
    evnts = EVENTS("Sensors1","192.168.1.118",id)



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

    timer.init(period=150, mode=machine.Timer.PERIODIC, callback=handleInterrupt)
    timer1.init(period=125, mode=machine.Timer.PERIODIC, callback=handleInterrupt2)


    while interruptCounter<200:

        if interruptCounter>0:
            state = machine.disable_irq()
            interruptCounter = interruptCounter-1
            machine.enable_irq(state)

            totalInterruptsCounter = totalInterruptsCounter+1
            print("Interrupt has occurred: " + str(totalInterruptsCounter))



        ts = rtc.datetime()

        pres = b.pressure
        temp = b.temperature
        hum = b.humidity
        evnts.logit(ts,temp,eval(pres),hum,device=118)



        print("now:      ",rtc.datetime())
        print("pressure: ",pres);
        print("temp:     ",temp)
        print("hum:      ",hum)
        led2.duty(i)



        if alert == "001":
            for i in range(3):
                if motion:
                    print('motion detected',interrupt_pin)
                    motion_led.value(1)
                    sleep(20)
                    motion_led.value(0)
                    motion = False



        if alert == "001":
            for i in range(1023):
                #print("i=",i),
                led2.duty(i)
                #print("PWM.duty=",led2.duty())
                time.sleep(1)
            time.sleep(1)
            led2.duty(1023)
            time.sleep(1)
            led2.duty(0)
            time.sleep(1)
            led2.duty(1023)
            time.sleep(1)


    # check if the device woke from a deep sleep
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print('woke from a deep sleep')

         # put the device to sleep for 10 seconds
    machine.deepsleep(10000)
