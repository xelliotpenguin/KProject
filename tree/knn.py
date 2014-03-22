import sys, time
import json
import random
import numpy as np
import heapq, random
from scipy import spatial
from scipy.sparse import csr_matrix
from sklearn.svm import LinearSVC
from sklearn.datasets import load_svmlight_file
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from scipy.sparse import vstack
from sklearn import preprocessing

max_number_features = 2000000
# Knn classifier benchmark

print 'reading testing data ... '
X_test= np.loadtxt("X_test_reduced.txt")


print 'reading training data ... '
X_train = np.loadtxt("X_train_reduced.txt")
Y_train = []
train_label_file = open("train-labels.txt", "rw+")

for labels in train_label_file:
	Y_train.append(labels.split())

def calculateDistance(doc1, doc2):
	return spatial.distance.cosine(doc1, doc2)

print 'start classification ... '
outputfile = open('output','w')
outputfile.write("Id,Predicted\n")

for i in range(len(X_test)):

	print '\r>> You have finished %d iter %d%%' % (i+1, (100.0 * i/len(X_test))),
	sys.stdout.flush()

	doc_distance_pairs = []
	test_doc = X_test[0]
	
	# for each train_doc , calculate its distance to test_doc
	for j in range(len(X_train)):
		train_doc = X_train[j]
		dist = calculateDistance(train_doc, test_doc)
		doc_distance_pairs.append((j, dist))


	n_closest = heapq.nsmallest(5, doc_distance_pairs, key=lambda pair: pair[1])

	n_label_indices = [x[0] for x in n_closest]	
	results = []
	for i in range(len(n_label_indices)):
		label_index = n_label_indices[i]
		labels = [str(int(label)) for label in Y_train[label_index]]
		results.extend(labels)
		if len(results) >= 3:
			break

	outputfile.write(str(i+1) +",")
	if len(results) > 0:
		outputfile.write(' '.join(results)+"\n")
	else:
		outputfile.write("0\n")
outputfile.close()

#print 'start preprocessing tranining data ... '

# trans = TfidfTransformer()
# X_test = trans.fit_transform(X_test)

# print 'X_shape before transformation ', X_train.shape

# X_train_subset = set();
# for i in range(X_test.shape[0]):
# 	n_largest = heapq.nlargest(3, enumerate(X_test.getrow(i).data))

# 	top_indices = [x[0] for x in n_largest]

# 	# iterate all training examples, find docs that share at least one feature with the top 3 feature


# 	for j in range(X_train.shape[0]):
# 		for top_feature_indice in top_indices:
# 			if X_train[j,top_feature_indice] > 0.05: 
# 				X_train_subset.add(j)
# 				break


# matrix = None

# for doc_index in X_train_subset:
# 	if matrix == None:
# 		matrix = csr_matrix(X_train.getrow(doc_index))
# 	else:
# 		matrix = vstack([matrix, X_train.getrow(doc_index)])

# print 'X_shape after transformation ', matrix.shape



            