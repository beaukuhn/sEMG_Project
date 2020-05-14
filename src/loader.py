from numpy import genfromtxt
import os
import numpy as np

def get_data_from_csv(data_path='./data/subject-0/motion-fist/trial-1.csv'):
    """
    @params
    data_path(str) - Required: Where you want to store data

    @returns
    raw_emg(np.Arr[np.Arr[Int]]) - 2D Array w/ dimensions NUM_SENSORS x N
    """
    # print("Reading data from {}...".format(data_path))
    raw_emg = genfromtxt(data_path, delimiter=',')[2:, :]  # skips first 2 csv lines that are nonsense
    # print("Data read complete")
    return raw_emg

def readFullData(grips, subjectNumber):
	'''
	subjectNumber -> subject number of trials to be used

	'''
	gripLabels = []
	rawData  = []
	cutOffs = []
	dirname = os.path.dirname(__file__)
	subjectPath = os.path.join(dirname,'data/subject-' + str(subjectNumber) )
	for grip in grips:
		dataCount = 0
		folder = os.path.join(subjectPath,grip)
		for root, dirs, files in os.walk(folder):
			for file in files:
				if file.endswith(".csv"):
					path = os.path.join(root,file)
					f=open(path, 'r')
					rawData.append(get_data_from_csv(f))
					gripLabels.append(grip)
					f.close()
					dataCount +=1
		cutOffs.append(dataCount)
	return rawData, gripLabels, np.array(cutOffs)
