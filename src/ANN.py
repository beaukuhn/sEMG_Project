#Artificial Neural Network implementation


from sklearn.neural_network import MLPClassifier
import numpy as np


classify = MLPClassifier(hidden_layer_sizes=(100, ), activation='relu', solver='adam', alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001)
semg = scipy.io.loadmat('./data/subject-0/motion-fist/trial-0.csv')
classify.fit(training_data,training_labels)
prediction_ann = classify.predict(training_data)
print("accuracy:", 1 - (np.sum(training_labels != prediction_ann)/len(training_labels)))
