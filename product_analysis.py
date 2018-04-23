#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 14:09:32 2018

@author: dbrevesf
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

def manipulate_date(day, month, year):

    d = None
    m = None
    y = None
    
    
    if(day == 1):
        d = "seg"
    elif(day == 2):
        d = "ter"
    elif(day == 3):
        d = "qua"
    elif(day == 4):
        d = "qui"
    elif(day == 5):
        d = "sex"
    elif(day == 6):
        d = "sab"
    elif(day == 7):
        d = "dom"
    else:
        d = "DIA ERRADO"
        
    if(month == 1):
        m = "jan"
    elif(month == 2):
        m = "fev"
    elif(month == 3):
        m = "mar"
    elif(month == 4):
        m = "abr"
    elif(month == 5):
        m = "mai"
    elif(month == 6):
        m = "jun"
    elif(month == 7):
        m = "jul"
    elif(month == 8):
        m = "ago"
    elif(month == 9):
        m = "set"
    elif(month == 10):
        m = "out"
    elif(month == 11):
        m = "nov"
    elif(month == 12):
        m = "dez"
    else:
        m = "MES ERRADO"
        
    if(year == 2016):
        y = "16"
    elif(year == 2017):
        y = "17"
    elif(year == 2018):
        y = "18"
    else:
        y = "ANO ERRADO"
    
    if(d and m and y):
        return d+m+y
    else:
        return "DATA ERRADA"
    
def divide_by_days(value, days):
    
    return value/days

def change_string(string):
    return string[3::]
    

def generate_plot(product_id, df, day):
    
    product = df.loc[df['ID'] == product_id]
    product = product.loc[product['DIA'] == day]
    x = product['DATA']
    y = product['VALOR']
    name = product['NOME'].values[0]
    plt.bar(x, y, align='center', label=name)
    plt.title('Vendas de %s por dia da semana' % (name))
    plt.xticks(fontsize=8, rotation=90)
    plt.legend(loc='upper left')
    plt.show()    
    
def get_product_info_by_day(df, product_id, day):
    
    product = df.loc[df['ID'] == product_id]
    product = product.loc[product['DIA'] == day]
    name = None
    if(product['NOME'].values.any()):
        name = product['NOME'].values[0]
    dict_return = None
    if(not product.empty):
        max_value = product.max()['VALOR']
        min_value = product.min()['VALOR']
        mean_value = product.mean()['VALOR']
        std_value = product.std()['VALOR']
        dict_return = {'id': product_id,
                       'name': name, 
                       'day': day,
                       'max': max_value,
                       'min': min_value,
                       'mean': mean_value,
                       'std': std_value
                       }
    return dict_return


def get_day_name(day_id):
    
    day_name = None
    if(day_id == 1):
        day_name = "Segunda-Feira"
    elif(day_id == 2):
        day_name = "Terça-Feira"
    elif(day_id == 3):
        day_name = "Quarta-Feira"
    elif(day_id == 4):
        day_name = "Quinta-Feira"
    elif(day_id == 5):
        day_name = "Sexta-Feira"
    elif(day_id == 6):
        day_name = "Sabado"
    else:
        day_name = "Domingo"
        
    return day_name


def get_dataset(path):
    
    data = pd.read_csv(path, sep=";", encoding='latin-1')
    data['DATA'] = data.apply(lambda row: manipulate_date(row['DIA'],
                                                          row['MES'],
                                                          row['ANO']), axis=1)
    return data
    
    
    
DATASET_PATH = "produtox_caseirox.csv"    
data = get_dataset(DATASET_PATH)
id_list = set(data['ID'].values)


# gerando graficos de vendas de produtos de toda a serie temporal
print("+ Gerando graficos de vendas de produtos de toda a serie temporal")
if not os.path.exists("curvas_por_produtos_geral"):
    print("- Criando diretorio")
    os.makedirs("curvas_por_produtos_geral")
    print("- Diretorio criado")
    
for product_id in id_list:
    print("- Buscando informacoes do produto: %s" % (product_id))
    product_data = data.loc[data['ID'] == product_id]
    if(not product_data.empty):
        print("- Produto %s encontrado" % (product_id))
        product_name = product_data['NOME'].values[0]
        plt.figure(figsize=(30,20))
        plt.suptitle(product_name, fontsize=16)
        x = product_data['DATA']
        y = product_data['VALOR']
        plt.bar(x,y)
        plt.xticks(fontsize=8, rotation=90)
        plt.title(product_name)
        plot_path = "curvas_por_produtos_geral/"+str(product_id)+".pdf"
        plt.savefig(plot_path)
        plt.close()
        print("- Grafico criado e armazenado em: %s" % (os.path.abspath(plot_path)))
    else:
        print("- Produto %s não encontrado" % (product_id))


# gerando graficos de vendas de produtos por mes
print("+ Gerando graficos de vendas de produtos por mês")
if not os.path.exists("curvas_por_produtos_por_mes"):
    print("- Criando diretorio")
    os.makedirs("curvas_por_produtos_por_mes")
    print("- Diretorio criado")
    
for product_id in id_list:
    print("- Buscando informacoes do produto: %s" % (product_id))
    product_data = data.loc[data['ID'] == product_id]
    if(not product_data.empty):
        print("- Produto %s encontrado" % (product_id))
        product_name = product_data['NOME'].values[0]
        plt.figure(figsize=(30,20))
        plt.suptitle(product_name, fontsize=16)
        x = product_data['DATA']
        x = x.apply(lambda row: change_string(row))
        y = product_data['VALOR']
        plt.bar(x,y)
        plt.xticks(fontsize=8, rotation=90)
        plt.title(product_name)
        plot_path = "curvas_por_produtos_por_mes/"+str(product_id)+".pdf"
        plt.savefig(plot_path)
        plt.close()
        print("- Grafico criado e armazenado em: %s" % (os.path.abspath(plot_path)))

# gerando graficos de vendas de produtos por dia
print("+ Gerando graficos de vendas de produtos por dia")
day_list = list(range(1, 7))
if not os.path.exists("curvas_por_produtos_por_dia"):
    print("- Criando diretorio")
    os.makedirs("curvas_por_produtos_por_dia")
    print("- Diretorio criado")
    
for product_id in id_list: 
    print("- Buscando informacoes do produto: %s" % (product_id))
    product_data = data.loc[data['ID'] == product_id]
    if(not product_data.empty):
        print("- Produto %s encontrado" % (product_id))
        product_name = product_data['NOME'].values[0]
        plt.figure(figsize=(30,20))
        plt.suptitle(product_name, fontsize=16)
        for day in day_list:
            print("- Buscando vendas do produto: %s para o dia %d" % (product_id, day))
            product_data_by_day = product_data.loc[product_data['DIA'] == day]
            if(not product_data_by_day.empty):
                print("- Venda de %s para o dia %d encontrada" % (product_id, day))
                plot_position = "32"+str(day)
                plt.subplot(plot_position)
                x = product_data_by_day['DATA']
                y = product_data_by_day['VALOR']
                plt.bar(x,y)
                plt.xticks(fontsize=8, rotation=90)
                plt.title(get_day_name(day))
        plot_path = "curvas_por_produtos_por_dia/"+str(product_id)+".pdf"
        plt.savefig(plot_path)
        plt.close()
        print("- Grafico criado e armazenado em: %s" % (os.path.abspath(plot_path)))

        