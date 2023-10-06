import os
import pandas as pd
from sqlalchemy import create_engine
import FileDetails as fd


section1 = '\n\n' + '***********************************************************' + '\n\n'
section2 = '\n' + '-----------------------------------------------------------' + '\n'


##########################################################################################
##                                                                                      ##
##             This function takes the list of unifin addresses and queries             ##
##                                SQL for TLO file data.                                ##
##                                                                                      ##
##########################################################################################


def TLOData(ADRList, cobor):

    # For cobor Join is applied to different table

    if cobor == 'Y':

        join = "INNER JOIN CDS.ADR as ADR WITH (NOLOCK) \
                on ADR.ADR_DBR_NO = DBR.DBR_NO AND ADR.ADR_SEQ_NO = '02'"
    
    else:

        join = "INNER JOIN UFN.[01.ADR] ADR on ADR_DBR_NO = DBR_NO"

    # Converts the list of addresses given 
    # into a string to attach in SQL query

    ADRString = ','.join(ADRList)

    # Creates an engine to connect with MSSQL

    config = "mssql+pyodbc://read_only:Neustar01@unifin-sql/tiger?driver=ODBC+Driver+17+for+SQL+Server"

    engine = create_engine(config)

    queryTLO = "SELECT DBR_NO AS 'ACCOUNT ID', \
                IIF(CHARINDEX(',',REVERSE(ADR.ADR_NAME)) > 0, \
                RIGHT(ADR.ADR_NAME,CHARINDEX(',',REVERSE(ADR.ADR_NAME))-1), '') AS \
                'FIRST NAME', '' AS 'MIDDLE NAME', \
		        IIF(CHARINDEX(',',ADR.ADR_NAME) > 0, \
                LEFT(ADR.ADR_NAME,CHARINDEX(',',ADR.ADR_NAME) - 1), \
                ADR.ADR_NAME) AS 'LAST NAME', \
                IIF(LEN(ADR_ADDR1) > 1, ADR_ADDR1, '') AS 'ADDRESS LINE 1', \
                IIF(LEN(ADR_ADDR2) > 1, ADR_ADDR2, '') AS 'ADDRESS LINE 2', \
                ADR_CITY AS 'CITY', ADR_STATE AS 'STATE', ADR_ZIP_CODE AS 'ZIP', \
                IIF(ADR_DOB_O IS NOT NULL,Convert(varchar,ADR_DOB_O,101),'') AS 'DOB', \
                ADR_TAX_ID AS 'SSN' FROM CDS.DBR " + join + " INNER JOIN \
                CDS.CLT on CLT_NO = DBR_CLIENT \
                WHERE dbr_no IN (" + ADRString +  ")"
    
    dfTLO = pd.read_sql(queryTLO, engine, dtype=str)

    return dfTLO


##########################################################################################
##                                                                                      ##
##             This function compares the consumer name in both TLO and raw             ##
##                     file and prints if consumer name doesnt match                    ##
##                                                                                      ##
##########################################################################################


def TLONameCheck(df_Raw, df_TLO):

    # Columns of df_TLO required for QA

    TLOcols = ['ACCOUNT ID', 'FIRST NAME', 'MIDDLE NAME', 'LAST NAME']

    # Concatenates 'FIRST NAME', 'MIDDLE NAME', 'LAST NAME'
    # and creates a new column named 'ConsumerName'

    df_TLO['ConsumerName'] = df_TLO['FIRST NAME'] + df_TLO['MIDDLE NAME'] + df_TLO['LAST NAME']

    # Renames 'ACCOUNT ID' column to 'UnifinID'

    df_TLO.rename(columns={'ACCOUNT ID': 'UnifinID'}, inplace=True)

    # Gets dataframe columns to be comapared

    df1 = df_TLO[['UnifinID', 'ConsumerName']]

    # Removes spaces within ConsumerName

    df1.loc[:, 'ConsumerName'] = df1['ConsumerName'].str.replace(' ', '')

    # Sets 'UnifinID' as index

    df1.set_index('UnifinID', inplace=True)

    # Sorts dataframe on index

    df1 = df1.sort_index()

    # Columns of df_Raw required for QA

    df2 = df_Raw[['UnifinID', 'ConsumerName']][df_Raw['ExperianAddress'] == 0]

    # Removes spaces within ConsumerName

    df2.loc[:, 'ConsumerName'] = df2['ConsumerName'].str.replace(' ', '')

    # Sets 'UnifinID' as index

    df2.set_index('UnifinID', inplace=True)

    # Sorts dataframe on index

    df2 = df2.sort_index()

    # Compares both dataframes 'ConsumerName'

    is_equal = (df1['ConsumerName'] == df2['ConsumerName'])

    if not is_equal.all():

        misCount = (is_equal[is_equal == False]).count()

        # Prints that mismatches are found in 'ConsumerName'

        toprint = f'Mismatch in ConsumerName for {misCount} Accounts'.center(60)

        print('\n' + toprint + '\n')

        # Gets List of UnifinIDs that have mismatching ConsumerNames

        misIDs = is_equal[is_equal == False].index.tolist()

        # Creates a dataframe with unifinIDs as index
        # and columns of raw and TLO 'ConsumerNames'

        misRaw = df1.loc[misIDs]
        misTLO = df2.loc[misIDs]

        merged = pd.merge(misRaw, misTLO, left_index=True, 
                          right_index=True, suffixes=('_TLO', '_raw'))

        print(section2)
        print(merged)
        print(section2)


##########################################################################################
##                                                                                      ##
##             This function takes approved dataframe & generates TLO file              ##
##                                                                                      ##
##########################################################################################


def PrepareTLO(df, cobor):

    print(section1)
    print('Preparing TLO File.'.center(60))

    # List for unifinIds having experian address 0

    TLOAddressList = []

    # column names as list

    cols = ['ACCOUNT ID', 'FIRST NAME', 'MIDDLE NAME', 'LAST NAME',
            'ADDRESS LINE 1', 'ADDRESS LINE 2', 'CITY', 'STATE', 
            'ZIP', 'DOB', 'SSN']

    # Creates an empty dataframe for TLO

    dfTLO = pd.DataFrame(columns=cols)

    # Series of unifinIDs that have Experian address 0

    x = df['UnifinID'][df['ExperianAddress'] == 0]

    # List of unifinIDs with inverted commas around them

    TLOAddressList = (x.apply(lambda id: f"'{id}'")).tolist()
    
    # TLO Addresses can be sent 20000 at a time
    # so if it exceeds 20000 it must be divided
    # into chunks. 
    
    if len(TLOAddressList) > 20000:

        chunks = (len(TLOAddressList) // 20000) + 1
    
        # Splitting list of addresses in chunks
    
        for i in range(chunks):

            # start of chunk

            strt = 20000 * i

            # end of chunk

            end = strt + 20000

            if i == chunks - 1:

                end = len(TLOAddressList)

            # Creates a list containing 20000 address only

            address = TLOAddressList[strt:end]

            # sends address chunks to TLOData

            tempdf = TLOData(address, cobor)

            # concatenates all chunks to create TLO dataframe

            dfTLO = pd.concat([dfTLO, tempdf], ignore_index=True)
    
    else: dfTLO = TLOData(TLOAddressList, cobor)

    # Saves TLO File in current directory

    dfTLO.to_csv(fd.curr_dir + fd.TLOFile, index=False)

    print('\n' + 'TLO FIle is generated.'.center(60))

    # Does QA of Cosumer Names picked from SQL with original data

    TLONameCheck(df, dfTLO)

    return dfTLO






