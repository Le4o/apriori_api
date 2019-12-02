#PARTE1
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import numpy as np
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import os


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
print(itemsTotais)

porcentagemC = len(C)/itemsTotais
porcentagemB = len(B)/itemsTotais
porcentagemA = len(A)/itemsTotais

print(porcentagemA, porcentagemB, porcentagemC)

data.append(A)
data.append(B)
data.append(C)