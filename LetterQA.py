import time
import numpy as np
from datetime import datetime, timedelta


section1 = '\n\n' + '***********************************************************' + '\n\n'
section2 = '\n' + '-----------------------------------------------------------' + '\n'


##########################################################################################
##                                                                                      ##
##               Takes Dataframe and column name. Checks if dates matches               ##
##                 our date pattern mm/dd/yyyy. Returns boolean values.                 ##
##                                                                                      ##
##########################################################################################


def DatesPattern(df, columnName, DOFD):

    # regex pattern for date

    if DOFD:

        # mm/dd/yyyy or yyyymmdd

        date_pattern = '^\d{2}\/\d{2}\/\d{4}$|^\d{8}$'

    else:

        # mm/dd/yyyy

        date_pattern = '^\d{2}\/\d{2}\/\d{4}$'

    # Creates a df of rows having column value blank or np.nan

    condition1 = (df[columnName] == '')
    condition2 = (df[columnName].isnull())

    dfBlank = df[condition1 | condition2]

    # Gets a True value if there are no blanks in Column

    blankValues = dfBlank.empty

    # Executes If there are some blanks in Column

    if not blankValues:

        # Gets non blank values in Column

        condition1 = (df[columnName] != '')
        condition2 = (df[columnName].notnull())

        nonBlankValues = df[condition1 & condition2][columnName]

        isColumnValid = nonBlankValues.str.match(date_pattern).all()

    else:

        # Checks date pattern on whole column

        isColumnValid = df[columnName].str.match(date_pattern).all()

    # Returns True and True if there are no blanks
    # and all dates matches our pattern.

    return blankValues, isColumnValid


##########################################################################################
##                                                                                      ##
##             Reports only that there is a blank/0/-ve in specific column.             ##
##                                                                                      ##
##########################################################################################


def CheckNumeric(df, columnName, numType):

    # Checks number of blanks in Columns

    blankInColumn = len(df[df[columnName].isnull()])

    if blankInColumn > 0:

        print(section1)

        print('There are blanks/NULL in ' + columnName)

        print('\n' + 'Count: ' + str(blankInColumn))

        time.sleep(2)

    # Prints if there are 0 or -ve in Columns

    if numType == 1:

        zeroInColumn = len(df[df[columnName] <= 0.001])

        if zeroInColumn > 0:

            print(section1)

            print('There are zeros or negative in ' + columnName)

            print('\n' + 'Count: ' + str(zeroInColumn))

            time.sleep(2)


##########################################################################################
##                                                                                      ##
##                 Checks if the column contains only a single value: 1                 ##
##                                                                                      ##
##########################################################################################


def OneInColumn(df, columnName):

    notOneInColumn = len(df[df[columnName] != 1])

    if notOneInColumn > 0:

        print(section1)

        print('There are values other than 1 in ' + columnName)

        print('\n' + 'Count: ' + str(notOneInColumn))

        time.sleep(2)


##########################################################################################
##                                                                                      ##
##              Takes a dataframe and columnName, returns a new dataframe.              ##
##               after removing rows having null or blanks values in the                ##
##               ColumnName provided. Also returns deleted rows count.                  ##
##                                                                                      ##
##########################################################################################


def Text(df, columnName):

    blankNum = len(df[df[columnName].isnull()])

    if blankNum > 0:

        df = df[df[columnName].notnull()]

    return df, blankNum


##########################################################################################
##                                                                                      ##
##                   Takes whole data and returns updated data after                    ##
##                              removing invalid instances.                             ##
##                                                                                      ##
##########################################################################################


def FullQA(df, curr_date):

    # Gets total Number of Accounts in dataframe

    totalAcc = len(df)


    # --------------------------------UnifinID----------------------------- #


    # Checks if there are any blanks in UnifinID

    blankID = len(df[df['UnifinID'].isnull()])

    if blankID > 0:

        print('There are blank(s) in UnifinID.')

        time.sleep(2)

    # Checks if all elements in UnifinID are unique

    if not df['UnifinID'].is_unique:

        print('\n' + "There are duplicates in UnifinID.")

        time.sleep(2)

        # Checks if all UnifinID's are of 10 digits

        ID_have_10_digits = all((val.isdigit() and len(val) == 10) for val in df['UnifinID'])

        # ID_have_10_digits will be True if all ID's are 10 digits

        if not ID_have_10_digits:

            print('\n' + "Not All UnifinID's are of 10 digits or valid length.")

            time.sleep(2)


    # -------------------------------LetterCodes---------------------------- #


    print(section1)

    while True:

        inp = input("Wanna see the LetterCodes in today's file (Y/N): ")

        if inp == 'Y' or inp == 'N': break
        else: print('\n' + 'Invalid input.')

    if inp == 'Y':

        print('\n' + "LetterCodes in Today's File: " + '\n')

        uniqueCodes = df['LetterCode'].unique()

        for codes in uniqueCodes:

            print(codes.center(60))


    # -------------------------------ClientCodes---------------------------- #


    print(section1)

    while True:

        uniqueClients = df['ClientCode'].unique()

        inp = input("Wanna see the ClientCodes in today's file (Y/N): ")

        if inp == 'Y' or inp == 'N': break
        else: print('\n' + 'Invalid input.')

    if inp == 'Y':

        print('\n' + "ClientCodes in Today's File: " + '\n')

        # Gets a list of unique ClientCodes in today's file
        # Prints List with 5 codes in each line

        for i in range(0, len(uniqueClients), 5):

            forPrint = ', '.join(uniqueClients[i:i+5])
            print(forPrint.center(60))

        print('\n' + ("Total Client Codes: " + str(len(uniqueClients))).center(60))
    

    # -----------------------------------QA-------------------------------- #


    while True:

        print(section1)

        inp = input('Continue with QA? (Y for yes, N to terminate): ')

        if inp == 'Y': break
        elif inp == 'N': return df
        else: print('\n' + 'Invalid Input.')

    # Creates a date object from curr_date

    today = datetime.strptime(curr_date, '%m/%d/%Y').date()

    # Gets the date after 40 days

    forty = today + timedelta(days=40)

    # Converts it into a string

    fortyDate = forty.strftime('%m/%d/%Y')


    # -----------------------------LetterDate---------------------------- #


    # Checks if whole column has Only 1 value

    isDateValid = (df['LetterDate'] == curr_date).all()

    if not isDateValid:

        print(section1)

        print('Column LetterDate is invalid. '.center(60))

        time.sleep(2)


    # -------------------------40DaysLastLetter------------------------- #


    # Checks if whole column has Only 1 value

    isDateValid = (df['40DaysLastLetter'] == fortyDate).all()

    if not isDateValid:

        print(section1)

        print('Column 40DaysLastLetter is invalid. '.center(60))

        time.sleep(2)


    # ----------------------------MailType---------------------------- #


    # Checks if whole Column contains M only

    isMailValid = (df['MailType'] == 'M').all()

    if not isMailValid:

        print(section1)

        print('Column MailType is invalid.'.center(60))

        time.sleep(2)


    # -----------------------------Flags----------------------------- #


    # Checks if flags are only 'Y' or 'N' (or blanks in case of CRNegFlag)

    areFlagsValid = (df['OOSFlag'].isin(['Y', 'N'])).all() and \
                    (df['CRFlag'].isin(['Y', 'N'])).all() and \
                    (df['CRNegFlag'].isin(['Y', 'N', np.NAN])).all()

    if not areFlagsValid:

        print(section1)

        print('Flags are invalid. '.center(60))

        time.sleep(2)


    # -----------------------------Filler11----------------------------- #


    # Filler11 should be N002, N021 only

    isFiller11valid = df['Filler11'].isin(['N002', 'N021']).all()

    if not isFiller11valid:

        print(section1)

        print('Filler11 has values other than N002, N021.'.center(60))

        time.sleep(2)


    # -----------------------------Filler12----------------------------- #


    # Filler12 should be from ClientCodes only

    isFiller12valid = df['Filler12'].isin(uniqueClients).all()

    if not isFiller12valid:

        print(section1)

        print('Filler12 has Codes that are not in Client Codes.'.center(60))

        time.sleep(2)


    # -------------------------ChargeOffDate--------------------------- #


    blankChargeOff, isChargeOffValid = DatesPattern(df, 'ChargeOffDate', False)

    if not isChargeOffValid:

        print(section1)

        print('ChargeOffDate Column is invalid.'.center(60))

        time.sleep(2)


    # ------------------------LastPaymentDate-------------------------- #


    blankPayment, isPaymentValid = DatesPattern(df, 'LastPaymentDate', False)

    if not isPaymentValid:

        print(section1)

        print('LastPaymentDate Column is invalid.'.center(60))

        time.sleep(2)


    # ------------------------ItemizationDate-------------------------- #


    blankItemization, isItemizationValid = DatesPattern(df, 'ItemizationDate', False)

    if not isItemizationValid:

        print(section1)

        print('ItemizationDate Column is invalid.'.center(60))

        time.sleep(2)


    # -----------------------------DOFD------------------------------ #


    # strips all strings from whitespaces

    df['DOFD'] = df['DOFD'].str.strip()
    
    # Checks DOFD column

    blankDOFD, isDOFDValid = DatesPattern(df, 'DOFD', True)

    if not isDOFDValid:

        print(section1)

        print('DOFD Column is invalid.'.center(60))

        time.sleep(2)

    ##########################################################
    ##                                                      ##
    ##                    Text Columns                      ##
    ##            To be checked for NULLS/Blanks            ##
    ##                                                      ##
    ##       ClientReferenceNumber, OriginalAccountID       ##
    ##   ClientAccountIDLabel, ConsumerName, Client Name    ##
    ##  DebtDescription, CurrentCreditor, OriginalCreditor  ##
    ##        ItemizationType, ItemizationCreditorName      ##
    ##                                                      ##
    ##########################################################


    # ------------------------DebtDescription------------------------- #


    # Number of blanks in DebtDescription

    blanksDebt = len(df[df['DebtDescription'].isnull()])

    df.loc[df['DebtDescription'].isnull(), 'DebtDescription'] = df['OriginalCreditor']



    # -------------------------COAmountDue-------------------------- #


    delData = {}

    zeroInCOAmount = len(df[df['COAmountDue'] <= 0.001])

    if zeroInCOAmount > 0:

        df = df[df['COAmountDue'] >= 0.001]

        time.sleep(2)

    delData['COAmountDue'] = zeroInCOAmount


    # -----------------------SettlementDueDate------------------------ #


    zeroInSettlement = len(df[df['SettlementDueDate'] == 0])

    if zeroInSettlement > 0:

        df = df[df['SettlementDueDate'] == 1]

        time.sleep(2)

    delData['SettlementDueDate'] = zeroInSettlement


    #########################################################
    ##                                                     ##
    ##    Checks Numeric columns for zeroes or negative    ##
    ##     Prints results if there are some 0 or -ve       ##
    ##                                                     ##
    #########################################################


    # -----------------------Numeric Columns------------------------ #


    positiveNumList = ['Sum3PayOffer', 'Sum12PayOffer', 'COAmountDue',
                       '1PayOffer', '3PayOffer', 'ItemizationBalance']

    for col in positiveNumList:

        CheckNumeric(df, col, 1)

    numList = ['AmountPaidSinceCO', 'LastPaymentAmount', 'AmountDue', 'PrincipleBalance',
               'InterestBalance', 'CostBalance', 'FeeBalance', 'RecievedTotal',
               'ItemizationInterest',  'ItemizationFees', 'ItemizationPmtsCredits',
               'ItemizationCurrBalance']

    for col in numList:

        CheckNumeric(df, col, 0)


    # ----------------------ExperianAddress----------------------- #


    # Checks if any Experian Address is not 0 or 1

    validExperian = len(df[df['ExperianAddress'].isin([0, 1])])

    if validExperian != len(df):

        print(section1)

        print('Invalid Experian Address.'.center(60))

        time.sleep(2)


    # -------------------------Filler30-------------------------- #


    # Checks if whole column is equal to 1

    isFiller30valid = (df['Filler30'] == 1).all()

    if not isFiller30valid:

        print(section1)

        print('There are some values other than 1 in Filler30.'.center(60))


    # ---------------------TotalQuarterPaid---------------------- #


    # Checks if whole column equals 0.00

    isZero = np.isclose(df['TotalQuarterPaid'], 0.0).all()

    if not isZero:

        print(section1)

        print('TotalQuarterPaid is invalid.'.center(60))


    # ---------------------1's Columns---------------------- #


    oneList = ['ReceiptNumber', 'TransactionDate',
               'TransactionAmount', 'TransactionAcceptedAs', 'Filler31']

    for col in oneList:

        OneInColumn(df, col)
    

    # -------------------------Remove Blanks------------------------- #


    # List of Text Columns that are to
    # be checked for Nulls and Blanks.

    textCols = ['ClientReferenceNumber', 'OriginalAccountID', 'ClientAccountIDLabel',
                'ConsumerName', 'DebtDescription', 'CurrentCreditor',
                'OriginalCreditor', 'ItemizationType', 'ItemizationCreditorName']

    # List of Date Columns that are to
    # be checked for Nulls and Blanks.

    dateCols = ['ChargeOffDate', 'ItemizationDate']

    for column in textCols:

        df, delCount = Text(df, column)

        delData[column] = delCount
    
    for column in dateCols:

        df, delCount = Text(df, column)

        delData[column] = delCount


    # -------------------Prints Summary--------------------- #


    deletedAcc = sum(delData.values())

    # Printing count of Deleted rows with corresponding columns name.

    if deletedAcc > 0:

        print(section1)

        print('ACCOUNTS REMOVED: '.center(60))

        for col, count in delData.items():

            if count > 0:

                print('\n' + ('Accounts deleted due to ' + col + ': ' + str(count)).center(60))

                time.sleep(1)

    print(section1)

    print(('QA COMPLETED.'.center(60)) + '\n')
    print(('Total Accounts: ' + str(totalAcc)).center(60) + '\n')
    print(('Accounts Removed: ' + str(deletedAcc)).center(60) + '\n')
    print(('Remaining Accounts: ' + str(len(df))).center(60))

    return df
