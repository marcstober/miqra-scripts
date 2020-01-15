
# SETUP:
1. pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
  (I used virtualenv instead of installing as admin. (.\venv/Scripts\activate))
2. Although this is accessing public data we're using an API that requires authentication. 
  Go to https://developers.google.com/sheets/api/quickstart/python, create an application, then
  download a credentials.json file. Then the first time you run this you'll be prompted to log in
  in your browser.
  (TODO: find a way to not require authentication, maybe publishing with the old API 
  as described here: https://stackoverflow.com/a/45731424 
  or using the chart API described here: https://stackoverflow.com/a/33727897)

# USAGE:
  (first time only:) mkdir ../miqra-data/
  python downloadcsv.py
CSV files for each sheet will be saved in miqra-data folder.

# Troubleshooting:

If you get an error try deleting token.pickle (and you will have to log in to Google Sheets again).
Here's the relevant Google dashboard: https://console.developers.google.com/apis/dashboard