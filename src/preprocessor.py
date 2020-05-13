from pywt import wavedec, threshold, downcoef, waverec
from utils import HAND_MOTIONS
import time
import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt

################################################
######## CONSTANTS - CONFIG PARAMETERS #########
################################################
NUM_SENSORS = 5
WAVELET = 'db2'  # also try coiflet5
LEVEL = 4  # decimation level
THRESH = 1
# SUBJECT = 0
# MOTION = 'fist'
# TRIAL = 0

def get_data_from_csv(data_path='./data/subject-0/motion-fist/trial-7.csv'):
    """
    Parses emg data from csv file

    @params
    data_path(str) - Required: Where you want to store data

    @returns
    raw_emg_data(np.Arr[np.Arr[Int]]) - 2D Array, w/ Dims NUM_SENSORS by Data
    """
    print("Reading data from {}...".format(data_path))
    raw_emg_data = genfromtxt(data_path, delimiter=',')[2:, :]  # skips first 2 csv lines that are nonsense
    time.sleep(5)  # Just to be safe
    print("Data read complete!")
    return raw_emg_data

def get_length(raw_emg_data):
    """
    Gets the length of the raw emg data signal for a particular sensor

    @params
    raw_emg_data(np.Arr[Int]) - Required: Raw emg data from particular sensor
    """
    N = np.shape(raw_emg_data)[0]  # Signal length
    # N = np.size(emg_data)  # Total signal samples
    return N

def create_sensor2data(raw_emg_data):
    """
    This function gets the raw signal data from an individual sensor.

    Ex: sensor2data[2] -> Sensor data from the third sensor

    @params:
    raw_emg_data(np.Arr[Int]) - Required: Raw emg data from get_data_from_csv

    @returns:
    sensor2data(Dict[Int] -> Arr[Int])
    """
    sensor2data = dict()
    for sensor_num in range(NUM_SENSORS):
        signal = raw_emg_data[:, sensor_num]
        sensor2data[sensor_num] = signal
    return sensor2data

def create_decimation_level_map(sig, max_lvl, mode=''):
    """
    Returns a mapping from c(A/D)n -> [coeffs @ c(A/D)n]
    called detail coefs cause high frequest captures details.

    This map contains the output of the dwt at every level

    @params:
     - sig(np.Array[int]) - Required -> raw data from a single sensor

    Remember:
    - detail coefs at current lvl are dwt of approx. coefs at prev. lvl
    - lowest level of dec. -> highest freq. content
    - full dwt output -> lowest level d-coefs cover half of total energy
    - '             ' -> energy of coefs current lvl half the energy of the prev lvl

        Ex: dwt(sig, 2) = [cA2, CD2, CD1] where CD1 -> .5TE, CD2 -> .25TE
    """
    if mode != 'thresh':
        decimation_map = {
            'c' + type.upper() + str(lvl): downcoef(type, sig, WAVELET, level=lvl)
                for type in ['a', 'd']
                    for lvl in range(1, max_lvl + 1)
            }
    else:
        decimation_map = {
            'c' + type.upper() + str(lvl): apply_threshold(downcoef(type, sig, WAVELET, level=lvl), THRESH)
                for type in ['a', 'd']
                    for lvl in range(1, max_lvl + 1)
        }
        print(decimation_map)
    return decimation_map

def create_sensor2dwt(sensor2data, mode='normal', decimation_level=4):
    """
    Creates a map `sensor2dwt` from sensors to the DWT output decimated at
    `level`

    While the decimation level map allows for analysis of the dwt at each level,
    the sensor2dwt generates the nth level output for the dwt.

    It contains less information than the decimation level map, but provides a
    realistic view of how the typical output for an nth level dwt.

    @params
    sensor2data(Dict[Int] -> Arr[Int]) - Required

    @returns
    sensor2dwt(Dict[Int] -> Arr[Float])
    """
    sensor2dwt = dict()
    if mode == 'normal':
        for sensor_num in range(NUM_SENSORS):
            sensor2dwt[sensor_num] = wavedec(sensor2data[sensor_num], WAVELET, level=decimation_level)
    elif mode == 'thresh':
        for sensor_num in range(NUM_SENSORS):
            arrays = wavedec(sensor2data[sensor_num], WAVELET, level=decimation_level)
            for i in range(len(arrays)):
                arrays[i] = apply_threshold(arrays[i], THRESH)
            sensor2dwt[sensor_num] = arrays
    return sensor2dwt

def plot1(sensor2coefs, sensor_num):
    s2d = sensor2coefs[sensor_num]
    plt.stem(s2d['cD4'])
    plt.show()

def plot_data(sensor2data, sensor2dwt, sensor_num):
    plt.subplot(121)
    plt.stem(sensor2data[sensor_num])
    plt.subplot(122)
    rec_sig = waverec(sensor2dwt[sensor_num], 'db2')
    plt.stem(rec_sig)
    plt.show()

def plot_dwt_data(sensor2coefs, sensor_num):
    coefs = sensor2coefs[sensor_num]
    y_bounds = [-1, 1]

    plt.subplot(421)
    plt.stem(coefs['cA1'])
    axes = plt.gca()
    axes.set_title('cA1', fontsize=10)

    plt.subplot(422)
    plt.stem(coefs['cD1'])
    axes = plt.gca()
    axes.set_title('cD1', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(423)
    axes = plt.gca()
    plt.stem(coefs['cA2'])
    axes.set_title('cA2', fontsize=10)

    plt.subplot(424)
    plt.stem(coefs['cD2'])
    axes = plt.gca()
    axes.set_title('cD2', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(425)
    axes = plt.gca()
    axes.set_title('cA3', fontsize=10)
    plt.stem(coefs['cA3'])

    plt.subplot(426)
    plt.stem(coefs['cD3'])
    axes = plt.gca()
    axes.set_title('cD3', fontsize=10)
    axes.set_ylim(y_bounds)

    plt.subplot(427)
    plt.stem(coefs['cA4'])
    axes = plt.gca()
    axes.set_title('cA4', fontsize=10)

    plt.subplot(428)
    plt.stem(coefs['cD4'])
    axes = plt.gca()
    axes.set_ylim(y_bounds)
    axes.set_title('cD4', fontsize=10)

    plt.tight_layout()
    plt.show()

def apply_threshold(data, thresh=1):
    for i in range(len(data)):
        datum = data[i]
        if datum < thresh:
            data[i] = 0.0
    return data

raw_emg_data = get_data_from_csv()
N = get_length(raw_emg_data)
sensor2data = create_sensor2data(raw_emg_data)
sensor2dwt = create_sensor2dwt(sensor2data)
s2dwt_thresh = create_sensor2dwt(sensor2data, mode='thresh')
coeffs4 = sensor2dwt[4]
sensor2coefs = dict()
s2c_thresh = dict()
for sensor_num in range(NUM_SENSORS):
    sensor2coefs[sensor_num] = create_decimation_level_map(sensor2data[sensor_num], 4)
    s2c_thresh[sensor_num] = create_decimation_level_map(sensor2data[sensor_num], 4, mode='thresh')

# plot_dwt_data(threshold_dwt_coefs(sensor2coefs[0]))
# plot_dwt_data(s2c_thresh, 0)
plot_data(sensor2data, s2dwt_thresh, 0)
plot_data(sensor2data, sensor2dwt, 0)

# d = sensor2dwt[0]
# plot_data2(sensor2data, sensor2dwt, 0)
# plot_data_thresh(sensor2data, sensor2dwt, 0)
# plot_dwt_data(sensor2dwt, sensor2coefs)

#### TODO ####
# calculate threshold
# renormalize w/ soft threshold over detail coefs
# plot_original_data(sensor2data, 0)
# plot_reconstructed_data(sensor2dwt, 0)
# create plotting functions to make research ezier
# d=sensor2data[4]
# a = butter_bandpass_filter(d, 50.0, 450.0, 1000.0)
# plt.subplot(1,2,1)
# plt.stem(d)
# plt.subplot(1,2,2)
# plt.stem(a)
# plt.show()
# base = 10  # log base
# universal_thresh = math.sqrt(2 * math.log(N, base))

def gather_parameters(key):
    subject_query = "What is the subject number?\n"
    motion_query = ("Which hand motion would like to process?\n" +
                    "1: thumb, 2: index, 3: middle, 4: ring+pinky, 5:pinky, 6: open-palm, 7: fist\n")
    decimation_level_query = "What level of decimation? (Should always be 4 for now.)\n"
    trial_query = "What is the trial number to process?\n"
    key2query = {
        "What is the subject number?": subject_query,
        "What is the motion?": motion_query,
        "What is the trial number?": trial_query,
        "What's the decimation lvl?": decimation_level_query,
    }
    try:
        num = int(input(key2query[key]))
        assert (num >= 0 or num in HAND_MOTIONS), "Invalid Integer Input"
        return num
    except ValueError:
        print("Input must be an integer. Please try again...")

# def main():
#     ## Which data file do you want to read?
#     # Gather parameters to construct the data path
#     SUBJECT = gather_parameters('What is the subject number?')
#     MOTION = gather_parameters("What is the motion?")
#     TRIAL = gather_parameters("What is the trial number?")
#     DATA_PATH = './data/subject-{}/motion-{}/trial-{}.csv'.format(
#         SUBJECT,
#         HAND_MOTIONS[MOTION],
#         TRIAL
#     )
#     print(DATA_PATH)
#     raw_emg_data = get_data_from_csv(DATA_PATH)
#     LEVEL = gather_parameters("What's the decimation lvl?")
#     assert (LEVEL == 4), "We're only dealing with level 4 decimation for now!"
#     N = get_length(raw_emg_data)
#
#     ## Create hashmaps
#     sensor2data = create_sensor2data(raw_emg_data)
#     sensor2dwt = create_sensor2dwt(sensor2data)
#     # coeffs4 = sensor2dwt[4]
#     sensor2coefs = dict()
#     for sensor_num in range(NUM_SENSORS):
#         sensor2coefs[sensor_num] = create_decimation_level_map(sensor2data[sensor_num], LEVEL)
#     # This separation of for loops is to encapsulate different logics
#     # Writing DWT Outputs
#     # for sensor_num in range(NUM_SENSORS):
#
# if __name__ == "__main__":
#     main()
