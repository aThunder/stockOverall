
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
        # self.symbolList = symbolList
        self.symbol = symbol
        # self.validSymbols = []
        # self.invalidSymbols = []


    def accessSite(self,start,end):
        # print('self.symbol: ', self.symbol)
        self.start = start
        self.end = end
        try:
            self.timeSeries0 = pullData.DataReader(self.symbol, 'yahoo', self.start, self.end)
            print("***CSV file for {0} has just been created".format(self.symbol.upper()))
            print()
        except:
            print()
            print("***ERROR***: {0} is not a valid symbol".format(self.symbol.upper()))
            print()
            placeFiller = input("Hit Enter/Return to continue")
            print()
            badSymbol = 'NO'
            return badSymbol

    def weekOrDay(self,freq):
        # self.timeSeries0 = self.timeSeries0.asfreq('W-TUE')
        self.timeSeries0 = self.timeSeries0.asfreq(freq)

        # print("Entered setStkCSVFile.py to use existing file")
        #alternate way to retrieve data
        #self.timeSeries0 = pd.io.data.get_data_yahoo(symbol, self.start, self.end)
        ##for SP500 in above line only use '%5EGSPC' as symbol
        # self.createCSV

    def createCSV(self):
        print
        self.timeSeries0.to_csv('{0} ohlc.csv'.format(self.symbol))
        self.dataFile = pullData.read_csv('{0} ohlc.csv'.format(self.symbol), index_col='Date',parse_dates=True)
        return self.dataFile

    def useCurrentCSV(self):
        self.dataFile = pullData.read_csv('{0} ohlc.csv'.format(self.symbol), index_col='Date',parse_dates=True)
        #print('self.dataFile print:', self.dataFile[2:3])
        print("Entered stxSetFile1b.py to create new file")
        return self.dataFile

    def countRows(self,csv1):
        self.dayCounter = 0
        #print('csv1: ', csv1)
        for i in range(len(csv1)):
            # print(i)
            self.dayCounter +=1
        print('days in the file:',self.dayCounter)
        return self.dayCounter

    def populateYorN(self,symbolList,ID_NameKey,freq):
        print()
        print('Populate SQL Table for: ')
        # print('SS: ',self.symbol)
        for i in self.symbolList:
            print(i.upper())
        populateSQL = input("Enter 'y' for yes or anything else for 'no': ")
        print()

        if populateSQL == 'y':
            createOrExisting = input("Create new table('newyesnew') or update existing ('u')? ")
            if createOrExisting == 'newyesnew' or createOrExisting == 'u':
                import stkSQLFill1
                stkSQLFill1.main(self.symbolList,createOrExisting,ID_NameKey,freq)
            else:
                print()
                print("'{0}' is an incorrect entry. Try again".format(createOrExisting))
                print()
                return False
        else:
            return

#########################################################
#########################################################
def main(symbol,choice1a,freq,startDate1,endDate1,ID_NameKey,actionSelected):
    # validSymbols = []
    # invalidSymbols = []
    valid = True
    # print("symbolList: ", symbol)
    # print(symbol,choice1a,freq,startDate1,endDate1,ID_NameKey,actionSelected)

    a = setCSVFile(symbol)
    # a = setCSVFile(symbolList,i)

    if choice1a == 'e' :
            csv1 = a.useCurrentCSV()
            # validSymbols.append(symbol)
            # return csv1

    if choice1a == 'n':
            # checker = True
            a2 = a.accessSite(startDate1,endDate1)
            if a2 == 'NO':
                # print("SKIP & MOVE ON AS {0} IS NOT A VALID SYMBOL".format(symbol.upper()))
                print()
                # invalidSymbols.append(symbol)
                toReturn = ['Dummy',False]
                return toReturn
            else:
                if freq != 'd':
                    a.weekOrDay(freq)
                    csv1 = a.createCSV()
                    # validSymbols.append(symbol)
                else:
                    csv1 = a.createCSV()
                    # validSymbols.append(symbol)

    # fileDays = a.countRows(csv1)
    # print("Valid: ",validSymbols)
    # print("Invalid: ",invalidSymbols)
    toReturn = [csv1,valid]
    return toReturn


## Following is for standalone testing (instead of main() being called by setStkList.py)
# startDate = '20150101'
# endDate = '20160301'

##Frequency options are 1)'D' 2)'W-TUE' (or whichever day of week preferred) 3)'M 4)'A'
# frequency = input('Enter Frequencyyyyyy: ').lower()

# if __name__ == '__main__': main('spy', 'n',frequency,startDate,endDate,1,'actionSelected')
# if __name__ == '__main__': main('gld', 'n',frequency,startDate,endDate,3,'actionSelected')
# if __name__ == '__main__': main('tlh', 'n',frequency,startDate,endDate,2,'actionSelected')
# # # if __name__ == '__main__': main('ief',frequency,startDate,endDate,2,'actionSelected')
# if __name__ == '__main__': main('uso', 'n',frequency,startDate,endDate,4,'actionSelected')
