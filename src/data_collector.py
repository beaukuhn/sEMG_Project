 #!/usr/bin/env python
"""
data_collector.py

Drives data collection of hand motions
"""
import serial
import time
import datetime
import csv
from utils import create_dirs, path_exists, HAND_MOTIONS, print_progress_bar

######### CONFIG PARAMETERS ###########
RECORDING_DURATION = 5  # Data recording length in seconds
WRITING_DURATION = 10  # Data writing length in seconds
BAUD_RATE = 2000000   # Will test varying BAUD rates, though this should suffice
INPUT_TIMEOUT = RECORDING_DURATION  # How long we wait to receive data b4 each iteration
PORT = '/dev/ttyACM0'  # Serial Device Port

######### CONNECT ARDUINO #############
arduino = serial.Serial(PORT, BAUD_RATE, timeout=INPUT_TIMEOUT)
print("Arduino connection established: {}".format(arduino.is_open))

def close_connection(arduino):
    """
    Closes serial port connection, effectively ending process.

    @params:
        arduino(PySerial Obj) - Required: Reads from serial port
    """
    arduino.close()
    print("Connection closed. Good luck with the project!\n")
    return False

def prompt_dispatcher(function_key):
    """
    Higher order function that dispatches functions which initialize prompts.

    @params:
        function_key(str) - Required : Key that maps to desired function

    @returns:
        function_dispatcher[function_key](function)
    """
    def gather_parameters(key):
        subject_query = "What is the subject number?\n"
        motion_query = ("Which hand motion would like to collect data for?\n" +
                        "1: thumb, 2: index, 3: middle, 4: ring+pinky, 5:pinky, 6: open-palm, 7: fist\n")
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

    def is_valid_path(data_path):
        if path_exists(data_path):
            ans = input("{} already exists. Continue? [Y/n]\n".format(data_path))
            if ans not in ['y', 'Y']:
                return close_connection(arduino)
        return True

    def start_new_trial():
        ans = input("Start trial? [y/N]\n")
        if ans != "y":
            return close_connection(arduino)
        return True

    function_dispatcher =  {
        "get gather_parameters function": gather_parameters,
        "Prepare for data collection.": prepare_for_collection,
        "Is this a valid path?": is_valid_path,
        "Begin a new trial?": start_new_trial,
    }
    return function_dispatcher[function_key]

def collect_data(data_path, hand_motion):
    """
    Initializes data collection for hand_motion and writes voltage data
    to csv file located at data_path.

    Note: Max size of Python arrays is 9223372036854775807, so this is fine.

    @param data_path(str) to the csv file where the data will be stored
    @param hand_motion(str) is the motion to be performed
    @param duration(int) is the length of time in seconds for recording
    @param write_time(int) is the amount of time(seconds) to wait for data write
    """
    print("Initializing Data Collection - Output File:{}".format(data_path))
    time.sleep(5)

    # Add names of columns for CSV file
    headers = ["Sensor" + str(num) for num in range(5)]
    rows = [ headers ]  # 2D Array that will contain data from each sensor

    # Create Datetimes that dictate length of data recording
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=RECORDING_DURATION)

    #######################################
    # --------- Data Recording ---------- #
    #######################################
    print("Data collection started!\nDuration - {} seconds".format(RECORDING_DURATION))
    # time.sleep(.1)
    arduino.flushInput()
    read_bytes = b''
    bytes = []
    while datetime.datetime.now() < end_time:
        # print(time.time())
        # read_bytes += arduino.read(10000000000)
        read_bytes += arduino.read(10000000000)
        # bytes.append(read_bytes)
        # print(time.time())
        print('hi :)')
        # print(read_bytes)
        # print_progress_bar(datetime.datetime.now(), start_time, end_time, length=50)
    # split_data = read_bytes.split()
    # print(split_data)
    print(len(bytes))
    # print(bytes[0] in bytes[1])
    parsed_data = [int(x) for x in read_bytes.split()]
    # print(read_bytes)
    N = len(parsed_data)
    curr_row = []
    for i in range(len(parsed_data)):
        if i % 5 == 0:  # Data from a sensors sent in succession
            rows.append(curr_row)
            curr_row = []  # After reading from five sensors, reset array
        curr_row.append(parsed_data[i])
    print("Total number of samples from this trial: {}".format(N))

    ######################################
    #----------- Data Writing -----------#
    ######################################
    print("Preparing file for write operation...")
    with open(data_path, 'a+', newline='') as f:
        time.sleep(5)  # This is here to be safe
        print("Waiting {} seconds for operation to complete...".format(WRITING_DURATION))
        writer = csv.writer(f)
        writer.writerows(rows)
        time.sleep(WRITING_DURATION)

    print("Data Collection Completed.")

def initialize_pipeline():
    """
    Begins the data collection pipeline.

    @params:
        arduino (PySerial Obj) - Required : Object that reads from serial port
    """
    # Gather parameters for directory and csv creation
    gather_parameters = prompt_dispatcher('get gather_parameters function')
    subject_num = gather_parameters('What is the subject number?')
    motion_num = gather_parameters('What is the motion?')
    trial_num = gather_parameters('What is the trial number?')

    # Creates directories if they don't exist, but return path regardless
    data_path = create_dirs(subject_num, HAND_MOTIONS[motion_num], trial_num)

    # If trial data already exists, ask if you wish to proceed.
    if not prompt_dispatcher("Is this a valid path?")(data_path):
        return

    # Prime for data collection
    prompt_dispatcher("Prepare for data collection.")()
    collect_data(data_path, HAND_MOTIONS[motion_num])

def main():
    while prompt_dispatcher("Begin a new trial?")():
        initialize_pipeline()

if __name__ == "__main__":
    main()
