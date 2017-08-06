import unittest
from math import isclose

from sorter.card   import Card
from sorter.reader import SubstringMatcher

class TestReader(unittest.TestCase):
    sampleCardName        = 'Terra Stomper'
    sampleInclusiveNames  = ['Terra Stomper', 'Island', 'Air Elemental'] #contains sampleCardName
    sampleOrthogonalNames = ['Lizzyquin','Vilify'] #contain no letters present in sampleCardName

    def testMaxPossibleScore1(self):
        inclusiveNamesSubstringMatcher = SubstringMatcher(self.sampleInclusiveNames)
        [matches,scores] = inclusiveNamesSubstringMatcher.matchesAndScores(self.sampleCardName)

        self.assertEqual(self.sampleCardName,matches[0])
        self.assertTrue(isclose(scores[0],1.0))

    def testMinPossibleScore0(self):
        orthogonalNamesSubstringMatcher = SubstringMatcher(self.sampleOrthogonalNames)
        [matches,scores] = orthogonalNamesSubstringMatcher.matchesAndScores(self.sampleCardName)

        self.assertTrue(isclose(scores[0],0.0))

if __name__ == '__main__':
    unittest.main()
