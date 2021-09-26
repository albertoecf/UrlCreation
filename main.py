#%%

# INPUT : DESCARGAR DESDE GOOGLE ADS A NIVEL ADGROUP 
# OUTPUT : DEVUELVE UNA URL PARA CADA KW 

# 0) Importamos librerias necesarias 
import pandas as pd
# para usar en google Colab y poder descargar archivos 
# from google.colab import files


#1) DEFINIMOS FUNCIONES 

def readFile(file_path):
    try:
        df2 = pd.read_csv(file_path, skiprows=2)
        print('csv')
    except:
        try: 
            df2 = pd.read_excel(file_path, skiprows=2)
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



def cleanKwMatchType(df):
    '''Nos permite limpiar los terminos de busqueda según matchType'''
    #caracteres matchtype
    replaceList = ['"','+', '[', ']']
    #Palabras a excluir
    
   
    df1 = df.copy()
   
    df1['kwNoMatchType'] = df1['kwCopy'].copy()
   
    #Limpiamos caracteres relacionados al matchType
    for i in replaceList:
        df1['kwNoMatchType'] = df1['kwNoMatchType'].str.replace(i, '')

    return df1 

def cleanKwGeneral(df, lista):
    '''Nos permite limpiar los terminos de busqueda según palabras no deseadas. '''
    df1 = df.copy()
    df1['kwNoGeneralList'] = df1['kwNoMatchType'].copy()

    #Limpiamos palabras Generales
    for j in lista:
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
# 2) EJECUCIÓN 

# 2.1) Leemos el archivo 

file_path = 'Informe de palabras clave de búsqueda (6).csv'
file = readFile(file_path)

# 2.2) Seleccionamos las columnas de interes
reducido = colsToUse(file)

#2.3) Limpiamos los caracteres relacionados al matchtype
reducidoNoMatchType = cleanKwMatchType(reducido)

# 2.4) Armamos lista de palabras no deseadas

palabrasExcluir = ['precios','precio', 'valor', 'de segunda', 'baratos' , 'barato', 'economicos', 'economico', 'nuevos', 'nuevo', 'liberados', 'liberado', ' y ', ' en ', ' de ', ' a ', 'ofertas', 'oferta', 'promociones' , 'promocion', 'peru', 'colombia', 'mexico', 'chile','uruguay', 'salta', 'cordoba', 'bogota', 'rosario', ' del ']

# 2.5) Arma lista de combinaciones agregando espacios antes después y ambas 
combinacionesExcluir = armarCombinaciones(palabrasExcluir)

# 2.6) con la lista generada en 2.5) limpiamos las kw y reemplazamos espacio por - 
reducidoLimpio = cleanKwGeneral(reducidoNoMatchType, combinacionesExcluir)

# 2.7) Seleccionamos la url con la que vamos a armar las urlFinales (listado y por pais)
UrlPais = 'https://listado.mercadolibre.com.ar/'

# 2.8) Armamos la url asociada a cada KW
reducidoLimpio['preUrl'] = UrlPais
reducidoLimpio['urlArmada'] = reducidoLimpio['preUrl'] + reducidoLimpio['kwCleanSlash']


# 3) OUTPUT : Van a ser dos archivos, uno de control, dónde podemos comparar cada kw original con la final. Y otro archivo directo para cargar con las columnas necesarias
control = reducidoLimpio.dropna().copy()
cargar = reducidoLimpio[['Campaña', 'Grupo de anuncios', 'Palabra clave', 'urlArmada']].dropna().copy()

#%%
# 3.1) Para usar en colab : 

# 3.2) Remplazamos con el nombre de la vertical y pais

Vertical = 'Celulares'
Pais = 'MLA'

# 3.3) Arma el nombre de archivo 
nombreDescarga = Vertical + "_" + Pais + '.xlsx'

# 3.4) Nos descarga el archivo 
#cargar.to_excel(nombreDescarga)
#files.download(nombreDescarga)




# %%



