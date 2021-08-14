#from variables import * 
#this script is used to process data from a csv file to a mysql db
#how to run: python3 sendData.py output_2021.07.22.csv 2021-07-22
#make sure that the two tables are already created from tablecreation

import json
import mysql.connector
import csv
import sys


dbname = "carddatabase"
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Irewick07",
    database = dbname, 
)

mycursor = mydb.cursor(buffered=True)
cardnamedb = "INSERT INTO " + dbname + ".Card(CardID, CardName, SetName, ProductID, SKUID, CardCondition, Edition, CardLanguage) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
cardpricedb = "INSERT INTO " + dbname + ".CardPrice(CardID, PriceDate, AvailableLowestPrice, SoldMarket, SoldLowest, SoldHighest) VALUES (%s, %s, %s, %s, %s, %s)"
filename = sys.argv[1]
datadate = sys.argv[2]

#logging.info("Sending data to MySQL")
mycursor.execute("SELECT COUNT(*) FROM " + dbname + ".Card")
rowcount = mycursor.fetchone()
if (rowcount[0] == 0):
    counter = 0
else:
    mycursor.execute("SELECT MAX(CardID) FROM " + dbname + ".Card")
    result = mycursor.fetchone()
    counter = (result[0])
with open(filename) as f:
    linenumber = 0
    for line in f.readlines():
        linenumber = linenumber + 1
        line = line.rstrip()
        commacount = line.count(',')
        a = line.split(",")
        cardname = a[0]
        setname = a[1]
        productid = a[2]
        skuid = a[3]
        condition = a[4]
        edition = a[5]
        language = a[6]
        avaiable_lowest_price = a[7]
        sold_market = a[9]
        sold_lowest = a[10]
        sold_highest = a[11]
        if (linenumber > 1 and commacount == 11):
            mycursor.execute("SELECT CardID FROM " + dbname + ".Card WHERE ProductID = " +  productid + " and SKUID = " + skuid)
            check = mycursor.fetchone()
            if (check == None):
                valname = (counter + 1, cardname, setname, productid, skuid, condition, edition, language)
                if (avaiable_lowest_price == "N/A"):
                    avaiable_lowest_price = None
                if (sold_market == "N/A"):
                    sold_market = None    
                if (sold_lowest == "N/A"):
                    sold_lowest = None   
                if (sold_highest == "N/A"):
                    sold_highest= None  
                valprice = (counter + 1, datadate, avaiable_lowest_price, sold_market, sold_lowest, sold_highest)
                mycursor.execute(cardnamedb,valname)
                mycursor.execute(cardpricedb,valprice)
            else:
                if (avaiable_lowest_price == "N/A"):
                    avaiable_lowest_price = None
                if (sold_market == "N/A"):
                    sold_market = None    
                if (sold_lowest == "N/A"):
                    sold_lowest = None   
                if (sold_highest == "N/A"):
                    sold_highest= None  
                valprice = (check[0], datadate, avaiable_lowest_price, sold_market, sold_lowest, sold_highest)
                mycursor.execute(cardpricedb,valprice)
            counter = counter + 1
        if (counter % 10000 == 0):
            mydb.commit()
            print(counter)
    mydb.commit()
    print("done!")
