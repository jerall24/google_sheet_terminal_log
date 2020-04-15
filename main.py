from __future__ import print_function
import os.path
# from os import *
from datetime import datetime
import sys
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# TODO:
# - Configure reading of terminal arguments to account for varying number of arguments
# - Will need to use the Drive API (link in architecture) to get Sheet IDs and manage the drive on a file-basis. Not MVP
# - Get list of all projects
#

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Will need to get a function that'll get the sheet and range
# This range will change for all of the functions though
SPREADSHEET_ID = "1qVVlVO0-8jq4giRJCSQiwxsPa3sFRWk0nb392KAUYG4"

# Metainformation for the sheet
MAIN_SHEET = 'Sheet1!'
ACTIVE_COLUMNS = 'A:C'
FIRST_COL = 'A'
LAST_COL = 'C'
SHEET_RANGE = MAIN_SHEET+ACTIVE_COLUMNS

# args comes in as a list of arguments
def function_calls(args):
    sheet = get_sheet(creds())
    # For testing always use the following command line code
    # gotest = go new "This is my comment"
    func = args[1]
    # when we get more robust argument reading uncomment this
    # project = args[2]
    message = " ".join(args[2:])
    flag = None
    project = None
    if(func == "new"):
        #use helper function for each command
        appendNewLog(sheet, flag, project, message)

        print("\"" + func + "\" feature is currently being worked on")
    elif(func == "last"):
        print("\"" + func + "\" action not completely implemented yet")
        print(getLastLog(sheet, None))
        print("prioritize last > last project_name")
    elif(func == "del"):
        print("\"" + func + "\" action not yet implemented")
        print("prioritize del > del project_name > del log_id")
    elif(func == "help"):
        print("There are 3 current commands: new, last, and del")
        print("If you want to specify a project add the flag -p after the command")
        print("implementation for them and this help is currently being worked on")
    else:
        print(func + " action not supported yet")

def creds():
    # authorize user to log something
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # uses Google discovery API
    return creds


def get_sheet(creds):
    # I believe the build function is a function that will connect to the API and version specified with the credentials that are passed through. This is to save us time looking for the API?
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()
    # returns the spreadsheet id
    # MVP - will only work with one spreadsheet so will always return
    # that id but want to create functionality to create new sheet
    # if sheet does not exist, create one
    # else return sheet id
    # all else fails default to regular sheet

def appendNewLog(sheet, flag, project, message):
    if flag != "-p":
        project = getLastLog(sheet, None)
    requests = []
    requests.append(
        {
          "insertDimension": {
            "range": {
              "dimension": "ROWS",
              "startIndex": 1,
              "endIndex": 2
            },
            "inheritFromBefore": True
          }
        })
    requests.append({
        # "majorDimension": "ROWS",
        # "range": "Sheet1!A2:C2",
        # "values": [[datetime.today().strftime("%m/%d/%Y %H:%M:%S"),getLastLog(sheet, None)[1],message]]
        "updateCells": {
        # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#UpdateCellsRequest
            "rows" : [
                {
                #object (RowData)
                "values": [
                        {
                            "userEnteredValue":
                            {
                            "stringValue" : datetime.today().strftime("%m/%d/%Y %H:%M:%S")
                            }
                        },
                        {
                            "userEnteredValue": {
                            "stringValue" : project
                            }
                        },
                        {
                            "userEnteredValue": {
                            "stringValue" : message
                            }
                        }
                    ]
                }
            ],
              "fields": "*",

              # Union field area can be only one of the following:
              "start": {
                # object (GridCoordinate)
                "sheetId" : 0,
                "rowIndex" : 1,
                "columnIndex" : 0
              },
              # "range": {
              #   object (GridRange)
              # }
              # End of list of possible types for union field area.
        }
    })
    body = {
        "requests" : requests
    }
    sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID,body=body).execute()
    # append_req = {
    #     "majorDimension": "ROWS",
    #     "range": "Sheet1!A2:C2",
    #     "values": [[datetime.today().strftime("%m/%d/%Y %H:%M:%S"),getLastLog(sheet, None)[1],message]]
    # }
    # result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A2:C2', insertDataOption="INSERT_ROWS",valueInputOption="USER_ENTERED",body=append_req).execute()
    return 0

# Helper function to get the first line after the headers
# If project is none then we'll get the most recent log
def getLastLog(sheet, project):
    if(project is None):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=MAIN_SHEET+FIRST_COL+"2:"+LAST_COL+"2").execute()
        return result.get('values', [])[0]
    else:
        return ["there's", "nothing", "here"]

def deleteLog():
    #https://developers.google.com/sheets/api/guides/batchupdate#example
    return

# Need a robust method of getting the arguments that are being passed
# through the terminal command - using flags
def decipherArgs():
    # [command, flags, [project, log], message]
    return sys.argv

if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    function_calls(decipherArgs())
