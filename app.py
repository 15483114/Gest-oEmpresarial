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
        # verefica se os campos de pesquisa estão presentes
        str_field = request.form['str_field']
        first_name = request.form['first_name']
        last_name = request.form['last_name'] 
        email = request.form['email']
        if 'gender' in request.form:
            gender = request.form['gender']
        else:
            gender = 'NA'
        
        # verifica se os campos essênciais estão preenchidos
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
            # retorna uma string com os campos vazios
            message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>Você não preencheu os seguinte(s) campo(s):</H3><font style="color:red;">'
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
    


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)