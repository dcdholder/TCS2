import os
import json

SET_DATA_FILENAME_RELATIVE = '../data/AllSets.json'
SET_DATA_FILENAME          = os.path.join(os.path.dirname(__file__), SET_DATA_FILENAME_RELATIVE)

class Card:
    def __init__(self,cardData):
        self.cardData = cardData

        self.id   = self.cardData['id']
        self.set  = self.cardData['setName']
        self.name = self.cardData['name']

    @staticmethod
    def getAllCards():
        return ALL_CARDS_BY_ID.values()

    @staticmethod
    def getCardById(cardId):
        try:
            return ALL_CARDS_BY_ID[cardId]
        except Exception as e:
            raise ValueError('No card found with ID ' + cardId + '.')

    @staticmethod
    def getCardBySetAndName(setName,cardName):
        try:
            return ALL_CARDS_BY_SET_AND_NAME[setName][cardName]
        except Exception as e:
            raise ValueError('No card found from set ' + setName + ' with name ' + cardName + '.')

#TODO: try to find some other way of doing static initializers inside the class proper - Python being a PITA for no reason
def allCardsByIdFromSetJson():
    allSets = None
    with open(SET_DATA_FILENAME) as allCardsJson:
        allSetsData = json.load(allCardsJson)

    cards = []
    for setAbbreviation,setData in allSetsData.items():
        cards += cardsFromSet(setData)

    cardsById = {}
    for card in cards:
        cardsById[card.id] = card

    return cardsById


def allCardsBySetAndName():
    cardSets = {}
    for card in ALL_CARDS_BY_ID.values():
        if not card.set in cardSets.keys():
            cardSets[card.set] = {}

        cardSets[card.set][card.name] = card

    return cardSets

def cardsFromSet(cardSetData):
    setName         = cardSetData['name']
    setAbbreviation = cardSetData['code']
    releaseDate     = cardSetData['releaseDate']

    setCards = []
    for cardData in cardSetData['cards']:
        finalCardData = dict(cardData)
        finalCardData['setName']         = setName
        finalCardData['setAbbreviation'] = setAbbreviation
        finalCardData['releaseDate']     = releaseDate

        setCards.append(Card(finalCardData))

    return setCards

ALL_CARDS_BY_ID            = allCardsByIdFromSetJson()
ALL_CARDS_BY_SET_AND_NAME  = allCardsBySetAndName()
