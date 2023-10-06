import pandas as pd
import numpy as np
import FileDetails as fd
import os


# This function creates workbook file for Pivot Table

def CreateXlsx(df, date, suffix, curr_dir):

    # Name of Letter file

    letterFile = f'Letters_{date}{suffix}.xlsx'

    # Changes directory to current working directory

    os.chdir(path=curr_dir)

    # Creates a pandas Excel writer using XlsxWriter as the engine

    wkbWriter = pd.ExcelWriter(letterFile, engine='xlsxwriter')

    # Get the xlsxwriter.Workbook object from the writer

    workbook = wkbWriter.book

    # Convert the dataframe to an XlsxWriter Excel object

    df.to_excel(wkbWriter, sheet_name='Letters', index=False)

    # Gets data frame worksheet

    worksheetDF = workbook.get_worksheet_by_name('Letters')

    # Add another worksheet named LTRCodes in our workbook

    worksheetLTR = workbook.add_worksheet('LTRCodes')

    worksheetLTR.write('A1', 'N021')
    worksheetLTR.write('A2', 'N021S')
    worksheetLTR.write('A3', 'E021')

    # Setting formats with font colors

    blueFormat = workbook.add_format()
    blueFormat.set_font_color('#00B0F0')

    redFormat = workbook.add_format()
    redFormat.set_font_color('#FF0000')

    # Setting columns with their respective font colors

    worksheetDF.set_column('S:W', None, blueFormat)
    worksheetDF.set_column('AQ:AV', None, redFormat)
    worksheetDF.set_column('AZ:BI', None, redFormat)
    worksheetDF.set_column('BY:BY', None, redFormat)
    worksheetDF.set_column('CI:CY', None, redFormat)

    # Sets width of columns

    worksheetDF.set_column('A:DJ', 25)

    # Formate header column of our dataframe worksheet

    simpleFormat = workbook.add_format({'bold': True, 'font_color': '#FF0000'})
    yellowFormat = workbook.add_format({'bold': True, 'font_color': '#FF0000', 'bg_color': '#FFFF00'})
    orangeFormat = workbook.add_format({'bold': True, 'font_color': '#FF0000', 'bg_color': '#FFC000'})
    blueFormat = workbook.add_format({'bold': True, 'font_color': '#FF0000', 'bg_color': '#1F4E78'})

    yellowCols = [0, 1, 2, 3, 4, 5, 6, 7, 11, 12, 13, 14, 15, 17, 26, 27, 28,
                  31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 48, 49, 61, 66,
                  67, 68, 69, 70, 71, 72, 73, 74, 106, 107, 108, 109]
    orangeCols = [42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 75, 76, 110]
    blueCols = [18, 19, 20, 21, 22]

    for col_num, value in enumerate(df.columns.values):

        if col_num in yellowCols: worksheetDF.write(0, col_num, value, yellowFormat)
        elif col_num in orangeCols: worksheetDF.write(0, col_num, value, orangeFormat)
        elif col_num in blueCols: worksheetDF.write(0, col_num, value, blueFormat)
        else: worksheetDF.write(0, col_num, value, simpleFormat)

    wkbWriter.close()