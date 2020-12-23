#!/bin/bash

#These run every night

echo "Running getSetNames"
python "getSetNames.py setDictionaryNew.csv"

DIFF=$(diff setDictionaryNew.csv setDictionary.csv) 

if [ "$DIFF" != "" ] 
then
    #This should run when a new set is released
    echo "Difference detected, loading new setDictionary"
    mv setDictionaryNew.csv setDictionary.csv
    echo "Running createSKUDictionary"
    #This generates a file whose entries contain 
    # Note that SKUs are representations of a set of condition, edition, and language
    # {Set Name: [Card Name, PID, {SKU: [Condition, Edition, Language]}]
    python "createSKUDictionary.py"
else
    echo "No difference, no need to update SKUs"
fi

echo "Running readSkuinput"
#This reads the file created from createSKUDictionary and pulls the market price information from tcgplayer for each SKU 
python "readSKUinput.py"

echo "Running SKUmerge"
#Generastes files (csv, txt) that contains each card's static information + pricing information 
python "SKUmerge.py"
