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
# - See if I have to remove the quotes around the log

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#Will need to get a function that'll get the sheet and range
SAMPLE_RANGE_NAME = 'Sheet1!A1:C'

def function_calls(args):
    #for testing always use the following command line code
    # gotest = go new "This is my comment"
    func = args[1]
    # when we get more robust argument reading uncomment this
    # project = args[2]
    message = " ".join(args[2:])
    daytime = datetime.today()
    if(func == "new"):
        print("\"" + func + "\" feature is currently being worked on")
        print(daytime)
        print(message)
    elif(func == "last"):
        print("\"" + func + "\" action not yet implemented")
        print("prioritize last > last project_name")
    elif(func == "del"):
        print("\"" + func + "\" action not yet implemented")
        print("prioritize del > del project_name > del log_id")
    elif(func == "help"):
        print("There are 3 current commands: new, last, and del")
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
    spreadsheet = "1qVVlVO0-8jq4giRJCSQiwxsPa3sFRWk0nb392KAUYG4"
    # I believe the build function is a function that will connect to the API and version specified with the credentials that are passed through. This is to save us time looking for the API?
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    print(sheet)
    result = sheet.values().get(spreadsheetId=spreadsheet,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[2]))
    # returns the spreadsheet id
    # MVP - will only work with one spreadsheet so will always return
    # that id but want to create functionality to create new sheet
    # if sheet does not exist, create one
    # else return sheet id
    # all else fails default to regular sheet


    return;


if __name__ == '__main__':
    # print('Number of arguments:', len(sys.argv), 'arguments.')
    # print('Argument List:', str(sys.argv))
    get_sheet(creds())
    function_calls(sys.argv)
