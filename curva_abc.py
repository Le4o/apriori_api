import pandas as pd

data = []

store_data = pd.read_csv('sale.csv')
df = pd.DataFrame(store_data, columns=['descricao'])

itens = [df.loc[i, 'descricao'] for i in range(df['descricao'].count())]

itens = sorted(itens)

totalItens = df['descricao'].count()
cat_A = (2/totalItens)
cat_B = (3/totalItens)
cat_C = (5/totalItens)

print(cat_A)
print(cat_B)
print(cat_C)

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
        if frequencia >= cat_C:
            C.append([anterior, 'C', frequencia])
        elif frequencia >= cat_B and frequencia < cat_A:
            B.append([anterior,'B', frequencia])
        elif frequencia <= cat_A:
            A.append([anterior, 'A', frequencia])

        anterior = item
        count=1

data.append(A)
data.append(B)
data.append(C)

print(data)

