from queue import Queue
import logging
import concurrent.futures
from config import BAUD_RATE, PORT, WRITING_DURATION, RECORDING_DURATION
import serial
import time
from datetime import datetime, timedelta
import csv

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def connect(port=PORT, baud=BAUD_RATE):
    connection = serial.Serial(port, baud, timeout=None)
    logging.info("Connection established: %s" % connection.is_open)
    time.sleep(1)
    return connection

def read(tid, connection, end, q):
# def read(*args):
    # tid, connection, end, q = args
    logging.info("thread-%d started" % tid)
    while datetime.now() < end:
        # q.put_nowait(connection.read(rate))
        q.put(connection.read(15))
    logging.info("thread-%d done" % tid)


def write(path, data):
    with open(path, 'a+', newline='') as f:
        logging.info("Waiting %d seconds for operation to complete..." % WRITING_DURATION)
        writer = csv.writer(f)
        writer.writerows(data)
        time.sleep(WRITING_DURATION)


def close(connection):
    logging.info("Connection closed")
    connection.close()


if __name__ == "__main__":
    data_path = './data/async/%d.csv' % i
    p = '/dev/ttyACM0'
    baud = 2000000
    rate = 10000
    nthreads = 2
    qmap = {tid: Queue() for tid in range(nthreads)}
    # q = Queue()
    connection = connect(p, baud)
    connection.reset_input_buffer()
    connection.flush()
    start = datetime.now()
    end = start + timedelta(seconds=RECORDING_DURATION)
    # args = [(tid, connection, end, q) for tid in range(nthreads)]
    args = [(tid, connection, end, qmap[tid]) for tid in range(nthreads)]
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda p: read(*p), args)
    # print([list(qmap[tid].queue) for tid in range(nthreads)])
    # print([len(qmap[tid].queue) for tid in qmap])
    close(connection)
    # print(list(q.queue), len(list(q.queue)))
