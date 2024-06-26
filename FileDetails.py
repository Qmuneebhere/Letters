from datetime import datetime, date
import shutil
import os, time


section1 = '\n\n' + '***********************************************************' + '\n\n'

###########################################################################################
# ------------------------------------ Configuration ------------------------------------ #
###########################################################################################


# Mapping of EDI and administration drive on local machine

mapAdmin = 'Y'
mapEDI = 'Y'

# Drive name on which administration network drive is mapped

adminDrive = 'N'

# Type in your username of local pc here

user = 'MUNEEB'

# If file is coborrower set cobor to Y

cobor = 'N'

# If Lettering Mail file is prepared manually, set prepped to Y

prepped = 'N'

# Cobor Files are prepared Manually

if cobor == 'Y': prepped = 'Y'


###########################################################################################
# ---------------------------------- Current Date info ---------------------------------- #
###########################################################################################


print(section1)

print('Welcome! Do you want to process for today?'.center(60) + '\n')

while True:

    isToday = input('Y for today N for custom date: ')

    if isToday == 'Y':

        # Current Date

        currDate = date.today()

        # Current date in format mm/dd/yyyy

        curr_date = currDate.strftime('%m/%d/%Y')

        break

    elif isToday == 'N': 
        
        strDate = input('\nEnter Date (mm-dd-yyyy): ')

        # Current Date

        currDate = datetime.strptime(strDate, '%m-%d-%Y')

        # Current date in format mm/dd/yyyy

        curr_date = currDate.strftime('%m/%d/%Y')

        break
    
    else:

        print('\nInvalid Input.\n')

# Current Day, Month and Year in dd, mm, yyyy format

cDay = str(format(currDate.day, '02d'))
cMonth = str(format(currDate.month, '02d'))
cMonthName = str(currDate.strftime('%b'))
cYear = str(format(currDate.year, '04d'))

# Current Month and year in format: mmm yyyy (Aug 2023)

mmmyyyy = cMonthName + ' ' + cYear


###########################################################################################
# -------------------------------- Current Folders name --------------------------------- #
###########################################################################################


# Current Working Folder name: mm-dd-yyyy

currFolderName = f'{cMonth}-{cDay}-{cYear}'

# Current TLO folder name: yyyy-mm-dd

currTLOfolder = f'{cYear}-{cMonth}-{cDay}'


###########################################################################################
# ----------------------------- Current Working Directory ------------------------------- #
###########################################################################################


# Path to Letters Folder in Documents

Documents = f'C:\\Users\\{user}\\OneDrive - GCS Inc\\Documents\\'

# Current Working Directory for Letters

letters_dir = f'{Documents}Unifin\\Letters\\'


###########################################################################################
# ----------------------- Templates & required File Directories ------------------------- #
###########################################################################################


SIF_Dir = f'{Documents}SIF\\'

LM_Dir = f'{Documents}LM\\'

Temp_Dir = f'{Documents}Templates\\'


###########################################################################################
# ---------------------------------- EDI Directories ------------------------------------ #
###########################################################################################


if mapEDI == 'Y':

    # Path to EDI Letter & Emails folder mapped on Local pc

    EDI_dir = f'C:\\Users\\{user}\\OneDrive - Gcs Inc\\Letters & Emails\\'

    # Path to Templates Folder on EDI

    Temp_Dir = EDI_dir + 'Files\\Templates\\'

    # Path to SIF folder on EDI

    SIF_Dir = f'{EDI_dir}Files\\SIF\\'

    # Path to current folder in EDI

    currEDI_dir = EDI_dir + f'{cYear}\\{mmmyyyy}\\{currFolderName}\\Letters\\'


###########################################################################################
# --------------------------Administration Drive Directories----------------------------- #
###########################################################################################


if mapAdmin == 'Y':

    # Path to Lettering Mail folder in administration

    LM_Dir = f'{adminDrive}:\\FTP_Transfers\\Incoming\\Unprocessed\\Unifin Inc\\'

    # Path to processed folder in administration

    processed_Dir = f'{adminDrive}:\\FTP_Transfers\\Incoming\\Processed\\Unifin Inc\\'

    # Path to vendor PCI folder

    vendor_Dir = f'{adminDrive}:\\Vendor_Related\\Lettering\\PCI\\Sent Files\\'

    currPCI_Dir = f'{vendor_Dir}{currFolderName}\\'

    # Path to TLO Address folder in vendor related

    currTLO_dir = f'{adminDrive}:\\Vendor_Related\\Skip Tracing\\' \
                f'TLO\\{cYear}\\Address\\{currTLOfolder}\\'

    # Path to TLO folder in FTP Transfers

    TLOFTP_dir = f'{adminDrive}:\\FTP_Transfers\\Incoming\\Unprocessed\\Vendor\\TLO\\'

    # Path to Staging folder for job

    staging_dir = f'{adminDrive}:\\FTP_Transfers\\Incoming - Staging\\Unifin Inc\\'


###########################################################################################
# ------------------------------------ Gets Filetype ------------------------------------ #
###########################################################################################


# Suffixes for possible Letter files

suffixes = ['b', 'c', 'd', 'e', 'f']

print(section1)

while True:

    print('Which letter file you want to prepare? (b/c/d/e)'.center(60))

    suffix = input('\n' + 'FileType: ')

    if suffix in suffixes: break

    else: print('\n' + 'Invalid Input.')

curr_dir = f'{letters_dir}{cYear}\\{cMonthName}\\{currFolderName}\\{suffix}-File\\'


###########################################################################################
# ------------------- Names of files required for Lettering procedure ------------------- #
###########################################################################################


# Name of Lettering Mail File

if suffix == 'b': 
    
    mailFile = f'Lettering-Mail-{cYear}-{cMonth}-{cDay}.csv'

else: 

    if cobor == 'Y': mailFile = f'Lettering-Mail-{cYear}-{cMonth}-{cDay}{suffix}-Cobor.csv'
    
    else: mailFile = f'Lettering-Mail-{cYear}-{cMonth}-{cDay}{suffix}.csv'

# Name of Templates required for Lettering procedure

tempWorkbookFile = 'WkbTemplate.xlsx'
tempAutoFile = 'AutoTemplate.csv'
tempText = 'DelAccounts.txt'

# Pattern for RegE Files

patternRegE = f'Letters-*_{cYear}-{cMonth}-{cDay}-N03?.csv'

# Name of current Workbook file

if cobor == 'Y': workbookFile = f'Unifin-PCI_{currFolderName}{suffix}-Cobor.xlsx' 

else: workbookFile = f'Unifin-PCI_{currFolderName}{suffix}.xlsx'

# Name of current csv file

if cobor == 'Y': csvFile = f'Unifin-PCI_{currFolderName}{suffix}-Cobor.csv'

else: csvFile = f'Unifin-PCI_{currFolderName}{suffix}.csv'

TLOFile = 'TLO-Address-' + cMonth + cDay + cYear + suffix + '.csv'
TLOAppend = 'TLO-Address-' + cMonth + cDay + cYear + suffix + '-append.csv'


autoFile = 'Unifin-PCI_' + currFolderName + suffix + '_Auto.csv'
rejectFile = 'Rejected_Accounts_' + currFolderName + suffix + '.txt'
mismatchFile = 'Mismatch_Accounts_' + currFolderName + suffix + '.txt'

importFile = 'Import_Data_' + currFolderName + suffix + '.csv'
veriADRFile = 'Verified_ADR_' + currFolderName + suffix + '.csv'


# -----------------------------Moves File in created Folder------------------------------ #


def MoveFiles():

    # If filetype b --> Incorrect Accounts File

    if suffix == 'b':

        delFile = rejectFile

    # For other files --> Mismatch Accounts File

    else:

	    delFile = mismatchFile

    #####################################################
    ##                                                 ##
    ##            Moves Lettering Mail file            ##
    ##                                                 ##
    #####################################################

    # Path to Mail file in administration drive

    aMail = LM_Dir + mailFile

    # Path to mail file in current folder

    bMail = curr_dir + mailFile

    # Moves Lettering Mail file to current folder

    shutil.copy(aMail, bMail)

    #####################################################
    ##                                                 ##
    ##                 Moves Templates                 ##
    ##                                                 ##
    #####################################################

    # Creates a list of template file names

    tempList = [tempWorkbookFile, tempAutoFile, tempText]

    # Creates a list of files in current folder

    fileList = [workbookFile, autoFile, delFile]

    for tempName, fileName in zip(tempList, fileList):

        # Path to template on EDI

        aFile = Temp_Dir + tempName
        
        # Path to file in current folder

        bFile = curr_dir + fileName

        # Moves Tempates to current folder

        shutil.copy(aFile, bFile)


# ---------------------------Moves TLO File in Address Folder---------------------------- #


def MoveTLO():

    # Path to TLO file in current directory

    cTLO = curr_dir + TLOFile

    # Path to TLO file in Administration drive

    aTLO = currTLO_dir + TLOFile

    # Moves TLO File from current to Administration directory

    shutil.copy(cTLO, aTLO)


# ------------------------Moves TLO Append File in current Folder------------------------ #


def MoveTLOAppend():

    # Path to TLO file in current directory

    cTLO = curr_dir + TLOAppend

    # Path to TLO file in Administration drive

    aTLO = currTLO_dir + TLOAppend

    # Path to TLO file in FTP folder

    fTLO = TLOFTP_dir + TLOAppend

    # Moves TLO File from Administration to current directory

    shutil.copy(aTLO, cTLO)

    # Moves TLO File to FTP Transfer folder

    shutil.copy(aTLO, fTLO)


# -------------------------------Moves Files to EDI Folder------------------------------- #


def MoveFilesEDI(stage, fileType):


    # File name of Pivot Table file

    lettersFile = f'Letters_{currFolderName}{fileType}.xlsx'

    # Paths to file in current local folder

    cWkb = curr_dir + workbookFile
    cAuto = curr_dir + autoFile
    cMail = curr_dir + mailFile
    cCsv = curr_dir + csvFile
    cLetter = curr_dir + lettersFile

    # Paths to file in EDI folder

    eWkb = currEDI_dir + workbookFile
    eAuto = currEDI_dir + autoFile
    eMail = currEDI_dir + mailFile
    eCsv = currEDI_dir + csvFile
    eLetter = currEDI_dir + lettersFile

    # There are three stages in which files are to be moved to EDI
    # Stage 1 is before QA. (workbook, mail, csv and Letter) files
    # are to moved in this stage. Letter file is for Letter b only

    if stage == 1:

        shutil.copy(cWkb, eWkb)
        shutil.copy(cCsv, eCsv)
        shutil.copy(cMail, eMail)

        if fileType == 'b': shutil.copy(cLetter, eLetter)

    # Stage 2 is when auto file is to be moved.

    elif stage == 2:

        shutil.copy(cAuto, eAuto)

    # Stage 3 is when files are ready. Final workbook and csv
    # files are to be moved in this stage.

    elif stage == 3:

        shutil.copy(cWkb, eWkb)
        shutil.copy(cCsv, eCsv)


# --------------------------------Copies csv File for job-------------------------------- #


def CopyCsvForJob():

    # Path to csv File in current folder

    cCsv = curr_dir + csvFile

    # Path to csv File in Staging folder

    sCsv = staging_dir + csvFile

    # Moves csv file from current to staging folder

    shutil.copy(cCsv, sCsv)


# -----------------------------Copies RegE File to VendorPCI----------------------------- #


def CopyRegE():

    os.makedirs(currPCI_Dir)

    while True:

        if not os.path.exists(processed_Dir + newRegE):

            print(section1)
            print('Searching for RegE files in processed folder.'.center(60))

            time.sleep(900)
        
        else: 

            shutil.copy(processed_Dir + newRegE, currPCI_Dir + newRegE)

            print(section1)
            print('You can send RegE file to FTP'.center(60))
            
            break
    
