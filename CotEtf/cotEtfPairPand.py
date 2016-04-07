# cotsqlqPandas.py

'''
    1. Queries 2 SQLite tables (COT & ETFs) and uses Join for results
    2. Performs several calculations and summaries on results
    3. Weekly data only
    4.
'''


import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class spCOT():

    def __init__(self):
        self.conn = sqlite3.connect('allCotEtf.db')
        self.cursor = self.conn.cursor()
        self.cursor.row_factory = sqlite3.Row
        self.diskEngine = create_engine('sqlite:///allCotEtf.db')
        self.recentList =[]

    def checkCotData(self,IDKEY):
        print(IDKEY)
        self.cotDataDetail = pd.read_sql_query("SELECT NAME,DATE,OPENINT "
                                               "FROM DataCOT "
                                               "WHERE ID_NAMEKEY = {0} "
                                               "AND DATE > '2014-01-01' ".format(IDKEY),self.diskEngine)
        print("CotDataDetail: ", self.cotDataDetail)

    def checkEtfData(self,IDKEY):
        print(IDKEY)
        self.EtfDataDetail = pd.read_sql_query("SELECT SYMBOL,DATE,CLOSE "
                                               "FROM CotEtfDataWeekly "
                                               "WHERE ID_NAMEKEY = {0} "
                                               "AND DATE > '2015-01-01' ".format(IDKEY),self.diskEngine)
        print("ETFDetail: ", self.EtfDataDetail)


    def innerJoin1(self,criteria1,startDate):
        self.criteria1 = criteria1
        # startDate = '2015-11-01'
        print('startDate: ', startDate)
        self.intoPandasJoin1 = pd.read_sql_query("SELECT DataCOT.NAME,"
                                                 " DataCOT.OPENINT, "
                                                 "DataCOT.DATE,"
                                                 " DataCOT.RptableLong,"
                                                 " DataCOT.RptableShort,"
                                                 " CotEtfDataWeekly.SYMBOL,"
                                                 " CotEtfDataWeekly.CLOSE,"
                                                 " CotEtfDataWeekly.VOL, "
                                                 " CotEtfDataWeekly.DATE "
                                                 " FROM DataCOT "
                                                 "INNER JOIN CotEtfDataWeekly "
                                                 "ON DataCOT.ID_NAMEKEY =  CotEtfDataWeekly.ID_NAMEKEY "
                                                 "AND DataCOT.DATE = CotEtfDataWeekly.DATE "
                                                 "WHERE DataCOT.DATE > '{0}' "
                                                 "AND NAME LIKE '{1}'"
                                                 "ORDER BY CotEtfDataWeekly.DATE asc".format(startDate,self.criteria1),
                                                 self.diskEngine)

        countLinesAll = self.intoPandasJoin1['Date'].count()
        self.intoPandasJoin1['NetReportable'] = self.intoPandasJoin1['RptableLong']-self.intoPandasJoin1['RptableShort']
        self.intoPandasJoin1['WkNetRptableChg'] = self.intoPandasJoin1['NetReportable'].diff()
        self.intoPandasJoin1['WkPriceChg'] = np.round(self.intoPandasJoin1['close'].diff(),decimals=2)

        print("JOINED: ",self.intoPandasJoin1)

    def mostRecent(self):

        countLines = self.intoPandasJoin1['WkNetRptableChg'].count()
        # print('#Lines: ',countLines)
        mostRecent = ("{0}: NetReportable: {1}  WeeklyChg: {2} WkPriceChg: {3}".
                format(self.intoPandasJoin1['Symbol'][countLines],self.intoPandasJoin1['NetReportable'][countLines],
                self.intoPandasJoin1['WkNetRptableChg'][countLines],self.intoPandasJoin1['WkPriceChg'][countLines]))

        # print("MostRecent {0}: {1}".
        #         format(self.criteria1,mostRecent))

        self.recentList.append(mostRecent)

    def summary1(self):
        print()
        counter=1
        for i in self.recentList:
            print(counter, i)
            counter +=1

    def plot1(self):
        print("Now plotting")
        plt.plot(self.intoPandas1['NetReportable'])
        plt.ylabel("Net Position")
        plt.xlabel("Date")
        plt.title("COT: {0} Net Reportable Position".format(self.criteria))
        plt.show()
        print("Was there a plot?")

    #         # db.execute('insert into test(t1, i1) values(?,?)', ('one', 1)) ## sample for format syntax

def main():
    a = spCOT()
    # criteria5 = ['%S&P%','%Gold%','%Bond%','%Oil%']
    criteria5 = ['%Oil%']
    startDate = input("Enter start date (YYYY-MM-DD): ") ## commented out for testing only
    # startDate = '2015-10-01' ## for testing expediting only
    for i in criteria5:
        # a.checkCotData(1)
        # a.checkEtfData(1)
        a.innerJoin1(i,startDate)
        a.mostRecent()
        # c= a.plot1()
    a.summary1()

if __name__ == '__main__': main()



############
 # def updateSQLNet(self):
    #     for i in self.netReportable:
    #         self.cursor.execute("INSERT INTO comboCOT"
    #                            "(NetRptable,NetNonRptable)"
    #                             " VALUES(?,?)",
    #                             (self.netReportable[counter],self.netNonReportable[counter]))
    #         self.conn.commit()
    #
    #     # db.execute("insert into test(t1, i1) values(?,?)", ('one', 1)) ## sample for format syntax

############
# def queryData(self,criteria):
    #     self.criteria = criteria
    #     counter = 1
    #     self.netReportableList = []
    #
    #     # for item in self.criteria:
    #     print("Criteria: ",self.criteria)
    #
    #     self.intoPandas1 = pd.read_sql_query("SELECT NAME,DATE,RPTABLELONG,RPTABLESHORT FROM comboCOT"
    #                                      " WHERE DATE > '2015-12-31' AND "
    #                                          "NAME LIKE '{0}'"
    #                                          " ORDER BY DATE".format(self.criteria),self.diskEngine)
    #
    #     # print("PandaTest1: ", (self.intoPandas1.values))
    #     # print("PandaTest1: ", (self.intoPandas1.values)[4][5])
    #     # print("PandaTest2: ", self.intoPandas1[['Name','OpenInt']])
    # def calcNets(self):
    #     # df['new_col'] = range(1, len(df) + 1) # general format example to add new dataframe column
    #
    #     # self.intoPandas1['NetReportable'] = self.intoPandas1['RptableLong']-self.intoPandas1['RptableShort']
    #     # print('NetReportable: ',self.intoPandas1['NetReportable'])
    #     # self.intoPandas1['NetNonReportable'] = self.intoPandas1['NonRptableLong']-self.intoPandas1['NonRptableShort']
    #     # self.intoPandas1['WeeklyNetRptableChg'] = self.intoPandas1['NetReportable'].diff()
    #     # # print(self.intoPandas1)
    #     print("WeeklyChg: ", self.intoPandas1['NetReportable'].diff())
