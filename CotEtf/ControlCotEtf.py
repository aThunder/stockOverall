#controlCotUpdate.py

'''
    1. prompts user to create new SQL table or use existing
       for each specified COT commodity and
       then calls Type1CotFormat.py or Type2CotFormat.py (depending on requirements)
       to to populate SQL table
    2. Which of the 2 files is called depends on the COT format for each specific commodity
    3. Allows for creating new table or updating existing table
'''

import json
import urllib.request
import sqlite3
# import cotEtfSQLP
# import cotEtfCSV

class BuildCotAll():

    def __init__(self):
        self.conn = sqlite3.connect('../allCotEtf.db')
        self.c = self.conn.cursor()

    def createSQL(self):
        self.c.execute("DROP TABLE IF EXISTS DataCOT")

        self.c.execute("CREATE TABLE DataCOT (ID INTEGER PRIMARY KEY,ID_NameKey,"
                       "Dataset TEXT,Database TEXT,Name TEXT,Date,OpenInt INTEGER,"
                       "RptableLong INTEGER,RptableShort INTEGER, "
                  "NonRptableLong INTEGER,NonRptableShort INTEGER,UNIQUE (Name,Date))")
        # NetRptable REAL,NetNonRptable REAL

            # db.execute('insert into test(t1, i1) values(?,?)', ('one', 1)) ## sample for format syntax

    def createSQLAlt1(self):
        import cotCotSQL
        cotCotSQL.main()

    def populateTables(self,createOrUpdate):
        self.createOrUpdate = createOrUpdate
        self.etfList = []
        import cotType1Format,cotType2Format
        # import cotType1FormatX
        stocks = cotType1Format.main("https://www.quandl.com/api/v3/datasets/CFTC/TIFF_CME_SC_ALL.json", 1,'SPY')
        self.etfList.append(stocks)
        bonds = cotType1Format.main("https://www.quandl.com/api/v3/datasets/CFTC/US_F_ALL.json",2,'THL')
        self.etfList.append(bonds)
        gold = cotType2Format.main("https://www.quandl.com/api/v3/datasets/CFTC/GC_F_ALL.json",3,'GLD')
        self.etfList.append(gold)
        oil = cotType2Format.main("https://www.quandl.com/api/v3/datasets/CFTC/CL_F_ALL.json",4,'USO')
        self.etfList.append(oil)
        print('etfList: ', self.etfList)

    def printMessage(self):
        counter = 1
        print()
        print()
        print("COT Table has been {0}/populated for: ".format(self.createOrUpdate))
        for i in self.etfList:
            print("{0}: {1}".format(counter,i))
            counter +=1

    def createEtfCsv(self):
        print()
        print()
        import cotEtfCSV
        startDate = input("ETF Data: Enter start date. Format: yyyymmdd (example: 20150115): ")
        endDate = input("Enter end date (Leave blank for most recent date): ")
        cotEtfCSV.correspondingSymbols(startDate,endDate)

    def populateSQL(self):
         populateSQL = input("Populate SQL Table for all ETFs? ('y' or 'n'): ")
         if populateSQL == 'y':
            # print('heading to cotEtfSQLP')
            import cotEtfSQLP
            cotEtfSQLP.start()


def main():
    a = BuildCotAll()
    print()
    newOrExist = input("COT Data: Create new table('new') or update existing table('u')?: ")
    print()
    if newOrExist == 'new':
        print("CAUTION: Creating a new table will delete all current data")
        print()
        doubleCheck = input("Type 'y' to verify you want to create a new table: ")
        if doubleCheck == 'y':
            a.createSQL()
            # a.createSQLAlt1()
            b = a.populateTables('created')
            print('b: ',b)
        else:
            main()
    else:
        print("Updating existing table")
        a.populateTables('updated')

    a.printMessage()
    a.createEtfCsv()
    a.populateSQL()

if __name__ == '__main__': main()
