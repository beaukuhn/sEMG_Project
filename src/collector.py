 #!/usr/bin/env python
"""
collector.py

Drives data collection of sEMG data
"""
import serial
import time
import datetime
import csv
from utils import create_dirs, path_exists
from config import (
    RECORDING_DURATION,
    WRITING_DURATION,
    BAUD_RATE,
    INPUT_TIMEOUT,
    HAND_MOTIONS,
    PORT,
)

def open_connection(port=PORT, baud=BAUD_RATE, timeout=INPUT_TIMEOUT):
    connection = serial.Serial(PORT, BAUD_RATE, timeout=INPUT_TIMEOUT)
    print("Arduino connection established: {}".format(connection.is_open))
    return connection

def close_connection(connection):
    connection.close()
    print("Connection closed. Good luck with the project!\n")
    return False

def prompt_dispatcher(connection, function_key):
    """
    Higher order function that dispatches functions that require user input.

    @params:
        function_key(str) - Required : Key that maps to desired function

    @returns:
        function_dispatcher[function_key](function)
    """
    def gather_parameters(key):
        subject_query = "What is the subject number?\n"
        motion_query = ("Which hand motion would like to collect data for?\n" +
                        "1: thumb, 2: index, 3: middle, 4: ring+pinky," +
                        "5:pinky, 6: open-palm, 7: fist\n")
        trial_query = "What is the trial number?\n"
        key2query = {
            "What is the subject number?": subject_query,
            "What is the motion?": motion_query,
            "What is the trial number?": trial_query,
        }
        try:
            num = int(input(key2query[key]))
            assert (num >= 0 or num in HAND_MOTIONS), "Invalid Integer Input"
            return num
        except ValueError:
            print("Input must be an integer. Please try again...")

    def prepare_for_collection():
        prompt = "Prepare yourself for data collection.\nPress any key to begin"
        input(prompt)

    def is_valid_path(path):
        if path_exists(path):
            ans = input("{} already exists. Continue? [Y/n]\n".format(path))
            if ans not in ['y', 'Y']:
                return close_connection(connection)
        return True

    def start_new_trial():
        ans = input("Start trial? [Y/n]\n")
        if ans == "n":
            return close_connection(connection)
        return True

    function_dispatcher =  {
        "gather_parameters_func": gather_parameters,
        "Prepare for data collection.": prepare_for_collection,
        "Is this a valid path?": is_valid_path,
        "Begin a new trial?": start_new_trial,
    }
    return function_dispatcher[function_key]

def parse_data(bytes):
    parsed_data = [int(x) for x in bytes.split()]
    headers = ["Sensor" + str(num) for num in range(5)]
    rows = [ headers ]  # 2D Array that will contain data from each sensor
    curr_row = []
    for i in range(len(parsed_data)):
        if i % 5 == 0:
            rows.append(curr_row)
            curr_row = []
        curr_row.append(parsed_data[i])
    return rows

def write_data(path, data):
    """
    Writes data to the specified CSV file located at `path`
    """
    with open(path, 'a+', newline='') as f:
        print("Waiting {} seconds for operation to complete...".format(WRITING_DURATION))
        writer = csv.writer(f)
        writer.writerows(data)
        time.sleep(WRITING_DURATION)

def record_data(connection, path, hand_motion):
    """
    Initializes the recording of sEMG data for the specified `HAND_MOTION`.
    Writes results to a csv file located at `path` via `connection`

    @param connection(PySerial Obj) - abstract representation of an arduino connection
    @param path(str) - the csv file where the data will be stored
    @param hand_motion(str) - the motion to be performed
    """
    print("Initializing Data Collection - Output File:{}".format(path))
    connection.flushInput()
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=RECORDING_DURATION)
    read_bytes = b''
    print("Data collection started!\nDuration - {} seconds".format(RECORDING_DURATION))
    while datetime.datetime.now() < end_time:
        read_bytes += connection.read(100000000)
    parsed_data = parse_data(read_bytes)
    print("Total number of samples from this trial: {}".format(len(parsed_data)))
    print("Preparing file for write operation...")
    write_data(path, parsed_data)
    print("Data Collection Completed")

def initialize_pipeline(connection):
    """
    Begins the data collection pipeline.
    """
    gather_parameters = prompt_dispatcher(connection, 'gather_parameters_func')
    subject_num = gather_parameters('What is the subject number?')
    motion_num = gather_parameters('What is the motion?')
    trial_num = gather_parameters('What is the trial number?')
    data_path = create_dirs(subject_num, HAND_MOTIONS[motion_num], trial_num)
    if not prompt_dispatcher(connection, "Is this a valid path?")(data_path):
        return close_connection(connection)
    prompt_dispatcher(connection, "Prepare for data collection.")()
    record_data(connection, data_path, HAND_MOTIONS[motion_num])

def main():
    connection = open_connection()
    while prompt_dispatcher(connection, "Begin a new trial?")():
        initialize_pipeline(connection)
    close_connection(connection)

if __name__ == "__main__":
    main()
