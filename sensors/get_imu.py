'''
===========================================================
Author:			Matthew Wnuk
Business:		None of Yours Incorporated
Date Modified:		Feb 2018
Discription:		Functions for setting the BMI160
===========================================================
Notes:
	Page numbers refer to Data Sheet DS000-07-786474
'''

import spidev
import time
import smbus
from bmi150_regmap import *
from bmi160_regmap import *
from ctypes import c_short


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
	breaker = 0
	imu.xfer2([CMD + write, ACC_NORMAL])
	while((imu.xfer2([PMU_STATUS + read, READBYTE])[1] & 0x30) != 0x10):
		breaker += 1
		if(breaker > 10):
			return -1
	imu.xfer2([CMD + write, GYR_NORMAL])
	while((imu.xfer2([PMU_STATUS + read, READBYTE])[1] & 0x0C) != 0x04):
		if(breaker > 20):
			return -1
	
def fast_offset_procedure(imu):
	'''
	Set offset compensation, for procedure see page 43
	'''
	print 'starting offset compensation procedure'
	imu.xfer2([FOC_CONF + write, 0x7E])	#auto compensate for x->0, y->0, z->-1
	while(imu.xfer2([FOC_CONF + read, READBYTE])[1] != 0x7E):
		pass
	imu.xfer2([CMD + write, FOC_START])	#send start command	
	while((imu.xfer2([STATUS + read, READBYTE])[1] & 0x04) != 0x04):
		pass
	print
	print 'procedure complete, updating non-volatile memory'
	imu.xfer2([CONF + write, 0x02])		#unlock the non-volatile memory
	while((imu.xfer2([CONF + read, READBYTE])[1] & 0x02) != 0x02):
		pass
	imu.xfer2([CMD + write, PROG_NVM])	#program non-volatile memory
	while((imu.xfer2([STATUS + read, READBYTE])[1] & 0x08) != 0x08):
		pass
	print 'memory update complete'



def configure_acc(imu):
	'''
	Set Acc Data Rate @ 100Hz, see page 56
	'''
	imu.xfer2([ACC_CONF + write, 0x28])		#ac_bwp = normal, acc_odr = 100Hz
	breaker = 0
	while((imu.xfer2([ACC_CONF + read, READBYTE])[1] & 0x7F) != 0x28):
		breaker += 1
		if(breaker > 10):
			return -1	
	imu.xfer2([ACC_RANGE + write, A_RANGE_2G])		#
	while((imu.xfer2([ACC_RANGE + read, READBYTE])[1] & 0x0F) != A_RANGE_2G):
		breaker += 1
		if(breaker > 10):
			return -1

def configure_gyr(imu):	
	'''
	Set Gyro Data Rate @ 100Hz, see page 57
	'''
	imu.xfer2([GYR_CONF + write, 0x28])		#gyr_bwp = normal, gyr_odr = 100Hz
	breaker = 0
	while((imu.xfer2([GYR_CONF + read, READBYTE])[1] & 0x6F) != 0x28):
		breaker += 1
		if(breaker > 10):
			return -1	
	imu.xfer2([GYR_RANGE + write, G_RANGE_125])
	while((imu.xfer2([GYR_RANGE + read, READBYTE])[1] & 0x07) != G_RANGE_125):
		breaker += 1
		if(breaker > 20):
			return -1

def enable_mag(imu):
	imu.xfer2([MAG_IF_1 + write, 0x03])
	time.sleep(0.05)
	imu.xfer2([Aux_Data2write + write, 0x00])
	time.sleep(0.05)
	imu.xfer2([Aux_Reg2write + write, 0x03])
	time.sleep(0.05)
	print 'STATUS: ', imu.xfer2([STATUS + read, READBYTE])[1]

def configure_FIFO(imu):	
	'''
	Set Acc & Gyro Feeds to FIFO
	'''
	imu.xfer2([FIFO_CONFIG2 + write, 0xC2])
	while((imu.xfer2([FIFO_CONFIG2 + read, READBYTE])[1] & 0xC2) != 0xC2):
		breaker += 1
		if(breaker > 10):
			return -1


def read_FIFO_frame(imu):
	FIFO_Length = imu.xfer2([FIFO_LENGTH + read, 0,0])[1:]	#Check if the FIFO is empty
	if((FIFO_Length[0] + FIFO_Length[1]*255) > 12):		#If not, read frame
		data =  imu.xfer2([FIFO_DATA + read, 0,0,0,0,0,0,0,0,0,0,0,0])
		gx = c_short(fuse_bits(data[1], data[2])).value
		gy = c_short(fuse_bits(data[3], data[4])).value
		gz = c_short(fuse_bits(data[5], data[6])).value
		ax = c_short(fuse_bits(data[7], data[8])).value
		ay = c_short(fuse_bits(data[9], data[10])).value
		az = c_short(fuse_bits(data[11], data[12])).value
		return [gx, gy, gz, ax, ay, az]
	return -1

def read_raw_FIFO_frame(imu):
	FIFO_Length = imu.xfer2([FIFO_LENGTH + read, 0,0])[1:]	#Check if the FIFO is empty
	if((FIFO_Length[0] + FIFO_Length[1]*255) > 12):		#If not, read frame
		data =  imu.xfer2([FIFO_DATA + read, 0,0,0,0,0,0,0,0,0,0,0,0,0])

		return data
	return -1

def fuse_bits(lsb, msb):
	return lsb + 256*msb


def read_raw_sensors(imu):
	ACC = imu.xfer2([ACC_ALL + read, 0,0,0,0,0,0])
	GYR = imu.xfer2([GYR_ALL + read, 0,0,0,0,0,0])

	return [ACC[1:], GYR[1:]]

def update_Offset(imu, value):
	imu.xfer2([OFFSET0 + write, value])
	breaker = 0
	while(imu.xfer2([OFFSET0 + read, READBYTE])[1] != value):
		breaker += 1
		if(breaker > 10):
			return -1


def configure_Offset(imu):
	imu.xfer2([OFFSET0 + write, 0x7F])
	breaker = 0
	while(imu.xfer2([OFFSET0 + read, READBYTE])[1] != 0x7F):
		breaker += 1
		if(breaker > 10):
			return -1

	imu.xfer2([OFFSET1 + write, 0x7F])
	breaker = 0
	while(imu.xfer2([OFFSET1 + read, READBYTE])[1] != 0x7F):
		breaker += 1
		if(breaker > 10):
			return -1
	imu.xfer2([OFFSET3 + write, 0xFF])
	breaker = 0
	while(imu.xfer2([OFFSET3 + read, READBYTE])[1] != 0xFF):
		breaker += 1
		if(breaker > 10):
			return -1

	imu.xfer2([OFFSET4 + write, 0xFF])
	breaker = 0
	while(imu.xfer2([OFFSET4 + read, READBYTE])[1] != 0xFF):
		breaker += 1
		if(breaker > 10):
			return -1
	imu.xfer2([OFFSET5 + write, 0xFF])
	breaker = 0
	while(imu.xfer2([OFFSET5 + read, READBYTE])[1] != 0xFF):
		breaker += 1
		if(breaker > 10):
			return -1
	imu.xfer2([OFFSET6 + write, OFFSET_OFF])
	breaker = 0
	while(imu.xfer2([OFFSET6 + read, READBYTE])[1] != OFFSET_OFF):
		breaker += 1
		if(breaker > 10):
			return -1

def configure_bmi160():
	imu = open_imu()
	if(imu == -1):
		exit()
	if configure_pmu(imu) == -1:
		print 'pmu config failed'
	if configure_acc(imu) == -1:
		print 'acc config failed'
	if configure_gyr(imu) == -1:
		print 'gyro config failed'
	if configure_FIFO(imu) == -1:
		print 'FIFO config failed'
	'''
	if configure_Offset(imu) == -1:
		print 'Offset config failed'
	'''

	
	return imu

def log_imu(imu):
	'''
	Intended to be used in multi-thread, not correctly writen
	'''
	while(1):
		check_imu = read_FIFO_frame(imu)
		if(check_imu != -1):
			sensors = add_to_dic(sensors, check_imu, time.now())

def get_error(imu):
	error = imu.xfer2([ERR_REG + read, READBYTE])[1]
	if error & 0x1F != 0:
		print 'error occured: ', error


if __name__=="__main__":
	imu = configure_bmi160()

	while True:
		time.sleep(0.5)
		check = read_FIFO_frame(imu)
		if(check != -1):
			print 'IMU: ', check
			[gx, gy, gz, ax, ay, az] = check 


	imu.close()





