'''
===========================================================
Author:			Matthew Wnuk
Business:		None of Yours Incorporated
Date Modified:		Feb 2018
Discription:		Loose End Functions
===========================================================
'''

import pickle
import matplotlib.pyplot as plt
import numpy as np

def load_data(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_data(data, name):
    with open('data/' + name + '.pkl', 'w') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def plot_data(sensors):
	'''
	param: sensors, type dictionary
		plots IMU data from imput dictionary
	'''
	if(isinstance(sensors,list)):
		AX = sensors[0]
		AY = sensors[1]
		AZ = sensors[2]
		GX = sensors[3]
		GY = sensors[4]
		GZ = sensors[5]
		MX = sensors[6]
		MY = sensors[7]
		MZ = sensors[8]	
	else:
		AX = sensors['ax']
		AY = sensors['ay']
		AZ = sensors['az']
		GX = sensors['gx']
		GY = sensors['gy']
		GZ = sensors['gz']
		MX = sensors['mag_x']
		MY = sensors['mag_y']
		MZ = sensors['mag_z']
	
		
	plt.figure()
	plt.subplot(311)
	plt.plot(AX, label='Acc X')
	plt.plot(AY, label='Acc Y')
	plt.plot(AZ, label='Acc Z')
	plt.legend()
	plt.title('Accelerometer')

	plt.subplot(312)
	plt.plot(GX, label='Gyr X')
	plt.plot(GY, label='Gyr Y')
	plt.plot(GZ, label='Gyr Z')
	plt.legend()
	plt.title('Gyro')

	plt.subplot(313)
	plt.plot(MX, label='Mag X')
	plt.plot(MY, label='Mag Y')
	plt.plot(MZ, label='Mag Z')
	plt.legend()
	plt.title('Magnetometer')

	plt.show()


def ComputeBias(sensors):
	'''
	input param: sensors, type dictionary of sensor values
		computes the bias of each degree of freedom of
		the sensors while platform is still

	output param: saves and returns bias data as list

	Only to be called with the calibration set.		
	'''
	AX = sum(sensors['ax'][500:])/len(sensors['ax'][500:])
	AY = sum(sensors['ay'][500:])/len(sensors['ay'][500:])
	AZ = sum(sensors['az'][500:])/len(sensors['az'][500:])
	GX = sum(sensors['gx'][500:])/len(sensors['gx'][500:])
	GY = sum(sensors['gy'][500:])/len(sensors['gy'][500:])
	GZ = sum(sensors['gz'][500:])/len(sensors['gz'][500:])
	'''
	MX = sum(sensors['mag_x'])/len(sensors['mag_x'])
	MY = sum(sensors['mag_y'])/len(sensors['mag_y'])
	MZ = sum(sensors['mag_z'])/len(sensors['mag_z'])
	
	BIAS = [AX, AY, AZ, GX, GY, GZ, MX, MY, MZ]
	'''
	BIAS = [AX, AY, AZ, GX, GY, GZ, 1, 1, 1]
	save_data(BIAS, 'bias')
	return BIAS

def AdjustReadings(ax, ay, az, wx, wy, wz, mx, my, mz, bias):
	#Acc_sensitivity = 2048.		#p8 configured to +/-16g 
	Acc_sensitivity = 16384.		#p8 +/-2g setting by default
	Gyr_sensitivity = 262.4			#p9 configured to 125 range
	AX = (ax - bias[0])/Acc_sensitivity
	AY = (ay - bias[1])/Acc_sensitivity
	AZ = (az - bias[2])/Acc_sensitivity + 1
	GX = (np.pi/180)*(wx - bias[3])/Gyr_sensitivity
	GY = (np.pi/180)*(wy - bias[4])/Gyr_sensitivity
	GZ = (np.pi/180)*(wz - bias[5])/Gyr_sensitivity
	MX = (mx - bias[6])
	MY = (my - bias[7])
	MZ = (mz - bias[8])

	return AX, AY, AZ, GX, GY, GZ, MX, MY, MZ

def np_sensors(sensors):
	AX = np.array(sensors['ax'])
	AY = np.array(sensors['ay'])
	AZ = np.array(sensors['az'])
	GX = np.array(sensors['gx'])
	GY = np.array(sensors['gy'])
	GZ = np.array(sensors['gz'])
	MX = np.array(sensors['mag_x'])
	MY = np.array(sensors['mag_y'])
	MZ = np.array(sensors['mag_z'])

	return AX, AY, AZ, GX, GY, GZ, MX, MY, MZ


def get_reading(sensors, i):
	AX = sensors['ax'][i]
	AY = sensors['ay'][i]
	AZ = sensors['az'][i]
	GX = sensors['gx'][i]
	GY = sensors['gy'][i]
	GZ = sensors['gz'][i]
	imu_time = sensors['imu_time'][i]
	Index_Mag = np.argmin(np.abs(np.array(sensors['mag_time']) - imu_time))
	MX = sensors['mag_x'][Index_Mag]
	MY = sensors['mag_y'][Index_Mag]
	MZ = sensors['mag_z'][Index_Mag]

	return AX, AY, AZ, GX, GY, GZ, MX, MY, MZ, imu_time





































