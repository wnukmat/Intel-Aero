import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option


with pyrs.Service() as serv:
    with serv.Device() as dev:

        dev.apply_ivcam_preset(0)

        while True:


		dev.wait_for_frames()
		RGB = dev.color
		GBR = cv2.cvtColor(RGB, cv2.COLOR_RGB2BGR)
		depth = dev.depth * dev.depth_scale * 1000
		depth = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_RAINBOW)


		cv2.imshow('', depth)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
