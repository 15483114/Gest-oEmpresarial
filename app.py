from flask import Flask, session, app, render_template, request, Markup, url_for, redirect
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
categoria_3_data = []

def __salvar_dados_csv():
    str_dados = ''

    for dado in id_data :
        str_dados = str_dados + dado + ','

    for dado in categoria_1_data :
        str_dados = str_dados + dado + ','

    for dado in categoria_2_data :
        str_dados = str_dados + dado + ','
    str_dados = str_dados + '\n'

    with open(BASE_DIR + '/surveys/survey_samp_1.csv','a+') as myfile: # use a+ to append and create file if it doesn't exist
            myfile.write(str_dados)


# survey page
@app.route("/", methods=['POST', 'GET'])
@app.route("/cat1", methods=['POST', 'GET'])
def cat1():
    message = ''
    if len(id_data) == 0 :
        nome_examinador = ''
        nome_avaliado = ''
        email = ''
        genero = ''
        pergunta_1_1 = ''
        aval_1_1 = ''
        pergunta_1_2 = ''
        aval_1_2 = ''
    else :
        nome_examinador = id_data[1]
        nome_avaliado = id_data[2]
        email = id_data[3]
        genero = id_data[4]
        pergunta_1_1 = categoria_1_data[0]
        aval_1_1 = categoria_1_data[1]
        pergunta_1_2 = categoria_1_data[2]
        aval_1_2 = categoria_1_data[3]


    if request.method == 'POST':
        if request.form['action'] == 'Para categoria 2':
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

                # Limpa a lista antes de adicionar os novos valores
                id_data.clear()
                categoria_1_data.clear()

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

                return redirect(url_for('cat2'))
    
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


@app.route("/cat2", methods=['POST', 'GET'])
def cat2():
    aval_2_1 = ''
    aval_2_2 = ''
    aval_2_3 = ''
    aval_2_4 = ''
    aval_2_5 = ''
    message = ''
    if request.method == 'POST':
        if request.form['action'] == 'Para categoria 1':

            return redirect(url_for('cat1'))
        elif request.form['action'] == 'Para categoria 3':
            # verefica se os campos de pesquisa estão presentes
            aval_2_1 = request.form['aval_2_1']
            aval_2_2 = request.form['aval_2_2']
            aval_2_3 = request.form['aval_2_3']
            aval_2_4 = request.form['aval_2_4']
            aval_2_5 = request.form['aval_2_5']

            # verifica se os campos essênciais estão preenchidos
            
            missing_required_answers_list = []
    
            if aval_2_1 == '':
                missing_required_answers_list.append('Pergunta 2.1')
            if aval_2_2 == '':
                    missing_required_answers_list.append('Pergunta 2.2')
            if aval_2_3 == '':
                    missing_required_answers_list.append('Pergunta 2.3')
            if aval_2_4 == '':
                    missing_required_answers_list.append('Pergunta 2.4')
            if aval_2_5 == '':
                    missing_required_answers_list.append('Pergunta 2.5')

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
            
                categoria_2_data.append(aval_2_1)
                categoria_2_data.append(aval_2_2)
                categoria_2_data.append(aval_2_3)
                categoria_2_data.append(aval_2_4)
                categoria_2_data.append(aval_2_5)

                __salvar_dados_csv()

                return redirect(url_for('cat3'))

    # show the form, it wasn't submitted
    return render_template('cat2.html',
                            message = Markup(message),
                            aval_2_1 = aval_2_1,
                            aval_2_2 = aval_2_2,
                            aval_2_3 = aval_2_3,
                            aval_2_4 = aval_2_4,
                            aval_2_5 = aval_2_5)

@app.route("/cat3", methods=['POST', 'GET'])
def cat3():
    aval_3_1 = ''
    aval_3_2 = ''
    aval_3_3 = ''
    aval_3_4 = ''
    aval_3_5 = ''
    aval_3_6 = ''
    aval_3_7 = ''
    aval_3_8 = ''
    message = ''


    if request.method == 'POST':
        categoria_3_data.append(aval_3_1)
        categoria_3_data.append(aval_3_2)
        categoria_3_data.append(aval_3_3)
        categoria_3_data.append(aval_3_4)
        categoria_3_data.append(aval_3_5)
        categoria_3_data.append(aval_3_6)
        categoria_3_data.append(aval_3_7)
        categoria_3_data.append(aval_3_8)
        print()

    # show the form, it wasn't submitted
    return render_template('cat3.html')
    
    


# used only in local mode
if __name__=='__main__':
    app.run(debug=True)