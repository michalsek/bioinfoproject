import numpy as np
import re

reversePseudoKnotsMap = {
    '([)]': 'H',
    '([S)]': 'LL',
    '([)S]': 'HL_out',
    '(([)S)]': 'HL_int',
    '(S([))]': 'HH',
    '([)(])': 'HHH'
}

def checkPairs(rna):
    pairs = {}

    for nuc in rna:
        if nuc in pairs:
            pairs[nuc] += 1
        else:
            pairs[nuc] = 1
    print pairs
    if ('(' in pairs) and (')' in pairs) and (not '[' in pairs) and (not ']' in pairs):
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
        # removes dots from dot brackets string
        newRna = self.rna
        newRna = newRna.translate(None, '.')
        return Rna(newRna)

    def reducePairs(self):
        # reduces series of paired nucleotides to single pair.
        newRna = ''
        paired = self.findPairs()

        prevPairIdx = 0
        prevPairSign = ''
        for elem in paired:
            if (prevPairSign != elem['sign'] or (prevPairIdx - elem['pairIdx']) != 1):
                newRna += elem['sign']
            prevPairIdx = elem['pairIdx']
            prevPairSign = elem['sign']

        return Rna(newRna)

    def reduceSubstructures(self):
        return Rna(re.sub('SS+', 'S', self.rna))

    def findPairs(self):
        # returns array of indexed pairs
        normStack = []
        crossStack = []
        paired = []

        for i in range(0, len(self.rna)):
            paired.append(None) # make paired[i] accessible
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
            else:
                paired[i] = {'pairIdx': -1, 'sign': c}
        return paired

    def sliceStructure(self, start, end):
        # returns tuple of structure with substring replaced by 'S'
        # start and end are consitent with python ranging.
        newStructure = ""
        newSubstructure = ""

        for i in range(0, len(self.rna)):
            if i < start or i >= end:
                newStructure += self.rna[i]
            elif i == start:
                newStructure += 'S'
                newSubstructure += self.rna[i]
            elif i >= start or i < end:
                newSubstructure += self.rna[i]

        return (Rna(newStructure), Rna(newSubstructure))

    def findSubstructures(self):
        # returns list of substructures
        # top level structure is first element in list
        # each occurence of substructure is replaced by character 'S'
        # in higher level structure.
        # ahoi!
        singleStructures = []
        parseStack = []
        parseStack.append(self)

        def isClosedStruc(structure, start, end):
            for c in structure:
                if c['pairIdx'] <= start or c['pairIdx'] >= end:
                    return False

            return True

        while len(parseStack):
            structure = parseStack.pop()
            # print 'struct:', structure
            paired = structure.findPairs()
            # print 'paird:', paired
            foundSubstructs = False
            # raw_input("Press the <ENTER> key to continue...")
            for i in range(1,len(paired)-1):
                c = paired[i]
                if (c['sign'] == '('):
                    subPaired = paired[i+1:c['pairIdx']]
                    if isClosedStruc(subPaired, i, c['pairIdx']):
                        parentStruct, substruct = structure.sliceStructure(i, c['pairIdx']+1)
                        parseStack.append(substruct)
                        parseStack.append(parentStruct)
                        # print 'hehe', parentStruct, substruct
                        foundSubstructs = True
                        break
                    #fi
                #fi
            #rof
            if not foundSubstructs:
                singleStructures.append(structure)


        return singleStructures

    def classifyMinified(self):
        print self
        if self.rna in reversePseudoKnotsMap:
            print self.rna, 'is', reversePseudoKnotsMap[self.rna], 'pseudoknot'
        elif checkPairs(self.rna) == 1:
            print self.rna, 'is structure without pseudoknots'
        else:
            print self.rna, 'is not classifiable pseudoknot'

def classify(rnaString):
    valid = checkPairs(rnaString)
    if valid == 1:
        print rnaString, "is stucture without pseudoknots"
        pass
    elif valid == 0:
        print rnaString, "is invalid structure"
        pass

    rna = Rna(rnaString)

    singleStructures = rna.reduceUnpaired().reducePairs().findSubstructures()
    for structure in singleStructures:
        structure.reduceSubstructures().classifyMinified()
    pass
