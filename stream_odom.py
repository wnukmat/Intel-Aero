import time
import socket
import matplotlib.pyplot as plt
from sensors.get_mag import *
from sensors.get_imu import *
from sensors.process_data import *
from sensors.sensor_fusion import *
from sensors.Madgwich import *
from sensors.helper import *

'''
import sys
sys.path.append("/usr/local/lib/python2.7/dist-packages/pyrealsense-2.2-py2.7-linux-x86_64.egg/pyrealsense/extlib.py:~/pyrealsense-master/pyrealsense")
import pyrealsense as rs
'''
#sensors = load_data('Filter_Test_Set')
'''
sensors = load_data('calibration')
BIAS = ComputeBias(sensors)
'''
imu = configure_bmi160()
bus = configure_bmi150()
#fast_offset_procedure(imu)	#Status register does not seem to update, *****something wrong with this function*****
bias = load_data('bias')

Mfilter = Fusion(bias)		# sensor fusion using the Madgwich Filter
#Mfilter = fusion(bias)		# sensor fusion using unscented Kalman Filter by Kraft

#TCP_IP = '192.168.0.199'
TCP_IP = '192.168.0.105'
#TCP_IP = '192.168.8.140'
TCP_PORT = 5005
BUFFER_SIZE = 1024

roll = []
pitch = []
yaw = []

mx = None
my = None
mz = None

sensors = initialize_dic()
i=0
start_time = time.time()

while i < 12000:

	get_error(imu)
	check_imu = read_FIFO_frame(imu)
	if(check_imu != -1):
		gx, gy, gz, ax, ay, az = check_imu
		i = i + 1
		#sensors = add_to_dic(sensors, check_imu, time.time())

		check_mag = read_mag_frame(bus)
		if(check_mag != -1):
			mx, my, mz, mh = check_mag
			#sensors = add_to_dic(sensors, check_mag, time.time())
	
		Mfilter.Next(ax, ay, az, gx, gy, gz, time.time(), mx, my, mz)
		'''
		with open('orientation.txt', 'w') as fd:
			fd.write(str(Mfilter.roll) + ' ' + str(Mfilter.pitch) + ' ' + str(Mfilter.heading) + '\n')
			fd.close()
		'''
		roll.append(Mfilter.roll)	
		pitch.append(Mfilter.pitch)
		yaw.append(Mfilter.yaw)
		#print str(Mfilter.roll) + ' ' + str(Mfilter.pitch) + ' ' + str(Mfilter.yaw) + ' '
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))
		s.send(str(Mfilter.roll) + ' ' + str(Mfilter.pitch) + ' ' + str(Mfilter.yaw) + ' ')
		while not s.recv(BUFFER_SIZE): break
		#print Mfilter.roll, Mfilter.pitch, Mfilter.heading

'''
plt.figure()
plt.subplot(311)
plt.plot(roll, label='roll')
plt.title('Roll')
plt.subplot(312)
plt.plot(pitch, label='pitch')
plt.title('Pitch')
plt.subplot(313)
plt.plot(yaw, label='yaw')
plt.title('Yaw')
plt.show()
'''
save_data(sensors, 'test')
#plot_data(sensors)






