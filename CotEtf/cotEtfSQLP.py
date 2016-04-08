# stkSQLFill.py

'''
    1. Takes CSV file (created in setStkCSVFile.py) and
       creates and populates SQLite table
    2. Adds self.ID_NameKey to CSV data for Join purposes
    3. Allows for creating new table or updating existing table
'''

import sqlite3
import csv
# import sys

class Csv2SQL():

    def __init__(self,symbol,ID_NameKey):
        self.symbol = symbol
        self.ID_NameKey = ID_NameKey
        # self.frequency = frequency

        self.conn = sqlite3.connect('allCotEtf.db')
        self.c=self.conn.cursor()
        # self.keyFiller = 1

    def createTableName(self,frequency):
        self.frequency = frequency
        print("Symbol: ",self.symbol)
        print("Frequency: ",self.frequency)

        if self.frequency =='d':
            # print('Daily')
            self.tableName = 'CotEtfDataDaily'
        elif self.frequency == 'm':
            # print('Monthly')
            self.tableName = 'CotEtfDataMonthly'
        elif self.frequency == 'a':
            # print('Annual')
            self.tableName = 'CotEtfDataAnnual'
        elif self.frequency == 'w-mon' or 'w-tue' or 'w-wed' or 'w-thu' or 'w-fri':
            # print('Weekly-Tues')
            self.tableName = 'CotEtfDataWeekly'
        else:
            ('Cannot find a match for frequency {0}'.format(self.frequency))

        print("TableName: ",self.tableName)

    # def dailyExceptionCreateTableName(self):
    #     self.tableName = 'SymbolsDataWeekly'

    def createTables(self):

        for i in self.symbol:

            # print(i)
            # print(self.tableName)
            self.c.execute("DROP TABLE IF EXISTS {0}".format(self.tableName))

            ### Following uses ID as only PRIMARY KEY in order to get ID to autoincrement
            self.c.execute("CREATE TABLE {0}(ID INTEGER PRIMARY KEY, ID_NameKey INTEGER,Symbol CHAR,date, "
                           "open real,high real ,low real,close real ,vol int ,adjclose real,UNIQUE (Symbol,date))".format(self.tableName))

       ### Following 2 lines are for later development
            # self.index1 = self.c.execute("CREATE INDEX INDEXKEY ON StxData2(date)")
            # self.index2 = self.c.execute("CREATE UNIQUE INDEX INDEXDATE ON StxData2(keynumber)")

    def populateTables(self):
        for i in self.symbol:
            # print('asdfg: ',i)
            rowNumber=0
            # with open('{0} ohlc.csv'.format(i), newline='') as csvfile:
            with open('../{0} ohlc.csv'.format(i), newline='') as csvfile:
              reader = csv.reader(csvfile, delimiter=',', quotechar='|')
              for row in reader:
                if rowNumber > 0:

                  # print(self.keyFiller,i,row[0],row[1],row[2],row[3],row[4],row[5],row[6])

                  self.c.execute("INSERT OR IGNORE INTO {0} (ID_NameKey,symbol, date, "
                                 "open,high ,low ,close ,vol ,adjclose ) VALUES (?,?,?,?,?,?,?,?,?)".format(self.tableName),
                                 (self.ID_NameKey,i,row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

                  # print("rowNumberIf: ",rowNumber)
                  # self.c.execute("REPLACE INTO StxData2 (keynumber, symbol, date,open,high ,low ,close ,vol ,adjclose ) VALUES (?,?,?,?,?,?,?,?,?)", (self.keyFiller,i,row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
                else:
                    rowNumber += 1
                    # print("rowNumberElse: ",rowNumber)
              self.conn.commit()

              # print('SQL Table Updated')

            ###Leave here for now for future reference
              # cursor3 = conn.execute("SELECT date, close from Stock"+ i + " ORDER BY date")
              # for row in cursor3:
              #     print(row)
        roww = self.c.lastrowid
        print("lastrow: ",roww)

    def printMessage(self,whichOne):
        if whichOne == 'c':
            # print()
            print("SQL Table Created")
            print()
        else:
            # print()
            print("SQL Table Updated")
            print()
        # self.c.execute(select count(*) from <stxTable1> where ..

# main triggered by setStkCSVFile.py
def main(symbols,createOrUpdate,ID_NameKey,frequency):
    # print('XYZ: ',symbols,createOrUpdate,ID_NameKey,frequency)
    # print(symbols)
    # chooseTable = input("Add to existing Table ('a') or create new Table ('c')?: ")
    a = Csv2SQL(symbols,ID_NameKey)

    # if frequency != 'd':
    a.createTableName(frequency)

    if createOrUpdate== 'c':
        b = a.createTables()
        c= a.populateTables()
    elif createOrUpdate == 'u':
        c = a.populateTables()
    else:
        print("Invalid Response. Try Again")
        # start(symbols)
    d = a.printMessage(createOrUpdate)

def start():
    print('arrived in cotEtfSQLP')
    #Specify 'c' or 'e' for first item only. All others always 'e'
    frequency = 'w-tue'.lower()

    main(['SPY'], 'c',1,frequency)
    main(['GLD'], 'u',3,frequency)
    main(['TLH'], 'u',2,frequency)
    # main(['IEF'], 'u',2,frequency)
    main(['USO'], 'u',4,frequency)

    # if __name__ == '__main__': main(['SPY'], 'c',1,frequency)
    # if __name__ == '__main__': main(['GLD'], 'u',3,frequency)
    # if __name__ == '__main__': main(['TLH'], 'u',2,frequency)
    # if __name__ == '__main__': main(['IEF'], 'u',2,frequency)
    # if __name__ == '__main__': main(['USO'], 'u',4,frequency)
