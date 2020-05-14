from pywt import wavedec, threshold, downcoef, waverec
from preprocessor import s2dwt, thresh
from loader import get_data_from_csv, readFullData
import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

NUM_SENSORS = 5
WAVELET = 'db2'  # also try coiflet5
LEVEL = 4  # decimation level

def fairSubSample(rawData, gripLabels, cutOffs, percentage):
	"""

	"""
	trainingData = []
	trainingLabels = []
	testingData = []
	testingLabels = []
	start = 0
	for cutOff in cutOffs:
		trainingData.extend(rawData[start:start+math.floor(cutOff*percentage)])
		trainingLabels.extend(gripLabels[start:start+math.floor(cutOff*percentage)])
		testingData.extend(rawData[start+math.floor(cutOff*percentage):start+cutOff])
		testingLabels.extend(gripLabels[start+math.floor(cutOff*percentage):start+cutOff])
		start += cutOff
	return trainingData, testingData, trainingLabels, testingLabels

def trainClassifier(clf, data, gripLabels):
	"""
	Assumes each csv is a distinct grasp measurement
	Assumes there are at least as many trials as labels for each label for LDA
	(if using 3 graps, each grasp needs min of 3 trials)

	@params
	clf -> sklearn classifier to be trained

	train Percent -> amount of rawdata to be used for trainig 1=100% 0 = 0%

	@returns
	clf -> trained classifier using a subject's data
	"""
	clf.fit(data, gripLabels)
	return clf

if __name__ == "__main__":
	subjectNumber = 4
	clf = LinearDiscriminantAnalysis()
	# gripList = ["motion-fist", "motion-open-palm"]  # import hand motions then slice
	gripList = ["motion-fist", "motion-open-palm"]
	rawData, gripLabels, cutOffs = readFullData(gripList, subjectNumber)
	minLength =  min([len(trial) for trial in rawData])
	minPowerOf2 = 2**math.floor(math.log(minLength,2))
	rawData = [trial[:minPowerOf2] for trial in rawData]
	trainingData, testingData, trainingLabels, testingLabels = fairSubSample(rawData, gripLabels, cutOffs, .8)
	
	print(len(trainingData))
	print(len(testingData))

	trainingDWT = np.array([s2dwt(trial,LEVEL) for trial in trainingData])
	testingDWT = np.array([s2dwt(trial,LEVEL) for trial in testingData])
	clf = trainClassifier(clf, trainingDWT, trainingLabels)

	print(testingLabels)
	print(clf.predict(testingDWT))
	print(sum(clf.predict(testingDWT) == testingLabels)/len(testingLabels))

