import logging
logging.basicConfig(level=logging.INFO)

import time
import numpy as np
import cv2
import pyrealsense as pyrs
from pyrealsense.constants import rs_option
from pyrealsense.extruct import rs_intrinsics
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
depth_fps = 90
depth_stream = pyrs.stream.DepthStream(fps=depth_fps)


def convert_z16_to_bgr(frame):
    '''Performs depth histogram normalization

    This raw Python implementation is slow. See here for a fast implementation using Cython:
    https://github.com/pupil-labs/pupil/blob/master/pupil_src/shared_modules/cython_methods/methods.pyx
    '''
    hist = np.histogram(frame, bins=0x10000)[0]
    
    hist = np.cumsum(hist)
    hist -= hist[0]
    rgb_frame = np.empty(frame.shape[:2] + (3,), dtype=np.uint8)

    zeros = frame == 0
    non_zeros = frame != 0
    #print 'hist.shape: ', hist[frame[non_zeros]] * 255 / hist[0xFFFF]
    f = hist[frame[non_zeros]] * 255 / hist[0xFFFF]
    rgb_frame[non_zeros, 0] = 255 - f
    rgb_frame[non_zeros, 1] = 100
    rgb_frame[non_zeros, 2] = f
    rgb_frame[zeros, 0] = 0
    rgb_frame[zeros, 1] = 0
    rgb_frame[zeros, 2] = 0
    return rgb_frame


with pyrs.Service() as serv:
    with serv.Device(streams=(depth_stream,)) as dev:

        dev.apply_ivcam_preset(0)
        print extruct.rs_intrinsics
        cnt = 0
        last = time.time()
        smoothing = 0.9
        fps_smooth = depth_fps

        while True:

            cnt += 1
            if (cnt % 30) == 0:
                now = time.time()
                dt = now - last
                fps = 30/dt
                fps_smooth = (fps_smooth * smoothing) + (fps * (1.0-smoothing))
                last = now

            dev.wait_for_frames()
            d = dev.depth
            d[d >= 1000]  = 0
            indices = np.where(d > 0)
            points = np.zeros((len(indices[0]),3))
            print points.shape, indices[0].shape
            points[:,0] = indices[0]
            points[:,1] = indices[1]
            points[:,2] = d[indices[0], indices[1]]
            print points
            #cv2.imsave('depth', d)
            #d = convert_z16_to_bgr(d)
            #print np.max(d)
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            plt.scatter(points[0], points[1], zs=points[2],s=1,c='k')
            plt.xlabel('x axis')
            plt.ylabel('y axis')
            plt.show()
            '''
            cv2.putText(d, str(fps_smooth)[:4], (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255))

            cv2.imshow('', d)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            '''
