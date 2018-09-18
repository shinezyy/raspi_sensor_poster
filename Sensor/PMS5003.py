#-*- coding:UTF-8 -*-
import serial
import time
import struct
import sys  
import time
sys.path.append('../')

import Sensor

DeviceID = 'RPI2'
PM2_5_SenorID = 'pms5003st'
PM10_SenorID = 'pms5003st'

class PMS5003(Sensor.Sensor):
    def __init__(self):
        super(PMS5003, self).__init__()
        

    def GetData(self):
        while True:
            # 获得接收缓冲区字符
            self.ser = serial.Serial("/dev/ttyAMA0", 9600)
            count = self.ser.inWaiting()
            if count >= 40:
                recv = self.ser.read(40)

                sign1,sign2,frame_length,pm1_0_cf,pm2_5_cf,pm10_cf,pm1_0,pm2_5,pm10, \
						cnt_03,cnt_05,cnt_10,cnt_25,cnt_50,cnt_100,CHO, temperature, \
						hum, reserved, version, errno, checksum = \
						struct.unpack(">bbHHHHHHHHHHHHHHHHHbbH", recv)
                # d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13 = \
				# 		struct.unpack(">xxxxxBxBxBxBxBxBxBxBxBxBxBxBxBxx", recv)

                if sign1 == 0x42 and sign2 == 0x4d:
                    break
            self.ser.close()
            time.sleep(1)
        return [{
                    "name": "PM1.0",
                    "symbol": "ug/m^3",
                    "data": pm1_0
                },
				{
                    "name": "PM2.5",
                    "symbol": "ug/m^3",
                    "data": pm2_5
                },
                {
                    "name": "PM10",
                    "symbol": "ug/m^3",
                    "data": pm10
                },
				{
                    "name": "Formaldehyde concentration",
                    "symbol": "mg/m^3",
                    "data": CHO/1000.0
                },
				{
                    "name": "Temperature",
                    "symbol": "`C",
                    "data": temperature/10.0
                },
				{
                    "name": "Humidity",
                    "symbol": "%",
                    "data": hum/10.0
                },
				]
if __name__ == '__main__':
    sensor = PMS5003()
    while True:
        print sensor.GetData()
        time.sleep(3)
