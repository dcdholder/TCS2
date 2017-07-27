class SortingGroupChain:
    cardSetJsonFilename = 'AllSets.json'

    def __init__():
        self.cardsDict     = SortingGroupChain.convertAllSetsJsonToCardsDict()
        self.sortingGroups = {"color": ColorGroup(cardsDict), "rarity": RarityGroup(cardsDict), "set": SetGroup(cardsDict), "alphabetical": SetGroup(cardsDict)}

    @staticmethod
    def convertAllSetsJsonToCardsDict():


    def sortScoresFromJobAndCards(sortJob,cards):
        groups = []
        for sortGroup in sortJob:
            if sortGroup.keys()[0] in self.sortingGroups:
                sortGroupObject = self.sortingGroups[sortGroup.keys()[0]]
                sortGroupObject.setSubgroupOrdering(sortGroup[sortGroup.keys()[0]])
            else:
                raise ValueError("No such sorting group \'" + sortGroup + "\'")

            groups.append(sortGroupObject)

        #the idea here is to generate a list of partial sort orderings for every card, then reduce each list into a single sort score
        sortOrderingListOfLists = []
        maxPartialScores        = []

        for i in range(len(cards)):
            sortOrderingListOfLists[i] = []

        for group in groups:
            [partialSortOrdering,maxPartialScore] = group.getPartialSortOrdering()
            for i in range(len(partialSortOrdering)):
                sortOrderingListOfLists[i].append(partialSortOrdering[i])

        #here we reduce the lists into single-element sort scores
        finalScores = []
        for j in range(len(cards)):
            digitSum    = 0
            currentBase = 1
            for i in reversed(range(len(sortOrderingListOfLists[j]))):
                digitSum   += sortOrderingListOfLists[j][i]*currentBase
                currentBase = maxPartialScores[i]+1

            finalScores[j] = digitSum

        return finalScores

#abstract class
class SortingGroup:
    def __init__(cardsDict):
        getNamedSubgroupSortOrders(cardsDict)
        self.idSubgroupMap        = genIdSubgroupMap(cardsDict)
        self.subgroupSortOrderMap = genSubgroupSortOrderMap()

    def getPartialSortOrdering():
        pass

    @staticmethod
    def reduceSortScores(sortScores):
        reducedScoreMap = {}
        reducedScores   = []

        #create a mapping of scores in the original scores list to the reduced scores
        sortedSortScores = sorted(sortScores)

        currentMapping = 0
        for i in range(len(sortedSortScores)):
            if sortedSortScores[i]!=previousMapping: #multiples should have the same mapping
                currentMapping++

            reducedScoreMap[sortedSortScores[i]] = currentMapping

        #form a reduced-score copy of the input score list
        for i in range(len(sortScores)):
            reducedScores[i] = reducedScoreMap[sortScore[i]]

        return reducedScores

    def changeSubgroupSortOrder(desiredSubgroupSortOrder): #check whether the new ordering contains the same elements/is valid, before replacing
        currentSubgroupSortOrderSorted = sorted(self.subgroupSortOrder)
        desiredSubgroupSortOrderSorted = sorted(desiredSubgroupSortOrder)

        if currentSubgroupSortOrder==desiredSubgroupSortOrder:
            self.subgroupSortOrder = desiredSubgroupSortOrder
        else:
            raise ValueError("New subgroup sort ordering does not contain the same elements as the old one")

    def genSubgroupSortOrderMap():
        for i in range(len(self.subgroupSortOrder)):
            subgroupSortOrderMap[subgroups[i]] = i

    def genIdSubgroupMap(cardsDict):
        for cardDict in cardsDict:
            [id,subgroup] = getSubgroupFromCardDict[cardDict]

            if subgroup!=None:
                idSubgroupMap[id] = subgroup
            else:
                raise ValueError("No subgroup has been assigned to card with ID" + id)

    def sortOrder(cards):
        sortOrder = []
        for i in range(len(cards):
            sortOrder[i] = subgroupSortOrderMap[idSubgroupMap[cards[i].id]]

        return sortOrder

    def getInitialSubgroups(cardsDict):
        raise RuntimeError("Method should never be called from abstract parent")

    def getSubgroupFromCardDict(cardDict):
        raise RuntimeError("Method should never be called from abstract parent")

#color
class ColorGroup(SortingGroup):
    def getNamedSubgroupSortOrders(cardsDict):
        self.namedSubgroupSortOrders = {}
        self.namedSubgroupSortOrders["default"] = ["White","Black","Red","Blue","Green","Multicolor","Zero","Generic"]

    def getSubgroupFromCardDict(cardDict):
        subgroup = None

        if "colors" in cardDict:
            if len(cardDict["colors"])==1:
                subgroup=cardDict[colors][1]
            else:
                subgroup="multicolor"
        else:
            if "manaCost" in cardDict:
                reg = re.search("\{[0-9]+\}","cardDict["manaCost"]")
                if reg.group(0)=="0":
                    subgroup="zero"
                else:
                    subgroup="generic"

        return [cardDict["multiverseId"],subgroup]

#rarity
class RarityGroup(SortingGroup):
    def getNamedSubgroupSortOrders(cardsDict):
        self.namedSubgroupSortOrders = {}
        self.namedSubgroupSortOrders["default"] = ["Basic Land","Common","Uncommon","Rare","Mythic Rare"]

    @staticmethod
    def getSubgroupFromCardDict(cardDict):
        subgroup = None

        if "rarity" in cardDict:
            subgroup = cardDict["rarity"]

        return [cardDict["multiverseId"],subgroup]

#set
class SetGroup(SortingGroup):
    def getNamedSubgroupSortOrders(cardsDict):
        self.namedSubgroupSortOrders = {}
        self.namedSubgroupSortOrders["chronological"] = SetGroup.chronologicalOrder(cardsDict)
        self.namedSubgroupSortOrders["alphabetical"]  = SetGroup.alphabeticalOrder(cardsDict)
        self.namedSubgroupSortOrders["default"]       = self.namedSubgroupSortOrders["chronological"]

    @staticmethod
    def chronologicalOrder(cardsDict):
        #map set names to time stamps
        setToReleaseDate = {}
        for cardDict in cardsDict:
            #ensures that sets released on the same date are sorted separately, assuming YYYY-MM-DD date format
            setToReleaseDate[cardDict["setName"]] = cardDict["releaseDate"] + cardDict["setName"]

        #alphabetical ordering is the same as chronological for YYYY-MM-DD strings
        releaseDates = []
        for setName,releaseDate in setToReleaseDate:
            releaseDates.append(releaseDate)

        sortedReleaseDates = sorted(releaseDates)

        releaseDateToSortScore = {}
        for i in range(len(sortedReleaseDates):
            releaseDateToSortScore[sortedReleaseDates[i]] = sortScore

        #if two sets happen to have the same release date, sort alphabetically
        setToSortScore = {}
        for setName,releaseDate in setToReleaseDate:
            setToSortScore[setName] = releaseDateToSortScore[setToReleaseDate[setName]]

        #now use the set-to-score mapping to generate an ordered list
        setNamesChronologicalOrder = [None] * len(setToSortScore)
        for setName,sortScore in setToSortScore:
            setNamesChronologicalOrder[sortScore] = setName

        return setNamesChronologicalOrder

    @staticmethod
    def alphabeticalOrder(cardsDict):
        sets = Set([])
        for cardDict in cardsDict:
            cardDict["setName"].add()

        return sorted(list(sets))

    @staticmethod
    def getSubgroupFromCardDict(cardDict):
        subgroup = None

        if "setName" in cardDict:
            subgroup = cardDict["setName"]

        return [cardDict["multiverseId"],subgroup]

#alphabetical
class AlphabeticalGroup(SortingGroup):
    def getNamedSubgroupSortOrders(cardsDict):
        self.namedSubgroupSortOrders = {}
        self.namedSubgroupSortOrders["forward"] = sorted(AlphabeticalGroup.cardNames(cardsDict))
        self.namedSubgroupSortOrders["reverse"] = list(reversed(AlphabeticalGroup.cardNames(cardsDict)))
        self.namedSubgroupSortOrders["default"] = self.namedSubgroupSortOrders["forward"]

    @staticmethod
    def cardNames(cardsDict):
        cardNames = []
        for cardDict in cardsDict:
            cardNames.append(cardDict["name"])

        return cardNames

    @staticmethod
    def getSubgroupFromCardDict(cardDict):
        subgroup = None

        if "name" in cardDict:
            subgroup = cardDict["name"]

        return [cardDict["multiverseId"],subgroup]
