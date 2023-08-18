import pandas as pd
from dicionarios import estciv, esc2010, sexo

#region classes
def faixa_etaria(n):
    try:
        n = int(n)
    except:
        n = n.split('.')[0]
        if (n == ''):
            n = 0
    faixa = [(i*5, i*5+4) for i in range(20)] 
    for i, j in faixa:
        if i <= int(n) <= j:
            return i

def idade(df): #substitui a colula da idade pelo valor da faixa etaria
    df = df.rename(columns={'IDADE' : 'FAIXA_ETARIA'})
    age = df['FAIXA_ETARIA'].astype(str)
    for i in range(len(age)):
        f = age[i][0]
        if (int(f) < 4):
           df.iloc[i,0] = '0'
        elif(int(f) > 4):
            df.iloc[i,0] = '+99'
        else:
            s = age[i][1:]
            df.iloc[i,0] = str(faixa_etaria(s))
    return df    

def cargos(df): #com base nos valores do cbo, altera a coluna da ocupação e gera um novo csv
    df = df.reset_index()
    dfCargos = pd.read_csv('./SIM/cbo.txt', sep=',', encoding = "utf-8", on_bad_lines='skip', usecols=[0,1], header=None)

    for i in range(len(df)):
        v = False
        try:
            cargo = str(int(df.loc[i,'OCUP']))
        except:
            df.loc[i,'OCUP'] = 'Dado Invalido.'
            continue
        for j in range(len(dfCargos)):
            try:
                cbo =  dfCargos[1][j].replace("-",'') 
                if (len(cargo) == 5):
                    cargo = '0' + cargo
            except:
                continue

            if (cargo == cbo):
                v = True
                df.loc[i,'OCUP'] = dfCargos[0][j].strip().replace('"', '')
                break

    if (v == False):
        df.loc[i,'OCUP'] = 'Ignorado.'
    df.to_csv("./dados_preparados_SIM.csv", index=False, encoding='utf-8-sig', sep=',')

def substituir(coluna, dicionario):
    df[coluna] = df[coluna].astype(str)
    if(coluna =='SEXO'):
        df[coluna] = df[coluna].map(lambda x: dicionario[x] if x in sexo else 'Dado Incorreto')
    else:
        df[coluna] = df[coluna].map(lambda x: dicionario[x[0]] if x[0] in estciv else 'Dado Incorreto')
#endregion

df = pd.read_csv('./SIM/Mortalidade2010_2020.csv')

df = idade(df)
df[['LINHAA', 'LINHAB', 'LINHAC', 'LINHAD']] = df[['LINHAA', 'LINHAB', 'LINHAC', 'LINHAD']].astype(str)
cols = ['LINHAA', 'LINHAB', 'LINHAC', 'LINHAD']
condicao = df[cols].apply(lambda col: col.str.contains('*I21', regex=False)).any(axis=1) #Isolando casos de Infarto Agudo no Miocárdio
df = df[condicao]
substituir('SEXO', sexo)
substituir('ESC2010', esc2010)
substituir('ESTCIV', estciv)


cargos(df)
print('Encerrado.')

