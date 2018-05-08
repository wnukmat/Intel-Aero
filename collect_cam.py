import sys
import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
import pickle

def load_data(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_data(data, name):
    with open('data/' + name + '.pkl', 'w') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        

def main():
	Cameras = {}
	Cameras['RGB'] = []
	Cameras['DEP'] = []
	Cameras['PC'] = []
	Cameras['time'] = []
	with pyrs.Service() as serv:
		with serv.Device() as dev:
		
			dev.apply_ivcam_preset(0)

			try:  # set custom gain/exposure values to obtain good depth image
				custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 30.0),
					(rs_option.RS_OPTION_R200_LR_GAIN, 100.0)]
				dev.set_device_options(*zip(*custom_options))
			except pyrs.RealsenseError:
				pass  # options are not available on all devices

			try:
				while 1:

					dev.wait_for_frames()
					Cameras['RGB'].append(dev.color)
					Cameras['DEP'].append(dev.depth)
					Cameras['PC'].append(dev._get_pointcloud())
					Cameras['time'].append(time.time())
			
			except KeyboardInterrupt:
				print ''
				print 'Saving Data'
				save_data(Cameras, 'Cameras')	

if __name__ == "__main__":
	main()
