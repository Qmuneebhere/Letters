import os
import FileDetails as fd

##########################################################################################
##                                                                                      ##
##        This function takes the name of rejected/mismatch accounts file and           ##
##                and returns the list of unapproved/mismatch accounts.                 ##
##                                                                                      ##
##########################################################################################


def RemovedAccounts(name):

    # List for rejected/mismatch accounts accounts

    deleteList = []

    # Open the file in read mode and read lines into a list

    os.chdir(fd.curr_dir)

    with open(name, 'r') as file: 

        lines = file.readlines()

    for line in lines:

        dels = line.rstrip()
        deleteList.append(dels)
    
    return deleteList
 

##########################################################################################
##                                                                                      ##
##              This function takes the dataframe and return new dataframe              ##
##                   after removing unapproved/mismatch accounts.                       ##
##                                                                                      ##
##########################################################################################


def NewData(df, fileName, approval):

    if approval == 'Y': return df

    else:

        deleteList = RemovedAccounts(fileName)

        # Removes all rejected/mismatch accounts from dataframe
        
        newdf = df[~df['UnifinID'].isin(deleteList)]

        # Returns new dataframe

        return newdf