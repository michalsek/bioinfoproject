import numpy as np

def checkPairs(rna):
    pairs = {}

    for nuc in rna:
        if nuc in pairs:
            pairs[nuc] += 1
        else:
            pairs[nuc] = 1

    if (len(pairs.keys()) == 3) and '(' in pairs and ')' in pairs and '.' in pairs:
        if pairs['('] == pairs[')']:
            return 1
        else:
            return 0
    elif pairs['('] == pairs[')'] and pairs['['] == pairs[']']:
        return -1

    return 0

class Rna:
    def __init__(self, rnaString):
        self.rna = rnaString

    def __str__(self):
        return self.rna

    def reduceUnpaired(self):
        newRna = self.rna
        newRna = newRna.translate(None, '.')
        return Rna(newRna)

    def reducePairs(self):
        newRna = ''
        normStack = [] # stack for '(' sign indexes
        crossStack = [] # stack for '[' sign indexes
        # paired = [] # array of tuples { pairIdx: int, sign: char }
        paired = []

        for i in range(0, len(self.rna)):
            paired.append(None)
            c = self.rna[i]
            if c == '(':
                normStack.append(i)
            elif c == '[':
                crossStack.append(i)
            elif c == ')':
                pairIdx = normStack.pop()
                paired[pairIdx] = {'pairIdx': i, 'sign': '('}
                paired[i] = {'pairIdx': pairIdx, 'sign': ')'}
            elif c == ']':
                pairIdx = crossStack.pop()
                paired[pairIdx] = {'pairIdx': i, 'sign': '['}
                paired[i] = {'pairIdx': pairIdx, 'sign': ']'}

        prevPairIdx = 0
        prevPairSign = ''
        for elem in paired:
            if (prevPairSign != elem['sign'] or (prevPairIdx - elem['pairIdx']) != 1):
                newRna += elem['sign']
            prevPairIdx = elem['pairIdx']
            prevPairSign = elem['sign']

        return Rna(newRna)

def classify(rnaString):
    valid = checkPairs(rnaString)
    if valid == 1:
        print rnaString, "is stucture without pseudoknots"
        pass
    elif valid == 0:
        print rnaString, "is invalid structure"
        pass

    rna = Rna(rnaString)
    print rna
    print rna.reduceUnpaired()
    print rna.reduceUnpaired().reducePairs()
    pass
