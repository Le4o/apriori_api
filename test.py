from abc_analysis import abc_analysis, abc_plot
import pandas as pd

dict_ = {}

store_data = pd.read_csv('sale.csv')
df = pd.DataFrame(store_data, columns=['descricao'])

itens = []
for i in range(df['descricao'].count()):
    itens.append(df.loc[i, 'descricao'])

id_ = 0
for nome in itens:
    if nome not in dict_:
        dict_[nome] = id_
    id_+=1

lista2 = []
for nome in itens:
    lista2.append(dict_[nome])

dctAnalysis = abc_analysis(lista2)

print(dctAnalysis)

dctAnalysis = abc_analysis(lista2, True)
