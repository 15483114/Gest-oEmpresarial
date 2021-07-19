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

id_data = []
categoria_1_data = []
categoria_2_data = []

def __salvar_dados_csv():
    str_dados = ''

    for dado in id_data :
        str_dados = str_dados + dado + ','

    for dado in categoria_1_data :
        str_dados = str_dados + dado + ','

    str_dados = str_dados + '\n'

    with open(BASE_DIR + '/surveys/survey_samp_1.csv','a+') as myfile: # use a+ to append and create file if it doesn't exist
            myfile.write(str_dados)


# survey page
@app.route("/", methods=['POST', 'GET'])
def cat1_survey_page():
    message = ''
    nome_examinador = ''
    nome_avaliado = ''
    email = ''
    genero = ''
    pergunta_1_1 = ''
    aval_1_1 = ''
    pergunta_1_2 = ''
    aval_1_2 = ''

    if request.method == 'POST':
        # verefica se os campos de pesquisa estão presentes
        nome_examinador = request.form['nome_examinador'].strip()
        nome_avaliado = request.form['nome_avaliado'].strip()
        email = request.form['email'].strip()
        genero = request.form['genero'].strip()
        pergunta_1_1 = request.form['pergunta_1_1'].strip()
        aval_1_1 = request.form['aval_1_1']
        pergunta_1_2 = request.form['pergunta_1_2'].strip()
        aval_1_2 = request.form['aval_1_2']
        
        # verifica se os campos essênciais estão preenchidos
        message = ''
        missing_required_answers_list = []
        if nome_examinador == '':
            missing_required_answers_list.append('Nome do examinador')
        if nome_avaliado == '':
            missing_required_answers_list.append('Nome do avaliado')
        if email == '':
            missing_required_answers_list.append('Email do examinador')
        if genero == '':
            missing_required_answers_list.append('Genêro do examinador')

        if pergunta_1_1 == '':
            missing_required_answers_list.append('Pergunta 1.1')
        if aval_1_1 == '':
            missing_required_answers_list.append('Avaliação para pergunta 1.1')
        if pergunta_1_2 == '':
            missing_required_answers_list.append('Pergunta 1.2')
        if aval_1_2 == '':
            missing_required_answers_list.append('Avaliação para pergunta 1.2')
        

        if len(missing_required_answers_list) > 0:
            # retorna uma string com os campos vazios
            message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>Você não preencheu os seguinte(s) campo(s):</H3><font style="color:red;">'
            for ms in missing_required_answers_list:
                message += '<BR>' + str(ms)
            message += '</font></div>'
        else:
            message = ''
            # Cria marcação de tempo para entrada
            entry_time = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            
            id_data.append(entry_time)
            id_data.append(nome_examinador)
            id_data.append(nome_avaliado)
            id_data.append(email)
            id_data.append(genero)

            categoria_1_data.append(pergunta_1_1)
            categoria_1_data.append(aval_1_1)
            categoria_1_data.append(pergunta_1_2)
            categoria_1_data.append(aval_1_2)

            __salvar_dados_csv()
            return render_template('cat2.html')
    
    return render_template('cat1.html',
                            message = Markup(message),
                            nome_examinador = nome_examinador,
                            nome_avaliado = nome_avaliado,
                            email = email,
                            genero = genero,
                            pergunta_1_1 = pergunta_1_1,
                            aval_1_1 = aval_1_1,
                            pergunta_1_2 = pergunta_1_2,
                            aval_1_2 = aval_1_2)

@app.route("/", methods=['POST', 'GET'])
def cat2_survey_page():

    return ""
    


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)