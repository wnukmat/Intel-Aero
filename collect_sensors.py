import time
from sensors.get_mag import *
from sensors.get_imu import *
from sensors.process_data import *
from helper import *

imu = configure_bmi160()
bus = configure_bmi150()
bias = load_data('bias')
sensors = initialize_dic()

try:
	while 1:
		get_error(imu)
		check_imu = read_FIFO_frame(imu)
		if(check_imu != -1):
			gx, gy, gz, ax, ay, az = check_imu
			i = i + 1
			sensors = add_to_dic(sensors, check_imu, time.time())

			check_mag = read_mag_frame(bus)
			if(check_mag != -1):
				mx, my, mz, mh = check_mag
				sensors = add_to_dic(sensors, check_mag, time.time())
			
except KeyboardInterrupt:
	print ''
	print 'Saving Sensor Data'
	save_data(sensors, 'test')
	plot_data(sensors)






