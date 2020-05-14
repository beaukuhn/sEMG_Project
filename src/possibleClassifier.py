from pywt import wavedec, threshold, downcoef, waverec
from preprocessor import s2dwt, thresh, decimation_arrays
from loader import get_data_from_csv, readFullData
import numpy as np
from numpy import genfromtxt
import math
import matplotlib.pyplot as plt
import os
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
import sklearn.svm as svm

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

def randomSubSample(rawData, gripLabels, cutOffs, percentage):
	"""

	"""
	# trainingData = []
	# trainingLabels = []
	# testingData = []
	# testingLabels = []

	trainingCount = math.floor(len(gripLabels)*percentage)

	indexes = np.arange(len(gripLabels))
	np.random.shuffle(indexes)

	trainIndexes = indexes[0:trainingCount]
	testIndexes = indexes[trainingCount:]
	
	trainingData = [rawData[idx] for idx in trainIndexes]
	testingData = [rawData[idx] for idx in testIndexes]

	trainingLabels = [gripLabels[idx] for idx in trainIndexes]
	testingLabels = [gripLabels[idx] for idx in testIndexes]

	# print(len(testIndexes))
	# print(len(trainIndexes))
	return trainingData, testingData, trainingLabels, testingLabels

def trainClassifier(clf, data, gripLabels):
	"""
	Assumes each csv is a distinct grasp measurement
	Assumes there are at least as many trials as labels for each label in LDA
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
	# clf = LinearDiscriminantAnalysis()
	clf = QuadraticDiscriminantAnalysis()
	# clf = svm.SVC()
	# clf = svm.LinearSVC(dual = False, C = 100)

	# gripList = ["motion-fist", "motion-open-palm"]  # import hand motions then slice
	gripList = ["motion-fist", "motion-open-palm"]
	rawData, gripLabels, cutOffs = readFullData(gripList, subjectNumber)

	# butter_bandpass_filter(rawData,10,550)

	minLength =  min([len(trial) for trial in rawData])
	minPowerOf2 = 2**math.floor(math.log(minLength,2))
	# print(minLength)
	# print(minPowerOf2)

	rawData = [trial[:minPowerOf2] for trial in rawData]
	# rawData = [trial[:minLength] for trial in rawData]

	# trainingData, testingData, trainingLabels, testingLabels = randomSubSample(rawData, gripLabels, cutOffs, .8)
	trainingData, testingData, trainingLabels, testingLabels = fairSubSample(rawData, gripLabels, cutOffs, .8)
	
	print(len(trainingData))
	print(len(testingData))

	# trainingDWT = np.array([s2dwt(trial,LEVEL, mode = 'thresh') for trial in trainingData])
	# testingDWT = np.array([s2dwt(trial,LEVEL, mode = 'thresh') for trial in testingData])

	decimatedTraining = []

	for trial in trainingData:
		trialDeci = []
		for sensor in range(len(trial[0])):
			deciArray = decimation_arrays(trial[:,sensor], mode='normal')
			# print(np.shape(deciArray))
			trialDeci.extend(deciArray)

		# print(np.shape(trialDeci))
		decimatedTraining.append(trialDeci)
	# print(np.shape(decimatedTraining))

	decimatedTesting = []

	for trial in testingData:
		trialDeci = []
		for sensor in range(len(trial[0])):
			deciArray = decimation_arrays(trial[:,sensor], mode='normal')
			trialDeci.extend(deciArray)

		decimatedTesting.append(trialDeci)

	

	print("Training!")
	# for i in range()
	# clf = trainClassifier(clf, trainingDWT, trainingLabels)
	clf = trainClassifier(clf, decimatedTraining, trainingLabels)
	print("Classifying!")

	print(testingLabels)
	# print(clf.predict(testingDWT))
	# print(sum(clf.predict(testingDWT) == testingLabels)/len(testingLabels))

	print(clf.predict(decimatedTesting))
	print(sum(clf.predict(decimatedTesting) == testingLabels)/len(testingLabels))


