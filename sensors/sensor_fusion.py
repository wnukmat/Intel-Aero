import numpy as np
from QuaternionManipulation import *

class fusion():
	'''
	A Quaternion-based Unscented Kalman Filter for Orientation Tracking, 
		Based on Paper by: Edgar Kraft Physikalisches Institut, University of Bonn
	'''

	def __init__(self, bias):
		self.bias = bias
		self.Covar = 0.0001*np.eye(3)
		self.NCovar = 0.0001*np.eye(3)
		self.MCovar = 0.0001*np.eye(3)
		self.State = [1.,0.,0.,0.]
		self.roll = 0
		self.pitch = 0
		self.yaw = 0
		self.time = 0
		self.Gravity = np.array([0,0,0,1])
		self.Acc_sensitivity = 16384.
		self.Gyr_sensitivity = 262.4


	def _Adjust(self, ax, ay, az, gx, gy, gz, mx, my, mz):
		AX = (ax - self.bias[0])/self.Acc_sensitivity#
		AY = (ay - self.bias[1])/self.Acc_sensitivity#
		AZ = (az - self.bias[2])/self.Acc_sensitivity+1
		GX = (np.pi/180)*(gx - self.bias[3])/self.Gyr_sensitivity#
		GY = (np.pi/180)*(gy - self.bias[4])/self.Gyr_sensitivity#
		GZ = (np.pi/180)*(gz - self.bias[5])/self.Gyr_sensitivity#
		
		if(mx != None):
			MX = (mx - self.bias[6])
			MY = (my - self.bias[7])
			MZ = (mz - self.bias[8])
			return [AX, AY, AZ], [GX, GY, GZ], [MX, MY, MZ]
		return [AX, AY, AZ], [GX, GY, GZ], [None, None, None]
		
	def _GetSigmas(self):
		Wi = np.zeros((7, 3))
		Wo = np.zeros((1, 3))
		S = np.linalg.cholesky((self.Covar + self.NCovar)*3)
		self.sigmas = np.vstack((Wo, S, -S))
	
	
	def _Predict(self):
		self.Qm = RotVel2QuatIntagration(self.Gyro, self.dt)
		C = float(1)/(6.)
		Weights = C*np.ones((7))
		Qsigmas = [0.,0.,0.,0.]
		Gravity = [0.,0.,0.,1.]
		Sig = [0.,0.,0.,0.]
		StateSigmas = np.zeros((7,4))
		for i in range(7):
			Sig[1:4] = 0.5*self.sigmas[i,:]
			Qsigmas[0:4] = QuatExp(Sig)
			StateSigmas[i,:] = QuatMultiply(self.State, QuatMultiply(Qsigmas, self.Qm))

		StateGuess = QuatMultiply(self.State, self.Qm)
		self.state, self.EviMod, self.Covar = QuatAve(StateSigmas, StateGuess, Weights)
	
	
	def _update_euler(self):
		roll, pitch, yaw = Quat2Euler(self.State)
		self.yaw = 0#yaw*180/np.pi
		self.pitch = pitch*180/np.pi
		self.roll = roll*180/np.pi
		
		
	def _Update(self):
		Sig = np.zeros((7,4))
		StateSigmas = np.zeros((7,4))
		self._GetSigmas()
		for i in range(7):
			Sig[i,1:] = 0.5*self.sigmas[i,:]
			Qsigmas = QuatExp(Sig[i,:])
			StateSigmas[i,:] = QuatMultiply(self.State, QuatMultiply(np.array(Qsigmas).T, self.Qm))
		StateSigmas = np.array(StateSigmas)	
		V = 0.01*np.eye(3)
		Big_Zi = np.zeros((4,7))
		Measurements = np.array(self.Accel).T
		self.EviMod = np.array(self.EviMod).T
		StateSigmas = np.array(StateSigmas).T 
		for i in range(7):
			SigThis = np.array(StateSigmas[:,i]).reshape(4)
			zi = QuatMultiply(QuatMultiply(QuatInverse(SigThis),self.Gravity),(SigThis))
			Big_Zi[:,i] = np.array(zi).reshape(4)

		Big_Zi = Big_Zi[1:,:]
		Zmean = Big_Zi[:,0]*(0) + np.sum(Big_Zi[:,1::],axis = 1)*(1.0/(6))
		z = Big_Zi[:,0] -Zmean
		Pzz = np.outer(z,z)*2
		for i in range(1,7):
			z = Big_Zi[:,i] - Zmean
			Pzz = Pzz + np.outer(z,z)*(1.0/(6))

		Pvv = Pzz + self.NCovar
		z = Big_Zi[:,0] -Zmean
		Pxz = 2*np.outer(self.EviMod[:,0],z)
		for i in range(1,7):
			z = Big_Zi[:,i] - Zmean
			e = self.EviMod[:,i]
			Pxz = Pxz + np.outer(e,z)*(1.0/(6))
	    
		Pvinv = np.linalg.inv(Pvv)
		Kgain = np.dot(Pxz,Pvinv)
	    	gamma = np.dot(Kgain,(self.Accel - Zmean))
		Qgamma = np.append(0,gamma/2.0).reshape(4)
		self.State = QuatMultiply(self.State,  QuatExp(Qgamma)) 
		self.Covar = self.Covar - np.dot(np.dot(Kgain,Pvv),Kgain.T)
	
	
	def Next(self, ax, ay, az, gx, gy, gz, t, mx = None, my = None, mz = None):
		self.Accel, self.Gyro, self.Magnet = self._Adjust(ax, ay, az, gx, gy, gz, mx, my, mz)
		
		self.dt = 1
		if(self.time != 0):
			self.dt = t - self.time
		self.time = t
		
		self._GetSigmas()
		self._Predict()
		self._Update()
		self._update_euler()

		return self.roll, self.pitch, self.yaw



	
	
	

