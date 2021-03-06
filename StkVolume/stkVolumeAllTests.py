# stkVolumeAllTests.py

'''
    1. Is called by ControlStkVolume.py (and sent dataframes with required data)
    2. Performs several volume calculations & groups into 3 categories:
            a. Volume Up/Down
            b. Volume Moving Averages
            c. Volume Stock:Mkt Ratios
    3. ControlStkvolume also sends the symbol to be used & which of 3 categories
       above to run


'''

import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

class stkVolume():

    def __init__(self):
        self.IDInit = 'xxxxx'

    def setSettings(self,symbol,IDKEY,dfFullSet,dfSubSet,dfOverallMktSet,movAvgLen,daysToReport):
        self.symbol = symbol
        self.dfFullSet = dfFullSet
        self.dfSubSet = dfSubSet
        self.dfOverallMktSet = dfOverallMktSet
        self.movAvgLen = movAvgLen
        self.daysToReport = daysToReport
        self.includeInResults = self.daysToReport * -1
        print(type(movAvgLen))
        print()
        print()
        # print("Full: ", self.dfFullSet)

    def volumeChg(self):
        self.volChg = self.dfFullSet['vol']-self.dfFullSet['vol'][1]
        self.volChg1 = self.dfFullSet['vol'].diff()
        print('VolumeChg: ',self.volChg,self.volChg1)
        print("TESTS: ",self.dfFullSet.sort_index(ascending=False, by = ['vol']))

    def mask1(self):
        mask = self.dfFullSet.open>200
        results = self.dfFullSet[mask]
        print("Mask: ",results)

    def orderData(self):
        # print("SortClose: ",self.df.sort('close'))
        periodchg = self.dfFullSet['close'].diff(2)
        print("CloseChange: ",periodchg)

    def priceVolStats(self):
        self.dfSubSet['changeClose'] = self.dfSubSet['close'].diff()

        self.volMaskUp = self.dfFullSet['close'].diff() >= 0
        self.volMaskDn = self.dfFullSet['close'].diff() < 0
        # self.upMean = self.dfSubSet[self.volMaskUp].describe()
        # print("upMean: ",self.upMean)
        # print("volMask: ", volMaskUp)
        # gains = self.dfSubSet[volMaskUp]
        # print("Gains: ", gains, gains.count())
        # print("{0} Days of Tests For {1}".format(self.daysToReport,self.symbol.upper()))
        # print("Through ", self.dfFullSet['date'][-1:])
        # print()
        # print("UpDays: ")
        # print("Count: ",self.volMaskUp[self.includeInResults:].count())
        # print()
        # print("DownDays: ")
        # print("Count: ", self.dfFullSet[self.volMaskDn]['close'][self.includeInResults:].count())

    def onBalanceVolume(self):
        self.runningVol = 0
        obvFirstLast = []

        counter = 0
        for i in self.dfSubSet['close'].diff():
            # print("i: ",i)
            # print("counter: ", counter)
            # print(self.dfSubSet['date'][counter])

            if i > 0 and counter > 0:
                # print("YES")
                self.runningVol += self.dfSubSet['vol'][counter]
                # print("OBVPlus: ", self.dfSubSet['date'][counter],self.runningVol)
            elif i < 0 and counter > 0:
                # print("NO")
                self.runningVol -= self.dfSubSet['vol'][counter]
                # print("OBVMinus: ", self.dfSubSet['date'][counter],self.runningVol)

            obvFirstLast.append(self.runningVol)
            counter += 1

        firstOBV = obvFirstLast[1]
        lastOBV = obvFirstLast[counter-1]
        print()
        print("OBV:first,last: ",firstOBV,lastOBV)
        print("OBV Change From {0} days prior: {1}".format(self.daysToReport,lastOBV-firstOBV))
        print()

    def avgVolumeUpDown(self):
        self.upVol = []
        self.dnVol = []
        totalUp = 0
        totalDn = 0
        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
        print("counter: ", counter)
        print()

        for i in self.dfFullSet['close'][self.includeInResults-1:].diff():

            if i > 0 and counter > 0:
                self.upVol.append(self.dfFullSet['vol'][counter])
            elif i < 0 and counter > 0:
                self.dnVol.append(self.dfFullSet['vol'][counter])

            counter += 1

        # for i in self.dfFullSet['close'][self.includeInResults - 1:].diff():
        #
        #     if i > 0 and counter > 0:
        #         self.upVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
        #     elif i < 0 and counter > 0:
        #         self.dnVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
        #     counter += 1

        for i in self.upVol:
            totalUp += i
        try:
            # upAvg = totalUp/len(self.upVol) # redundant with the np.mean line below
            # print('upVolumeMean: ', upAvg)
            print("UpDaysCount: ",len(self.upVol))

            upVolNP = np.mean(self.upVol)
            print("upVolumeMeanNP: ", upVolNP)
            print()
        except:
            print("There were no UP days in the {0}-day range".format(self.daysToReport))
            print()
        for i in self.dnVol:
            totalDn += i
        try:
            # dnAvg = totalDn/len(self.dnVol) # redundant with the np.mean line below
            # print('downVolumeMean: ', dnAvg)
            print("DownDaysCount: ",len(self.dnVol))

            dnVolNP = np.mean(self.dnVol)
            print("downVolumeMeanNP: ", dnVolNP)
            print()
        except:
            print("There were no DOWN days in the {0}-day range".format(self.daysToReport))
            print()
        try:
            print("Up:Down Volume Avg: ", upVolNP/dnVolNP)
            print("Up:Down Volume Days: ",len(self.upVol)/len(self.dnVol))
        except:
            print("Ratio of Up:Down Volume Days N/A")
            print()

    def priceMove(self):
        print()
        # print("XXXXX: ", self.dfSubSet)
        print("{0} days Price Observations: ".format(self.daysToReport))
        mostRecentPrice = self.dfSubSet['close'][self.daysToReport-1]
        firstPrice = self.dfSubSet['close'][1]
        # print()
        print("First,Last: ",firstPrice, mostRecentPrice)
        print("PriceChange: ",mostRecentPrice-firstPrice)
        print("% Change: ", ((mostRecentPrice-firstPrice)/firstPrice)*100)
        print("==================================")
        return

    def movAvg(self):
        # displayDays = int(input("How many day of {0}-moving average results to display?: ".format(self.numberDays-1)))
        # displayDaysNegative = displayDays * -1
        print("DDN: ",self.daysToReport,self.includeInResults)
        self.dfFullSet['rolling'] = pd.rolling_mean(self.dfFullSet['vol'], self.movAvgLen)
        print("{0}-day moving average for {1} is".format(self.movAvgLen, self.symbol))
        print(self.dfFullSet[['date', 'rolling']][self.includeInResults:])
        # print(self.dfFullSet[['date', 'rolling']][-5:])

    def vsOverallVolume(self):
        self.dfFullSet['MktVolu'] = self.dfOverallMktSet['vol']
        self.dfFullSet['MktRatioVol'] = self.dfFullSet['MktVolu'] / pd.rolling_mean(self.dfFullSet['MktVolu'],
                                                                                    self.movAvgLen)
        # print('MktRatio: ', self.dfFullSet)

        self.dfFullSet['IndivRatioVol'] = self.dfFullSet['vol'] / pd.rolling_mean(self.dfFullSet['vol'],
                                                                                  self.movAvgLen)
        # print('MktRatio: ', self.dfFullSet)

        self.dfFullSet['IndivtoMktVol'] = np.round(self.dfFullSet['IndivRatioVol'] / self.dfFullSet['MktRatioVol'],
                                                   decimals=3)
        # print("Complete: ")
        # self.includeInResults = self.daysToReport * -1
        # print(self.includeInResults)
        # print(self.dfFullSet[self.includeInResults:])
        print(self.dfFullSet.tail())

    def vsOverallVolumeUpDownAvg(self):
        self.upVOV = []
        self.dnVOV = []
        totalUpVOV = 0
        totalDnVOV = 0

        counter = (self.dfFullSet['date'].count() - 1 - self.daysToReport)
        print("counter: ", counter)
        print()

        # print(self.dfFullSet['close'].diff())

        for i in self.dfFullSet['close'][self.includeInResults-1:].diff():

            if i > 0 and counter > 0:
                self.upVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            elif i < 0 and counter > 0:
                self.dnVOV.append(self.dfFullSet['IndivtoMktVol'][counter])
            counter += 1

        # print("upVOVList: ", self.upVOV)
        # print("dnVOVList: ", self.dnVOV)

        for i in self.upVOV:
            totalUpVOV += i
        try:
            # upAvg = totalUp/len(self.upVol) # redundant with the np.mean line below
            # print('upVolumeMean: ', upAvg)
            print("Results calculated for {0} days of data".format(self.daysToReport))
            print("{0}-day MovingAvgs used for comparisons".format(self.movAvgLen))
            print()
            print("UpDaysVOVCount: ", len(self.upVOV))
            len(self.upVOV) > 0 #exception test
            upVOVnp = np.mean(self.upVOV)
            print("upVolumeVOVMeanNP: ", upVOVnp)
            print()
        except:
            print("There were no UP days in the {0}-day range".format(self.daysToReport))
            print()
        for i in self.dnVOV:
            totalDnVOV += i
        try:
            # dnAvg = totalDn/len(self.dnVol) # redundant with the np.mean line below
            # print('downVolumeMean: ', dnAvg)
            print("DownDaysVOVCount: ", len(self.dnVOV))
            len(self.dnVOV) > 0 #exception test
            dnVOVnp = np.mean(self.dnVOV)
            print("downVolumeVOVMeanNP: ", dnVOVnp)
            print()
        except:
            print("There were no DOWN days in the {0}-day range".format(self.daysToReport))
            print()
        try:
            print("Up:Down Volume Days: ", len(self.upVOV) / len(self.dnVOV))
            print("Up:Down Volume Avg: ", upVOVnp / dnVOVnp)
        except:
            print("Ratio of Up:Down Volume Days N/A")
            print()



    # def plot1(self):
    #     print("Now plotting")
    #     plt.plot(self.intoPandas1['NetReportable'])
    #     plt.ylabel("Net Position")
    #     plt.xlabel("Date")
    #     plt.title("COT: {0} Net Reportable Position".format(self.criteria))
    #     plt.show()
    #     print("Was there a plot?")
    #
    # #         # db.execute('insert into test(t1, i1) values(?,?)', ('one', 1)) ## sample for format syntax

def main(choice1,symbol,dfFullSet,dfSubSet,dfOverallMktSet,movAvgLen,daysToReport,numberOfAvailableDays):
    a = stkVolume()

    a.setSettings(symbol,99,dfFullSet,dfSubSet,dfOverallMktSet,movAvgLen,daysToReport)
    # print("OverallMktSet: ")
    # print(dfOverallMktSet)
    #         # a.volumeChg()
    #         # a.mask1()
    #         # a.orderData()
    #         # # a.grouping()
    if choice1 == 1:
        print(symbol.upper(), " Volume: Up/Down ")
        print()
        a.priceVolStats()
        a.onBalanceVolume()
        a.avgVolumeUpDown()
        a.priceMove()
    if choice1 == 2:
        print(symbol.upper(), " Volume: Moving Averages")
        print()
        a.movAvg()
    if choice1 == 3:
        print(symbol.upper()," Volume:  Stock-to-Market Ratios")
        print()
        a.vsOverallVolume()
        a.vsOverallVolumeUpDownAvg()
    print()
    print("Request Completed. Select another choice")
    print()
    import ControlStkVolume
    ControlStkVolume.buildIndicators(symbol,dfFullSet,dfSubSet,dfOverallMktSet,numberOfAvailableDays)

if __name__ == '__main__': main(choice1,symbol,fullSet1,subSet1,overallMktSet,movAvgLen,daysToReport,numberOfAvailableDays)