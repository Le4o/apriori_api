#PARTE1
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from abc import ABC, abstractmethod
import os

#PARTE2
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'XYZ')

@app.route('/curva', methods=['GET'])
def curva_abc():
    data = []

    store_data = pd.read_csv('sale.csv')
    df = pd.DataFrame(store_data, columns=['descricao'])

    itens = [df.loc[i, 'descricao'] for i in range(df['descricao'].count())]

    itens = sorted(itens)

    totalItens = df['descricao'].count()
    cat_C = (1/totalItens)
    cat_B = (2/totalItens)
    cat_A = (3/totalItens)

    anterior = itens[0]
    count = 1
    A = []
    B = []
    C = []
    
    for item in itens:
        if item == anterior:
            count+=1
        else:

            frequencia = count/totalItens
            #print(frequencia)
            if frequencia >= cat_A:

                C.append([anterior, 'A', frequencia])
            elif frequencia <= cat_B and frequencia > cat_C:
                B.append([anterior,'B', frequencia])
            elif frequencia <= cat_C:
                A.append([anterior, 'C', frequencia])

            anterior = item
            count=1

    itemsTotais = len(C) + len(B) + len(A)
    
    porcentagemC = [len(C)/itemsTotais]
    porcentagemB = [len(B)/itemsTotais]
    porcentagemA = [len(A)/itemsTotais]

    data.append(porcentagemC)
    data.append(porcentagemB)
    data.append(porcentagemA)

    data.append(A)
    data.append(B)
    data.append(C)
    return jsonify({'data': data})

#PARTE3
@app.route('/apriori', methods=['GET'])
def getapriori():

    store_data = pd.read_csv('sale.csv')

    df = pd.DataFrame(store_data, columns=['descricao', 'id_compra'])

    records = []    
    buy = []

    group_id = df.loc[0, 'id_compra']

    for i in range(600):
        if df.loc[i, 'id_compra'] != group_id:
            group_id = df.loc[i, 'id_compra']
            records.append(buy)
            buy = []
            buy.append(df.loc[i, 'descricao'])
        else:
            buy.append(df.loc[i, 'descricao'])

    te = TransactionEncoder()
    te_ary = te.fit(records).transform(records)
    df2 = pd.DataFrame(te_ary, columns=te.columns_)

    data = apriori(df2, min_support=0.04, use_colnames=False)
    data_list = data.values.tolist()
    
    for x in range(len(data_list)):
        
        for _ in range(2):
            data_list[x][1] = list(data_list[x][1])
            val = np.float32(data_list[x][0]).item()
            data_list[x][0] = val

            for z in range(len(data_list[x][1])):
                val = np.uint32(data_list[x][1][z]).item()
                data_list[x][1][z] = val
    
    return jsonify({'data': data_list})


#PARTE4
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='127.0.0.1', port=port)



