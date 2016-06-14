import sys
import string
import pseudoClassifier
import pickle

with open('test.pickle', 'r') as fh:
    X, y1, y2 = pickle.load(fh)

errors = 0

for i in range(0,len(X)):
    [output, st] = pseudoClassifier.testClassify(X[i])
    if output != y1[i]:
        errors = errors + 1
        print output, y1[i], y2[i], i, st


print 'accuracy ', 100 - (errors / float(len(X))) * 100, '%'
