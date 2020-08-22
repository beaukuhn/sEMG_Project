from threading import Thread
from queue import Queue
import logging
import concurrent.futures
from config import BAUD_RATE, PORT, WRITING_DURATION, RECORDING_DURATION
import serial
import time
from datetime import datetime, timedelta
import csv
from utils import create_dirs, path_exists
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def connect(port=PORT, baud=BAUD_RATE):
    connection = serial.Serial(port, baud, timeout=None)
    logging.info("Connection established: %s" % connection.is_open)
    time.sleep(1)
    return connection


def read(connection, tid, start, end, q):
    logging.info("thread-%d started" % tid)
    while datetime.now() < end:
        # q.put_nowait(connection.read(rate))
        q.put_nowait(connection.readline())
    logging.info("thread-%d done" % tid)


def write(path, data):
    with open(path, 'a+', newline='') as f:
        logging.info("Waiting %d seconds for operation to complete..." % WRITING_DURATION)
        writer = csv.writer(f)
        writer.writerows(data)
        time.sleep(WRITING_DURATION)


def close(connection):
    connection.close()


if __name__ == "__main__":
    i = 0
    data_path = './data/async/%d.csv' % i
    p = '/dev/ttyACM0'
    baud = 2000000
    rate = 10000
    nthreads = 8
    # qmap = {tid : Queue() for tid in range(nthreads)}
    q = Queue()
    connection = connect(p, baud)
    start = datetime.now()
    end = start + timedelta(seconds=RECORDING_DURATION)
    with concurrent.futures.ThreadPoolExecutor(max_workers=nthreads) as executor:
        executor.map(read, [connection, range(8), start, end, q])
    list(q)
