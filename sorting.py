#initial implementation takes pre-numbered cards, uses the queue-based merge main technique to sort them
#output is the final ordering, and the array of instructions required to sort the cards
import collections
import random
import math

#acts as a stack
class CardTray:
    capacity = 1024

    def __init__(self):
        self.cardList = []

    def size(self):
        return len(self.cardList)

    def push(self,card):
        if len(self.cardList)!=CardTray.capacity:
            self.cardList.append(card)
        else:
            raise ValueError("Cannot add card to full card tray")

    def pop(self):
        return self.cardList.pop()

    def peekAll(self):
        return list(self.cardList)

    def withdrawAll(self):
        returnList = list(self.cardList)
        self.cardList = []

        return returnList

    def replaceAll(self,cards):
        self.cardList = list(cards)

class CardSorter:
    def __init__(self):
        self.trays = CardSorter.genTrays()

    @staticmethod
    def genTrays():
        return {"main": CardTray(), "A": CardTray(), "B": CardTray()}

    @staticmethod
    def cardSortDirections(sortScores):
        virtualTrays = CardSorter.genTrays()

        directions = []

        virtualTrays["main"].push(SubDeck(sortScores))
        while True: #sort is done when SubDecks are one card each
            subDeckExistsWithCardinalityGreaterThan1 = False
            for subDeck in virtualTrays["main"].peekAll():
                if subDeck.cardinalityGreaterThan1():
                    subDeckExistsWithCardinalityGreaterThan1 = True

            if not subDeckExistsWithCardinalityGreaterThan1:
                break

            parity = 0
            for subDeckIndex in range(virtualTrays["main"].size()):
                subDeck = virtualTrays["main"].pop()

                if subDeck.cardinalityGreaterThan1():
                    [subDeckA, subDeckB, splitDirections] = subDeck.split(parity)

                    directions.extend(splitDirections)

                    if parity%2==0: #no need to change parity when the number of operations is even
                        virtualTrays["A"].push(subDeckA)
                        virtualTrays["B"].push(subDeckB)
                    else:
                        virtualTrays["B"].push(subDeckA)
                        virtualTrays["A"].push(subDeckB)
                else:
                    if parity%2==0:
                        virtualTrays["A"].push(subDeck)
                        for i in range(subDeck.size()):
                            directions.append("To A")
                    else:
                        virtualTrays["B"].push(subDeck)
                        for i in range(subDeck.size()):
                            directions.append("To B")

                    parity+=1

            #withdraw subdecks from A and B in the reverse order that they were placed in
            while virtualTrays["A"].size()>0:
                if virtualTrays["A"].size()==virtualTrays["B"].size():
                    subDeck = virtualTrays["B"].pop()
                    subDeck.reverse() #cards pulled from subdeck form a reversed version of the subdeck when moved to a new stack
                    virtualTrays["main"].push(subDeck)

                    for i in range(subDeck.size()):
                        directions.append("From B")
                else:
                    subDeck = virtualTrays["A"].pop()
                    subDeck.reverse()
                    virtualTrays["main"].push(subDeck)

                    for i in range(subDeck.size()):
                        directions.append("From A")

        return directions

    #exists mainly for testing purposes
    def cardSortFromDirections(self,cards,directions):
        self.trays["main"].replaceAll(cards)

        for i in range(len(directions)):
            if directions[i]=="To A":
                self.trays["A"].push(self.trays["main"].pop())
            elif directions[i]=="To B":
                self.trays["B"].push(self.trays["main"].pop())
            elif directions[i]=="From A":
                self.trays["main"].push(self.trays["A"].pop())
            elif directions[i]=="From B":
                self.trays["main"].push(self.trays["B"].pop())

        return self.trays["main"].peekAll()

    def cardSort(self,cards,sortScores):
        directions = CardSorter.cardSortDirections(sortScores)
        return self.cardSortFromDirections(cards,directions)

class SubDeck():
    def __init__(self,cardList):
        if len(cardList)>0:
            self.cardList = list(cardList)
        else:
            raise ValueError("SubDeck must contain at least one card")

    def size(self):
        return len(self.cardList)

    def cardinalityGreaterThan1(self):
        sampleCard = self.cardList[0]

        for card in self.cardList:
            if card!=sampleCard:
                return True

        return False

    def reverse(self):
        newCards = []

        for i in range(len(self.cardList)):
            newCards.append(self.cardList[len(self.cardList)-i-1])

        self.cardList = newCards

    def split(self,parity):
        if self.size()>1:
            pivot = min(self.cardList)+(max(self.cardList)-min(self.cardList))/2

            directions = []

            cardListA = []
            cardListB = []
            for i in range(len(self.cardList)): #reverse order since push/pop are done from the highest index
                card = self.cardList[len(self.cardList)-i-1]
                if card<pivot:
                    cardListA.append(card)
                    if parity%2==0:
                        directions.append("To A")
                    else:
                        directions.append("To B")
                else:
                    cardListB.append(card)
                    if parity%2==0:
                        directions.append("To B")
                    else:
                        directions.append("To A")

            subDeckA = SubDeck(cardListA)
            subDeckB = SubDeck(cardListB)

            return [subDeckA,subDeckB,directions]
        else:
            raise ValueError("Cannot split SubDeck of cardinality 1")

#both tests have complexity n^2logn where n=numCardsMax
class TestCardSorter:
    @staticmethod
    def arrayOfDecksWithUniqueElementsAndSizeFrom1ToMax(numCardsMax):
        decks = []
        for numCards in range(1,numCardsMax+1):
            inputCards = list(range(1,numCards+1))
            random.shuffle(inputCards)

            decks.append(inputCards)

        return decks

    @staticmethod
    def arrayOfDecksWithDuplicatedElementsAndSizeFrom1ToMax(numCardsMax):
        duplicatedDecks = []

        uniqueDecks = TestCardSorter.arrayOfDecksWithUniqueElementsAndSizeFrom1ToMax(numCardsMax//2)
        for uniqueDeck in uniqueDecks:
            duplicatedDecks.append(uniqueDeck + uniqueDeck) #add two copies together
            random.shuffle(duplicatedDecks[len(duplicatedDecks)-1])

        return duplicatedDecks

    #verify the ordering generated by CardSorter.cardSortFromDirections
    @staticmethod
    def testSortSpeedAndAccuracyUnique():
        decks = TestCardSorter.arrayOfDecksWithUniqueElementsAndSizeFrom1ToMax(1024)

        for i in range(len(decks)):
            cardSorter  = CardSorter()
            outputCards = cardSorter.cardSort(decks[i],decks[i])

            reverseSortedDeck = sorted(decks[i])
            reverseSortedDeck.reverse()

            #confirm that the output ordering is the same as that generated by a built-in sorting method
            if outputCards!=reverseSortedDeck:
                raise ValueError("Output did not match input sorted with \'sorted()\'")

    def testSortSpeedAndAccuracyDuplicated():
        decks = TestCardSorter.arrayOfDecksWithDuplicatedElementsAndSizeFrom1ToMax(1024)

        for i in range(len(decks)):
            cardSorter  = CardSorter()
            outputCards = cardSorter.cardSort(decks[i],decks[i])

            reverseSortedDeck = sorted(decks[i])
            reverseSortedDeck.reverse()

            #confirm that the output ordering is the same as that generated by a built-in sorting method
            if outputCards!=reverseSortedDeck:
                raise ValueError("Output did not match input sorted with \'sorted()\'")
