#%%
from os import replace
import pandas as pd

def readFile(file_path):
    try:
        df2 = pd.read_csv(file_path)
        print('csv')
    except:
        try: 
            df2 = pd.read_excel(file_path)
            print('excel')
        except:
            print('not file found')
    return df2

def colsToUse(df1):
    cols_to_use = ['Campaña', 'Grupo de anuncios', 'Palabra clave', 'URL final', 'Estado de la palabra clave']
    df2 = df1[cols_to_use]
    df2['adgroupCopy'] = df2['Grupo de anuncios'].copy()
    df2['kwCopy'] = df2['Palabra clave'].copy()

    return df2

def cleanKw(df):
    '''Nos permite limpiar los terminos de busqueda y prepararlos para la url'''
    #Limpiamos caracteres relacionados al matchType
    replaceList = ['"','+', '[', ']']
    df1 = df.copy()
    for i in replaceList:
        df1['kwCopy'] = df1['kwCopy'].str.replace(i, '')
    # Borramos espacios en blanco en ambos lados 
    df1['kwCopy'] = df1['kwCopy'].str.strip()
    # Remplazamos el espacio que separa por guión medio 
    df1['kwCopy'] = df1['kwCopy'].str.replace(' ','-')
    return df1



#%%
# Accionable 
file_path = 'celuExcel.xlsx - celulares.csv'
file = readFile(file_path)

reducido = colsToUse(file)

reducidoLimpio = cleanKw(reducido)

reducidoLimpio.head()   

# %%
print(reducido.head())
reducido.info()
# %%
