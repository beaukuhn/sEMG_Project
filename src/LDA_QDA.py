"""
LDA_QDA.py

This file contains logic for implementing both LDA & QDA.
"""
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.stats import multivariate_normal
from sklearn.lda import LDA

def split_set(data_in, validation_size, labels):
    if validation_size < 1.0: # if it is a ratio
        validation_size = int(validation_size * len(labels))
    training_size = len(data_in) - validation_size
    random_index = np.random.permutation(len(labels))
    training_data = data_in[random_index][:training_size]
    training_labels = labels[random_index][:training_size]
    validation_data = data_in[random_index][training_size:]
    valid_labels = labels[random_index][training_size:]
    return validation_data, training_data, valid_labels, training_labels

def LDA_fit(inputs, Labels):
    Covar=0
    labels = np.unique(Labels)
    Prob = np.zeros([len(labels)])
    Mean = np.zeros([len(labels), inputs.shape[1]])
    for b,label in enumerate(labels):
        new = inputs[Labels==label, :]
        Covar += np.cov(np.transpose(new))*new.shape[0]
        Prob[b] = inputs.shape[0]/len(Labels)
        Mean[b, :] = np.mean(new, axis=0)
    Covar = Covar / len(Labels)
    return Mean, Covar, Prob

def LDA_predict(inputs, covariance, mean, Prob):
    Mat = np.linalg.pinv(covariance)
    A = np.transpose(np.dot(np.dot(mean,Mat), inputs.T)) - 1/2*np.diag(np.dot(np.dot(mean,Mat),np.transpose(mean))) - np.log(Prob)
    return np.argmax(np.transpose(A), axis = 0)

def QDA_fit(inputs, Labels):
    labels = np.unique(Labels)
    Prob = np.zeros([len(labels)])
    Mean = np.zeros([len(labels), inputs.shape[1]])
    Covar=np.zeros([inputs.shape[1],inputs.shape[1], len(labels)])
    for b,label in enumerate(labels):
        new = inputs[Labels==label, :]
        Prob[b] = new.shape[0]/len(Labels)
        Mean[b, :] = np.mean(new, axis=0)
        Cov[:,:,b] += np.cov(np.transpose(new)) + np.eye(inputs.shape[1])*1e-9
    return Mean, Covar, Prob

def QDA_predict(inputs, Prob, covariance, mean):
    B = np.zeros([len(Prob),len(inputs)])
    for b in range(len(Prob)):
        Mat = np.linalg.inv(covariance[:,:,b])
        A = -1/2*np.log(np.linalg.det(covariance[:,:,b])+ 1e-10) + np.log(Prob[b])
        B[b,:] = np.array([A - (1/2*np.dot(np.dot(a-mean[b], Mat), a-mean[b])) for a in inputs])
    return np.argmax(B, axis = 0)

semg = scipy.io.loadmat('./data/subject-0/motion-fist/trial-0.csv')

a, b, c, d = split_set(training_data, 10000, training_label)
Mean, Covar, P = LDA_fit(a, c)
prediction = LDA_predict(a, Covar, Mean, P)
print("accuracy:", 1 - (np.sum(c != prediction)/len(c)))

#sklearn implementation
classify = LDA()
classify.fit(a,c)
classify.predict(a)
print("accuracy:", 1 - (np.sum(c != prediction)/len(c)))
