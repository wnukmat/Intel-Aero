import time
import smbus
from ctypes import c_short
from bmi150_regmap import *
from process_data import *


def log_mag(bus, sensors):
	while(1):
		check_mag = read_mag_frame(bus)
		if(check_mag != -1):
			sensors = add_to_dic(sensors, check_mag, time.time())
		time.sleep(0.1)

def configure_bmi150():
	bus = smbus.SMBus(2)
	ret = bus.write_byte_data(address, Aux_Control, 0x01)	#Set Power Control bit to en
	ret = bus.write_byte_data(address, Aux_Op_Mode, 0x38)	#Set Operation mode to Normal, 30Hz

	return bus

def check_data_ready(bus):
	ret = bus.read_byte_data(address, Aux_HR_lsb)
	return ret & 0x01 == 0x01

def read_mag_frame(bus):
	if(check_data_ready(bus)):
		ret = bus.read_i2c_block_data(address, Aux_x_lsb, 8)
		x = ret[1]*32 + (ret[0]>>3)
		if(x > 4096):
			x = x - 8192
		y = ret[3]*32 + (ret[2]>>3)
		if(y > 4096):
			y = y - 8192
		z = ret[5]*128 + (ret[4]>>1)
		if(z > 16384):
			z = z - 32768
		Rhall = ret[7]*64 + (ret[6]>>2)
		if(Rhall > 8192):
			Rhall = Rhall - 16384
		return [x, y, z, Rhall]
	return -1

if __name__=="__main__":
	bus = configure_bmi150()

	
	while True:
		check = read_mag_frame()
		if(check != -1):
			print check



