import pprint
import json
from variables import *

prices = open("output_raw.txt")
priceDictionary = json.load(prices)

cleanPriceDictionary = {}

for cardName, setList in priceDictionary.items():
    for cardPrint in setList:
        for sku, priceInfo in cardPrint[2].items():
            # Removing price outliers (generally mispriced or not for sale)
            if priceInfo[3] is not None:
                if priceInfo[3] > 100000:
                    priceInfo.remove(priceInfo[3])
                    priceInfo.insert(3, None)

    # MongoDB cannot process key names with "."
    cleanPriceDictionary[cardName.replace(".","")] = setList

# Convert output to nested dictionary
cleanNested = {}
count = 0
for cardName, setList in cleanPriceDictionary.items():
    tempSet = {}
    for cardPrint in setList:
        tempEdition = {}
        tempConditionFirst = [Edition.First.value, {}]
        tempConditionUnlimited = [Edition.Unl.value, {}]
        tempConditionLimited = [Edition.Lim.value, {}]
        tempConditionSealed = [Edition.Sealed.value, {}]
        allConditions = [tempConditionFirst, tempConditionUnlimited, tempConditionLimited, tempConditionSealed]

        for sku, priceInfo in cardPrint[2].items():
            tempPricing = {}
            tempPricing["TCG_low"] = priceInfo[3]
            tempPricing["sold_market"] = priceInfo[5]
            tempPricing["sold_low"] = priceInfo[6]
            tempPricing["sold_high"] = priceInfo[7]
            count += 1

            for cardCondition in Condition:
                if priceInfo[0] == cardCondition.value:
                    conditionName = cardCondition.name
            for cardEdition in Edition:
                if priceInfo[1] == cardEdition.value:
                    editionName = cardEdition.name
                    for conditionList in allConditions:
                        if priceInfo[1] == conditionList[0]:
                            conditionList[1][conditionName] = tempPricing
                            tempEdition[editionName] = conditionList[1]
            tempSet[cardPrint[0]] = tempEdition

    try:
        cleanNested[cardName].append(tempSet)
    except:
        cleanNested[cardName] = tempSet

json.dump(cleanNested, open("output.txt", 'w'))