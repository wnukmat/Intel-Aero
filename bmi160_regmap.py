'''
===========================================================
Author:			Matthew Wnuk
Business:		None of Yours Incorporated
Date Modified:		Feb 2018
Discription:		Register Map for BMI_160 IMU
===========================================================
Notes:
	Default register values do not seem to match the stated values (this may be a function of configuration by the Intel-Aero RTF in which I am accessing the sensor), and LSBs of 'MAG_CONF' are listed as contents of 'GYR_RANGE' register
'''
write = 0x00
read = 0x80

###################################################
#	STATUS Register Map
###################################################
CHIP_ID = 0x00
ERR_REG = 0x02			#see BMI_160 p47 for error codes
PMU_STATUS = 0x03		#Shows power mode of acc, gyr, mag p48 manual
INT_STATUS = 0x1C		#Interrupt status reg p51-53		##(4 Bytes)##
STATUS = 0x1B 			#Status of Data reg p51
FIFO_LENGTH = 0x22		#Current FIFO fill level p54		##(2 Bytes)##
SSELF_TEST = 0x6D		#settings for self test configuration and trigger p77
ALL_NORMAL_MODE = 0x15		#pmu setting if acc, gyro, and mag and all in normal mode

###################################################
#	Raw IMU Sensor Readings Register Map
###################################################
MAG_X_LSB = 0x04
MAG_X_MSB = 0x05
MAG_Y_LSB = 0x06 
MAG_Y_MSB = 0x07
MAG_Z_LSB = 0x08 
MAG_Z_MSB = 0x09 
RHALL_LSB = 0x0A 
RHALL_MSB = 0x0B
GYR_X_LSB = 0x0C 
GYR_X_MSB = 0x0D 
GYR_Y_LSB = 0x0E 
GYR_Y_MSB = 0x0F 
GYR_Z_LSB = 0x10
GYR_Z_MSB = 0x11
ACC_X_LSB = 0x12
ACC_X_MSB = 0x13
ACC_Y_LSB = 0x14
ACC_Y_MSB = 0x15
ACC_Z_LSB = 0x16
ACC_Z_MSB = 0x17

###################################################
#	DATA Readings Register Map
###################################################
FIFO_DATA = 0x24		#Data format depends of settings of FIFO_CONFIG p55
TEMPERATURE = 0x20		#Temperature of sensor p53		##(2 Bytes)##
STEP_CNT = 0x78			#contains number of steps taken		##(2 Bytes)##

##################################################################################
# SENSOR TIME: 39us increments in 3 bytes over 3 registers
# 	starts at 0x000000 and wraps at 0xFFFFFF
# example:
# imu.xfer2([SENSORTIME_0, 0, 0, 0])[1:4] to read all 3 as list from LSByte to MSByte
##################################################################################
SENSORTIME_0 = 0x18										
SENSORTIME_1 = 0x19
SENSORTIME_2 = 0x1A

###################################################
#	Configuration Register Map
###################################################
ACC_CONF = 0x40			#[undersampling(7), bandwidth(6-4), output data rate(3-0)] p56
ACC_RANGE = 0x41 		#Selection of acc g-range [default +/- 2g] p56
GYR_CONF = 0x42 		#[bandwidth(5-4), output data rate(3-0)] p57
GYR_RANGE = 0x43 		#Selection of gyr angular rate range [default +/- 2000 degree/s] p58
MAG_CONF = 0x44 		#[output data rate(3-0)] p59
FIFO_DOWNS = 0x45 		#configures down sample rate of sensors p 59
FIFO_CONFIG = 0x46 		#configures FIFO register p60 		##(2 Bytes)##
MAG_IF = 0x4B 			#see page 61 for discription		##(5 Bytes)##
FOC_CONF = 0x69 		#configuration for fast offset acc/gyr p 75
CONF = 0x6A 			#enables NVM programming p75
IF_CONF = 0x6B 			#settings for digital interface (default 3-wire spi)
PMU_TRIGGER = 0x6C 		#sets trigger conditions to change gyro power mode p76
NV_CONF = 0x70 			#settings for digital interface (loaded at bootup) p78
OFFSET = 0x71 			#offset compensation for acc/gyr p79	##(7 Bytes)##
STEP_CONF = 0x7A 		#configures step detector		##(2 Bytes)##

###################################################
#	Interrupt Register Map
###################################################
INT_EN = 0x50 			#enables interrupts p62			##(3 Bytes)##
INT_OUT_CTRL = 0x53 		#configures interrupts p63			
INT_LATCH = 0x54 		#interrupts mode select p64	
INT_MAP = 0x55 			#controls which interrupts are connected to INT1, INT2 pins
				#	select p65, 			##(3 Bytes)##
INT_DATA = 0x58 		#data source definitions		##(2 Bytes)##
INT_LOWHIGH = 0x5A 		#definitions for low & high g int p67	##(5 Bytes)##
INT_MOTION = 0x5F 		#defines num samples examined for motion int
				#	p69				##(4 Bytes)##
INT_TAP = 0x63 			#defines timing definition for tap p71	##(2 Bytes)##
INT_ORIENT = 0x65 		#defines hysteresis, blocking, and mode for orientation int
				#	p72				##(2 Bytes)##	
INT_FLAT = 0x67 		#defines thresh angle for flat int p71	##(2 Bytes)##
			
###################################################
#	CMD Register Enumerated Settings
###################################################
CMD = 0x7E 			#triggers operations like softreset, NVM programming p81
ACC_NORMAL = 0x11		#puts acc into normal mode
ACC_LP = 0x12			#puts acc into low power mode
GYR_NORMAL = 0x15		#puts gyro into normal mode
GYR_FAST = 0x16			#puts gyro into fast start up mode, see page 76
MAG_SUS = 0x18			#puts magnometer into suspend mode
MAG_LP = 0x1A			#puts magnometer into low power mode
MAG_NORMAL = 0x19		#puts magnometer into normal mode










