#PARTE1
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import os

#PARTE2
app = Flask(__name__)

#PARTE3
@app.route('/api/apriori', methods=['GET'])
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
        for y in range(2):
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



