from __future__ import print_function

import datetime
import json
import os.path

import dateutil.parser as parser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import emailDatabase


def gmailCredential(SCOPES):
    """
    Function  :     Opens a connection request to GMAIL API and creates a token file if it is created for the first time.
    Arguments :     SCOPES - This is the default security scope on how to use the gmail api data.
    Return values : Returns the services for the authorized GMAIL API
    """
    try:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print("gmailCredential : ", e)


def getMessages(service, cn, cr):
    """
    Function :      Gets all the messages from the gmail, stores in the GMAIL database and process rules as per the rules mentioned in rules.json
    Arguments :     service - return value from function gmailCredential for accessing the GMAIL API
                    rules - the josn object from rules.json file which has the rules to be processed.
                    cn - Established Database connection
                    cr - cursor for the db to execute query
    Return values:  No return values.
    """
    try:
        # Call the Gmail API
        results = service.users().messages().list(maxResults=5, userId='me').execute()
        messages = results.get('messages')
        for msg in messages:    # Loops through the messages via msgId and gets the subject, sender, sent date.
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            for h in headers:   # Loops through the message headers and gets the subject, sender and sent date.
                if h['name'] == 'Subject':
                    subject = h['value']
                if h['name'] == 'From':
                    sender = h['value']
                    From = sender.split("<")[1][:-1]
                if h['name'] == 'Date':
                    msg_date = h['value']
                    date_parse = (parser.parse(msg_date))
                    Date = date_parse.date()
                    Days = str((datetime.datetime.now().date() - Date).days)    # variable to calculate the days for the date rule.
            # Below line inserts a row to the GMAIL database.
            emailDatabase.insertRow(cn, cr, Date, subject, From, msg['id'])
    except Exception as e:
        print("getMessages: ", e)


if __name__ == '__main__':
    # If modifying these scopes, delete the file token.json.
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    # Opening the rules.josn file and creating as json object
    with open("rules.json") as json_file:
        data = json.load(json_file)
    # Creating GMAIL service credentials.
    ser = gmailCredential(SCOPES)
    # Creating database connection
    DBcn, DBcr = emailDatabase.createDBconnection()
    # Creates Table if it is not created
    emailDatabase.createTable(DBcr)
    # Gets the messages and process the mesages as per the rules.
    getMessages(ser, DBcn, DBcr)
    print("Process completed - Reading gmails")