import gspread
import pandas as pd
import csv
import time

green = {
    "red": 0.0,
    "green": 1.0,
    "blue": 0.0
}
small_green = {
    "red": 0.3,
    "green": 0.7,
    "blue": 0.0
}
red = {
    "red": 1.0,
    "green": 0.0,
    "blue": 0.0
}
small_red = {
    "red": 0.7,
    "green": 0.3,
    "blue": 0.0
}
yellow = {
    "red": 1.0,
    "green": 1.0,
    "blue": 0.0
}

alpha = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', "Z"]
alpha2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', "Z"]
def importSpreadsheet(key_location: str, spreadsheet_name: str, worksheet_name: str, csv_location: str):
    gc = gspread.service_account(key_location) # connect to google account using api key
    sh = gc.open(spreadsheet_name) #connect to spreadsheet. defaults to first worksheet
    worksheet = sh.worksheet(worksheet_name) #open worksheet to write to
    worksheet.clear() #clear worksheet and dump csv
    sh.values_update(
        worksheet_name,
        params={'valueInputOption': 'USER_ENTERED'},
        body={'values': list(csv.reader(open(csv_location)))}
    )
    # Color cells
    alt = True
    size = pd.read_csv(csv_location).shape[0] # use pandas to get how many players there are in csv
    for row in range(2, 2+size): # Start on row 2
        alt = not alt
        for column in range(2,2+size): # start on second column
            val = worksheet.cell(row, column).value
            if val != 'N/A':
                try:
                    if column > 26:
                        chara = "A" + alpha2[column - 27]
                    else:
                        chara = alpha[column - 2]
                except IndexError:
                    breakpoint()
                
                colorCell(worksheet, chara + str(row), val.split('-'), alt)
                time.sleep(0.8) # google api only allows 100 writes a minute
  

def colorCell(worksheet, cell, score, alt):
    #win
    mod = 0.0
    if alt:
        mod = 0.2
    total_games = int(score[0]) + int(score[1])
    if int(score[0]) == total_games and total_games !=0:
        worksheet.format(cell, {
                    "backgroundColor": {
    "red": 0.0,
    "green": 1.0- mod,
    "blue": 0.0
},
                    "horizontalAlignment": "CENTER",
        })
    elif int(score[0]) > int(score[1]):
        worksheet.format(cell, {
                    "backgroundColor": {
    "red": 0.1,
    "green": 0.7- mod,
    "blue": 0.0
},
                    "horizontalAlignment": "CENTER",
        })
    #loss
    elif int(score[1]) == total_games and total_games !=0:
        worksheet.format(cell, {
                    "backgroundColor": {
    "red": 1.0- mod,
    "green": 0.0,
    "blue": 0.0
},
                    "horizontalAlignment": "CENTER",
        })
    elif int(score[0]) < int(score[1]):
        worksheet.format(cell, {
                    "backgroundColor":  {
    "red": 0.7- mod,
    "green": 0.1,
    "blue": 0.0
},
                    "horizontalAlignment": "CENTER",
        })
    #tie
    elif int(score[0]) == int(score[1]):
        worksheet.format(cell, {
                "backgroundColor": {
    "red": 0.5 - mod,
    "green": 0.5 - mod,
    "blue": 0.0
},
                "horizontalAlignment": "CENTER",
        })