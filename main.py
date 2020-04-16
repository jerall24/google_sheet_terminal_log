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
# - Confirmation of command being completed
# - log_id or search
# - list out last ## of logs, last ## of logs for a specific project
# - Consideration: Implement SQL in this to create a database of these so I can run SQL on them or just add to google sheets?
# - Limit combination of flags (p and l can't be used together)
# - If flag is designated but the first word in the message is a project then make that the project and use the rest of the message.

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
#default sheet is 0
SHEET_ID = 0
SHEET_RANGE = MAIN_SHEET+ACTIVE_COLUMNS

# args comes in as a list of arguments
def function_calls(args):
    # args = [command, flags[], identifier, message]
    print(args)
    sheet = get_sheet(creds())
    # For testing always use the following command line code
    # gotest = go new "This is my comment"
    func = args[0]
    flags = args[1]
    identifier = args[2]
    message = args[3]
    if(func == "new"):
        # Use helper function for each command
        appendNewLog(sheet, flags, identifier, message)
        print("\"" + func + "\" feature is currently being worked on")
    elif(func == "last"):
        print("\"" + func + "\" action not completely implemented yet")
        print(getLastLog(sheet, flags, identifier))
        print("prioritize last > last project_name")
    elif(func == "del"):
        print("\"" + func + "\" action not yet implemented")
        print("prioritize del > del project_name > del log_id")
    elif(func == "help"):
        print("There are 3 current commands: new, last, and del")
        print("If you want to specify a project add the flag -p after the command")
        print("When the delete function is implemented, add the flag -l after del and specify the log_id to delete that log")
        print("Don't use more than one flag for now")
        print("project names shouldn't include spaces")
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

def appendNewLog(sheet, flags, project, message):
    message = "No message logged" if message is None else message
    if (flags is None) or ("p" in flags and project is None) or ("p" not in flags):
        project = getLastLog(sheet, None, None)[1]
    # print(project)
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
                "sheetId" : SHEET_ID,
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
    return 0

# Helper function to get the first line after the headers
# If project is none then we'll get the most recent log
def getLastLog(sheet, flags, project):
    if(flags is None):
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=MAIN_SHEET+FIRST_COL+"2:"+LAST_COL+"2").execute()
        # return a list of 3 items [time, project, message]
        return result.get('values', [])[0]
    else:
        return ["time", "project", "message"]

def deleteLog():
    #https://developers.google.com/sheets/api/guides/batchupdate#example
    return

# Need a robust method of getting the arguments that are being passed
# through the terminal command - using flags
# Command - new, last, del, list (to be implemented)
# Flag - p, l
# Identifier - Either project_name or log_id
# Message - the message
def decipherArgs():
    it = iter(sys.argv)
    next(it)
    command = next(it)
    # Now at the 3rd argument
    try:
        current = next(it)
    except:
        return [command, None, None, None]
    if current[0] == '-':
        #we have a flag on the play
        flags = list(current[1:])
        # have to account when we do -lp or -pl
        # but also can't do a combo of p and l
    elif current is None:
        # Either go last or go del
        flags = identifier = message = None
        return [command, flags, identifier, message]
    else:
        # No flag so we either have a log message or nothing afterwards
        # Currently only command will be go new <message>
        flags = identifier = None
        message = current + " " + " ".join(it)
        return [command, flags, identifier, message]
    # At this point everything is using a flag
    # The next argument will always be a project_name or log_id
    identifier = next(it)
    message = " ".join(it)
    # [command, flags[], identifier, message]
    return [command, flags, identifier, message]

if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    function_calls(decipherArgs())
    # print(decipherArgs())
