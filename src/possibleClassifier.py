from pywt import wavedec, threshold, downcoef, waverec
import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

NUM_SENSORS = 5
wavelet = 'db2'  # also try coiflet5
level = 4  # decimation level


def get_data_from_csv(data_path):
    """
    Parses emg data from csv file

    @params
    data_path(str) - Required: Where you want to store data

    @returns
    raw_emg_data(np.Arr[np.Arr[Int]]) - 2D Array, w/ Dims NUM_SENSORS by Data
    """
    raw_emg_data = genfromtxt(data_path, delimiter=',')[1:, :]
    return raw_emg_data

def create_sensor2dwt(raw_emg_data, level):
	"""
	Creates a map `sensor2dwt` from sensors to the DWT output decimated at
	`level`

	While the decimation level map allows for analysis of the dwt at each level,
	the sensor2dwt generates the nth level output for the dwt.

	It contains less information than the decimation level map, but provides a
	realistic view of how the typical output for an nth level dwt.

	@params
	sensor2reads(Dict[Int] -> Arr[Int]) - Required

	@returns
	sensor2dwt(Dict[Int] -> Arr[Float])
	"""
	sensor2dwt = []
	for sensor_num in range(NUM_SENSORS):
		coefList = wavedec(raw_emg_data[:,sensor_num], wavelet, level=level)
		pureCoefficients = [coef for level in coefList for coef in level]
		sensor2dwt.extend(pureCoefficients)

	return sensor2dwt

def readFullData(grips, subjectNumber):
	'''
	subjectNumber -> subject number of trails to be used
	'''
	gripLabels = []
	rawData  = []
	cutOffs = []
	
	dirname = os.path.dirname(__file__)
	subjectPath = os.path.join(dirname,'data/subject-' + str(subjectNumber) )
	for grip in grips:
		dataCount = 0
		folder = os.path.join(subjectPath,grip)
		for root,dirs,files in os.walk(folder):
			for file in files:
				if file.endswith(".csv"):
					# print(os.path.join(root,file))
					path = os.path.join(root,file)
					f=open(path, 'r')
					rawData.append(get_data_from_csv(f))
					gripLabels.append(grip)
					f.close()
					dataCount +=1
		cutOffs.append(dataCount)
	# print(rawData[0].shape)
	# print(gripLabels)
	return rawData, gripLabels,np.array(cutOffs)

def fairSubSample(rawData, gripLabels, cutOffs, percentage):
	"""
	
	"""
	trainingData = []
	trainingLabels = []

	testingData = []
	testingLabels = []
	# trainingCut = math.floor(cutOffs*percentage)
	# print(cutOffs*percentage)
	start = 0
	for cutOff in cutOffs:
		# print(range(start,start+math.floor(cutOff*percentage)))
		# range1 = [start:start+math.floor(cutOff*percentage)]
		trainingData.extend(rawData[start:start+math.floor(cutOff*percentage)])
		trainingLabels.extend(gripLabels[start:start+math.floor(cutOff*percentage)])
		# print(len(rawData[start:start+math.floor(cutOff*percentage)]))

		# print(range(start+math.floor(cutOff*percentage), start+cutOff))
		testingData.extend(rawData[start+math.floor(cutOff*percentage):start+cutOff])
		testingLabels.extend(gripLabels[start+math.floor(cutOff*percentage):start+cutOff])
		# print(len(rawData[start:start+math.floor(cutOff*percentage)]))

		start += cutOff

	return trainingData, testingData, trainingLabels, testingLabels

def trainClassifier(clf, rawData, gripLabels):
	"""
	assumes each csv is a distinct grasp measurement
	assumes there are at least as many trials as labels for each label for LDA
	(if using 3 graps, each grasp needs min of 3 trials)

	@params
	clf -> sklearn classifier to be trained
	
	train Percent -> amount of rawdata to be used for trainig 1=100% 0 = 0%

	@returns
	clf -> trained classifier using a subject's data
	"""
	dwtData = np.array([create_sensor2dwt(trial,level) for trial in rawData])

	# print(dwtData.shape)
	clf.fit(dwtData, gripLabels)

	# print(clf.predict([dwtData[0,:]]))
	# print(clf.predict([dwtData[-1,:]]))
	return clf



if __name__ == "__main__":
	subjectNumber = 3
	clf = LinearDiscriminantAnalysis()
	gripList = ["motion-fist", "motion-open-palm"]

	rawData,gripLabels,cutOffs = readFullData(gripList, subjectNumber)
	# print(cutOffs)

	minLength =  min([len(trial) for trial in rawData])
	# print(minLength)
	minPowerOf2 = 2**math.floor(math.log(minLength,2))
	# print(minPowerOf2)
	rawData = [trial[:minPowerOf2] for trial in rawData]
	# print(len(rawData))
	# rawData = rawData[]
	trainingData, testingData, trainingLabels, testingLabels = fairSubSample(rawData, gripLabels, cutOffs, .8)
	print(len(trainingData))
	print(len(testingData))
	# print(np.array(testingData).shape)
	# print(trainingLabels)
	# print(testingLabels)
	testingDWT = np.array([create_sensor2dwt(trial,level) for trial in testingData])

	clf = trainClassifier(clf, trainingData, trainingLabels)
	# print(len(testingData))
	print(testingLabels)
	print(clf.predict(testingDWT))
	print(sum(clf.predict(testingDWT) == testingLabels)/len(testingLabels))

