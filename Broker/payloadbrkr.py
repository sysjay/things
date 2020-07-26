
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

@author: jay
'''

#
# This is the MQTT subscriber code.
# this reoutine subscribes to the topics and deals with the payloads
#
# @TODO jtc 6/27/20 build a log file start by redirecting the existing print
#                   statements to a local text file

import sys
import time
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import json

import paho.mqtt.client as mqtt
from numpy.core.setup_common import fname2def


class logs:
    def __init__(self, path, fname):
        self.logfile = path + fname
        self.bfr = ""
        try:
            self.f = open(self.logfile, 'w')
            print("file opened a")
            print("FILE: ", self.logfile)
        except:
            self.f = open(self.logfile, 'w+')
            print("file opend w+")

    def logit(self, *args):
        print("logit:::::::::::::::::::::::::::::::", file=self.f, flush=True)
        #for a in args:
        #    self.bfr = self.bfr + a
        try:
            print(self.bfr, file=self.f, flush=True)
        except:
            print(self.bfr)


class sensordata:

    def __init__(self, device, cached, fields):
        self.device = device
        self.data = np.zeros((cached, fields))
        self.datats = np.zeros(cached)
        self.ptr = 0
        self.fig = go.FigureWidget()
        self.fig.add_scatter()
        self.fig.show()

    def add(self, field, value):
        #
        # @TODO  research *kwargs or *argv
        #
        self.data[self.ptr, field] = value
        print("addingdata.............")
        print(self.data)
        print("eod....................")
        self.fig.data[0].y = self.data[:value]


class MyMQTTClass(mqtt.Client):

    def utc_to_local(self, utc_dt):
        return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
    
    

    def on_connect(self, mqttc, obj, flags, rc):
        self.l.logit( "rc: "+str(rc))

    def on_message(self, mqttc, obj, msg):
        if msg.payload != b'hello222':
            self.l.logit("Data###################")
            self.l.logit(
                  msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
            y = json.loads(msg.payload)

#            self.l.logit("msg        :", msg)
            self.l.logit("UID        :", y["uid"])
            self.l.logit("humidity   :", y["humidity"])
            self.l.logit("temperature:", y["temp"])
            self.l.logit("pressure   :", y["pressure"])
            ts2 = datetime.datetime.strptime(y["ts2"], '%Y/%m/%d %H:%M:%S.%f')
            self.l.logit("tzinfo     :", ts2.tzinfo)
            self.l.logit("ts2        :", ts2)
            self.l.logit("utc2Local  :",
                         self.utc_to_local(ts2))

            pl3 = pd.DataFrame({
                                'ts2':         [ts2],
                                'humidity':    [y["humidity"]],
                                'temperature': [y["temp"]],
                                'pressure':    [y['pressure']],
                                'device':      [y["device:"]]
                                }, index=[y["uid"]])
            if self.first:
                self.data = pl3
                self.first = False
            else:
                self.data = self.data.append(pl3)
            print ("PL3:::::::::::::::::::::::::::::::::::::::::\n", pl3)
            print ("data cached:::::::::::::::::::::::::::::::::\n", self.data)

            print ("len pl3 :", len(pl3.index))
            print ("len data:", len(self.data.index))

            self.data.to_csv(self.csvfile, index=True, mode='a')

# @TODO
# add code to manage memory based on cacheq..  i want to delete old rows
#            if len(self.data) > self.cacheq:
#                self.data.pop(1)

            # timestamp tuple
            #      0        1      2      3      4       5      6    7
            # "(  2020,     6,    17,     2,    23,      8,    13,  150866)"
            #     YYYY     MM     DD      W     HH      MM     SS   ms
            print("Data*******************")

    def on_publish(self, mqttc, obj, mid):
        print("mid: "+str(mid))

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        print("Subscribed: "+str(mid)+" "+str(granted_qos))

    def on_log(self, mqttc, obj, level, string):
        print(string)

    def run(self, bkripaddr, log):
        print ("run..................")
        self.l = log
        self.ipaddr = bkripaddr
        self.connect(bkripaddr, 1883, 60)

        self.first = True
        self.subscribe("sensors/#", 0)
        self.csvfile = "~/workspace-sensors2/esp8266/sensors.csv"
        self.cacheq = 3
#         self.data = pd.DataFrame(
#                                     {'ts2':        [],
#                                     'humidity':    [],
#                                     'temperature': [],
#                                     'pressure':    []
#                                 },
#                                 index=[]
#                                 )

#        self.bme280 = sensordata("sensor1",self.cacheq, 3)
#        pl3 = pd.DataFrame({'ts2':[],'humidity':[]})
        rc = 0
        while rc == 0:
            rc = self.loop(timeout=0.25)
        return rc


# #############################################################################################
# ## beinging of main loop control 
# #############################################################################################

logpath = '/home/jay/workspace-sensors2/FirstDashboard/log/'
logfile = 'testlog.log'
l = logs(logpath, logfile)

l.logit("##############################")
#l.logit(sys.implementation)
l.logit( "before main")
l.logit( "__name__=", __name__)
if __name__ == "__main__":
    l.logit( "Testing new subscribe")
#    main()
# If you want to use a specific client id, use
# mqttc = MyMQTTClass("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
    mqttc = MyMQTTClass()
    rc = mqttc.run("192.168.1.118", l)

    l.logit( "rc: "+str(rc))
