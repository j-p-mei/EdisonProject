import pprint
import json

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

json.dump(cleanPriceDictionary, open("output.txt", 'w'))