import pandas as pd
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="sensors",
    password="password",
    database="sensordata"
    )

df = pd.readsql("SELECT * FROM sensortbls", mydb, index=('event_ts'))
