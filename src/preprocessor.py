"""
preprocessor.py

This file handles preprocessing of the raw sEMG data, i.e. cleaning, etc.
"""
from pywt import wavedec, threshold, downcoef, waverec
from config import HAND_MOTIONS, NUM_SENSORS, LEVEL, THRESH, WAVELET
import numpy as np
import time
import math
import matplotlib.pyplot as plt

def thresh(data, thresh=THRESH):
	"""
	Applies a threshold to each element in data

	@params
	- data(List[Int])
	"""
	for i in range(len(data)):
		datum = data[i]
		if datum < thresh:
			data[i] = 0.0
	return data

def decimation_arrays(raw_emg, mode='normal'):
    """
	@returns
    	output[List[List[Int]]] := [cA4 cD4 cA3 cD3 cA2 ... ]
    """
    output = []
    for dec_level in range(LEVEL, -1, 0):
        for type in ['a', 'd']:
            if mode == 'normal':
                output.append(downcoef(type, raw_emg, WAVELET, level=dec_level))
            elif mode == 'thresh':
                output.append(thresh(downcoef(type, raw_emg, WAVELET, level=dec_level)))
    return output

def s2dwt(raw_emg, level=LEVEL, mode='normal'):
	"""
	@params
	raw_emg(List[List[Int]]) - Data from csv

	@returns
	s2dwt(Dict[Int] -> np.Arr[Float])
	"""
	s2dwt = []
	for sensor_num in range(NUM_SENSORS):
		coef_list = wavedec(raw_emg[:,sensor_num], WAVELET, level)
		if mode == 'normal':
			pure_coefs = [coef for level in coef_list for coef in level]
		elif mode == 'thresh':
			pure_coefs = thresh([coef for level in coef_list for coef in level])
		s2dwt.extend(pure_coefs)
	return s2dwt

def decimation_arrays(raw_emg, mode='normal'):
    """
	Returns the output of the dwt at each level of decimation in an array
    Ex: Output = [cA4 cD4 cA3 cD3 ... ]
    """
    output = []
    for dec_level in range(LEVEL, 0, -1):
        for type in ['a', 'd']:
            if mode == 'normal':
                output.extend(downcoef(type, raw_emg, WAVELET, level=dec_level))
            elif mode == 'thresh':
                output.extend(thresh(downcoef(type, raw_emg, WAVELET, level=dec_level)))
    return output
