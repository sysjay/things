


# Overview:
> These are my notes to build a MQTT based IOT mesh network based application.   The code is based on Python with the microcontrollers using Micropython.   
>
> The overall data is captured into a centralized database -- i chose mysql running local. Analytics and dashboard capabilities leveraging pandas, plotly, and dash
>

## Things Framework
<img src="https://github.com/sysjay/things/blob/master/images/things.jpg">

## Supported Sensors
> Sensor support mostly based on i2C bus.
>> BME280 -- Barometric Pressure, Temperature, and Humidity
>>
>> HC-SR501 -- PIR Motion Sensor
>> 
>> NRG #40C -- Annometer -- customized circut
