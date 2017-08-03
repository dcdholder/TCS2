import unittest
from sorter.card import Card

class TestCard(unittest.TestCase):
    setNameA = 'Magic 2015 Core Set'
    setNameB = 'Zendikar'
    cardName = 'Terra Stomper'

    def testCardBySetNameConsistent(self):
        sampleCardBySetAndName = Card.getCardBySetAndName(TestCard.setNameA,TestCard.cardName)

        self.assertEqual(sampleCardBySetAndName.set,TestCard.setNameA)
        self.assertEqual(sampleCardBySetAndName.name,TestCard.cardName)

    def testCardByIdConsistent(self):
        sampleCardBySetAndName = Card.getCardBySetAndName(TestCard.setNameA,TestCard.cardName)
        cardId = sampleCardBySetAndName.id

        sampleCardById = Card.getCardById(cardId)

        self.assertEqual(sampleCardById.set,TestCard.setNameA)
        self.assertEqual(sampleCardById.name,TestCard.cardName)

    def testDifferentSetDifferentId(self):
        sampleCardBySetAndNameA = Card.getCardBySetAndName(TestCard.setNameA,TestCard.cardName)
        sampleCardBySetAndNameB = Card.getCardBySetAndName(TestCard.setNameB,TestCard.cardName)

        self.assertEqual(sampleCardBySetAndNameA.name,sampleCardBySetAndNameB.name)
        self.assertNotEqual(sampleCardBySetAndNameA.set,sampleCardBySetAndNameB.set)
        self.assertNotEqual(sampleCardBySetAndNameA.id,sampleCardBySetAndNameB.id)

if __name__ == '__main__':
    unittest.main()
