 #!/usr/bin/env python
"""
data_collector.py

Drives data collection of hand motions
"""
import serial
import time
import datetime
import csv

from utils import print_progress_bar, create_directory

HAND_MOTIONS = {0: 'open_palm', 1: 'closed_fist'}  # Will be added to

def connect_arduino(port_str='/dev/ttyACM0', baud_rate=9600):
    """
    Connects to the Serial Port on the Arduino

    @param port_str(str) is found by typing ls /dev/tty* in terminal
    @param baud_rate(int) is the symbol transfer rate

    @return arduino(PySerial) is the PySerial port wrapper to be read from
    """
    arduino = serial.Serial(port_str, baud_rate)
    time.sleep(1)
    print("Serial Port Open?: {}".format(arduino.is_open))
    return arduino

def collect_data(data_path, hand_motion, arduino, duration=60, write_time=45):
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
    print("Data collection started!'\nDuration - {}".format(duration))
    headers = ["Sensor" + str(num) for num in range(5)]
    rows = [ headers ]
    start_time = datetime.datetime.now()
    end_time = start_time + datetime.timedelta(seconds=duration)
    while True:
        curr_row = []
        for sensor_num in range(5):
            read_bytes = arduino.read(size=2)
            val = int.from_bytes(read_bytes, 'little', signed=True)
            time.sleep(.5)
            curr_row.append(val)
        print_progress_bar(datetime.datetime.now(), start_time, end_time, length=50)
        rows.append(curr_row)
        if datetime.datetime.now() >= end_time:
            break
    print("Preparing file for write operation...")

    with open(data_path, 'a+', newline='') as f:
        time.sleep(5)  # This is here to be safe
        print("Waiting {} seconds for operation to complete...".format(write_time))
        writer = csv.writer(f)
        writer.writerows(rows)
        time.sleep(write_time)
    print("Data Collection Completed.")

def begin(arduino):
    """
    Begins the data collection pipeline.

    @params:
        arduino (PySerial Obj) - Required : Object that reads from serial port
    """
    while True:
        try:
            subject_num = int(input("What is the subject number?\n" ))
            assert (subject_num >= 0), "Subject number must be a nonnegative integer."
        except ValueError:
            print("Subject number is not integer. Please try again...")

        try:
            motion_num = input(
                "Which hand motion would like to collect data for?\
                \n 0: open-palm, 1: closed-fist\
                \n (Or press 'q' to exit)\n"
            )
            # Exit the function if desired
            if motion_num == 'q':
                print("Exiting trial...")
                return
            motion_num = int(motion_num)
            assert(motion_num in HAND_MOTIONS), "Invalid motion selection."
        except ValueError:
            print("Motion number is not an integer. Please try again...")

        try:
            trial_num = int(input("What trial number is this?\n"))
            assert(trial_num >= 0), "Trial number must be a nonnegative integer."
            break
        except ValueError:
            print("Trial number is not an integer. Please try again...")

    # Creates directories if they don't exist, else does nothing
    create_directory("subject", trial_num)
    create_directory("motion", HAND_MOTIONS[motion_num])
    data_path = './data/subject-{}/motion-{}/trial-{}.csv'\
        .format(subject_num, HAND_MOTIONS[motion_num], trial_num)

    input(
            "Please prepare hand for \
            data collection of {} motion.\
            \n Press any key when you're ready to begin.\n"
            .format(HAND_MOTIONS[motion_num])
    )

    collect_data(data_path, HAND_MOTIONS[motion_num], arduino)

def main():
    arduino = connect_arduino()
    while True:
        begin(arduino)
        ans = input("New trial? [y/n]\n")
        if ans == 'n':
            arduino.close()
            print("Program terminated. Good luck with the project! ")
            break

main()
