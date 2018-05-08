import math
import pickle
import matplotlib.pyplot as plt

class sensor_state():
	def __init__():
		self.acc_synth_reg = 0x80
def initialize_dic():
	dic = {}
	dic['gx'] = []
	dic['gy'] = []
	dic['gz'] = []
	dic['ax'] = []
	dic['ay'] = []
	dic['az'] = []
	dic['imu_time'] = []
	dic['mag_x'] = []
	dic['mag_y'] = []
	dic['mag_z'] = []
	dic['mag_hall'] = []
	dic['mag_time'] = []
	dic['RGB'] = []
	dic['DEPTH'] = []
	dic['cam_time'] = []
	return dic

def add_to_dic(dic, data, time):
	#acc_scale_factor = 3000. / (0xFFFF * 16384)
	#gyr_scale_factor = (math.pi / 180) * 3000. /(0xFFFF * 16.4)
	bias = 1.

	if (len(data) == 4):
		dic['mag_x'].append(data[0])
		dic['mag_y'].append(data[1])
		dic['mag_z'].append(data[2])
		dic['mag_hall'].append(data[3])
		dic['mag_time'].append(time)
	elif(len(data) == 6):
		dic['gx'].append(data[0])
		dic['gy'].append(data[1])
		dic['gz'].append(data[2])
		dic['ax'].append(data[3])
		dic['ay'].append(data[4])
		dic['az'].append(data[5])
		dic['imu_time'].append(time)
	else:
		dic['RGB'].append(data[0])
		dic['az'].append(data[1])
		dic['cam_time'].append(time)
	return dic


def save_data(data, name):
	with open('data/' + name + '.pkl', "w") as f:
		pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def load_data(name):
	with open('data/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)
