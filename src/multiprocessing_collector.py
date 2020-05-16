from queue import Queue
import os
import logging
from frozendict import frozendict
import multiprocessing as mp
from config import BAUD_RATE, PORT, WRITING_DURATION, RECORDING_DURATION
import serial
import time
from datetime import datetime, timedelta
import csv

Pool = mp.Pool
Process = mp.Process
Lock = mp.Lock
cpu_count = mp.cpu_count

connection = serial.Serial(port=PORT, baudrate=BAUD_RATE)
time.sleep(1)

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")
nthreads = cpu_count()


#
# def connect(port=PORT, baud=BAUD_RATE):
#     connection = serial.Serial(port, baud, timeout=None)
#     logging.info("Connection established: %s" % connection.is_open)
#     time.sleep(5)
#     return connection

def read(tid, end, q):
    # end, q = args[0]
    # q = qmap[tid]
    logging.info("process-%d started" % os.getpid())
    # q = qmap[tid]
    while datetime.now() < end:
        # q.put_nowait(connection.read(rate))
        read_bytes = connection.readline()
        q.put_nowait(read_bytes)
        # time.sleep(.01)
    logging.info(len(list(q.queue)))
    logging.info("thread-%d done" % tid)


def write(path, data):
    with open(path, 'a+', newline='') as f:
        logging.info("Waiting %d seconds for operation to complete..." % WRITING_DURATION)
        writer = csv.writer(f)
        writer.writerows(data)
        time.sleep(WRITING_DURATION)


def close():
    logging.info("Connection closed")
    connection.close()

# Split pins over arduinos

if __name__ == "__main__":
    cls = 'multi'
    data_path = './data/async/%s.csv' % cls
    p = '/dev/ttyACM0'
    baud = 2000000
    rate = 10000
    m = mp.Manager()
    qmap = m.dict({tid: m.Queue() for tid in range(nthreads)})


    # qmap = {tid: Queue() for tid in range(nthreads)}
    print(connection)
    # connection
    connection.flush()
    # pool = Pool(nthreads)
    start = datetime.now()
    end = start + timedelta(seconds=RECORDING_DURATION)
    # args = [(tid, connection, end, q) for tid in range(nthreads)]
    # args = [(tid, end, q) for tid in range(nthreads)]
    # p = Process()
    args = [(tid, end, qmap,) for tid in range(nthreads)]
    p = Process(target=read, args=())
    # with Pool(processes=nthreads, maxtasksperchild=1) as pool:
    #     logging.info(type(pool))
    #     pool.starmap(read, args)
    #executor.map(lambda p: read(*p), args)
    # print([list(qmap[tid].queue) for tid in range(nthreads)])
    # print([len(qmap[tid].queue) for tid in range(nthreads)])
    close()
    # print(list(q.queue), len(list(q.queue)))
