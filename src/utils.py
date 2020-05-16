"""
utils.py

This file contains various utility functions that can be used throughout the
application.
"""
from scipy.signal import butter, lfilter
import datetime
import os

def print_progress_bar(curr_time, start_time, stop_time, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Prints a progress bar to terminal that displays the percentage completion of
    the data recording process.

    Call in a loop to create terminal progress bar.

    Note: This can be used for any timed process.

    @params:
        curr_time   - Required  : current time (datetime.datetime)
        start_time  - Required  : process start time (datetime.datetime)
        stop_time   - Required  : end time (datetime.datetime)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    elapsed_time = curr_time - start_time
    process_time = stop_time - start_time
    percent = ("{0:." + str(decimals) + "f}").format(100 * (elapsed_time / process_time))
    filledLength = int(length * elapsed_time // process_time)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s\n' % (prefix, bar, percent, suffix), end = printEnd)
    if curr_time >= stop_time:
        print()

def path_exists(path):
    """
    Returns True if path exists
    """
    return os.path.exists(path)


def create_dirs(subject_suffix, motion_suffix, trial_suffix):
    """
    Creates subject and motion directories
    Does nothing if it already exists.

    @params:
        subject_suffix(str) - Required : End portion of directory name
        motion_suffix(str) - Required : End portion of motion directory name
        trial_suffix(str) - Required : End portion of CSV file
    """
    base = './data/'
    path = base + 'subject-{}'.format(subject_suffix)
    if not os.path.exists(path):
        os.makedirs(path)
    path += '/motion-{}'.format(motion_suffix)
    if not os.path.exists(path):
        os.makedirs(path)
    return path + '/trial-{}.csv'.format(trial_suffix)

def butter_bandpass(lowcut, highcut, fs, order=5):
    """
    Creates a butterworth filter.

    Used for analyzing the difference between the DWT and a typical bandpass

    @params:
        lowcut(Float) - Required: Lowerbound cutoff frequency
        highcut(Float) - Required: Upperbound cutoff frequency
        fs(Int) - Required: Sampling Rate
        order(Int) - Required: Heuristic proportional to attentuation strength
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    """
    Applies a butterworth filter to the the provided data.

    @params:
        data(Arr[Int]) - Required: Raw emg data from a particular sensor
        lowcut(Float) - Required: Lowerbound cutoff frequency
        highcut(Float) - Required: Upperbound cutoff frequency
        fs(Int) - Required: Sampling Rate
        order(Int) - Required: Heuristic proportional to attentuation strength
    """
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def create_decimation_level_map(sig, max_lvl, mode=''):
    """
    @params:
        sig(np.Array[int]) - Required -> raw data from a single sensor

    @returns:
        decimation_map
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
                arrays[i] = thresh(arrays[i], THRESH)
            sensor2dwt[sensor_num] = arrays
    return sensor2dwt
