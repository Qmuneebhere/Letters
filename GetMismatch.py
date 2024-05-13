import os
import shutil
import numpy as np
import pandas as pd
import FileDetails as fd

section1 = '\n\n' + '***********************************************************' + '\n\n'

# ----------------------------Sets Columns and their Data Types-------------------------- #


# Column Names to be picked and their specific datatypes

colNames = ['LetterCode', 'UnifinID', 'MailType', 'ClientCode',
            'OOSFlag', 'CRFlag', 'Sum3PayOffer', 'Sum12PayOffer',
            'DebtDescription', 'OriginalCreditor',
            'ServicerClientID', 'COAmountDue', 'ChargeOffDate',
            'AmountPaidSinceCO', 'LastPaymentAmount', 'LastPaymentDate',
            'AmountDue', 'PrincipleBalance', 'InterestBalance',
            'CostBalance', 'FeeBalance', 'RecievedTotal', '1PayOffer',
            '3PayOffer', 'TotalQuarterPaid', 'ItemizationBalance',
            'ItemizationInterest', 'ItemizationFees',
            'ItemizationPmtsCredits', 'ItemizationCurrBalance']

# Column names of dataframe

dfNames = ['LetterCode', 'MailType', 'ClientCode',
        'OOSFlag', 'CRFlag', 'Sum3PayOffer', 'Sum12PayOffer',
        'DebtDescription', 'OriginalCreditor',
        'ServicerClientID', 'COAmountDue', 'ChargeOffDate',
        'AmountPaidSinceCO', 'LastPaymentAmount', 'LastPaymentDate',
        'AmountDue', 'PrincipleBalance', 'InterestBalance',
        'CostBalance', 'FeeBalance', 'RecievedTotal', '1PayOffer',
        '3PayOffer', 'TotalQuarterPaid', 'ItemizationBalance',
        'ItemizationInterest', 'ItemizationFees',
        'ItemizationPmtsCredits', 'ItemizationCurrBalance']

dataTypes = {'LetterCode': 'object', 'UnifinID': 'object', 'MailType': 'object',
             'ClientCode': 'object', 'OOSFlag': 'object', 'CRFlag': 'object',
             'Sum3PayOffer': 'float64', 'Sum12PayOffer': 'float64',
             'DebtDescription': 'object', 'OriginalCreditor': 'object',
             'ServicerClientID': 'float64', 'COAmountDue': 'float64',
             'ChargeOffDate': 'object', 'AmountPaidSinceCO': 'float64',
             'LastPaymentAmount': 'float64', 'LastPaymentDate': 'object',
             'AmountDue': 'float64', 'PrincipleBalance': 'float64',
             'InterestBalance': 'float64', 'CostBalance': 'float64',
             'FeeBalance': 'float64', 'RecievedTotal': 'float64',
             '1PayOffer': 'float64', '3PayOffer': 'float64', 'TotalQuarterPaid': 'float64',
             'ItemizationBalance': 'float64', 'ItemizationInterest': 'float64',
             'ItemizationFees': 'float64', 'ItemizationPmtsCredits': 'float64',
             'ItemizationCurrBalance': 'float64'
             }

# Column Numbers to be compared

colNum = [0, 2, 5, 7, 11, 12, 14, 15, 26, 28, 29, 31, 32,
            33, 34, 35, 36, 37, 38, 39, 40, 41, 48, 49, 61,
            69, 70, 71, 72, 73]


##########################################################################################
##                                                                                      ##
##      This function reads auto file for specific columns and returns a dataframe      ##
##                      with unifin IDs as index and column names.                      ##
##                                                                                      ##
##########################################################################################

def ReadAutoFile():

    df = pd.read_csv(fd.curr_dir + fd.autoFile, header=None, usecols=colNum, dtype=dataTypes,
                     names=colNames)

    df.set_index('UnifinID', inplace=True)  # Column UnifinID is set to index

    print(section1)
    print(f'Rows in auto file: {len(df.index)}'.center(60))

    # Slicing DebtDescription, OriginalCreditor because first 5
    # characters are to be compared only

    df['DebtDescription'] = df['DebtDescription'].str.replace('"','')
    df['OriginalCreditor'] = df['OriginalCreditor'].str.replace('"','')

    # Replaces blank DebtDescription in auto file

    df.loc[df['DebtDescription'] == '', 'DebtDescription'] = df['OriginalCreditor']

    df['DebtDescription'] = df['DebtDescription'].str.slice(stop=10)
    df['OriginalCreditor'] = df['OriginalCreditor'].str.slice(stop=10)

    # Both columns are converted to uppercase

    df['DebtDescription'] = df['DebtDescription'].str.upper()
    df['OriginalCreditor'] = df['OriginalCreditor'].str.upper()

    # ChargeOffDate and LastPaymentDate converted to datatype datetime[64]

    df['ChargeOffDate'] = pd.to_datetime(df['ChargeOffDate'])
    df['LastPaymentDate'] = pd.to_datetime(df['LastPaymentDate'])

    # Filling NA values with 0

    df.fillna(0, inplace=True)

    return df


##########################################################################################
##                                                                                      ##
##        This function reads csv file for specific columns & returns a dataframe       ##
##                      with unifin IDs as index and column names.                      ##
##                                                                                      ##
##########################################################################################

def ReadCsvFile():

    df = pd.read_csv(fd.curr_dir + fd.csvFile, usecols=colNames, dtype=dataTypes)

    df.set_index('UnifinID', inplace=True)  # Column UnifinID is set to index

    print(section1)
    print(f'Rows in csv file: {len(df.index)}'.center(60))

    # Slicing DebtDescription, OriginalCreditor because first 5
    # characters are to be compared only

    df['DebtDescription'] = df['DebtDescription'].str.replace('"', '')
    df['OriginalCreditor'] = df['OriginalCreditor'].str.replace('"', '')

    df['DebtDescription'] = df['DebtDescription'].str.slice(stop=10)
    df['OriginalCreditor'] = df['OriginalCreditor'].str.slice(stop=10)

    # Both columns are converted to uppercase

    df['DebtDescription'] = df['DebtDescription'].str.upper()
    df['OriginalCreditor'] = df['OriginalCreditor'].str.upper()

    # ChargeOffDate and LastPaymentDate converted to datatype datetime[64]

    df['ChargeOffDate'] = pd.to_datetime(df['ChargeOffDate'])
    df['LastPaymentDate'] = pd.to_datetime(df['LastPaymentDate'])

    # Filling NA values with 0

    df.fillna(0, inplace=True)

    return df


##########################################################################################
##                                                                                      ##
##         This function compares indexes (UnifinIDs) of both auto and csv Files        ##
##                    and returns a list of accounts that are unique                    ##
##                                                                                      ##
##########################################################################################

def GetUniqueAccounts():

    auto = ReadAutoFile()  
    csv = ReadCsvFile()

    # Lists of all UnifinIDs in file

    autoUnifinIDList = auto.index.tolist() 
    csvUnifinIDList = csv.index.tolist()

    # Sets of all UnifinIDs in file

    autoIDset = set(autoUnifinIDList)
    csvIDset = set(csvUnifinIDList)

    # Sets of unique IDs

    autoIDsUnique = autoIDset.difference(csvIDset)
    csvIDsUnique = csvIDset.difference(autoIDset)

    # Lists of unique IDs

    autoUniqueList = list(autoIDsUnique)
    csvUniqueList = list(csvIDsUnique)

    if autoIDsUnique:

        print(section1)
        print(f'There are unique accounts in auto file: {len(autoIDsUnique)}'.center(60))
        inp = input('\nDo you want to print these IDs (Y/N): ')

        while True:

            if inp == 'Y':

                for autoID in autoIDsUnique: print(autoID)
                break

            elif inp == 'N': break

            else: print('\nInvalid Input.\n')

    # If there are any unique ids in csv file
    # they are added to csvUniqueList

    if csvIDsUnique:

        print(section1)
        print(f'There are unique accounts in csv file: {len(csvIDsUnique)}'.center(60))
        inp = input('\nDo you want to print these IDs (Y/N): ')

        while True:

            if inp == 'Y':

                for csvID in csvIDsUnique: print(csvID)
                break

            elif inp == 'N': break

            else: print('\nInvalid Input.\n')

    # If there are any elements in autoUniqueList/csvUniqueList
    # they are dropped from auto/csv dataframe because  there is
    # no need to compare them, they already are a mismatch

    if autoUniqueList:
        auto = auto.drop(autoUniqueList)

    if csvUniqueList:
        csv = csv.drop(csvUniqueList)

    # returns dataframes of auto and csv file
    # that will further be used for comparison

    return auto, csv


##########################################################################################
##                                                                                      ##
##             This function compares csv and auto dataframes and returns a             ##
##             list of mismatch accounts or an empty list if files are same             ##
##                                                                                      ##
##########################################################################################

def GetMismatchAccounts():

    # Gets dataframe of auto and csv file

    dfAuto, dfCsv = GetUniqueAccounts()

    # Sorts both dataframe according to index
    
    dfAuto.sort_index(inplace=True)
    dfCsv.sort_index(inplace=True)

    # Comparison dataframe

    comparison = dfCsv == dfAuto

    dfCompare = comparison.add_suffix('_Match')

    auto = dfAuto.add_suffix('_auto')

    csv = dfCsv.add_suffix('_csv')

    # merges both our dataframes csv and auto (side by side)
    # based on index which is unifinID. This merged dataframe
    # has 2 times the columns in auto or csv dataframe

    merged = pd.concat([csv, auto, dfCompare], axis=1)

    # Creates a list of Column names for merged file

    mergedCols = []

    for x in dfNames:

        mergedCols.append(x + '_csv')
        mergedCols.append(x + '_auto')
        mergedCols.append(x + '_Match')
    
    # Reorders columns
    
    merged = merged[mergedCols]

    # Saves merged file as csv

    merged.to_csv(fd.curr_dir + 'merged.csv')

    # Gets Mismatch Accounts' Unifin IDs

    mismatchAccounts = []

    for index, row in dfCompare.iterrows():

        if not row.all(): mismatchAccounts.append(index)

    return mismatchAccounts, merged, comparison


##########################################################################################
##                                                                                      ##
##             This function creates a dictionary with Columns names having             ##
##                mismatches as keys and number of mismatches as values.                ##
##                                                                                      ##
##########################################################################################

def MismatchInColumns(compare):

    # Dictionary for columns mismatch

    colMismatch = {}

    # Columns that have mismatch

    for x in dfNames:

        isMatch = compare[x].all()

        if isMatch: continue
        
        else:

            # Gets count of Mismatches in columns

            counts = compare[x].value_counts()
            
            colMismatch[x] = counts[False]
    
    print(section1)
    print('Mismatch in columns: '.center(60) + '\n')

    # Prints mismatch in columns

    for col, count in colMismatch.items():

        print(f'{col}: {count}'.center(60))
    
    return colMismatch


##########################################################################################
##                                                                                      ##
##                  This function gives further details on Mismatches.                  ##
##                                                                                      ##
##########################################################################################

def MismatchDetails(merged, mismatchCols, mismatchList):

    # Gets names of required columns

    cols = list(mismatchCols.keys())

    # Gets only required columns in merged dataframe

    allCols = []
    codeCols = ['ClientCode_csv', 'ClientCode_auto', 'ClientCode_Match']

    for x in cols:

        allCols.append(x + '_csv')
        allCols.append(x + '_auto')
        allCols.append(x + '_Match')

    # Gets only required Columns
    
    if 'ClientCode' in mismatchCols: dfmerge = merged[allCols]
    else: dfmerge = merged[allCols + codeCols]

    # Gets only required rows

    dfmismatch = dfmerge[dfmerge.index.isin(mismatchList)]

    # Saves Mismatch file as csv

    dfmismatch.to_csv(fd.curr_dir + 'mismatches.csv')

    # Assigning ClientCodes to accounts

    def CC(row):

        csvcode = row['ClientCode_csv']
        autocode = row['ClientCode_auto']

        if row['ClientCode_Match']: return csvcode
        else: return csvcode + '|' + autocode
    
    def info(row):

        columns = ''

        for col in mismatchCols:

            if not row[col + '_Match']: 
                
                if columns == '': columns = columns + col
                else: columns = columns + '|' + col
        
        return columns

    dfmismatch.insert(0, 'ClientCode', dfmismatch.apply(CC, axis=1))
    dfmismatch.insert(1, 'Columns', dfmismatch.apply(info, axis=1))

    # Creates a dictionary for compact summary having 
    # mismatch cols and ClientCodes as keys & values.

    x = dfmismatch['Columns'].unique().tolist()

    mismatchSummary = {key: [] for key in x}

    for index, row in dfmismatch.iterrows():

        if not row['ClientCode'] in mismatchSummary[row['Columns']]:

            mismatchSummary[row['Columns']].append(row['ClientCode'])

    # Prints out summary of mismatches

    print(section1)

    for col, code in mismatchSummary.items():

        print(f'Mismatch Column(s): {col}\n')

        for i in range(0, len(code), 3):

            forPrint = ', '.join(code[i:i+3])
            print(forPrint.center(60))
        
        print('\n')


##########################################################################################
##                                                                                      ##
##                This function creates a text file of Mismatch Accounts                ##
##                                                                                      ##
##########################################################################################

# def CreateTextFile(mismatches):

#     text = ''
#     for i in range(2):

#         if i == 1:

#             text = text + '\n' + '-------------' + '\n' + '\n'
#             for unifinID in mismatches:
#                 text = text + str(unifinID) + '\n'
#         else:

#             for unifinID in mismatches:
#                 text = text + "'00" + str(unifinID) + "'," + '\n'

#     textFile = 'Mismatch_Accounts.txt'

#     with open(textFile, 'w') as file:

#         file.write(text)

#     print(section1)
#     print('Text File of Mismatch Accounts is created successfully.'.center(60))



# # Copies text file and upload it to EDI

# def MoveTextFile(textFile, fileDetails):

#     while True:

#         inp = input('\n' + 'Press (Y) if the Letters Folder is created on EDI (Y): ')

#         if inp == 'Y' or inp == 'y':

#             EDI_dir = fileDetails[3][0]
#             EDITextFile = EDI_dir + textFile

#             fd.curr_dir = fileDetails[3][1]
#             cTextFile = fd.curr_dir + textFile

#             shutil.copy(cTextFile, EDITextFile)

#             print('\n' + 'Text File is uploaded to EDI.')
#             break

#         else:

#             print('\n' + 'Text File is pasted in local only (not on EDI)')
#             break



