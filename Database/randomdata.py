import sys
sys.path.append("/home/jay/workspace-sensors2/FirstDashboard/tools")
import timing




import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
)

import random
import datetime

ts = datetime.datetime.now()
ts2 = ts
mycursor = mydb.cursor()



print(mycursor.rowcount, "record inserted.")
print(mydb)
sql = "INSERT INTO sensortbl (sensor, device, devtype, value, event_ts, capture_ts) VALUES (%s, %s, %s, %s, %s, %s)"
total = 0
things = ['esp32-01','rpi-01']
devices =['118','119']
devicetypes = ['tempi', 'pressure','humidity']
for i in range(100):
    for t in things:
        for n in devices:
            for o in devicetypes:
                ts2 = ts2 + datetime.timedelta(seconds=30)
                val = (t, n, o, random.random(), ts, ts2)
                mycursor.execute(sql, val)
                print(o, ts, i, n, random.random())
                mydb.commit()
print("END::::::::::::::::::::::::::::::::")
