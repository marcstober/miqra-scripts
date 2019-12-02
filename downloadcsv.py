import os
import pickle
import re
import requests
import shutil
import urllib.parse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# SETUP:
# 1. pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#   (I used virtualenv instead of installing as admin.)
# 2. Although this is accessing public data we're using an API that requires authentication. 
#   Go to https://developers.google.com/sheets/api/quickstart/python, create an application, then
#   download a credentials.json file. Then the first time you run this you'll be prompted to log in
#   in your browser.
#   (TODO: find a way to not require authentication, maybe publishing with the old API 
#   as described here: https://stackoverflow.com/a/45731424 
#   or using the chart API described here: https://stackoverflow.com/a/33727897)

# USAGE:
#   (first time only:) mkdir ../miqra-data/
#   python downloadcsv.py
# CSV files for each sheet will be saved in miqra-data folder.

# See also: https://stackoverflow.com/a/51235960

class Downloader:
    def run(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

        SPREADSHEET_ID = '1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs'

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

        service = build('sheets', 'v4', credentials=creds)

        # get all the sheets in the spreadsheet document
        result = service.spreadsheets().get(spreadsheetId = SPREADSHEET_ID).execute()
        spreadsheetUrl = result['spreadsheetUrl']
        exportUrl = re.sub("\/edit$", '/export', spreadsheetUrl)
        for sheet in result['sheets']:
            params = {
                'format': 'csv',
                'gid': sheet['properties']['sheetId'],
            } 
            sheet_title = create_filename(sheet['properties']['title'])
            queryParams = urllib.parse.urlencode(params)
            url = exportUrl + '?' + queryParams
            response = requests.get(url)
            filePath = '../miqra-data/%s.csv' % (sheet_title)
            with open(filePath, 'wb') as csvFile:
                csvFile.write(response.content)

def create_filename(sheet_title):
    return re.sub('"', '', sheet_title)

if __name__ == '__main__':
    Downloader().run()