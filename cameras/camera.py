import numpy as np
import cv2
import imutils
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyrealsense as pyrs
from pyrealsense.constants import rs_option


class camera():

	def __init__(self):
		self.surf = cv2.xfeatures2d.SURF_create(800)
		self.orb = cv2.ORB_create()
		self.brisk = cv2.BRISK_create()
		self.kaze = cv2.KAZE_create()

	def GetPointCloudIR(self, Depth, Pts):
		DEPTH_MAX = 3
		DEPTH_MIN = 0.2
	
		oTc = np.zeros((3,3))
		oTc[0,1] = -1
		oTc[1,2] = -1
		oTc[2,0] = 1

	
		fx = 588.998
		fy = 588.998
		cx = 312.165
		cy = 239.368
		depth_scale = 0.001

		x = np.zeros(len(Pts[1]))
		y = np.zeros(len(Pts[1]))
		z = np.zeros(len(Pts[1]))
	
	
		for i in range(len(Pts[1])):
			z[i] = Depth[Pts[1][i],Pts[0][i]]*depth_scale
			x[i] = (Pts[0][i]-cx )*z[i]/fx
			y[i] = (Pts[1][i]-cy )*z[i]/fy
	
		valid = np.logical_and( (z >= DEPTH_MIN) , (z < DEPTH_MAX) )

		x=x[valid]
		y=y[valid]
		z=z[valid]

		depth = np.zeros((3,len(x)))
		depth[0,:] = x
		depth[1,:] = y
		depth[2,:] = z
		pc = np.dot(oTc.T, depth[0:3,:])

		return pc

	def Plot_PC(self, pc):
		plt.cla()
		ax.scatter(pc[0,::1], pc[1,::1], zs=pc[2,::1], s=3, c='k')
		ax.set_xlabel('X axis')
		ax.set_ylabel('Y axis')
		ax.set_zlabel('Z axis')
		ax.set_xlim((0, 5))
		ax.set_ylim((-0.5,0.5))
		ax.set_zbound((-.5,.5))
		    		
		plt.draw()
		plt.pause(1)

	def Extract_Features(self, Image):
		pc = [[],[]]
		gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
		kps, des = self.surf.detectAndCompute(gray, None)
		kpo, des = self.orb.detectAndCompute(gray, None)
		kpb, des = self.brisk.detectAndCompute(gray, None)
		kpk, des = self.kaze.detectAndCompute(gray, None)
		#cv2.drawKeypoints(rgb, kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, outImage=Image)
		for i in range(len(kps)):
			pc[0].append(int(kps[i].pt[0]))
			pc[1].append(int(kps[i].pt[1]))
		for i in range(len(kpo)):
			pc[0].append(int(kpo[i].pt[0]))
			pc[1].append(int(kpo[i].pt[1]))		
		for i in range(len(kpb)):
			pc[0].append(int(kpb[i].pt[0]))
			pc[1].append(int(kpb[i].pt[1]))
		for i in range(len(kpk)):
			pc[0].append(int(kpk[i].pt[0]))
			pc[1].append(int(kpk[i].pt[1]))	
		#print len(pc[1])
		return Image, pc


	def cat(self, RGB, Depth):
		return np.concatenate((RGB, Depth), axis=1)
		



if __name__ == '__main__':
	cam = camera()
	with pyrs.Service() as serv:
		with serv.Device() as dev:
			dev.apply_ivcam_preset(0)
			fig = plt.figure()
			ax = fig.gca(projection='3d')
			plt.ion()
			plt.show()
			while 1:
				dev.wait_for_frames()
				rgb = dev.color
				depth = dev.depth

				rgb, pts = cam.Extract_Features(rgb)
				PC = cam.GetPointCloudIR(depth, pts)
				cam.Plot_PC(PC)

				'''
				cv2.imshow('frame', rgb)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
				'''
