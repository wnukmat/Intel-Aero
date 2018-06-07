#!/usr/bin/python
'''
	Author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
from PIL import Image
import threading
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from SocketServer import ThreadingMixIn
import StringIO
import time
capture=None
import numpy as np
import imutils
import pyrealsense as pyrs
from pyrealsense.constants import rs_option

class CamHandler(BaseHTTPRequestHandler):
	def extract_harris_corners(self, rgb):
		gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
		dst = cv2.cornerHarris(gray,2,3,0.04)
		dst = cv2.dilate(dst,None)
		rgb[dst>0.1*dst.max()]=[0,0,255]
	
		return rgb

	def do_GET(self):
		with pyrs.Service() as serv:
			with serv.Device() as dev:
		
				dev.apply_ivcam_preset(0)

				try:  # set custom gain/exposure values to obtain good depth image
					custom_options = [(rs_option.RS_OPTION_R200_LR_EXPOSURE, 30.0),
						(rs_option.RS_OPTION_R200_LR_GAIN, 100.0)]
					dev.set_device_options(*zip(*custom_options))
				except pyrs.RealsenseError:
					pass  # options are not available on all devices

				self.send_response(200)
				self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
				self.end_headers()
				
				while 1:
					dev.wait_for_frames()
					rgb = dev.color
					depth = dev.depth * dev.depth_scale * 1000
					depth = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_RAINBOW)


					try:
						imgRGB=cv2.cvtColor(rgb,cv2.COLOR_BGR2RGB)
						imgRGB = np.concatenate((imgRGB, depth), axis=1)
						jpg = Image.fromarray(imgRGB)
						tmpFile = StringIO.StringIO()
						jpg.save(tmpFile,'JPEG')
						self.wfile.write("--jpgboundary")
						self.send_header('Content-type','image/jpeg')
						self.send_header('Content-length',str(tmpFile.len))
						self.end_headers()
						jpg.save(self.wfile,'JPEG')
						print("SERVED IMAGE")
						time.sleep(0.05)
					except KeyboardInterrupt:
						break
				return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	"""Handle requests in a separate thread."""

def stream():
	try:
		server = ThreadedHTTPServer(('', 8080), CamHandler)
		print "server started"
		server.serve_forever()
	except KeyboardInterrupt:
		server.socket.close()

if __name__ == '__main__':
	stream()

