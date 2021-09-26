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


palabrasGeneral = [' precios ' , 'precios ', 'precios ', ' precio ', 'precio ' , ' precio' , ' colores ', ' valor ', ' de segunda ' , ' baratos ',' barato ', ' economicos ' ,' y ']

def cleanKw(df):
    '''Nos permite limpiar los terminos de busqueda y prepararlos para la url'''
    #caracteres matchtype
    replaceList = ['"','+', '[', ']']
    #Palabras a excluir
    
   
    df1 = df.copy()
   
    df1['kwNoMatchType'] = df1['kwCopy'].copy()
   
    #Limpiamos caracteres relacionados al matchType
    for i in replaceList:
        df1['kwNoMatchType'] = df1['kwNoMatchType'].str.replace(i, '')

    df1['kwNoGeneralList'] = df1['kwNoMatchType'].copy()

    #Limpiamos palabras Generales
    for j in palabrasGeneral:
        df1['kwNoGeneralList'] = df1['kwNoGeneralList'].str.replace(j, ' ')
    
    # Borramos espacios en blanco en ambos lados 
    df1['kwClean'] = df1['kwNoGeneralList'].str.strip()
    # Remplazamos el espacio que separa por guión medio 
    df1['kwCleanSlash'] = df1['kwClean'].str.replace(' ','-')
    return df1


def armarCombinaciones(listaPalabras):
    '''Nos permite armar combinaciones de palabras agregando espacios antes, después, ambos y palabra original'''
    combinacionesPalabras = []
    for pal in listaPalabras: 
        nuevaCombinacion = " " + pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = " " +  pal 
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        combinacionesPalabras.append(pal)
    return combinacionesPalabras


#%%
# Accionable 
file_path = 'celuExcel.xlsx - celulares.csv'
file = readFile(file_path)

reducido = colsToUse(file)

reducidoLimpio = cleanKw(reducido)

reducidoLimpio.head()   




UrlPais = 'https://listado.mercadolibre.com.ar/'

reducidoLimpio['preUrl'] = UrlPais

reducidoLimpio['urlArmada'] = reducidoLimpio['preUrl'] + reducidoLimpio['kwCopy']
# %%

# %%

palabrasExcluir = ['precio', 'barato', 'peru']

def armarCombinaciones(listaPalabras):
    combinacionesPalabras = []
    for pal in listaPalabras: 
        nuevaCombinacion = " " + pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = " " +  pal 
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        combinacionesPalabras.append(pal)
    return combinacionesPalabras


combinacionesExcluir = armarCombinaciones(palabrasExcluir)

print(combinacionesExcluir)


# %%

# %%

# %%

# %%
