"""
config.py

This file is used for storing configuration settings in order to
reduce redundancy
"""

HAND_MOTIONS = { # This is here to avoid redundancy via imports
    1: "thumb",
    2: "index",
    3: "middle",
    4: "ring+pinky",
    5: "pinky",
    6: "open-palm",
    7: "fist"
}

NUM_SENSORS = 5
WAVELET = 'db2'  # also try coiflet5
LEVEL = 4  # decimation level
THRESH = 1
RECORDING_DURATION = 5  # Data recording length in seconds
WRITING_DURATION = 10  # Data writing length in seconds
BAUD_RATE = 2000000   # Will test varying BAUD rates, though this should suffice
INPUT_TIMEOUT = RECORDING_DURATION  # How long we wait to receive data b4 each iteration
# PORT = '/dev/cu.usbmodem14201' #'/dev/ttyACM0'  # Serial Device Port
PORT = '/dev/ttyACM0'
