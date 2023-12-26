import shutil
import os
import math
import csv
import time
import numpy as np
import pandas as pd
import FileDetails as fd
import LetteringMailFile as lm
import PivotTable as pt
import Approval as a
import TLO as t


section1 = '\n\n' + '***********************************************************' + '\n\n'


# ----------------------------------Renames RegE File------------------------------------ #


if fd.suffix == 'b':

    print(section1)

    while True:

        print('Do you want to process RegE file?'.center(60) + '\n')

        rege = input('(Y/N): ')

        if rege == 'Y' or rege == 'N': break
        else: print('\nInvalid Input.\n')

    if fd.mapAdmin == 'Y' and rege == 'Y':

        if os.path.exists(fd.LM_Dir + fd.oldRegE):

            os.rename(fd.LM_Dir + fd.oldRegE, fd.LM_Dir + fd.newRegE)

            print(section1)

            print('RegE File has been renamed.'.center(60))


# ----------------------------------Gets today's date------------------------------------ #


curr_date = fd.currFolderName.replace('-', '/')


# ---------------------------------Creates folder in local------------------------------- #


if not os.path.exists(fd.curr_dir): os.makedirs(fd.curr_dir)


# -------------------------------Moves file to local folder------------------------------ #


# Checks if Lettering Mail file is in folder

LM_Path = fd.curr_dir + fd.mailFile

if os.path.exists(LM_Path):

    while True:

        print(section1)

        print("I see Lettering Mail file already in today's folder.".center(60))
        print("Want me to replace Mail file and templates? (Y/N)".center(60))

        inp = input('\n' + 'Replace Files: ')

        if inp == 'Y': 

            fd.MoveFiles()

            print(section1)
            print('Files are moved successfully.'.center(60))
            
            break

        elif inp == 'N': break

        else: print('\n' + 'Invalid Input.' + '\n')

else: 
    
    fd.MoveFiles()
    
    print(section1)
    print('Files are moved successfully.'.center(60))


###########################################################################################
##                                                                                       ##
##            Works on Lettering Mail file. Does cleaning and transformation             ##
##                 of data and returns data which is ready for approval.                 ##
##                                                                                       ##
###########################################################################################


df = lm.LetteringMail(fd.mailFile, fd.curr_dir, curr_date, fd.prepped)


# -------------------------Asks user for Creating Pivot Table File----------------------- #


if fd.suffix != 'b':

    print(section1)

    while True:

        pvt = input('Do you want to create Pivot table file? (Y/N): ')

        if pvt == 'Y' or pvt == 'N': break

        else: print('\n' + 'Invalid Input.' + '\n')


# --------------------------------Creates Pivot Table File------------------------------- #


if fd.suffix == 'b' or pvt == 'Y':

    print(section1)
    print('Preparing Pivot Table File'.center(60))

    pt.CreateXlsx(df, fd.currFolderName, fd.suffix, fd.curr_dir)

    print('\n' + 'Pivot Table file is ready.'.center(60))


# -------------------------Asks user if file is approved or not-------------------------- #


print(section1)

if fd.suffix == 'b':

    print("If Letter File is Approved Type 'Y' as input".center(60))
    print("If not, add rejected accounts in text file &".center(60))
    print("Type 'N' as input.".center(60) + '\n')

    deleteFile = fd.rejectFile

else:

    print("If there are no Mismatch Type 'Y' as input".center(60))
    print("If not, add mismatch accounts in text file".center(60))
    print("Type 'N' as input.".center(60) + '\n')

    deleteFile = fd.mismatchFile

while True:

    approval = input('All Accounts are valid? (Y/N): ')

    if approval == 'Y' or approval == 'N': break
    
    else: print('\n' + 'Invalid Input.' + '\n')


# ------------------------------Gets approved accounts only------------------------------ #


dfApproved = a.NewData(df, deleteFile, approval)

print(section1)

print(f'Approved Accounts: {dfApproved.shape[0]}'.center(60))


# --------------------------------Creates Import file Data------------------------------- #


# Saves data with approved accounts only

dfApproved.to_csv(fd.curr_dir + fd.importFile, index=False, header=False)

print(section1)

print('Import Data file is ready.'.center(60))


###########################################################################################
##                                                                                       ##
##            This function generates TLO file, Matches ConsumerName in both             ##
##            TLO and raw file, saves TLO file in current folder & returns a             ##
##                   series of UnifinIDs that have experian address 0.                   ##
##                                                                                       ##
###########################################################################################


expZero = t.PrepareTLO(dfApproved, fd.cobor)


# -----------------------Creates TLO folder administration drive------------------------- #


if fd.mapAdmin == 'Y': 
    
    if not os.path.exists(fd.currTLO_dir):

        os.makedirs(fd.currTLO_dir)


# ------------------------Moves TLO file to administration drive------------------------- #


if fd.mapAdmin == 'Y':

    while True:

        print(section1)

        inp = input('TLO Raw file ready to move? (Y): ')
        
        if inp == 'Y': 
            
            fd.MoveTLO()
            break
        
        else:

            print('\n' + 'Invalid Input.')

print(section1)

print('You can send TLO file on FTP'.center(60))


# -------------------Moves TLO Append file from administration drive--------------------- #


if fd.mapAdmin == 'Y':

    while True:

        print(section1)

        inp = input('TLO Append file ready to move? (Y): ')
        
        if inp == 'Y': 
            
            fd.MoveTLOAppend()
            break
        
        else:

            print('\n' + 'Invalid Input.')


# -------------------Replaces Addresses with verified Address in TLO--------------------- #


dfverifiedADR = t.ReplaceAddress(dfApproved, expZero)

# Saves Verified Address file in current directory

dfverifiedADR.to_csv(fd.curr_dir + fd.veriADRFile, index=False, header=False)

print(section1)

print('Verified Address file is ready.'.center(60))


# ----------------------------Creates Today's folder in EDI------------------------------ #


if fd.mapEDI == 'Y': 
    
    if not os.path.exists(fd.currEDI_dir):

        os.makedirs(fd.currEDI_dir)


# ------------------------------Moves File to EDI for QA--------------------------------- #


if fd.mapEDI == 'Y':

    while True:

        print(section1)

        inp = input('Are files ready for QA (Y): ')

        if inp == 'Y': break
        
        else: print('\n' + 'Get files ready ASAP.')

    fd.MoveFilesEDI(1, fd.suffix)


# -------------------------------Moves csv File for job---------------------------------- #


if fd.mapAdmin == 'Y':

    while True:

        print(section1)

        inp = input('Is csv File ready for job? (Y): ')

        if inp == 'Y': break
    
        else: print('\n' + 'Get csv file ready ASAP.')

    fd.CopyCsvForJob()

    print(section1)

    print('Csv File has been moved for Job.'.center(60))


# ------------------------Moves Auto File to EDI for comparison-------------------------- #


if fd.mapEDI == 'Y':

    while True:

        print(section1)

        inp = input('Is Auto File ready (Y): ')

        if inp == 'Y': break
        
        else: print('\n' + 'Get Auto File ready ASAP.')

    fd.MoveFilesEDI(2, fd.suffix)


# ------------------------------Moves final Files to EDI--------------------------------- #


if fd.mapEDI == 'Y':

    while True:

        print(section1)

        inp = input('Are final Files ready for EDI (Y): ')

        if inp == 'Y': break
        
        else: print('\n' + 'Get Files ready ASAP.')

    fd.MoveFilesEDI(3, fd.suffix)


# ------------------------------Copies RegE files to PCI--------------------------------- #


if fd.suffix == 'b' and rege == 'Y':

    fd.CopyRegE()

print(section1)