from __future__ import print_function

import datetime
import json
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events.owned']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None

    with open('output.json', encoding='utf-8') as f:
        events = json.load(f)
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

    try:
        service = build('calendar', 'v3', credentials=creds)
        for event in events:
            d = datetime.date.fromisoformat(event['date'])
            t_from = datetime.time.fromisoformat(event['from'])
            t_to = datetime.time.fromisoformat(event['to'])
            dt_from = datetime.datetime.combine(d, t_from)
            dt_to = datetime.datetime.combine(d, t_to)
            meta = {
                'summary': event['name'],
                'description': 'generated',
                'start': {
                    'dateTime': dt_from.isoformat(),
                    'timeZone': 'Asia/Ho_Chi_Minh'
                },
                'end': {
                    'dateTime': dt_to.isoformat(),
                    'timeZone': 'Asia/Ho_Chi_Minh'
                }
            }
            service.events().insert(calendarId='primary', body=meta).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
