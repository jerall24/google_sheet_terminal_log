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

def function_calls(args):
    func = args[1]
    project = args[2]
    message = " ".join(args[3:])
    daytime = datetime.today()
    if(func == "new"):
        print(func + " feature is currently being worked on")
        print(daytime)
        print(message)
    elif(func == "last"):
        print(func + " action not yet implemented")
        print("prioritize last > last project_name")
    elif(func == "del"):
        print(func + " action not yet implemented")
        print("prioritize del > del project_name > del log_id")
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
    service = build('sheets', 'v4', credentials=creds)
    return creds


def get_sheet():
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
    creds()
    function_calls(sys.argv)
