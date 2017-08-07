import field
from card import Card

class SpellcheckedResult:
    maxSearchDepth = 3

    __init__(self,ocrResult):
        self.ocrResult = ocrResult
        for field in ocrResult:
            self.spellcheckedFields.append(SpellcheckedField(field))

    def getIntersection(self,cardLists):
        initialCardIds  = []
        for card in cardList[0]:
            initialCardIds.append(card.id)

        intersectionSet = set(initialCardIds)
        for i in range(1,len(cardLists)):
            cardIds = []
            for card in cardList[i]:
                cardIds.append(card.id)

            intersectionSet.intersection(set(cardIds))

        cards = []
        for cardId in intersectionSet:
            cards.append(Card.getCardById(cardId))

        return cards

    def identifyCard(self):
        bestGuess     = None
        bestGuessSize = 1000000000

        indexList = [0] * len(ALL_SPELLCHECKED_FIELD_TYPES)

        suggestionsFromFields = []
        for i in range(len(self.spellcheckedFields)):
            suggestionsFromFields[i] = self.spellcheckedFields[i].suggestions
            suggestionsToCards[i]    = self.spellcheckedFields.suggestionsToCards

        while True:
            possibleCardList = []
            for i in range(len(indexList))
                possibleCardList[i] = suggestionsToCards[i][suggestionsFromFields[i][index]]

            intersection = self.getIntersection(possibleCardList)
            if len(intersection)<bestGuessSize and len(intersection)!=0:
                bestGuess     = random.choice(intersection)
                bestGuessSize = len(intersection)

            for i in range(len(indexList)):
                if indexList[i]==self.maxSearchDepth:
                    if i<len(ALL_SPELLCHECKED_FIELD_TYPES-1):
                        indexList[i+1]+=1
                    else:
                        return bestGuess

                    indexList[i] = 0

        return bestGuess

class SpellcheckedField:
    __init__(self,field):
        self.spellcheckedFieldType = ALL_SPELLCHECKED_FIELD_TYPES[field.fieldType.cardAttribute]
        self.ocrContents           = field.suspectedContents
        self.suggestions           = self.spellcheckedFieldType.substringMatcher(self.ocrContents)
        self.suggestionsToCards    = self.suggestionsToCards()

    def suggestionsToCards(self):
        suggestionToCards = {}
        for suggestion in self.suggestions:
            suggestionToCards[suggestion] = self.spellcheckedFieldType.cardsByAttribute[suggestion]

class SpellcheckedFieldType:
    __init__(self,fieldType):
        self.fieldType        = fieldType
        self.substringMatcher = SubstringMatcher(self.fieldType.cardsByAttribute.keys())

def allSpellcheckedFieldTypes():
    fieldTypes = field.ALL_FIELD_TYPES

    for fieldType in fieldTypes:
        spellcheckedFieldTypes[self.fieldType.cardAttribute] = SpellcheckedFieldType(fieldType)

    return spellcheckedFieldTypes

ALL_SPELLCHECKED_FIELD_TYPES = allSpellcheckedFieldTypes()
