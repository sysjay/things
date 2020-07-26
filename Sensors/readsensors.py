#!/usr/bin/env python
import smbus
import time
import datetime
import sys
import paho.mqtt.client as mqtt 
import json as js


#import math
#from pygments.lexers import business
#print '\n'.join(sys.path)
#print ("****")
#print smbus.__file__

bus = smbus.SMBus(1)
ADDRESS = 0x20 # address of MCP23017 (ground A0, A1, and A2)
I2C_ADDR = 0x77# address of BMP080 
I2C_HTU21D = 0X40
BROKER_ADDRESS="192.168.1.118" 
BROKER_ADDRESS="fd9a:6f5b:21d1::ee1"




class EVENTS:
    def mqtt_sub_cb(self, topic, msg):
        print((topic, msg))
    
    def __init__(self,client,broker,uid):
        self.counter = 0
        self.errcount = 0
        self.uid = str(uid) 
        #self.uid = '{:02x}{:%02x}{:%02x}{:%02x}'.format(uid[0], uid[1], uid[2], uid[3]) 
        try:
            self.client = mqtt(client, broker)
            self.client.set_callback(self.mqtt_sub_cb)
            print('attempt to %s MQTT broker' % (broker))
            try:
                self.client.connect()
                print('Connected to %s MQTT broker' % (broker))
            except:
                print ("error connecting to MQTT broker")
                pass
        except:
            self.broker = broker
            print("MQTT Starting -- exception")
            self.client = mqtt.Client(client) #create new instance
            self.client.connect(self.broker) #connect to broker
            print ("MQTT Done")

    
    def logit(self,ts,temp, pressure,humidity,device="",delimiter=","):
        print ("ts=", ts)
        
        try:
            #ts2_fmt = datetime.datetime.strftime(ts, "%m/%d/%Y %H:%M:%S.%f")
            ts2_fmt = datetime.datetime.strftime(ts, "%Y/%m/%d %H:%M:%S.%f")
        except:
            ts2_fmt = '{:04d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}.{:06d}'.format(ts[0],ts[1],ts[2],ts[4],ts[5],ts[6],ts[7])
        payload = {"uid":str(self.uid),
                   "device:":str(device),
                   "ts":str(ts),
                   "ts2":str(ts2_fmt),
                   "temp":'{:3.2f}'.format(temp),
#                   "pressure":str(pressure),
                   "pressure":'{:3.2f}'.format(pressure),
                   "humidity":'{:3.2f}'.format(humidity)}
        d = js.dumps(payload)
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
        
    def compare(self,value):
#        print value, self.counter,
        if value == 0 and self.counter == 60:
            self.counter = value + 1
            return True
        elif self.counter == value:
            self.counter = self.counter + 1
            return True
        else:
            self.counter = value + 1
            self.errcount = self.errcount + 1
            return False
    
        
class MCP23x17:

    def __init__(self,bus,address):
        """configure appropraite outputs and inputs."""
        self.bus = bus
        self.ADDRESS = address
        self.bus.write_byte_data(self.ADDRESS,0,255) # all is GPIO A input
        self.bus.write_byte_data(self.ADDRESS,1,0) # all is GPIO B output
        self.readA = 0
        print ("****")
        # Python program to illustrate 
        # enumerate function in loops 
        l1 = ["Initilazation Starting","Program is used to track sensors","Each Sensor will Run on it's own timer loop","loop is based on a 1 second sample rate"] 
      
        # printing the tuples in object directly 
        for ele in enumerate(l1): 
          print (ele) 
        print 
        # changing index and printing separately 
        for count,ele in enumerate(l1,100): 
          print (count,ele) 
    
    
        print ("init completed")
        print ("****")
    
    def read(self):
        """read each of the four 8-bit registers."""
        vals=0
        for i,reg in enumerate([0b11111110,0b11111101,0b11111011,0b11110111]):
            self.bus.write_byte_data(self.ADDRESS,0x13,reg) # set GPIO B
            vals+=float(self.bus.read_byte_data(self.ADDRESS,18))*(256**i)
        return int(vals)
        
    def readTwice(self):
        """only return a read if it's gotten twice."""
#        print "*****self.readA=",self.readA,
        while True:
            self.readA=self.read()
            time.sleep(0.2) # reset takes 15ms so let's give it some time
            readB=self.read()
#            print "readB=",readB,self.readA
            if self.readA==readB:
                self.readA=readB
                return None

    def reading(self):
        return self.readA

            
class HTU21D:
    
    def __init__(self,bus,address,):
        # i2c bus, if you have a Raspberry Pi Rev A, change this to 0
        # HTU21D-F Commands
        self.bus = bus
        self.addr = address
        self.rdtemp = 0xE3
        self.rdhumi = 0xE5
        self.wtreg = 0xE6
        self.rdreg = 0xE7
        self.reset = 0xFE
        
    def read_temperature(self):
##      handle = bus.i2c_open(bus, addr) # open i2c bus
        self.bus.write_byte(self.addr, self.rdtemp) # send read temp command
        time.sleep(0.05) # readings take up to 50ms, lets give it some time
        byteArray = self.bus.read_i2c_block_data(self.addr, 3) # vacuum up those bytes
        t1 = byteArray[0] # most significant byte msb
        t2 = byteArray[1] # least significant byte lsb
        temp_reading = float((t1 * 256) + t2) # combine both bytes into one big integer
        self.temperature = ((temp_reading / 65536) * 175.72 ) - 46.85 # formula from datasheet
        print("%.2f F " %float(self.temperature * 1.8 + 32)),

        
        return self.temperature * 1.8 + 32

    def read_humidity(self):
        self.bus.write_byte(self.addr, self.rdhumi) # send read humi command
        time.sleep(0.05) # readings take up to 50ms, lets give it some time
        byteArray = self.bus.read_i2c_block_data(self.addr, 3) # vacuum up those bytes
        h1 = byteArray[0] # most significant byte msb
        h2 = byteArray[1] # least significant byte lsb
        humi_reading = float((h1 * 256) + h2 )# combine both bytes into one big integer
        uncomp_humidity = ((humi_reading / 65536) * 125 ) - 6 # formula from datasheet
        # to get the compensated humidity we need to read the temperature
        self.temperature = self.read_temperature()
        self.humidity = ((25 - self.temperature) * -0.15) + uncomp_humidity
        print("%.2f%%" %self.humidity),
        return self.humidity

#    def read_HTU21D(self):
        
        
class BMP080:

    def __init__(self, bus, address, register, length):

        # BMP280 address, 0x76(118)
        # Read data back from 0x88(136), 24 bytes
        self.b1 = bus.read_i2c_block_data(address, register, length)
        # Convert the data
        # Temp coefficents
        self.dig_T1 = self.b1[1] * 256 + self.b1[0]
        self.dig_T2 = self.b1[3] * 256 + self.b1[2]
        if self.dig_T2 > 32767 :
            self.dig_T2 -= 65536
        self.dig_T3 = self.b1[5] * 256 + self.b1[4]
        if self.dig_T3 > 32767 :
            self.dig_T3 -= 65536
            # Pressure coefficents
        self.dig_P1 = self.b1[7] * 256 + self.b1[6]
        self.dig_P2 = self.b1[9] * 256 + self.b1[8]
        if self.dig_P2 > 32767 :
            self.dig_P2 -= 65536
        self.dig_P3 = self.b1[11] * 256 + self.b1[10]
        if self.dig_P3 > 32767 :
            self.dig_P3 -= 65536
        self.dig_P4 = self.b1[13] * 256 + self.b1[12]
        if self.dig_P4 > 32767 :
            self.dig_P4 -= 65536
        self.dig_P5 = self.b1[15] * 256 + self.b1[14]
        if self.dig_P5 > 32767 :
            self.dig_P5 -= 65536
        self.dig_P6 = self.b1[17] * 256 + self.b1[16]
        if self.dig_P6 > 32767 :
            self.dig_P6 -= 65536
        self.dig_P7 = self.b1[19] * 256 + self.b1[18]
        if self.dig_P7 > 32767 :
            self.dig_P7 -= 65536
        self.dig_P8 = self.b1[21] * 256 + self.b1[20]
        if self.dig_P8 > 32767 :
            self.dig_P8 -= 65536
        self.dig_P9 = self.b1[23] * 256 + self.b1[22]
        if self.dig_P9 > 32767 :
            self.dig_P9 -= 65536
        self.jay = 9

    def read_BMP080(self):
    
        # BMP280 address, 0x76(118)
        # Select Control measurement register, 0xF4(244)
        # 0x27(39) Pressure and Temperature Oversampling rate = 1
        # Normal mode
        bus.write_byte_data(0x77, 0xF4, 0x27)
        # BMP280 address, 0x76(118)
        # Select Configuration register, 0xF5(245)
        # 0xA0(00) Stand_by time = 1000 ms
        bus.write_byte_data(0x77, 0xF5, 0xA0)
        time.sleep(0.05)
        # BMP280 address, 0x76(118)
        # Read data back from 0xF7(247), 8 bytes
        # Pressure MSB, Pressure LSB, Pressure xLSB, Temperature MSB, Temperature LSB
        # Temperature xLSB, Humidity MSB, Humidity LSB
        data = bus.read_i2c_block_data(0x77, 0xF7, 8)
        # Convert pressure and temperature data to 19-bits
        adc_p = ((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16
        adc_t = ((data[3] * 65536) + (data[4] * 256) + (data[5] & 0xF0)) / 16
        # Temperature offset calculations
        var1 = ((adc_t) / 16384.0 - (self.dig_T1) / 1024.0) * (self.dig_T2)
        var2 = (((adc_t) / 131072.0 - (self.dig_T1) / 8192.0) * ((adc_t)/131072.0 - (self.dig_T1)/8192.0)) * (self.dig_T3)
        t_fine = (var1 + var2)
        self.tempC = (var1 + var2) / 5120.0
        self.tempF = self.tempC * 1.8 + 32
        # Pressure offset calculations
        var1 = (t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (self.dig_P6) / 32768.0
        var2 = var2 + var1 * (self.dig_P5) * 2.0
        var2 = (var2 / 4.0) + ((self.dig_P4) * 65536.0)
        var1 = ((self.dig_P3) * var1 * var1 / 524288.0 + ( self.dig_P2) * var1) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * (self.dig_P1)
        p = 1048576.0 - adc_p
        p = (p - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (self.dig_P9) * p * p / 2147483648.0
        var2 = p * (self.dig_P8) / 32768.0
        self.pressure = (p + (var1 + var2 + (self.dig_P7)) / 16.0) / 100
        # Output data to screen
        print("%.2f C" %self.tempC),
        print("%.2f F" %self.tempF),
        print("%.2f hPa " %self.pressure),




if __name__=="__main__":
    
    
    

    
    
    nrg40 = MCP23x17(bus,ADDRESS)
    bmpressure = BMP080(bus, I2C_ADDR, 0x88, 24)
    htuhumidity = HTU21D(bus,I2C_HTU21D)
    
    readA=None
    last_ts = datetime.datetime.utcnow()
    uid = 0x3c71bf2
    evnts = EVENTS("Sensors2","192.168.1.118",uid)
    first_ts = last_ts
    time.sleep(.01)
    lastct = 0
    while True:
        nrg40.readTwice()
        print (nrg40.reading()),
        diff = nrg40.reading() - lastct
        lastct = nrg40.reading()
        print (diff), 
        print("%.0f" %diff),
        ts = datetime.datetime.utcnow()
        print(ts),

        todays_hours = ts.hour*3600
        todays_minutes = ts.minute*60
        todays_seconds = ts.second+todays_minutes+todays_hours
        
        difference = ts - last_ts
        total_time = ts - first_ts
        last_ts = ts
        mydelay = 0.74022 - ts.microsecond/1000000.0
        print ("totaltime  : ", total_time),
        print ("mydelay    : ", mydelay),
        time.sleep(5)
        time.sleep(mydelay)

        bmpressure.read_BMP080()
        
        #hum =  htuhumidity.read_humidity()
        #hum =  htuhumidity.read_HTU21D()
        #temp = htuhumidity.read_temperature()
        
        if not evnts.compare(last_ts.second):
            print ("reset", evnts.counter),
        print (evnts.errcount),
        print ()
        lastct = nrg40.reading()
        
        evnts.logit(ts,bmpressure.tempC,bmpressure.pressure,0,0x77)

