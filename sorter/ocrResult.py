class OcrResult:
    __init__(self,fields):
        self.fields = fields

class Field:
    __init__(self,attribute,suspectedContents):
        self.fieldType         = ALL_FIELD_TYPES[attribute]
        self.suspectedContents = suspectedContents

class FieldType:
    __init__(self,cardAttribute,position):
        self.cardAttribute    = cardAttribute
        self.position         = position
        self.cardsByAttribute = self.cardsByAttribute()

    def cardsByAttribute(self):
        allCards = Card.getAllCards()

        cardsByAttribute = {}
        for card in allCards:
            try:
                cardsByAttribute[card.cardData[self.cardAttribute]]
            except KeyError:
                cardsByAttribute[card.cardData[self.cardAttribute]] = []

            cardsByAttribute[card.cardData[self.cardAttribute]].append(card)

        return cardsByAttribute

def allFieldTypes():
    attributesToPositions = {}
    attributesToPositions['name']            = ()
    attributesToPositions['cardType']        = ()
    attributesToPositions['rarityCharacter'] = ()
    attributesToPositions['collectorNumber'] = ()
    attributesToPositions['setAbbreviation'] = ()
    attributesToPositions['artistName']      = ()

    fieldTypes = {}
    for attribute in attributeToPositions:
        fieldTypes[attribute] = FieldType(attribute,attributeToPositions[attribute])

    return fieldTypes

ALL_FIELD_TYPES = allFieldTypes()
