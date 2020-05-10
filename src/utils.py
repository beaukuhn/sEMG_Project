"""
This file contains various utility functions used throughout the application.

"""
from scipy.signal import butter, lfilter
import datetime
import os

HAND_MOTIONS = { # This is here to simplify imports
    1: "thumb",
    2: "index",
    3: "middle",
    4: "ring+pinky",
    5: "pinky",
    6: "open-palm",
    7: "fist"
} # Will be refined somehow (Integration with ROS for poses?)

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
    # Print New Line on Complete
    if curr_time >= stop_time:
        print()

def path_exists(path):
    """
    Returns True if path exists

    @params:
        path(str) - Required: File/Directory path
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

    Used for analyzing the different between the DWT and a typical bandpass

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
