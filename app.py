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

    for dado in categoria_3_data :
        str_dados = str_dados + dado + ','

    str_dados = str_dados + '\n'

    with open(BASE_DIR + '/surveys/survey_samp_1.csv','a+') as myfile: # use a+ to append and create file if it doesn't exist
            myfile.write(str_dados)


# survey page
@app.route("/", methods=['POST', 'GET'])
@app.route("/cat1", methods=['POST', 'GET'])
def cat1():
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

            if aval_1_1 == '':
                missing_required_answers_list.append('Avaliação para pergunta 1.1')
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

                categoria_1_data.append(aval_1_1)
                categoria_1_data.append(aval_1_2)
                categoria_1_data.append(pergunta_1_1)
                categoria_1_data.append(pergunta_1_2)

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
    message = ''
    aval_2_1 = ''
    aval_2_2 = ''
    aval_2_3 = ''
    aval_2_4 = ''
    aval_2_5 = ''
    pergunta_2_1 = ''
    pergunta_2_2 = ''
    pergunta_2_3 = ''
    pergunta_2_4 = ''
    pergunta_2_5 = ''
    
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
            pergunta_2_1 = request.form['pergunta_2_1'].strip()
            pergunta_2_2 = request.form['pergunta_2_2'].strip()
            pergunta_2_3 = request.form['pergunta_2_3'].strip()
            pergunta_2_4 = request.form['pergunta_2_4'].strip()
            pergunta_2_5 = request.form['pergunta_2_5'].strip()

            # verifica se os campos essênciais estão preenchidos
            message = ''
            missing_required_answers_list = []
    
            if aval_2_1 == '':
                missing_required_answers_list.append('Avaliação para pergunta 2.1')
            if aval_2_2 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 2.2')
            if aval_2_3 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 2.3')
            if aval_2_4 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 2.4')
            if aval_2_5 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 2.5')

            if len(missing_required_answers_list) > 0:
                # retorna uma string com os campos vazios
                message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>Você não preencheu os seguinte(s) campo(s):</H3><font style="color:red;">'
                for ms in missing_required_answers_list:
                    message += '<BR>' + str(ms)
                message += '</font></div>'
            else:
                message = ''
                # Cria marcação de tempo para entrada

                categoria_2_data.clear()
            
                categoria_2_data.append(aval_2_1)
                categoria_2_data.append(aval_2_2)
                categoria_2_data.append(aval_2_3)
                categoria_2_data.append(aval_2_4)
                categoria_2_data.append(aval_2_5)
                categoria_2_data.append(pergunta_2_1)
                categoria_2_data.append(pergunta_2_2)
                categoria_2_data.append(pergunta_2_3)
                categoria_2_data.append(pergunta_2_4)
                categoria_2_data.append(pergunta_2_5)

                return redirect(url_for('cat3'))

    # show the form, it wasn't submitted
    return render_template('cat2.html',
                            message = Markup(message),
                            aval_2_1 = aval_2_1,
                            aval_2_2 = aval_2_2,
                            aval_2_3 = aval_2_3,
                            aval_2_4 = aval_2_4,
                            aval_2_5 = aval_2_5,
                            pergunta_2_1 = pergunta_2_1,
                            pergunta_2_2 = pergunta_2_2,
                            pergunta_2_3 = pergunta_2_3,
                            pergunta_2_4 = pergunta_2_4,
                            pergunta_2_5 = pergunta_2_5)

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
    pergunta_3_1 = ''
    pergunta_3_2 = ''
    pergunta_3_3 = ''
    pergunta_3_4 = ''
    pergunta_3_5 = ''
    pergunta_3_6 = ''
    pergunta_3_7 = ''
    pergunta_3_8 = ''
    message = ''
    

    if request.method == 'POST':

         if request.form['action'] == 'Para categoria 2':

            return redirect(url_for('cat2'))
         elif request.form['action'] == 'Submit':
            # verefica se os campos de pesquisa estão presentes
            aval_3_1 = request.form['aval_3_1']
            aval_3_2 = request.form['aval_3_2']
            aval_3_3 = request.form['aval_3_3']
            aval_3_4 = request.form['aval_3_4']
            aval_3_5 = request.form['aval_3_5']
            aval_3_6 = request.form['aval_3_6']
            aval_3_7 = request.form['aval_3_7']
            aval_3_8 = request.form['aval_3_8']
            pergunta_3_1 = request.form['pergunta_3_1'].strip()
            pergunta_3_2 = request.form['pergunta_3_2'].strip()
            pergunta_3_3 = request.form['pergunta_3_3'].strip()
            pergunta_3_4 = request.form['pergunta_3_4'].strip()
            pergunta_3_5 = request.form['pergunta_3_5'].strip()
            pergunta_3_6 = request.form['pergunta_3_6'].strip()
            pergunta_3_7 = request.form['pergunta_3_7'].strip()
            pergunta_3_8 = request.form['pergunta_3_8'].strip()

            # verifica se os campos essênciais estão preenchidos
            message = ''
            missing_required_answers_list = []
    
            if aval_3_1 == '':
                missing_required_answers_list.append('Avaliação para pergunta 3.1')
            if aval_3_2 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 3.2')
            if aval_3_3 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 3.3')
            if aval_3_4 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 3.4')
            if aval_3_5 == '':
                    missing_required_answers_list.append('Avaliação para pergunta 3.5')

            if len(missing_required_answers_list) > 0:
                # retorna uma string com os campos vazios
                message = '<div class="w3-row-padding w3-padding-16 w3-center"><H3>Você não preencheu os seguinte(s) campo(s):</H3><font style="color:red;">'
                for ms in missing_required_answers_list:
                    message += '<BR>' + str(ms)
                message += '</font></div>'
            else:                         
                categoria_3_data.clear()

                categoria_3_data.append(aval_3_1)
                categoria_3_data.append(aval_3_2)
                categoria_3_data.append(aval_3_3)
                categoria_3_data.append(aval_3_4)
                categoria_3_data.append(aval_3_5)
                categoria_3_data.append(aval_3_6)
                categoria_3_data.append(aval_3_7)
                categoria_3_data.append(aval_3_8)
                categoria_3_data.append(pergunta_3_1)
                categoria_3_data.append(pergunta_3_2)
                categoria_3_data.append(pergunta_3_3)
                categoria_3_data.append(pergunta_3_4)
                categoria_3_data.append(pergunta_3_5)
                categoria_3_data.append(pergunta_3_6)
                categoria_3_data.append(pergunta_3_7)
                categoria_3_data.append(pergunta_3_8)

                __salvar_dados_csv()

                return redirect(url_for('results'))


        # show the form, it wasn't submitted
    return render_template('cat3.html',
                    message = Markup(message),
                    aval_3_1 = aval_3_1,
                    aval_3_2 = aval_3_2,
                    aval_3_3 = aval_3_3,
                    aval_3_4 = aval_3_4,
                    aval_3_5 = aval_3_5,
                    aval_3_6 = aval_3_6,
                    aval_3_7 = aval_3_7,
                    aval_3_8 = aval_3_8,
                    pergunta_3_1 = pergunta_3_1,
                    pergunta_3_2 = pergunta_3_2,
                    pergunta_3_3 = pergunta_3_3,
                    pergunta_3_4 = pergunta_3_4,
                    pergunta_3_5 = pergunta_3_5,
                    pergunta_3_6 = pergunta_3_6,
                    pergunta_3_7 = pergunta_3_7,
                    pergunta_3_8 = pergunta_3_8)

@app.route("/results", methods=['POST', 'GET'])
def results():
    nome_examinador = id_data[1]
    email = id_data[3]
    nome_avaliado = id_data[2]
 
    cat_1_min = min(int(categoria_1_data[0]), int(categoria_1_data[1]))
    cat_1_max = max(int(categoria_1_data[0]), int(categoria_1_data[1]))
    cat_1_avg = round((int(categoria_1_data[0]) + int(categoria_1_data[1])) / 2, 3)

    cat_2_min = min(int(categoria_2_data[0]), int(categoria_2_data[1]), int(categoria_2_data[2]), int(categoria_2_data[3]), int(categoria_2_data[4]))
    cat_2_max = max(int(categoria_2_data[0]), int(categoria_2_data[1]), int(categoria_2_data[2]), int(categoria_2_data[3]), int(categoria_2_data[4]))
    cat_2_avg = round((int(categoria_2_data[0]) + int(categoria_2_data[1]) + int(categoria_2_data[2]) + int(categoria_2_data[3]) + int(categoria_2_data[4])) / 5, 3)

    cat_3_min = min(int(categoria_3_data[0]), int(categoria_3_data[1]), int(categoria_3_data[2]), int(categoria_3_data[3]), int(categoria_3_data[4]), int(categoria_3_data[5]), int(categoria_3_data[6]), int(categoria_3_data[7]))
    cat_3_max = max(int(categoria_3_data[0]), int(categoria_3_data[1]), int(categoria_3_data[2]), int(categoria_3_data[3]), int(categoria_3_data[4]), int(categoria_3_data[5]), int(categoria_3_data[6]), int(categoria_3_data[7]))
    cat_3_avg = round((int(categoria_3_data[0]) + int(categoria_3_data[1]) + int(categoria_3_data[2]) + int(categoria_3_data[3]) + int(categoria_3_data[4]) + int(categoria_3_data[5]) + int(categoria_3_data[6]) + int(categoria_3_data[7])) / 8, 3)

    avg_total = round((cat_1_avg + cat_2_avg + cat_3_avg) / 3, 3)

    horario = id_data[0]

    # show the form, it wasn't submitted
    return render_template('results.html',
                            nome_examinador = nome_examinador,
                            email = email,
                            nome_avaliado = nome_avaliado,
                            cat_1_min = cat_1_min,
                            cat_1_max = cat_1_max,
                            cat_1_avg = cat_1_avg,
                            cat_2_min = cat_2_min,
                            cat_2_max = cat_2_max,
                            cat_2_avg = cat_2_avg,
                            cat_3_min = cat_3_min,
                            cat_3_max = cat_3_max,
                            cat_3_avg = cat_3_avg,
                            avg_total = avg_total,
                            horario = horario)
    
    

# used only in local mode
if __name__=='__main__':
    app.run(debug=True)