from flask import render_template, request, jsonify
import gspread

import os
import json

from aprimon import app
from aprimon.collection import Collection
from aprimon.data import ALL_SPREADSHEETS

# Initialise Google Sheets API access
try:
    # read credentials from the default filepath, which is
    # ~/.config/gspread/service_account.json
    gc = gspread.service_account()
except FileNotFoundError:
    # read in the credentials from an environment variable (which is a secret
    # on Heroku)
    creds_dict = json.loads(os.getenv("GOOGLE_SHEETS_CREDS_JSON"))
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    gc = gspread.service_account_from_dict(creds_dict)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/_all_users', methods=['GET'])
def _all_users():
    game = request.args.get('game')
    all_users = {user: ALL_SPREADSHEETS[user][game]["key"]
                 for user in ALL_SPREADSHEETS.keys()
                 if game in ALL_SPREADSHEETS[user]}
    return jsonify({"allUsers": all_users})


@app.route('/_calculate_aprimon', methods=['POST'])
def _calculate_aprimon():
    j = request.get_json()
    game = j['game']

    if "username" in j['user1']:
        c1 = Collection.read(gc, ALL_SPREADSHEETS[j['user1']['username']][game])
    elif "list" in j['user1']:
        c1 = Collection.from_manual(j['user1']['list'])
    if "extra_list" in j['user1']:
        c1 = c1 + Collection.from_manual(j['user1']['extra_list'])

    if "username" in j['user2']:
        c2 = Collection.read(gc, ALL_SPREADSHEETS[j['user2']['username']][game])
    elif "list" in j['user2']:
        c2 = Collection.from_manual(j['user2']['list'])
    if "extra_list" in j['user2']:
        c2 = c2 + Collection.from_manual(j['user2']['extra_list'])

    diff = c2 - c1
    return jsonify({"aprimon": diff.to_list()})
