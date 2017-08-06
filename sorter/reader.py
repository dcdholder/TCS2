class SubstringMatcher:
    def __init__(self,containingStrings):
        self.containingStrings = containingStrings
        self.substringToContainingStrings = SubstringMatcher.substringToContainingStrings(containingStrings)

    @staticmethod
    def substringToContainingStrings(containingStrings):
        substringToContainingStrings = {}

        for containingString in containingStrings:
            substringWheel = SubstringWheel(containingString)
            allSubstrings  = substringWheel.allCircularSubstrings()

            for substring in allSubstrings:
                try:
                    substringToContainingStrings[substring]
                except KeyError:
                    substringToContainingStrings[substring] = {}

                try:
                    substringToContainingStrings[substring][containingString]
                except KeyError:
                    substringToContainingStrings[substring][containingString] = 0

                substringToContainingStrings[substring][containingString]+=1

        return substringToContainingStrings

    def dictionaryStringToMatchingScore(self,stringToSpellcheck):
        wheel                = SubstringWheel(stringToSpellcheck)
        spellcheckSubstrings = wheel.allCircularSubstrings()

        stringToMatchingScore       = {}
        stringToMatchingNumerator   = {}
        stringToMatchingDenominator = {}

        for dictionaryString in self.containingStrings:
            stringToMatchingNumerator[dictionaryString] = 0

        for spellcheckSubstring in spellcheckSubstrings:
            if spellcheckSubstring!=SubstringWheel.newlineChar:
                try:
                    for matchingString in self.substringToContainingStrings[spellcheckSubstring].keys():
                        stringToMatchingNumerator[matchingString]+=len(spellcheckSubstring)*self.substringToContainingStrings[spellcheckSubstring][matchingString]
                except KeyError:
                    pass

        for dictionaryString in self.containingStrings:
            if len(dictionaryString)>len(stringToSpellcheck):
                n = len(dictionaryString)
            else:
                n = len(stringToSpellcheck)

            n+=1 #to account for the line terminator

            stringToMatchingDenominator[dictionaryString] = n*n*(n+1)/2-1 #-1 to account for solo line terminator

        for dictionaryString in self.containingStrings:
            stringToMatchingScore[dictionaryString] = stringToMatchingNumerator[dictionaryString]/float(stringToMatchingDenominator[dictionaryString])


        #TODO: figure out why the perfect matching score is not exactly 1.0 yet
        return stringToMatchingScore

    def matchesAndScores(self,stringToSpellcheck):
        matchingScoreDict = self.dictionaryStringToMatchingScore(stringToSpellcheck)

        strings = []
        scores  = []
        for string in matchingScoreDict.keys():
            strings.append(string)
            scores.append(matchingScoreDict[string])

        sortedStrings = list(reversed([string for (score,string) in sorted(zip(scores,strings), key=lambda pair: pair[0])]))
        sortedScores  = list(reversed(sorted(scores)))

        return [sortedStrings,sortedScores]

#create a circular, singly-linked list
class SubstringWheel:
    newlineChar = '$'

    def __init__(self,inputString):
        self.contents = inputString + self.newlineChar

        self.firstNode = SubstringWheelNode(self.contents[0])
        currentNode = self.firstNode
        for i in range(len(self.contents)-1):
            nextNode = SubstringWheelNode(self.contents[i+1])
            currentNode.nextNode = nextNode
            currentNode = nextNode

        currentNode.nextNode = self.firstNode

    def allCircularSubstrings(self):
        circularSubstrings  = []

        for i in range(1,len(self.contents)+1):
            circularSubstrings += self.allCircularSubstringsOfLength(i)

        return circularSubstrings

    def allCircularSubstringsOfLength(self,length):
        substrings  = []
        currentNode = self.firstNode

        #one iteration for each of len(self.contents) substrings
        for j in range(len(self.contents)):
            substring = []

            #collect substring characters by advancing through nodes
            for i in range(length):
                substring.append(currentNode.contents)
                currentNode = currentNode.nextNode

            substrings.append(''.join(substring))

            #fast forward through nodes to the start of the next substring
            for i in range(len(self.contents)-length+1):
                currentNode = currentNode.nextNode

        return substrings

class SubstringWheelNode:
    def __init__(self,contents):
        self.contents = contents
        self.nextNode = None
