import csv
import pprint

# Card Name, Rarity, Release Set, Group ID, Edition, Condition
cardDictionary = {}

with open('card_list.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["Card Name"]
        rarity = row['Rarity']
        set = row['Set']
        edition = row['Edition']
        condition = row['Condition']
        #print(row["Card Name"], row['Rarity'], row['Set'])
        try:
            cardDictionary[set].append((name, rarity, edition, condition))
        except:
            cardDictionary[set] = [(name, rarity, edition, condition)]

pprint.pprint(cardDictionary)
