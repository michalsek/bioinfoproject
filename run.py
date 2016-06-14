import sys
import string
import pseudoClassifier

filePath = ""
if len(sys.argv) != 2:
    print "No arguments. Using test.in as input"
    filePath = "./test.in"
else:
    filePath = sys.argv[1]

with open(filePath, 'r') as fh:
    for line in fh:
        pseudoClassifier.classify(line.translate(None, string.whitespace))
