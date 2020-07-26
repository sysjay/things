import sys
sys.path.append("/home/jay/workspace-sensors2/FirstDashboard/tools")
import timing
from sqlalchemy import create_engine


sqlEngine       = create_engine('mysql+pymysql://sensors:password@localhost/sensordata', pool_recycle=3600)


import random
import datetime

ts = datetime.datetime.now()
ts2 = ts



#print(mycursor.rowcount, "record inserted.")
print(sqlEngine)
sql = "INSERT INTO sensortbl (sensor, device, value, event_ts, capture_ts) VALUES (%s, %s, %s, %s, %s)"
total = 0
devices =['118','119']
things = ['esp32-01','rpi-01']
devicetypes = ['tempi', 'pressure','humidity']
for i in range(100):
    for n in devices:
        for o in devicetypes:
            ts2 = ts2 + datetime.timedelta(seconds=30)
            val = (n.encode('utf-8'),o.encode('utf-8'), random.random(),ts,ts2)
            sqlEngine.execute(sql, val)
            print(o, ts, i, n, random.random())
