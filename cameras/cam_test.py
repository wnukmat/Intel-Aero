import numpy as np
import cv2
#from skimage.feature import CENSURE
import imutils
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
import pickle
	
def load_data(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_data(data, name):
    with open('data/' + name + '.pkl', 'w') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def extract_harris_corners(rgb):
	gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
	dst = cv2.cornerHarris(gray,2,3,0.04)
	dst = cv2.dilate(dst,None)
	rgb[dst>0.1*dst.max()]=[0,0,255]
	
	return rgb


def main():
	feat = 'surf'
	
	if(feat == 'orb'):
		feature = cv2.ORB_create()
	#if(feat == 'censure'):
	#	feature = CENSURE()
	if(feat == 'sift'):
		feature = cv2.xfeatures2d.SIFT_create()
	if(feat == 'surf'):
		feature = cv2.xfeatures2d.SURF_create(400)
	if(feat == 'brisk'):
		feature = cv2.BRISK_create()
	if(feat == 'kaze'):
		feature = cv2.KAZE_create()
	if(feat == 'akaze'):
		feature = cv2.AKAZE_create()
	if(feat == 'freak'):
		feature = cv2.xfeatures2d.FREAK_create()
	if(feat == 'ensamble'):
		orb = cv2.ORB_create()
		akaze = cv2.AKAZE_create()
		
	with pyrs.Service() as serv:
		with serv.Device() as dev:
		
			dev.apply_ivcam_preset(0)

			try:  # set custom gain/exposure values to obtain good depth image
				custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 30.0),
					(rs_option.RS_OPTION_R200_LR_GAIN, 100.0)]
				dev.set_device_options(*zip(*custom_options))
			except pyrs.RealsenseError:
				pass  # options are not available on all devices

			while 1:
				dev.wait_for_frames()
				rgb = dev.color

				if(feat == 'corners'):
					rgb = extract_harris_corners(rgb)
				'''
				elif(feat == 'freak'):	# Doesn't seems to find any features
					gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
					kp, des = feature.compute(gray, None)
					rgb = cv2.drawKeypoints(rgb, kp, None, color=(0,255,0), flags=0)
				'''
				elif(feat == 'ensamble'):
					rgb = extract_harris_corners(rgb)
					gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
					kpo, des = orb.detectAndCompute(gray, None)
					#kpa, des = akaze.detectAndCompute(gray, None)
					rgb = cv2.drawKeypoints(rgb, kpo, None, color=(0,255,0), flags=0)
					#rgb = cv2.drawKeypoints(rgb, kpa, None, color=(255,0,0), flags=0)					
				else:
					gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
					kp, des = feature.detectAndCompute(gray, None)
					rgb = cv2.drawKeypoints(rgb,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)	

				cv2.imshow('frame', rgb)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
			
if __name__ == "__main__":
	main()




