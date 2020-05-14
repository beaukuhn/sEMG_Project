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
