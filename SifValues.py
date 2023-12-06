import os
import math
import time
import pandas as pd
import FileDetails as fd
from sqlalchemy import create_engine


section1 = '\n\n' + '***********************************************************' + '\n\n'

#################################################################
##                                                             ##
##     ReadSif reads our Sif file and returns a dictionary     ##
##     with tuples (LetterCodes & ClientCodes) as keys and     ##
##                 their Sif Rules as values.                  ## 
##                                                             ##
#################################################################


def ReadSif():

    # Creates a dictionary which will store sif rule
    # for each group as value and group (tuple) as key

    sifDict = {}

    # Reads Sif File

    df = pd.read_csv(fd.SIF_Dir + 'Sif_Rules.csv')

    # Iterates over rows, creating 2 tuples for each one of them.
    # These tuples are groups based on Letter and Client Codes.

    for index, rows in df.iterrows():
        code = rows['ClientCodes']
        val1 = rows['CLT_SIF_Letter1']
        val2 = rows['CLT_SIF_Letter2']

        tuple1 = ('N002', code)
        tuple2 = ('N021', code)

        # Each group have their own Sif Rules. These tuples
        # and Sif Rules are added to dictionary as keys and values

        sifDict[tuple1] = val1
        sifDict[tuple2] = val2

    return sifDict


#################################################################
##                                                             ##
##     Takes a tuple (LetterCode, ClientCode) as input and     ##
##             and Returns sif value for the group.            ##
##                                                             ##
#################################################################


def SifRules(group):

    # ruleDict have group (tuple) as keys
    # Sif Rule of that group as value

    ruleDict = ReadSif()

    # It checks if the group is in our dictionary
    # if it exists it returns sif value of it

    if group in ruleDict:

        # Checks if the value for the specific group exists
        # if there is a blank it calls function UpdateSif

        if math.isnan(ruleDict[group]):

            print(section1)

            print(f'Sif was blank for: {group}'.center(60))

            return UpdateSif(group)

        else:

            return ruleDict[group]

    # Else it calls AddSif which adds new clientCode
    # to our Sif_Rule File and also returns its value

    else:

        print(section1)

        print(f'Client Code does not exist in file: {group[1]}'.center(60))

        return AddSif(group)


#################################################################
##                                                             ##
##     Takes a tuple (LetterCode, ClientCode) as input and     ##
##     adds new sif value against that clientcode. Returns     ##
##                   sif value for the group.                  ##
##                                                             ##
#################################################################


def AddSif(group):

    # First element of tuple is letter code, while
    # second element of tuple is client code.

    letterCode = group[0]
    clientCode = group[1]

    # Changes directory to our current and reads Sif File

    df = pd.read_csv(fd.SIF_Dir + 'Sif_Rules.csv')

    # Takes both sif values as input from user

    inp1 = float(input('\n' + 'Enter the Letter1 value for ' + clientCode + ': '))
    inp2 = float(input('\n' + 'Enter the Letter2 value for ' + clientCode + ': '))

    # creates a new row as dictionary

    add = 'Added on ' + fd.curr_date
    new_row = pd.DataFrame({'ClientCodes': [clientCode], 'CLT_SIF_Letter1': [inp1],
                            'CLT_SIF_Letter2': [inp2], 'Date1': [add], 'Date2': ['']})

    # Adds a new row to dataframe with new ClientCode
    # and its sif value and today's date

    df = pd.concat([df, new_row], ignore_index=True)

    # Updates our csv File

    df.to_csv(fd.SIF_Dir + 'Sif_Rules.csv', index=False)

    # returns sif Value

    if letterCode == 'N002':
        return inp1
    else:
        return inp2


#################################################################
##                                                             ##
##     Takes a tuple (LetterCode, ClientCode) as input and     ##
##     updates sif value of the group in sif File. Returns     ##
##                   sif value for the group.                  ##
##                                                             ##
#################################################################


def UpdateSif(group):

    # gets letter and client code from group

    letterCode = group[0]
    clientCode = group[1]

    # Changes directory to our current and reads Sif File

    df = pd.read_csv(fd.SIF_Dir + 'Sif_Rules.csv')

    # Gets the index location of ClientCode to be updated

    location = df.loc[df['ClientCodes'] == clientCode].index[0]

    # Takes both sif values as input from user

    inp1 = float(input('\n' + 'Enter the updated Letter1 value for ' + clientCode + ': '))
    inp2 = float(input('\n' + 'Enter the updated Letter2 value for ' + clientCode + ': '))

    # Updates the values in dataframe with new ones
    # Adds today's date in date2 column for the
    # documentation of when sif rule was updated

    df.loc[location, 'CLT_SIF_Letter1'] = inp1
    df.loc[location, 'CLT_SIF_Letter2'] = inp2
    df.loc[location, 'Date2'] = 'Updated on ' + fd.curr_date

    # Updates our csv File

    df.to_csv(fd.SIF_Dir + 'Sif_Rules.csv', index=False)

    # returns sif Value

    if letterCode == 'N002': return inp1
    else: return inp2


#################################################################
##                                                             ##
##    This function takes a string of unifin IDs and returns   ##
##    a dataframe containing two columns UnifinID & SifValue   ##
##                                                             ##
#################################################################


def SQL_SIF(unifinIDs, group):

    # Creates an engine to connect with MSSQL

    config = "mssql+pyodbc://read_only:Neustar01@unifin-sql/ \
    tiger?driver=ODBC+Driver+17+for+SQL+Server"

    engine = create_engine(config)

    querySIF = "SELECT UDW_DBR_NO AS UnifinID, UDW_FLD29 AS SIF FROM CDS.UDW \
                WHERE UDW_DBR_NO IN (" + unifinIDs + ") AND UDW_SEQ = '097'"

    dtypes = {'UnifinID': 'object', 'SIF': 'float'}
    
    dfSIF = pd.read_sql(querySIF, engine, dtype=dtypes)

    dfSIF.set_index('UnifinID', inplace=True)

    dfSIF['SIF'] = (dfSIF['SIF'] + 10) / 100

    # Conditions for filtering UnifinIDs for N002 & N021

    condition1 = lambda value: value[0] == 'N002' or value[0] == 'N002S'
    condition2 = lambda value: value[0] == 'N021' or value[0] == 'N021S'

    # Creates List of unifinIDs that are N002 category or N021

    N021 = [key for key, value in group.items() if condition2(value)]

    dfSIF.loc[N021] = dfSIF.loc[N021].apply(lambda x: x - 0.1)

    return dfSIF


#################################################################
##                                                             ##
##    Takes a group of data 'dfGroup' as input and returns a   ##
##          new group with sif values in PatientName.          ##
##                                                             ##
##     If 'unifinID' is true then 'group' is a dictionary      ##
##     with id and (LetterCode, CLientCode) = key - value      ##
##                                                             ##
##          If 'unifinID' is false, group is a tuple           ##
##                  (LetterCode, CLientCode)                   ##
##                                                             ##
##      Checks filler15 Column, if the sif value is to be      ##
##           updated sets new sif value. Also updates          ## 
##                   HospitalAddress Column.                   ##
##                                                             ##
#################################################################


def SetSifValues1(group, dfGroup):

    # If unifinID is false, group will be a tuple
    # Gets letter code and client code from group

    letterCode = group[0]
    ClientCode = group[1]        

    # Sets sif values for N001, N002, N002S, N021, N021S clients
    # and blanks for groups other than the mentioned above.

    if letterCode in ['N001', 'N002', 'N002S']:

        sifValue = SifRules(('N002', ClientCode))

    elif letterCode in ['N021', 'N021S']:

        sifValue = SifRules(('N021', ClientCode))

    else:

        # If there is no sif Value for the group
        # we don't need to check it, so returns group

        return dfGroup

    dfGroup['PatientName'] = sifValue

    # converts PatientName column to float64

    dfGroup['PatientName'] = pd.to_numeric(dfGroup['PatientName']).astype('float64')

    # Sets value of Column HospitalAddress

    dfGroup['HospitalAddress'] = dfGroup['AmountDue'] * dfGroup['PatientName']

    # Compares HospitalAddress and 1PayOffer (Same working as Filler15)

    difference = abs(dfGroup['HospitalAddress'] - dfGroup['1PayOffer']) <= 0.01

    # convert HospitalAddress column to four decimal places

    dfGroup['HospitalAddress'] = dfGroup['HospitalAddress'].apply(lambda x: round(x, 4))

    # Checks if sif Value is proper for this specific group

    if difference.all(): return dfGroup

    # if not, sif value needs to be updated

    else:

        print(section1)

        print(f'Filler15 not minimized, Enter sif Values for: {group}'.center(60))

        if letterCode in ['N001', 'N002', 'N002S']:

            sifValue = UpdateSif(('N002', ClientCode))

        elif letterCode in ['N021', 'N021S']:

            sifValue = UpdateSif(('N021', ClientCode))

        dfGroup['PatientName'] = sifValue

        # converts PatientName column to float64

        dfGroup['PatientName'] = pd.to_numeric(dfGroup['PatientName']).astype('float64')

        # convert PatientName column to four decimal places

        dfGroup['PatientName'] = dfGroup['PatientName'].apply(lambda x: round(x, 4))

        # Sets value of Column HospitalAddress

        dfGroup['HospitalAddress'] = dfGroup['AmountDue'] * dfGroup['PatientName']

        # convert HospitalAddress column to four decimal places

        dfGroup['HospitalAddress'] = dfGroup['HospitalAddress'].apply(lambda x: round(x, 4))

        return dfGroup


#################################################################
##                                                             ##
##    Takes a group of data as input and returns a new group   ##
##    with updated values in HospitalName and HospitalPhone.   ##
##                                                             ##
#################################################################


def SetSifValues2(df):

    # This is a custom function to calculate 'HospitalPhone' value

    def custom(row):

        if row['PatientName'] <= 0.7: x = 0.15
        
        else: x = 0.1

        result = row['AmountDue'] * (row['PatientName'] + x) / 3

        return result
    
    # Applying custom function on column 'HospitalPhone'

    df['HospitalPhone'] = df.apply(custom, axis=1)

    # convert HospitalPhone column to four decimal places

    df['HospitalPhone'] = df['HospitalPhone'].apply(lambda x: round(x, 4))

    # Updates HospitalName column

    df['HospitalName'] = df['HospitalPhone'] / df['AmountDue']

    # convert HospitalName column to four decimal places

    df['HospitalName'] = df['HospitalName'].apply(lambda x: round(x, 4))

    return df
