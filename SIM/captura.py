import requests as r
import pandas as pd

def captura():
    for i in range(10, 21):
        with(r.get("https://diaad.s3.sa-east-1.amazonaws.com/sim/Mortalidade_Geral_20" + str(i) + ".csv")) as req:
            file = open("./files/M_G20" + str(i) + ".csv", "wb")
            file.write(req.content)
            file.close()
captura() 

def filtragem(df):
    df['CODMUNOCOR'] = df['CODMUNOCOR'].astype(str)

    cities = {
        '351870': 'Guarujá',
        '354850': 'Santos',
        '355100': 'São Vicente',
        '351350': 'Cubatão',
        '354100': 'Praia Grande',
        '350635': 'Bertioga',
        '353110': 'Mongaguá',
        '352210': 'Itanhaém',
        '353760': 'Peruíbe'
    }


    df['CIDADE'] = df['CODMUNOCOR'].map(lambda x: cities[x] if x in cities else None)
    return df


fdf = pd.DataFrame()
for i in (range(10,21)):
    try:
        df = pd.read_csv("./files/M_G20"+ str(i) +".csv", encoding = "ISO-8859-1", on_bad_lines='skip', sep=';',  usecols=['LINHAA','LINHAB','LINHAC','LINHAD','LINHAII','IDADE','CIRURGIA','ESC2010','OCUP','RACACOR', 'SEXO', 'CODMUNOCOR', 'ESTCIV'])
    except:
        df = pd.read_csv("./files/M_G20"+ str(i) +".csv", encoding = "ISO-8859-1", on_bad_lines='skip', sep=';',  usecols=['LINHAA','LINHAB','LINHAC','LINHAD','LINHAII','IDADE','CIRURGIA','OCUP','RACACOR', 'SEXO', 'CODMUNOCOR', 'ESTCIV'])
        df['ESC2010'] = ''
    df['ANO'] = "20" + str(i)
    fdf = pd.concat([fdf, df], axis=0).reset_index(drop=True)
    print("20" + str(i) + " processado.")

filtragem(fdf) #elimina todos os casos fora da baixada e acrescenta uma coluna com o nome da cidade
fdf = fdf[fdf['CIDADE'].notna()]
fdf.to_csv("Mortalidade2010_2020.csv", index=False, encoding='utf-8-sig', sep=',')
print("Encerrado.")
