import time
import numpy as np
import cv2
import thread
from sensors.get_mag import *
from sensors.get_imu import *
from sensors.process_data import *
from helper import *

sensors = load_data('calibration')

plt.subplot(231)
plt.plot(sensors['ax'], label='Acc X')
plt.subplot(232)
plt.plot(sensors['ay'], label='Acc Y')
plt.subplot(233)
plt.plot(sensors['az'], label='Acc Z')
plt.title('Accerometer')

plt.subplot(234)
plt.plot(sensors['gx'], label='Gyr X')
plt.subplot(235)
plt.plot(sensors['gy'], label='Gyr Y')
plt.subplot(236)
plt.plot(sensors['gz'], label='Gyr Z')
plt.title('Gyroscope')
plt.show()

bias = ComputeBias(sensors)

[AX, AY, AZ, GX, GY, GZ, MX, MY, MZ] = np_sensors(sensors)
[AX, AY, AZ, GX, GY, GZ, MX, MY, MZ] = AdjustReadings(AX, AY, AZ, GX, GY, GZ, 1, 1, 1, bias)


plt.subplot(231)
plt.plot(AX, label='Acc X')
plt.subplot(232)
plt.plot(AY, label='Acc Y')
plt.subplot(233)
plt.plot(AZ, label='Acc Z')
plt.title('Accerometer')

plt.subplot(234)
plt.plot(GX, label='Gyr X')
plt.subplot(235)
plt.plot(GY, label='Gyr Y')
plt.subplot(236)
plt.plot(GZ, label='Gyr Z')
plt.title('Gyroscope')
plt.show()
