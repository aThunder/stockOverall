# ControlStkVolume.py

'''
    1. Queries SQLite table for symbol and date range specified by user
    2. Performs several volume calculations:
    3. Prompts user to select one of 3 Volume Indicators categories
    4. Calls stkVolumeAllTests to perform the calcs in step 3
'''

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class QueryData():

    def __init__(self):
        self.conn = sqlite3.connect('../allStks.db')
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = sqlite3.Row
        self.diskEngine = create_engine('sqlite:///../allStks.db')
        self.recentList =[]

    def setSettings(self,symbol,IDKEY,numberDays):
        self.symbol = symbol
        self.numberDays = numberDays + 1 #for subset
        self.numberDaysRetrieve = numberDays * 2 #for fullset
        print()
        print(self.symbol.upper())
        # print("Begin Exception Testing")

    def retrieveFullSet(self):
        # status1 = True
        try:
            # self.dfFull = pd.read_sql_query("SELECT SYMBOL, date('now','-1 day'),CLOSE,date " #max(DATE), CLOSE " #date('now','-1 day'), CLOSE " # date('now') - 1 day "#max(date)-1,SYMBOL,CLOSE "
            #                                        "FROM SymbolsDataDaily "
            #                                        "WHERE SYMBOL IN ('aapl') "
            #                                        " AND date('now',-5 days) "
            #                                        " ".format(IDKEY,self.symbol),self.diskEngine)
            #
            self.dfFullSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
                                                   "FROM (SELECT * FROM SymbolsDataDaily "
                                                   "WHERE SYMBOL IN ('{0}')"
                                                   "ORDER BY DATE DESC LIMIT {1}) "
                                                   "ORDER BY DATE ASC "
                                                   " ".format(self.symbol,self.numberDaysRetrieve),self.diskEngine)

            test1 = self.dfFullSet['date'][1]
            # print("FullSet 2nd row: ", self.dfFullSet['date'][1])

            status1 = True
            return status1

        except:
            print("==================================")
            print("******{0} Not in Database******".format(self.symbol))
            print()
            print("==================================")
            status1 = False
            return status1

    def retrieveSubSet(self):
        # # self.df = self.dfFull[0:][self.numberDays-2:]
        # # print("Self df2: ", self.dfFull['vol'][4])
        # self.df3 = self.dfFull.ix[self.numberDays-2:]
        # print("Self df3: ", self.dfFull3[3:4])

        try:
            self.dfSubSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
                                                   "FROM (SELECT * FROM SymbolsDataDaily "
                                                   "WHERE SYMBOL IN ('{0}')"
                                                   "ORDER BY DATE DESC LIMIT {1}) "
                                                   "ORDER BY DATE ASC "
                                                   " ".format(self.symbol,self.numberDays),self.diskEngine)
            # print("Subset: ", self.dfSubset)
            test2 = test1 = self.dfSubSet['date'][1]
            # print("Subset 2nd row: ", self.dfSubSet['date'][1])
            status2 = True
            return status2
        except:
            print('False 2')
            status2 = False
            return status2

    def retrieveOverallMktSet(self,symbolMkt):
        self.symbolMkt = symbolMkt
        try:
            self.dfOverallMktSet = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE,VOL "
                                              "FROM (SELECT * FROM SymbolsDataDaily "
                                              "WHERE SYMBOL IN ('{0}')"
                                              "ORDER BY DATE DESC LIMIT {1}) "
                                              "ORDER BY DATE ASC "
                                              " ".format(self.symbolMkt, self.numberDaysRetrieve), self.diskEngine)
            # print("Subset: ", self.dfSubset)
            test3 = test1 = self.dfOverallMktSet['date'][1]
            # print("OverallMkt ({0}) 2nd row: {1}".format(self.symbolMkt,self.dfOverallMktSet['date'][1]))
            status2 = True
            return status2
        except:
            print('False 3')
            status2 = False
            return status2

    def returnFullSet(self):
        return self.dfFullSet
    def returnSubSet1(self):
        return self.dfSubSet
    def returnOverallMktSet1(self):
        return self.dfOverallMktSet

class IndicatorsVolume(QueryData):

    def chooseIndicators(self):
        try:
            print("Select one of these Volume Indicators: ")
            print("   1. Volume Up/Down")
            print("   2. Volume Mov Avgs")
            print("   3. Volume Stock:Market Ratios")
            print("   4. Exit")
            print()
            choice1 = int(input("Enter number here: "))
            print("Choice Selected: ",choice1)
            return choice1
        except:
            print()
            print("INVALID ENTRY. Enter only a number 1-4")
            print("DEBUG1")
            choice1 = "NaN"
            print("Choice1: ", choice1)
            return choice1

    def callStkVolumeUpDown(self,symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays):
        import stkVolumeAllTests
        stkVolumeAllTests.main(1,symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)

    def callStkVolumeMovAvgs(self, symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays):
        import stkVolumeAllTests
        stkVolumeAllTests.main(2,symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)

    def callStkVolumeMktRto(self, symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays):
        import stkVolumeAllTests
        stkVolumeAllTests.main(3, symbol1, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)

def main():
    a = QueryData()
    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    criteria5 = ['aapl','spx'] #,';dssdf','spy'] #,'sl;dfk','spy'] #,'mmm','gld']
    # numberOfDays = input("Enter Number of Days for Volume Tests: ") ## commented out for testing only
    numberOfDays = 50

    for i in criteria5:
        a.setSettings(i,99,numberOfDays)
        fullSet1 = a.retrieveFullSet()
        subSet1 = a.retrieveSubSet()
        overallMktSet1 = a.retrieveOverallMktSet('spy')

        if fullSet1:
            fullSet1a = a.returnFullSet()
            subSet1a = a.returnSubSet1()
            overallMktSet1a = a.returnOverallMktSet1()
            print("===================================")
            buildIndicators(i,fullSet1a,subSet1a,overallMktSet1a,numberOfDays)
        else:
            print('NOOOOOO')
            print()

def buildIndicators(i,fullSet1a,subSet1a,overallMktSet1a,numberOfDays):
            b = IndicatorsVolume()

            choice1 = b.chooseIndicators()
            # print("Type: ",type(choice1))
            # print("choice1: ",choice1)

            if choice1 == 1:
                b.callStkVolumeUpDown(i, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)
            elif choice1 == 2:
                b.callStkVolumeMovAvgs(i, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)
            elif choice1 == 3:
                b.callStkVolumeMktRto(i, fullSet1a, subSet1a, overallMktSet1a, numberOfDays)
            elif choice1 == 4:
                print("Bye")
                # break
            else:
                print("**********Invalid Entry. Try Again**********")
                # b.chooseIndicators()
                buildIndicators(i,fullSet1a,subSet1a,overallMktSet1a,numberOfDays)

if __name__ == '__main__': main()



################################
################################


