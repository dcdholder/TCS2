#initial implementation takes pre-numbered cards, uses the queue-based merge source technique to sort them
#output is the final ordering, and the array of instructions required to sort the cards
import collections
import random
import math

class CardSorter:
    sourceHopperSize = 1000

    @staticmethod
    def cardSortDirections(cards):
        #the physical mergesort is faster when the card/group diversity is high
        #the physical "quicksort" is much faster when you only have a few sorting groups
        if max(cards)>2**(math.ceil(math.log2(CardSorter.sourceHopperSize))-2):
            return CardSorter.cardMergeSortDirections(cards)
        else:
            #return CardSorter.cardQuickSortDirections(cards)
            return CardSorter.cardMergeSortDirections(cards)

    @staticmethod
    def cardMergeSortDirections(cards):
        sortingDecks = {};
        for sortingDeckLabel in ["source","sortA","sortB"]:
            sortingDecks[sortingDeckLabel] = collections.deque()

        #create initial subdecks of one card each
        for cardIndex in range(len(cards)):
            sortingDecks["source"].appendleft(SubDeck([cards[cardIndex]]))

        #essentially a queue-based merge sort
        directions = []
        while len(sortingDecks["source"])!=1:
            #evenly divide up subDecks between sortA and sortB
            for subDeckIndex in range(len(sortingDecks["source"])):
                subDeck = sortingDecks["source"].pop()

                direction = ""
                if subDeckIndex%2==0:
                    sortingDecks["sortA"].appendleft(subDeck)
                    direction = "To A"
                else:
                    sortingDecks["sortB"].appendleft(subDeck)
                    direction = "To B"

                for cardIndex in range(len(subDeck)):
                    directions.append(direction)

            #combine sorted subDeck pairs, one pair at a time
            while len(sortingDecks["sortB"])!=0: #sortB will always have the same amount of subdecks or less than sortA
                subDeckA = sortingDecks["sortA"].pop()
                subDeckB = sortingDecks["sortB"].pop()
                [combinedSubDeck,combiningDirections] = subDeckA.combine(subDeckB)
                directions += combiningDirections
                sortingDecks["source"].appendleft(combinedSubDeck)

            #handle unpaired subDeck, if one exists
            if len(sortingDecks["sortA"])!=0:
                subDeckA = sortingDecks["sortA"].pop()
                sortingDecks["source"].appendleft(subDeckA)
                for i in range(len(subDeckA)):
                    directions.append("From A")

        finalSubDeck = sortingDecks["source"].pop()
        outputCards = list(finalSubDeck)

        return [outputCards,directions]

    @staticmethod
    def cardQuickSortDirections(cards): #TODO: implement this
        pass

    #exists mainly for testing purposes
    @staticmethod
    def cardSortFromDirections(cards,directions):
        sortHopperSize = 2**(math.ceil(math.log2(CardSorter.sourceHopperSize))-1) #e.g. 512 for source hopper size of 1000

        sortingDecks = {};
        sortingDecks["source"] = collections.deque([],CardSorter.sourceHopperSize)
        sortingDecks["sortA"]  = collections.deque([],sortHopperSize)
        sortingDecks["sortB"]  = collections.deque([],sortHopperSize)

        for cardIndex in range(len(cards)):
            sortingDecks["source"].appendleft(cards[cardIndex])

        for i in range(len(directions)):
            (sortingDecks["source"])
            if directions[i]=="To A":
                sortingDecks["sortA"].appendleft(sortingDecks["source"].pop())
            elif directions[i]=="To B":
                sortingDecks["sortB"].appendleft(sortingDecks["source"].pop())
            elif directions[i]=="From A":
                sortingDecks["source"].appendleft(sortingDecks["sortA"].pop())
            elif directions[i]=="From B":
                sortingDecks["source"].appendleft(sortingDecks["sortB"].pop())

        return list(sortingDecks["source"])

class SubDeck(collections.deque):
    def combine(self,subDeckB):
        combinedSubDeck = SubDeck()
        directions = []
        while len(self)>0 or len(subDeckB)>0:
            if len(self)>0 and len(subDeckB)>0:
                if self[len(self)-1]>=subDeckB[len(subDeckB)-1]:
                    combinedSubDeck.appendleft(self.pop())
                    directions.append("From A")
                else:
                    combinedSubDeck.appendleft(subDeckB.pop())
                    directions.append("From B")
            elif len(self)>0:
                combinedSubDeck.appendleft(self.pop())
                directions.append("From A")
            elif len(subDeckB)>0:
                combinedSubDeck.appendleft(subDeckB.pop())
                directions.append("From B")

        return [combinedSubDeck,directions]

#both tests have complexity n^2logn where n=numCardsMax
class TestCardSorter:
    @staticmethod
    def arrayOfDecksWithSizeFrom1ToMax():
        numCardsMax  = 1000
        cardValueMax = 10000

        decks = []
        for numCards in range(1,numCardsMax+1):
            inputCards = []
            for i in range(numCards):
                inputCards.append(random.randint(1,cardValueMax))

            decks.append(inputCards)

        return decks

    #verify the ordering generated by CardSorter.cardSortDirections
    @staticmethod
    def testRangeOfDeckSizesTheoreticalOrdering():
        decks = TestCardSorter.arrayOfDecksWithSizeFrom1ToMax()

        for i in range(len(decks)):
            [outputCards,directions] = CardSorter.cardSortDirections(decks[i])

            #confirm that the output ordering is the same as that generated by a built-in sorting method
            if outputCards!=sorted(decks[i]):
                raise ValueError("Output did not match input sorted with \'sorted()\'")

    #verify the ordering generated by CardSorter.cardSortFromDirections
    @staticmethod
    def testRangeOfDeckSizesActualOrdering():
        decks = TestCardSorter.arrayOfDecksWithSizeFrom1ToMax()

        for i in range(len(decks)):
            [predictedOutputCards,directions] = CardSorter.cardSortDirections(decks[i])
            actualOutputCards                 = CardSorter.cardSortFromDirections(decks[i],directions)

            #confirm that the output ordering is the same as predicted by CardSortDirections
            if actualOutputCards!=predictedOutputCards:
                raise ValueError("Predicted output did not match actual sorter output.")
