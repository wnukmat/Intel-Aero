import pickle
import matplotlib.pyplot as plt
import numpy as np
import cv2

def load_data(name):
    with open('data/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_data(data, name):
    with open('data/' + name + '.pkl', 'w') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        
Cameras = load_data('Cameras')

print np.array(Cameras['RGB']).shape

for i in range(np.array(Cameras['RGB']).shape[0]):
	frame = Cameras['RGB'][i]
	cv2.imshow('', frame)		
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
