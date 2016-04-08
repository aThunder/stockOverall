
#setStkCSVFile.py


"""Very basic program with no prompts or GUI:
              1. Creates new CSV file or accesses existing file
                 for specified list of stock symbols and
                 date ranges. (uses Yahoo Finance for data)
              2. Also allows for choosing between updating existing CSV file
                 or creating a new CSV file
              3. Weekly data as of close Tuesday is used to sync witg COT data
              4. counts # of rows in file
"""
import pandas.io.data as pullData
import datetime
import time

#############################################################
class setCSVFile():
    def __init__(self,symbol):
        self.symbol = symbol

    def accessSite(self,start,end):
        print('Symbol: ', self.symbol.upper())
        self.start = start
        self.end = end
        self.timeSeries0 = pullData.DataReader(self.symbol, 'yahoo', self.start, self.end)

    def weekOrDay(self,freq):
        # self.timeSeries0 = self.timeSeries0.asfreq('W-TUE')
        self.timeSeries0 = self.timeSeries0.asfreq(freq)

        # print("Entered stxSetFile1b.py to use existing file")
        #alternate way to retrieve data
        #self.timeSeries0 = pd.io.data.get_data_yahoo(symbol, self.start, self.end)
        ##for SP500 in above line only use '%5EGSPC' as symbol
        # self.createCSV

    def createCSV(self):
        # self.timeSeries0.to_csv('{0} ohlc.csv'.format(self.symbol))
        # self.dataFile = pullData.read_csv('{0} ohlc.csv'.format(self.symbol), index_col='Date', parse_dates=True)
        self.timeSeries0.to_csv('../{0} ohlc.csv'.format(self.symbol))
        self.dataFile = pullData.read_csv('../{0} ohlc.csv'.format(self.symbol), index_col='Date', parse_dates=True)
        return self.dataFile

    def useCurrentCSV(self):
        # self.dataFile = pullData.read_csv('{0} ohlc.csv'.format(self.symbol), index_col='Date',parse_dates=True)
        self.dataFile = pullData.read_csv('../{0} ohlc.csv'.format(self.symbol), index_col='Date', parse_dates=True)
        #print('self.dataFile print:', self.dataFile[2:3])
        print("Entered stxSetFile1b.py to create new file")
        return self.dataFile

    def countRows(self,csv1):
        self.dayCounter = 0
        for i in range(len(csv1)):
            self.dayCounter +=1
        print('days in the file:',self.dayCounter)
        print()
        return self.dayCounter

#########################################################
#########################################################
def main(symbol,choice1a,freq,startDate1,endDate1,ID_NameKey,actionSelected):
    # print('hi again')
    a = setCSVFile(symbol)

    if choice1a == 'e' :
            csv1 = a.useCurrentCSV()
            return csv1

    if choice1a == 'n':
            # checker = Trueƒar
            a2 = a.accessSite(startDate1,endDate1)
            if freq != 'd':
                a.weekOrDay(freq)
                csv1 = a.createCSV()
            else:
                csv1 = a.createCSV()

    fileDays = a.countRows(csv1)

def correspondingSymbols(startDate,endDate):
    # startDate = '20050101'
    # endDate = '20160301'
    # Frequency options are 1)'D' 2)'W-TUE' (or whichever day of week preferred) 3)'M 4)'A'
    # frequency = input('Enter Frequency: ').lower()

    print('hi')
    frequency = 'w-tue'

    main('spy', 'n',frequency,startDate,endDate,1,'actionSelected')
    main('gld', 'n',frequency,startDate,endDate,3,'actionSelected')
    main('tlh', 'n',frequency,startDate,endDate,2,'actionSelected')
    # main('ief',frequency,startDate,endDate,2,'actionSelected')
    main('uso', 'n',frequency,startDate,endDate,4,'actionSelected')

    # if __name__ == '__main__': main('spy', 'n',frequency,startDate,endDate,1,'actionSelected')
    # if __name__ == '__main__': main('gld', 'n',frequency,startDate,endDate,3,'actionSelected')
    # if __name__ == '__main__': main('tlh', 'n',frequency,startDate,endDate,2,'actionSelected')
    # # # if __name__ == '__main__': main('ief',frequency,startDate,endDate,2,'actionSelected')
    # if __name__ == '__main__': main('uso', 'n',frequency,startDate,endDate,4,'actionSelected')

# correspondingSymbols(startDate,endDate)