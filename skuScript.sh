#!/bin/bash

# This script runs every night and pulls pricing data by calling the TCGPlayer API

echo "Running getSetNames"

touch setDictionaryNew.csv

python getSetNames.py setDictionaryNew.csv

DIFF=$(diff setDictionaryNew.csv setDictionary.csv) 

if [ "$DIFF" != "" ] 
then
    # This should run when a new set is released
    echo "Difference detected, loading new setDictionary"
    mv setDictionaryNew.csv setDictionary.csv
    echo "Running getCardsBySet"
    # Set update requires update the dictionary of cards and corresponding product ID and set
    python getCardsBySet.py
    echo "Running createSKUDictionary"
    # This generates a file whose entries contain 
    # Note that SKUs are representations of condition, edition, and language combinations
    # {Card Name: [[Set Name, PID, {SKU: [Condition, Edition, Language]}]]
    python createSKUDictionary.py
else
    echo "No difference detected, SKU update not required"
    rm setDictionaryNew.csv
fi

if [ -f "skuMarketPricing.txt" ]
then
    echo "Removing skuMarketPricing.txt"
    rm "skuMarketPricing.txt"
fi

if [ -f "skuSoldPricing.txt" ]
then
    echo "Removing skuSoldPricing.txt"
    rm "skuSoldPricing.txt"
fi

if [ -f "skuSoldPricingIncomplete.txt" ]
then
    echo "Removing skuSoldPricingIncomplete.txt"
    rm "skuSoldPricingIncomplete.txt"
fi

echo "Running getMarketPrices"
# This reads the .txt file created from createSKUDictionary and pulls the market pricing information from TCGPlayer for each SKU
# Expected runtime is 7 minutes
python getMarketPrices.py

echo "Running getSoldPrices"
# This reads the .txt file created from createSKUDictionary and pulls the sales pricing information from TCGPlayer for each SKU
# Expected runtime is 14 hours
python getSoldPrices.py

echo "Running SKUmerge"
#Generastes files (csv, txt) that contains each card's static information + pricing information 
python SKUmerge.py

echo "Running dataCleanse"
# Generates files (csv, txt) that contains each card's static information + pricing information 
python dataCleanse.py

echo "Running sendData"
# Sends .txt file from dataCleanse to MongoDB
python sendData.py
echo "Output sent to MongoDB"

echo "Removing temporary data files"
# Removes skuMarketPricing.txt (produced by getMarketPrices.py) and skuSoldPricing.txt (produced by getSoldPrices.py)
# Removes skuSoldPricingIncomplete.txt if getSoldPrices.py did not pull a complete set of data

if [ -f "skuMarketPricing.txt" ]
then
    echo "Removing skuMarketPricing.txt"
    rm "skuMarketPricing.txt"
fi

if [ -f "skuSoldPricing.txt" ]
then
    echo "Removing skuSoldPricing.txt"
    rm "skuSoldPricing.txt"
fi

if [ -f "skuSoldPricingIncomplete.txt" ]
then
    echo "Removing skuSoldPricingIncomplete.txt"
    rm "skuSoldPricingIncomplete.txt"
fi

echo "Successful pull"