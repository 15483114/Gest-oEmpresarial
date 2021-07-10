from flask import Flask, session, app, render_template, request, Markup
import sys, io, re
import os, base64
from io import StringIO
from datetime import datetime
import pandas as pd
import time

app = Flask(__name__)

# get root path for account in cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

survey_data = []

# survey page
@app.route("/", methods=['POST', 'GET'])
def cat1_survey_page():
    message = ''
    first_name = ''
    last_name = ''
    email = ''
    radio_field = ''
    str_field = ''


    if request.method == 'POST':

        # check that we have all the required fields to append to file
        str_field = request.form['str_field']
        # remove special characters from input for security
        str_field = re.sub(r"[^a-zA-Z0-9]","",str_field)

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # optional fields
        if 'radio_field' in request.form:
            radio_field = request.form['radio_field']
        else:
            radio_field = 'NA'


        # check that essential fields have been filled
        message = ''
        missing_required_answers_list = []
            
        if str_field == '':
            missing_required_answers_list.append('Tells us more')
        if first_name == '':
            missing_required_answers_list.append('First name')
        if last_name == '':
            missing_required_answers_list.append('Last name')
        if email == '':
            missing_required_answers_list.append('Email')


        if len(missing_required_answers_list) > 0:
            # return back a string with missing fields
            message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>You missed the following question(s):</H3><font style="color:red;">'
            for ms in missing_required_answers_list:
                message += '<BR>' + str(ms)
            message += '</font></div>'
        
            return render_template('cat1.html',
                                    message = Markup(message),
                                    first_name = first_name,
                                    last_name = last_name,
                                    email = email,
                                    radio_field = radio_field,
                                    str_field = str_field)
        else:
            # append survey answers to data array
            survey_data.extend([first_name, last_name, email, str_field, radio_field])
            
            return render_template('cat2.html')

    return render_template('cat1.html',
                            message = Markup(message),
                            first_name = first_name,
                            last_name = last_name,
                            email = email,
                            radio_field = radio_field,
                            str_field = str_field)

@app.route("/", methods=['POST', 'GET'])
def cat2_survey_page():

    return ""
    


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)