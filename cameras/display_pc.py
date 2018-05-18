import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def GetPointCloudIR(Image):
	DEPTH_MAX = 10
	DEPTH_MIN = 0.25
	
	oTc = np.zeros((3,3))
	oTc[0,1] = -1
	oTc[1,2] = -1
	oTc[2,0] = 1

	
	fx = 588.998
	fy = 588.998
	cx = 312.165
	cy = 239.368
	depth_scale = 0.001

	increment = 10
	x = np.zeros((Image.shape[0]/increment,Image.shape[1]/increment))
	y = np.zeros((Image.shape[0]/increment,Image.shape[1]/increment))
	z = np.zeros((Image.shape[0]/increment,Image.shape[1]/increment))
	
	
	for i in range(0,Image.shape[0]-increment,increment):
		for j in range(0,Image.shape[1]-increment,increment):
			z[i/increment,j/increment] = Image[i,j]*depth_scale
			x[i/increment,j/increment] = ((j-cx )*z[i/increment,j/increment])/fx
			y[i/increment,j/increment] = ((i-cy )*z[i/increment,j/increment])/fy
		
	x = x.reshape((Image.shape[0]/increment)*(Image.shape[1]/increment))
	y = y.reshape((Image.shape[0]/increment)*(Image.shape[1]/increment))
	z = z.reshape((Image.shape[0]/increment)*(Image.shape[1]/increment))
	
	valid = np.logical_and( (z >= DEPTH_MIN) , (z < DEPTH_MAX) )

	
	x=x[valid]
	y=y[valid]
	z=z[valid
	
	print 'len(x): ', len(x)
	depth = np.zeros((3,len(x)))
	depth[0,:] = x
	depth[1,:] = y
	depth[2,:] = z
	pc = np.dot(oTc.T, depth[0:3,:])

	return pc

def GetPointCloud(Image):
	DEPTH_MAX = 10
	DEPTH_MIN = 0.25
	pc = np.zeros((3,480*640))
	pc[0,:] = Image[:,:,0].reshape(480*640)
	pc[1,:] = Image[:,:,1].reshape(480*640)
	pc[2,:] = Image[:,:,2].reshape(480*640)
	valid = np.logical_and( (pc[2,:] >= DEPTH_MIN) , (pc[2,:] < DEPTH_MAX) )
	pc = pc[:,valid]

	oTc = np.zeros((3,3))
	oTc[0,1] = -1
	oTc[1,2] = -1
	oTc[2,0] = 1
	
	return np.dot(oTc.T, pc)

def Plot_PC(pc):
	ax.scatter(pc[0,::10], pc[1,::10], zs=pc[2,::10], s=3, c='k')
	ax.set_xlabel('X axis')
	ax.set_ylabel('Y axis')
	ax.set_zlabel('Z axis')
	ax.set_xlim((0, 10))
	ax.set_ylim((-0.5,0.5))
	ax.set_zbound((-1,1))
            		
	plt.draw()
	plt.pause(1)	

plot = False
from_depth = False
with pyrs.Service() as serv:
	with serv.Device() as dev:

		dev.apply_ivcam_preset(0)
		if(plot == True):
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			plt.ion()
			plt.show()

		while True:

			plt.cla()
			dev.wait_for_frames()
			if(from_depth==True):
				d = dev.depth# * dev.depth_scale * 1000
				pc = GetPointCloudIR(d)
			else:
				pc = dev.points
				pc = GetPointCloud(pc)
			if(plot == True):
				Plot_PC(pc)












