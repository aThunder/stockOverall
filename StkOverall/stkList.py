# setStkList.py

'''
    1. Prompts user to input stock symbols
    2. Can handle blanks (even extra blanks) and commas as separators
    3. Creates List of symbols and sends to setStkCSVFile.py
'''

# import sys

class StkSpecs():

    def __init__(self,ID_NameKey):
        self.ID_NameKey = ID_NameKey
        # print("Entered setStkList")

    def promptForList(self):
        self.list1 = []
        self.list2 = []
        print()
        self.list1 = input("Type List of Stocks (separated by spaces): ")
        # print(self.list1)

    def parseList(self):
        counter=0
        self.completeList = []
        oneSymbol = ''
        # x =[i for i in self.list1]
        # print(x)

        check = False
        for i in self.list1:
            counter += 1
            if (i == " " or i == ",") and check == True:
                self.completeList.append(oneSymbol)
                oneSymbol = ''
                check = False
            elif (i == " " or i == ",") and check == False:
                oneSymbol = ''
            else:
                oneSymbol += i
                if counter == len(self.list1):
                    self.completeList.append(oneSymbol)
                else:
                    check = True

        print(self.completeList)

    def promptForDates(self):
        print()
        self.start1 = input("Start Date (yyyymmdd): ")
        print()
        self.end1 = input("End Date (leave blank for latest date): ")
        print()

    def promptForFreq(self):
        # print()
        self.freq = input("Daily (d), Weekly (w-tue), Monthly (m), Annually (a): ")
        if self.freq.lower() == ('d' or 'w-tue' or 'm' or 'a'):
            print()
        else:
            print()
            print("{0} is an INVALID FREQUENCY...Try again".format(self.freq))
            print()
            self.promptForFreq()
    def returnInputs(self):
        # print(self.completeList,self.start1,self.end1)
        return self.completeList,self.start1,self.end1,self.freq


    ## 1. iterate through self.completeList OR
    # def createCSV(self):
    #     import setStkCSVFile
    #     for i in self.completeList:
    #         setStkCSVFile.main(i,'n','d',self.start1,self.end1,99,'Action Selected')

    ## 2. Send self.complete to be iterated through by setStkCSVFile
    def createCSV(self):
        import setStkCSVFile
        frequency = input('Enter Freq: ').lower()
        setStkCSVFile.main(self.completeList,'n',frequency,'20160210',self.end1,99,'Action Selected')


def main():
    ID_NameKey = 0
    a = StkSpecs(ID_NameKey)
    a.promptForList()
    a.parseList()
    a.promptForDates()
    a.promptForFreq()
    # a.createCSV()
    stkList1 = a.returnInputs()
    # print("stkList1: ",stkList1)
    return stkList1


if __name__ == '__main__': main()



