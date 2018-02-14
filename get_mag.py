import time
import smbus
from bmi150_regmap import *



def configure_bmi150():
	bus = smbus.SMBus(2)
	ret = bus.write_byte_data(address, Aux_Control, 0x01)	#Set Power Control bit to en
	ret = bus.write_byte_data(address, Aux_Op_Mode, 0x00)	#Set Operation mode to Normal

	return bus

def check_data_ready(bus):
	ret = bus.read_byte_data(address, Aux_HR_lsb)
	return ret & 0x01 == 0x01

def read_mag_frame(bus):
	if(check_data_ready(bus)):
		ret = bus.read_i2c_block_data(address, Aux_x_lsb, 8)
		x = ret[1]*32 + (ret[0]>>3)
		y = ret[3]*32 + (ret[2]>>3)
		z = ret[1]*128 + (ret[4]>>1)
		Rhall = ret[5]*64 + (ret[6]>>2)
		return [x, y, z, Rhall]
	return -1

if __name__=="__main__":
	bus = configure_bmi150()

	
	while True:
		check = read_mag_frame()
		if(check != -1):
			print check



