from pywt import wavedec, threshold, downcoef, waverec
import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt

NUM_SENSORS = 5
wavelet = 'db2'  # also try coiflet5
level = 4  # decimation level
#fs = 1000 # sampling rate Probably not necessary

def get_data_from_csv(data_path):
    """
    Parses emg data from csv file

    @params
    data_path(str) - Required:
    """
    raw_emg_data = genfromtxt(data_path, delimiter=',')[1:, :]
    return raw_emg_data

def get_length(raw_emg_data):
    """
    Gets the length of the raw emg data signal for a particular sensor

    @params
    raw_emg_data(Arr[Int]) - Required: Raw emg data from particular sensor
    """
    N = np.shape(raw_emg_data)[0]  # Signal length
    # N = np.size(emg_data)  # Total signal samples
    return N

def create_threshhold():
    """
    Creates a threshold based off of signal characteristics. This is used for
    getting rid of noise in the sparse representation of the DWT data
    """
    # universal_thresh = math.sqrt(math.log(N, base))
    # threshed_sig = threshold(signal, , 'soft')
    return

def create_sensor2reads(raw_emg_data):
    """
    This function gets the raw signal data from an individual sensor.

    Ex: sensor2reads[2] -> Sensor data from the third sensor

    @params:
    raw_emg_data(Arr[Int]) - Required: Raw emg data from get_data_from_csv

    @returns:
    sensor2reads(Dict[Int] -> Arr[Int])
    """
    sensor2reads = dict()
    for sensor_num in range(NUM_SENSORS):
        signal = raw_emg_data[:, sensor_num]
        sensor2reads[sensor_num] = signal
    return sensor2reads
# for sensor in range(NUM_SENSORS):
#     signal = emg_data[:, sensor]
#     output = wavedec(signal, wavelet, level=level)
# output is [cA_n, cD_n, cD_n-1,...,cD2, cD1]
# >>> cD1
# array([-0.70710678, -0.70710678, -0.70710678, -0.70710678])

# get Ai,N coefficients at
def create_decimation_level_map(sig, max_lvl, wavelet='db2'):
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
    d = {
        'c' + type.upper() + str(lvl): downcoef(type, sig, wavelet, level=lvl)
            for type in ['a', 'd']
                for lvl in range(1, max_lvl + 1)
        }
    return d

def create_sensor2dwt(sensor2reads, level):
    """
    Creates a map `sensor2dwt` from sensors to the DWT output decimated at
    `level`

    While the decimation level map allows for analysis of the dwt at each level,
    the sensor2dwt generates the nth level output for the dwt.

    It contains less information than the decimation level map, but provides a
    realistic view of how the typical output for an nth level dwt.

    @params
    sensor2reads(Dict[Int] -> Arr[Int]) - Required

    @returns
    sensor2dwt(Dict[Int] -> Arr[Float])
    """
    sensor2dwt = dict()
    for sensor_num in range(NUM_SENSORS):
        sensor2dwt[sensor_num] = wavedec(sensor2reads[sensor_num], wavelet, level=level)
    return sensor2dwt

def get_level_coeffs(sig, level):
    # returns part ('a') or ('d') coefficients at level)
    return

def plot1(sensor2declvlmap, sensor_num):
    s2d = sensor2declvlmap[sensor_num]
    plt.stem(s2d['cD4'])
    plt.show()

def plot_data(sensor2reads, sensor2dwt, sensor_num):
    plt.subplot(121)
    plt.stem(sensor2reads[sensor_num])
    plt.subplot(122)
    rec_sig = waverec(sensor2dwt[sensor_num], 'db2')
    plt.stem(rec_sig)
    plt.show()

def plot_reconstructed_data(sensor2dwt, sensor_num):
    plt.show()

data_path = './data/subject-0/motion-fist/trial-3b.csv'
raw_emg_data = get_data_from_csv(data_path)
N = get_length(raw_emg_data)
sensor2reads = create_sensor2reads(raw_emg_data)
sensor2dwt = create_sensor2dwt(sensor2reads)
coeffs4 = sensor2dwt[4]
sensor2declvlmap = dict()
for sensor_num in range(NUM_SENSORS):
    sensor2declvlmap[sensor_num] = create_decimation_level_map(sensor2reads[sensor_num], 4)
# plot1(sensor2declvlmap, 4)
plot_data(sensor2reads, sensor2dwt, 4)

#### TODO ####
# calculate threshold
# renormalize w/ soft threshold over detail coefs
# plot_original_data(sensor2reads, 0)
# plot_reconstructed_data(sensor2dwt, 0)
# create plotting functions to make research ezier
# d=sensor2reads[4]
# a = butter_bandpass_filter(d, 50.0, 450.0, 1000.0)
# plt.subplot(1,2,1)
# plt.stem(d)
# plt.subplot(1,2,2)
# plt.stem(a)
# plt.show()
# base = 10  # log base
# universal_thresh = math.sqrt(2 * math.log(N, base))
