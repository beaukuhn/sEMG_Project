from pywt import wavedec, threshold, downcoef, waverec
from utils import HAND_MOTIONS
import numpy as np
import time
import math
import matplotlib.pyplot as plt

NUM_SENSORS = 5
WAVELET = 'db2'  # also try coiflet5
LEVEL = 4  # decimation level
THRESH = 1

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

def s2dwt(raw_emg, level=LEVEL, mode='normal'):
	"""
	@params
	raw_emg(List[List[Int]]) - Data from csv

	@returns
	s2dwt(Dict[Int] -> Arr[Float])
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
    Output = [cA04 cD04 cA03 cD03 ... cA14 cD24 ... cA44 cD4 ....]
    Ex: cA04 -> 1st Sensor, 4th level of decimation
    Ex: cD31 -> 4th Sensor, 1st level of decimation
    """
    output = []
    for dec_level in range(LEVEL, -1, -1):
        for type in ['a', 'd']:
            if mode == 'normal':
                output.append(downcoef(type, raw_emg, WAVELET, level=dec_level))
            elif mode == 'thresh':
                output.append(thresh(downcoef(type, raw_emg, WAVELET, level=dec_level)))
    return output

# def gather_parameters(key):
#     subject_query = "What is the subject number?\n"
#     motion_query = ("Which hand motion would like to process?\n" +
#                     "1: thumb, 2: index, 3: middle, 4: ring+pinky, 5:pinky, 6: open-palm, 7: fist\n")
#     decimation_level_query = "What level of decimation? (Should always be 4 for now.)\n"
#     trial_query = "What is the trial number to process?\n"
#     key2query = {
#         "What is the subject number?": subject_query,
#         "What is the motion?": motion_query,
#         "What is the trial number?": trial_query,
#         "What's the decimation lvl?": decimation_level_query,
#     }
#     try:
#         num = int(input(key2query[key]))
#         assert (num >= 0 or num in HAND_MOTIONS), "Invalid Integer Input"
#         return num
#     except ValueError:
#         print("Input must be an integer. Please try again...")

# raw_emg = get_data_from_csv()
# N = get_length(raw_emg)
# sensor2data = create_sensor2data(raw_emg)
# sensor2dwt = create_sensor2dwt(sensor2data)
# s2dwt_thresh = create_sensor2dwt(sensor2data, mode='thresh')
# coeffs4 = sensor2dwt[4]
# sensor2coefs = dict()
# s2c_thresh = dict()
# for sensor_num in range(NUM_SENSORS):
#     sensor2coefs[sensor_num] = create_decimation_level_map(sensor2data[sensor_num], 4)
#     s2c_thresh[sensor_num] = create_decimation_level_map(sensor2data[sensor_num], 4, mode='thresh')
