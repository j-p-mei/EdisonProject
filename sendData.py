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
cardpricedb = "INSERT INTO " + dbname + ".CardPrice(CardID, PriceDate, Price) VALUES (%s, %s, %s)"
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
        cardname = line.split(',')[0]
        setname = line.split(',')[1]
        productid = line.split(',')[2]
        skuid = line.split(',')[3]
        condition = line.split(',')[4]
        edition = line.split(',')[5]
        language = line.split(',')[6]
        price = line.split(',')[9]
        if (linenumber > 1 and commacount == 11):
            valname = (counter + 1, cardname, setname, productid, skuid, condition, edition, language)
            if (price == "N/A"):
                valprice = (counter + 1, datadate, None)
            else:
                valprice = (counter + 1, datadate, price)
            mycursor.execute(cardnamedb,valname)
            mycursor.execute(cardpricedb,valprice)
            counter = counter + 1
        if (counter % 10000 == 0):
            mydb.commit()
            print(counter)
    mydb.commit()
    print("done!")
