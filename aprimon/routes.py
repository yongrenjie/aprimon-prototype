from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import ValidationError
from flask import render_template, redirect, url_for, request
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import warnings
import os
import json

from aprimon import app
from aprimon.collection import Collection
from aprimon.data import ALL_SPREADSHEETS


try:
    gc = gspread.service_account()
except FileNotFoundError:
    scopes = ['https://spreadsheets.google.com/feeds']
    json_creds = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
    creds_dict = json.loads(json_creds)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\\\n", "\n")
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scopes)
    gc = gspread.authorize(creds)


def check_usernames_unequal(form, field):
    if (form.my_username.data and form.their_username.data
            and form.my_username.data == form.their_username.data):
        raise ValidationError('Must choose different usernames')

def check_not_none(form, field):
    if field.data == '0':
        raise ValidationError('Must choose a username')


class AprimonForm(FlaskForm):
    choices = [(0, "-- Select --")]
    choices = choices + [(user, user) for user in ALL_SPREADSHEETS.keys()]
    my_username = SelectField(label='Your username', choices=choices,
                              validators=[check_not_none])
    their_username = SelectField(label="Trading partner's username",
                                 choices=choices,
                                 validators=[check_not_none, check_usernames_unequal])
    sort_by = SelectField(label="Sort results by",
                          choices=[("dex", "National Dex number"),
                                   ("name", "Alphabetical")])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def start_form():
    form = AprimonForm()
    if form.validate_on_submit():
        return redirect(url_for('display_collection',
                                me=form.my_username.data,
                                them=form.their_username.data,
                                sort=form.sort_by.data))
    return render_template('start_form.html', form=form)


@app.route('/display_collection')
def display_collection():
    me = request.args.get('me')
    them = request.args.get('them')
    sort = request.args.get('sort')
    c1 = Collection.from_sheet(gc, username=me)
    c2 = Collection.from_sheet(gc, username=them)
    diff = c2 - c1
    if diff.is_empty():
        return render_template('empty_collection.html', me=me, them=them)
    else:
        return render_template('display_collection.html', me=me, them=them,
                               entries=diff.get_entries(sort=sort))
