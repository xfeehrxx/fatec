import requests as r
import pandas as pd

def captura():
    for i in range(10, 21):
        with(r.get("https://diaad.s3.sa-east-1.amazonaws.com/sim/Mortalidade_Geral_20" + str(i) + ".csv")) as req:
            file = open("SIM/files/M_G20" + str(i) + ".csv", "wb")
            file.write(req.content)
            file.close()
captura() 

fdf = pd.DataFrame()
for i in (range(10,21)):
    try:
        df = pd.read_csv("SIM/files/M_G20"+ str(i) +".csv", encoding = "ISO-8859-1", on_bad_lines='skip', sep=';',  usecols=['LINHAA','LINHAB','LINHAC','LINHAD','LINHAII','IDADE','CIRURGIA','ESC2010','OCUP','RACACOR', 'SEXO', 'CODMUNOCOR'])
    except:
        df = pd.read_csv("SIM/files/M_G20"+ str(i) +".csv", encoding = "ISO-8859-1", on_bad_lines='skip', sep=';',  usecols=['LINHAA','LINHAB','LINHAC','LINHAD','LINHAII','IDADE','CIRURGIA','OCUP','RACACOR', 'SEXO', 'CODMUNOCOR'])
        df['ESC2010'] = ''
    df['ANO'] = "20" + str(i)
    fdf = pd.concat([fdf, df], axis=0).reset_index(drop=True)
    print("20" + str(i) + " processado.")
fdf.to_csv("Mortalidade2010_2020.csv", index=False, encoding='utf-8-sig', sep=',')
print("Encerrado.")

