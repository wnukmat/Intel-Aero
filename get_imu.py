import spidev
import time
import smbus
from bmi150_regmap import *
from bmi160_regmap import *


def open_imu():
	'''
	Opens BMI_160 imu on bus 3, cs 0 associated with the Intel-Aero RTF platform
	'''
	imu = spidev.SpiDev()
	opened = imu.open(3,0)		# SPI bus 3, CS 0

	if(opened == 0):
		print 'failed to open'
		return -1

	return imu

def configure_pmu(imu):
	'''
	###############################################################################
	Need to write a while catch to ensure registers are writen to before moving on.
	###############################################################################
	'''
	imu.xfer2([CMD + write, ACC_NORMAL])
	time.sleep(0.05)
	imu.xfer2([CMD + write, GYR_NORMAL])
	time.sleep(0.05)
	imu.xfer2([CMD + write, MAG_NORMAL])
	print 'pmu status: ', imu.xfer2([PMU_STATUS + read, 0x00])[1]


def configure_acc(imu):
	'''
	Set Acc Data Rate @ 100Hz, see page 56
	'''
	imu.xfer2([ACC_CONF + write, 0x28])
	time.sleep(0.05)	


def configure_gyr(imu):	
	'''
	Set Gyro Data Rate @ 100Hz, see page 57
	'''
	imu.xfer2([GYR_CONF + write, 0x28])
	time.sleep(0.05)

def enable_mag(imu):
	imu.xfer2([MAG_IF_1 + write, 0x03])
	time.sleep(0.05)
	imu.xfer2([Aux_Data2write + write, 0x00])
	time.sleep(0.05)
	imu.xfer2([Aux_Reg2write + write, 0x03])
	time.sleep(0.05)
	print 'STATUS: ', imu.xfer2([STATUS + read, 0x00])[1]

def configure_FIFO(imu):	
	'''
	Set Acc & Gyro Feeds to FIFO
	'''
	imu.xfer2([FIFO_CONFIG2 + write, 0xC2])
	time.sleep(0.05)


def read_FIFO_frame(imu):
	FIFO_Length = imu.xfer2([FIFO_LENGTH + read, 0,0])[1:]	#Check if the FIFO is empty
	if((FIFO_Length[0] + FIFO_Length[1]*255) > 12):		#If not, read frame
		data =  imu.xfer2([FIFO_DATA + read, 0,0,0,0,0,0,0,0,0,0,0,0,0])[2:]
		gx = fuse_bits(data[0], data[1])
		gy = fuse_bits(data[2], data[3])
		gz = fuse_bits(data[4], data[5])
		ax = fuse_bits(data[6], data[7])
		ay = fuse_bits(data[8], data[9])
		az = fuse_bits(data[10], data[11])
		return [gx, gy, gz, ax, ay, az]
	return -1


def fuse_bits(lsb, msb):
	return lsb + 256*msb


def read_raw_sensors(imu):
	ACC = imu.xfer2([ACC_ALL + read, 0,0,0,0,0,0])
	GYR = imu.xfer2([GYR_ALL + read, 0,0,0,0,0,0])

	return [ACC[1:], GYR[1:]]


def configure_bmi160():
	imu = open_imu()
	if(imu == -1):
		exit()
	configure_pmu(imu)
	configure_acc(imu)
	configure_gyr(imu)

	imu.xfer2([FIFO_CONFIG2 + write, 0xD0])
	
	return imu

if __name__=="__main__":
	imu = configure_bmi160()

	while True:
		time.sleep(0.5)
		check = read_FIFO_frame(imu)
		if(check != -1):
			print 'IMU: ', check
			[gx, gy, gz, ax, ay, az] = check 


	imu.close()





