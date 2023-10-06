import os
import time
import pandas as pd
from pandas.errors import ParserError
import SifValues as sif
import LetterQA as qa


section1 = '\n\n' + '***********************************************************' + '\n\n'


##########################################################################################
##                                                                                      ##
##       This function takes whole dataframe and set values of following columns:       ## 
##                                                                                      ##
##        SettlementDueDate, Filler15, Filler16, ReceiptNumber, TransactionDate,        ##
##                  TransactionAmount, TransactionAcceptedAs, Filler31                  ##
##                                                                                      ##
##########################################################################################


def EightColumns(df):

    # These 6 columns are checks for our data each of them
    # have either value 0 or 1, default value being 0

    cols = ['SettlementDueDate', 'ReceiptNumber', 'TransactionDate',
            'TransactionAmount', 'TransactionAcceptedAs', 'Filler31']

    # Above 6 columns are assigned default value 0

    df[cols] = 0

    # ----------------------------SettlementDueDate--------------------------------- #

    # Checks if AmountDue is equal to ItemizationCurrBalance and
    # filler30 is equal to 1, if yes 1 value is assigned to SettlementDueDate

    df.loc[(abs(df['AmountDue'] - df['ItemizationCurrBalance']) <= 0.01) &
           (df['Filler30'] == 1), 'SettlementDueDate'] = 1

    # Checks if sum of 4 mentioned Columns - RecievedTotal is equal to AmountDue,
    # and COAmountDue > 0 If yes, 1 value is assigned to SettlementDueDate

    col1 = 'PrincipleBalance'
    col2 = 'InterestBalance'
    col3 = 'CostBalance'
    col4 = 'FeeBalance'

    df.loc[(abs((df[col1] + df[col2] + df[col3] + df[col4] - df['RecievedTotal']) - df['AmountDue']) < 0.01)
           & (df['COAmountDue'] > 0), 'SettlementDueDate'] = 1

    # --------------------------filler15 & filler16------------------------------- #

    # Getting values of column Filler15

    df['Filler15'] = df['1PayOffer'] - df['HospitalAddress']

    # rounding off to two decimal places only

    df['Filler15'] = df['Filler15'].round(2)

    # For EFF clients filler16 is the difference of AmountDue/3 - 3PayOffer

    df.loc[df['Filler12'].str[:3] == 'EFF', 'Filler16'] = df['AmountDue'] / 12 - df['3PayOffer']

    # For other clients Filler16 = 3PayOffer - HospitalPhone

    df['Filler16'] = df['3PayOffer'] - df['HospitalPhone']

    # rounding off to two decimal places only

    df['Filler16'] = df['Filler16'].round(2)

    # -----------------------------ReceiptNumber--------------------------------- #

    # If Column AmountDue is greater than 1PayOffer, ReceiptNumber = 1

    df.loc[df['AmountDue'] > df['1PayOffer'], 'ReceiptNumber'] = 1

    # ----------------------------TransactionDate--------------------------------- #

    # If Column 1PayOffer is greater than 3PayOffer, TransactionDate = 1

    df.loc[df['1PayOffer'] > df['3PayOffer'], 'TransactionDate'] = 1

    # ----------------------------TransactionAmount-------------------------------- #

    # If Column 1PayOffer is greater than 0, TransactionAmount = 1

    df.loc[df['1PayOffer'] > 0, 'TransactionAmount'] = 1

    # --------------------------TransactionAcceptedAs------------------------------ #

    # If product of Sum12PayOffer and 12 is lesser or equal
    # to AmountDue, TransactionAcceptedAs = 1

    df.loc[df['Sum12PayOffer'] * 12 - df['AmountDue'] <= 0.01, 'TransactionAcceptedAs'] = 1

    # --------------------------------Filler31------------------------------------- #

    # Assigns 1 to Filler31 for N021, N021S, E021 clients

    df.loc[df['LetterCode'].isin(['N021', 'N021S', 'E021']), 'Filler31'] = 1

    # Checks if difference of (ItemizationBalance + ItemizationInterest + ItemizationFees)
    # and absolute value of ItemizationPmtsCredits equals ItemizationCurrBalance, if yes
    # Assigns 1 to Filler31

    df.loc[df['ItemizationBalance'] + df['ItemizationInterest'] + df['ItemizationFees'] -
           abs(df['ItemizationPmtsCredits']) - df['ItemizationCurrBalance'] <= 0.01, 'Filler31'] = 1

    return df


##########################################################################################
##                                                                                      ##
##              LetteringMail: This function works on Lettering Maile file              ##
##                   and updates values in following 4 sif columns:                     ##
##                                                                                      ##
##              PatientName, Hospital Address, HospitalName, HospitalPhone              ##
##                                                                                      ##
##                                                                                      ##
##                      After which, Calls Function EightColumns:                       ##
##                                                                                      ##
##               EightColumns: This function works on following 8 columns:              ##
##                                                                                      ##
##         SettlementDueDate, Filler15, Filler16, ReceiptNumber, TransactionDate        ##
##                  TransactionAmount, TransactionAcceptedAs, Filler31                  ##
##                                                                                      ##
##             six of these columns (except Filler15, Filler16) have either             ##
##             value 1 or 0 in them. These 6 columns are set to 0 initially             ##
##              and if the specific condition for each column is satisfied              ##
##                              value 1 is assigned to them                             ##
##                                                                                      ##
##             Filler15: is the difference of 1PayOffer & HospitalAddress               ##
##              Filler16: is the difference of 3PayOffer & HospitalPhone                ##
##                  (For Eff, Filler16 = AmountDue / 12 - 3PayOffer)                    ##
##                                                                                      ##
##########################################################################################


def LetteringMail(mailFile, curr_dir, curr_date, prep):

    # Changes directory to current folder

    os.chdir(path=curr_dir)

    # A list of column names for Lettering Mail file

    colNames = ['LetterCode', 'LetterDate', 'UnifinID', 'ClientReferenceNumber',
                'OriginalAccountID', 'MailType', 'ClientAccountIDLabel', 'ClientCode',
                'DebtType', 'InitialNoticeFlag', 'SendGLBNoticeFlag', 'OOSFlag',
                'CRFlag', 'CRNegFlag', 'Sum3PayOffer', 'Sum12PayOffer', 'EmailAddress',
                'ConsumerName', 'Address1', 'Address2', 'City', 'State', 'Zip',
                'ExperianAddress', 'Filler8', 'Client Name', 'DebtDescription',
                'CurrentCreditor', 'OriginalCreditor', 'ServicerClientID',
                'Filler10', 'COAmountDue', 'ChargeOffDate', 'AmountPaidSinceCO',
                'LastPaymentAmount', 'LastPaymentDate', 'AmountDue', 'PrincipleBalance',
                'InterestBalance', 'CostBalance', 'FeeBalance', 'RecievedTotal', 'Filler11',
                'Filler12', 'PatientName', 'HospitalName', 'HospitalAddress', 'HospitalPhone',
                '1PayOffer', '3PayOffer', 'SettlementOffer', 'SettlementDueDate', 'Filler15', 'Filler16',
                'AVSCardholderName', 'AVSCardNumber', 'AVSStreet', 'ReceiptNumber',
                'TransactionDate', 'TransactionAmount', 'TransactionAcceptedAs',
                'TotalQuarterPaid', 'DocketNo', 'JudgementDate', 'JudgementCourt', 'CustomFlag1',
                'ItemizationType', 'ItemizationCreditorName', 'ItemizationDate', 'ItemizationBalance',
                'ItemizationInterest', 'ItemizationFees', 'ItemizationPmtsCredits', 'ItemizationCurrBalance',
                '40DaysLastLetter', 'Filler30', 'Filler31', 'DOFD', 'DateofAccident', 'AccidentInfo', 'County',
                'StateofAccident', 'CRDeletionFlag', 'Filler38', 'Filler39', 'Filler40', 'Account Information*',
                'Phone 1', 'Phone 2', 'CLT_CATEGORY', 'SSN', 'DBR_STATUS', 'CLT_NOTE_TO_COLL', 'CLT_SET_AUTH',
                'ADR_CITY', 'ADR_STATE', 'ADR_ZIP_CODE', 'DBR_PRIORITY', 'DBR_ASSIGN_DATE_O',
                'General_Offer_Last_Date', 'General_Offer', 'E_General_Offer', 'E_General_Offer_Last_Date',
                'Validation_Offer_Date', 'DBR_LANGUAGE', 'Expiration_Date', 'Last_Letter_Date',
                '1PayOffer_O', '3PayOffer_O', 'DBR_PRINCIPAL_DUE', 'UnitYield', 'Letter1',
                'Letter2', 'send_letter']

    dataTypes = {'LetterCode': 'object', 'LetterDate': 'object', 'UnifinID': 'object',
                 'ClientReferenceNumber': 'object', 'OriginalAccountID': 'object',
                 'MailType': 'object', 'ClientAccountIDLabel': 'object',
                 'ClientCode': 'object', 'DebtType': 'object',  # -------------- #
                 'InitialNoticeFlag': 'object', 'SendGLBNoticeFlag': 'object',
                 'OOSFlag': 'object', 'CRFlag': 'object', 'CRNegFlag': 'object',
                 'Sum3PayOffer': 'float64', 'Sum12PayOffer': 'float64',
                 'EmailAddress': 'object', 'ConsumerName': 'object',
                 'Address1': 'object', 'Address2': 'object',
                 'City': 'object', 'State': 'object', 'Zip': 'object',
                 'ExperianAddress': 'int64', 'Filler8': 'float64',  # -------------- #
                 'Client Name': 'object', 'DebtDescription': 'object',
                 'CurrentCreditor': 'object', 'OriginalCreditor': 'object',
                 'ServicerClientID': 'float64', 'Filler10': 'float64',  # -------------- #
                 'COAmountDue': 'float64', 'ChargeOffDate': 'object',
                 'AmountPaidSinceCO': 'float64', 'LastPaymentAmount': 'float64',
                 'LastPaymentDate': 'object', 'AmountDue': 'float64',
                 'PrincipleBalance': 'float64', 'InterestBalance': 'float64',
                 'CostBalance': 'float64', 'FeeBalance': 'float64',
                 'RecievedTotal': 'float64', 'Filler11': 'object',
                 'Filler12': 'object', 'PatientName': 'float64',
                 'HospitalName': 'float64', 'HospitalAddress': 'float64',
                 'HospitalPhone': 'float64', '1PayOffer': 'float64',
                 '3PayOffer': 'float64', 'SettlementOffer': 'float64',  # -------------- #
                 'SettlementDueDate': 'float64', 'Filler15': 'float64',
                 'Filler16': 'float64', 'AVSCardholderName': 'float64',
                 'AVSCardNumber': 'float64', 'AVSStreet': 'float64',
                 'ReceiptNumber': 'float64', 'TransactionDate': 'float64',
                 'TransactionAmount': 'float64', 'TransactionAcceptedAs': 'float64',
                 'TotalQuarterPaid': 'float64', 'DocketNo': 'object',
                 'JudgementDate': 'object', 'JudgementCourt': 'object',  # -------------- #
                 'CustomFlag1': 'float64', 'ItemizationType': 'object',
                 'ItemizationCreditorName': 'object', 'ItemizationDate': 'object',
                 'ItemizationBalance': 'float64', 'ItemizationInterest': 'float64',
                 'ItemizationFees': 'float64', 'ItemizationPmtsCredits': 'float64',
                 'ItemizationCurrBalance': 'float64', '40DaysLastLetter': 'object',
                 'Filler30': 'int64', 'Filler31': 'float64', 'DOFD': 'object',
                 'DateofAccident': 'float64', 'AccidentInfo': 'float64',  # -------------- #
                 'County': 'float64', 'StateofAccident': 'float64',  # -------------- #
                 'CRDeletionFlag': 'object', 'Filler38': 'float64',  # -------------- #
                 'Filler39': 'float64', 'Filler40': 'float64',  # -------------- #
                 'Account Information*': 'object', 'Phone 1': 'object',
                 'Phone 2': 'object', 'CLT_CATEGORY': 'object',
                 'SSN': 'object', 'DBR_STATUS': 'object',
                 'CLT_NOTE_TO_COLL': 'object', 'CLT_SET_AUTH': 'object',
                 'ADR_CITY': 'object', 'ADR_STATE': 'object',
                 'ADR_ZIP_CODE': 'object', 'DBR_PRIORITY': 'object',
                 'DBR_ASSIGN_DATE_O': 'object', 'General_Offer_Last_Date': 'object',
                 'General_Offer': 'object', 'E_General_Offer': 'object',
                 'E_General_Offer_Last_Date': 'object', 'Validation_Offer_Date': 'object',
                 'DBR_LANGUAGE': 'object', 'Expiration_Date': 'object',
                 'Last_Letter_Date': 'object', '1PayOffer_O': 'object',
                 '3PayOffer_O': 'object', 'DBR_PRINCIPAL_DUE': 'object',
                 'UnitYield': 'object', 'Letter1': 'object',
                 'Letter2': 'object', 'send_letter': 'object'}


    # ----------------------Reads Lettering Mail File------------------------ #


    # Both auto generated files and manual files can be read in the same way
    # If some error occurs for auto generated file, encoding used previously
    # was: encoding="ISO-8859-1"

    while True:

        try:

            if prep == 'N':
            
                df = pd.read_csv(mailFile, header=None, names=colNames,
                                 dtype=dataTypes, encoding="ISO-8859-1")
            
            elif prep == 'Y':

                df = pd.read_csv(mailFile, header=None, names=colNames,
                                 dtype=dataTypes)

        except ParserError as pe:

            print(section1)
            print('An error occured while parsing Lettering Mail File'.center(60))
            print('Check if there are only 114 fields, update file in'.center(60))
            print('current folder and press (Y).'.center(60))

            while True:

                inp = input('\n' + 'Proceed Further: ')

                if inp == 'Y': break
                else:

                    print('\n' + 'Invalid Input.')
        
        else:

            print(section1)
            print('Lettering Mail File parsed successfully.'.center(60))
            break

    
    # ------------------------Replaces Syn Character------------------------- #


    synChr = '\x16'
    synList = []

    for index, row in df.iterrows():

        row_string = ''.join(map(str, row.values))

        if synChr in row_string:

            synList.append(row['UnifinID'])

    if synList:

        df = df.replace('\x16', "'")


    ###################################################################
    ##                                                               ##
    ##   Splits data in groups based on criteria to get sif values   ##
    ##                                                               ##
    ##       1. Groups that get their sif values by unifinID         ##
    ##      2. Groups that get their sif values by ClientCode        ##
    ##                                                               ##
    ###################################################################


    print(section1)
    print('Fetching Sif Values & computing values of:'.center(60) + '\n')
    print('PatientName, Hospital Address'.center(60))
    print('HospitalName, HospitalPhone'.center(60))

    # Sets unifinID as index

    df.set_index('UnifinID', inplace=True)

    # Index Values of accounts that are cavalry

    cavalry = df[df['ClientCode'].str[:3] == 'CAV'].index

    # Cavalry Dataframe

    dfCAV = df.loc[cavalry]

    # Gets the rows and columns of Cavalry Dataframe

    cavRows = dfCAV.shape[0]

    # Dataframe other than cavalry

    dfOther = df[~df.index.isin(cavalry)]

    # Gets the rows and columns of Other Clients Dataframe

    otherRows = dfOther.shape[0]

    # Sets sif value for cavalry dataframe First argument passed
    # is unifinID set to True because sif values must be accessed
    # using Unifin IDs.

    if not cavRows == 0:

        # Creating a dictionary which contains unifinID as keys
        # & values are tuple containing LetterCode & ClientCode

        group = {}

        for index, row in dfCAV.iterrows():

            group[index] = (row['LetterCode'], row['ClientCode'])

        dfCAV = sif.SetSifValues1(True, group, dfCAV)

        updatedGroups = [dfCAV]
    
    else:

        updatedGroups = []


    ###################################################################
    ##                                                               ##
    ##       For Groups that get their sif value by ClientCode       ##
    ##    Splits data in groups based on LetterCode & ClientCode:    ##
    ##                 Join groups together after:                   ##
    ##                                                               ##
    ##             1. Assigning sif value to each group              ##
    ##                                                               ##
    ###################################################################


    # More on sif Columns --> SifValues.py

    if not otherRows == 0:

        for group, dfGroup in dfOther.groupby(['LetterCode', 'ClientCode']):

            dfGroup = sif.SetSifValues1(False, group, dfGroup)

            updatedGroups.append(dfGroup)

        df = pd.concat(updatedGroups)

    
    # --------------Calculate HospitalPhone and HospitalAddress--------------- #


    df = sif.SetSifValues2(df)


    # -------------------Assigning values to Eight Columns-------------------- #


    print(section1)
    print('Computing Values of Check Columns:'.center(60) + '\n')
    print('SettlementDueDate, Filler15, Filler16'.center(60))
    print('ReceiptNumber, TransactionDate, TransactionAmount'.center(60))
    print('TransactionAcceptedAs, Filler31'.center(60))

    df = EightColumns(df)


    # ------------Removing UnifinID as Index and setting up column------------ #


    # Creates a new dataframe with index reset

    df.reset_index(inplace=True)

    # Changes dataframe to its desired order

    df = df[colNames]


    # ------------------QA & Cleaning of Lettering Mail File------------------- #


    print(section1)
    print("Starting QA of Today's Letter File.".center(60))

    # Returns a dataframe after cleaning accounts.

    df = qa.FullQA(df, curr_date)
    
    return df

    
