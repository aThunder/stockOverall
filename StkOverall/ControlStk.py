#ControlStksOnly.py

'''This program will call each of the following programs:
    1. setStkList.py: Prompts user to specify list of stock symbols
                      and returns list to ControlStksOnly.py
    2.setStkCSVFile.py: Checks to make sure each symbol is valid
                        and creates a CSV file for each valid symbol
                        and returns CSV files to ControlStksOnly.py
    3. stkSQLFill1.py: ControlStksOnly.py prompts for whether to populate
                       SQL and if so whether to update existing table or to
                       create a new table


    Iteration Overview:
    1. setStkList.py : N/A
    2. setStkCSVFile: Processes one symbol at a time as each one is passed from ControlStksOnly.py
    3. stkSQLFill1.py: Receives a List from ControlStksOnly.py and iterates through it

'''

class UpdateAll():

    def __init__(self,answer1):
        self.answer1 = answer1
        self.validSymbols = []
        self.invalidSymbols = []


    def createList(self):
        # print("Will now call setStkList")
        import stkList
        x = stkList.main()
        return x

    def setCSV(self,symbol,startDate,endDate,freq):
        self.freq = freq
        # print("Will now call setStkCSVFile")
        import stkCSV
        # freq = 'd'
        # startDate = '20160215'
        xx = stkCSV.main(symbol,'n',self.freq,startDate,endDate,99,'actionSelected')
        # print(xx[1])
        if xx[1] == True:
            self.validSymbols.append(symbol)
        else:
            self.invalidSymbols.append(symbol)
        # print("Valid: ", self.validSymbols)
        # print("Invalid: ",self.invalidSymbols)
        # return xx

    def populateYorN(self,symbolList):
        counter = 1
        print()
        print('Populate {0} SQL Table for: '.format(self.freq))
        for i in self.validSymbols:
            print("{0}: {1}".format(counter,i))
            counter += 1

        # if self.frequency == 'd':
        #     print('Daily')
        #     self.tableName = 'SymbolsDataDaily'
        # elif self.frequency == 'w-mon' or 'w-tue' or 'w-wed' or 'w-thu' or 'w-fri':
        #     print('Weekly-Tues')
        #     self.tableName = 'SymbolsDataWeekly'
        # elif self.frequency == 'm':
        #     print('Monthly')
        #     self.tableName = 'SymaabolsDataMonthly'
        # elif self.frequency == 'a':
        #     print('Annual')
        #     self.tableName = 'SymbolsDataAnnual'
        # else:
        #     print("{0} is an INVALID FREQUENCY")


        populateSQL = input("Enter 'y' for yes or anything else for 'no': ")
        print()

        if populateSQL == 'y':
            createOrExisting = input("Create new table('newyesnew') or update existing ('u')? ")
            if createOrExisting == 'newyesnew' or createOrExisting == 'u':
                import stkSQLP
                # print("sssL: ",self.validSymbols)
                stkSQLP.main(self.validSymbols,createOrExisting,99,self.freq)
            else:
                print()
                print("'{0}' is an incorrect entry. Try again".format(createOrExisting))
                print()
                return False
        else:
            return

    # def populateSQL(self,csv):
    #     print("Will now call stkSQLFill1")
    #     import stkSQLFill1
    #     xxx = stkSQLFill1.main(csv)

def main():
    a = UpdateAll('filler')
    step1 = a.createList()
    # print("Step1: ",step1)

    for i in step1[0]:
        # print("iControl: ",i)
        step2 = a.setCSV(i,step1[1],step1[2],step1[3])
        # print(step2)

    step3 = a.populateYorN(step1[0])
    if step3 == False:
        a.populateYorN(step1[0])


if __name__ == '__main__': main()
