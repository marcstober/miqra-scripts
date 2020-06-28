
This retrieves the raw data from Seth (Avi) Kadish's "Miqra al pi ha-Masorah" version of the Tanakh [from Google Sheets](https://docs.google.com/spreadsheets/d/1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs/edit?usp=sharing).

# Setup

1. `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib` 
  You may need to use virtualenv (recommended) or run as admin.

2. Although this is accessing public data, we're using an API that requires authentication. 
  Go to https://developers.google.com/sheets/api/quickstart/python, create an application, then
  download a credentials.json file. Then the first time you run this you'll be prompted to log in
  in your browser.


## TODO

Find a way to not require authentication, maybe publishing with the old API 
as described here: https://stackoverflow.com/a/45731424 
or using the chart API described here: https://stackoverflow.com/a/33727897.


# Usage

First time only: `mkdir ../miqra-data/`

If using virtualenv: `.\venv/Scripts\activate`

1. `python downloadfromgoogle.py`

TSV files for each sheet will be saved in the `downloads` folder.

2. `python splitbooks.py`

Split download files into per-book files and put them in `../miqra-data/source`. Also fixes quoting from Github display.

# Troubleshooting

If you get an error try deleting `token.pickle` (and you be prompted to log in to Google Sheets again).
Here's the relevant Google dashboard: https://console.developers.google.com/apis/dashboard