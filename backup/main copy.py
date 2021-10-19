# %%
# Configuración :
# 3.1) Para usar en colab :
# 3.2) Remplazamos con el nombre de la vertical y pais
from os import rename
import pandas as pd
Vertical = 'AccVehiculos'
Pais = 'MLA'
# 2.7) Seleccionamos la url con la que vamos a armar las urlFinales (listado y por pais)
UrlPais = 'https://listado.mercadolibre.com.ar/'
# 3.3) Arma el nombre de archivo y el de control
nombreDescarga = Vertical + "_" + Pais + '.xlsx'
nombreDescargaControl = Vertical + "_" + Pais +'Control' +'.xlsx'
# 2.4) Armamos lista de palabras no deseadas
palabrasExcluir = ['precios', 'precio', 'valor', 'de segunda', 'baratos', 'barato', 'economicos', 'economico', 'nuevos', 'nuevo', 'liberados', 'liberado', ' y ', ' en ',
                   ' de ', ' a ', 'ofertas', 'oferta', 'promociones', 'promocion', 'peru', 'colombia', 'mexico', 'chile', 'uruguay', 'salta', 'cordoba', 'bogota', 'rosario', ' del ']

# INPUT : DESCARGAR DESDE GOOGLE ADS A NIVEL ADGROUP
# OUTPUT : DEVUELVE UNA URL PARA CADA KW

# 0) Importamos librerias necesarias
# para usar en google Colab y poder descargar archivos
# from google.colab import files


# 1) DEFINIMOS FUNCIONES

def readFile(file_path):
    try:
        df2 = pd.read_csv(file_path, skiprows=2)

        print('csv')
        return df2
    except:
        try:
            df2 = pd.read_excel(file_path, skiprows=2)
            print('excel')
            return df2
        except:
            print('not file found')


def colsToUse(df1):
    cols_to_use = ['Campaña', 'Grupo de anuncios',
                   'Palabra clave', 'URL final', 'Estado de la palabra clave']
    df2 = df1[cols_to_use]
    df2['adgroupCopy'] = df2['Grupo de anuncios'].copy()
    df2['kwCopy'] = df2['Palabra clave'].copy()

    return df2


def cleanKwMatchType(df):
    '''Nos permite limpiar los terminos de busqueda según matchType'''
    # caracteres matchtype
    replaceList = ['"', '+', '[', ']']
    # Palabras a excluir
    df1 = df.copy()
    df1['kwNoMatchType'] = df1['kwCopy'].copy()
    # Limpiamos caracteres relacionados al matchType
    for i in replaceList:
        df1['kwNoMatchType'] = df1['kwNoMatchType'].str.replace(i, '')
    return df1


def cleanKwGeneral(df, lista):
    '''Nos permite limpiar los terminos de busqueda según palabras no deseadas. '''
    df1 = df.copy()
    df1['kwNoGeneralList'] = df1['kwNoMatchType'].copy()
    # Limpiamos palabras Generales
    for j in lista:
        df1['kwNoGeneralList'] = df1['kwNoGeneralList'].str.replace(j, ' ')
    # Borramos espacios en blanco en ambos lados
    df1['kwClean'] = df1['kwNoGeneralList'].str.strip()
    # Remplazamos el espacio que separa por guión medio
    df1['kwCleanSlash'] = df1['kwClean'].str.replace(' ', '-')
    return df1


def armarCombinaciones(listaPalabras):
    '''Nos permite armar combinaciones de palabras agregando espacios antes, después, ambos y palabra original'''
    combinacionesPalabras = []
    for pal in listaPalabras:
        nuevaCombinacion = " " + pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = " " + pal
        combinacionesPalabras.append(nuevaCombinacion)
        nuevaCombinacion = pal + " "
        combinacionesPalabras.append(nuevaCombinacion)
        combinacionesPalabras.append(pal)
    return combinacionesPalabras


def armarFiltros(df1):
    '''Nos permite armar la lógica para filtrar los adgroups'''
    try:
        df2 = df1.copy()
        df2['COMP'] = df2['Grupo de anuncios'].str.startswith('COMP_')
        df2['Mpura'] = df2['Grupo de anuncios'].str.startswith('MARC_Pura')
        df2['To'] = df2['Grupo de anuncios'].str.contains('_TO')
        return df2
    except:
        print('Fallo armarFiltros')

def adgroupsCambiar(df2):
    """ Eliminamos los adroups que arrancan por COMP_ y los que (arrancan por MARC_Pura y no contienen _TO_ """
    try:
        df3 = df2.copy()
        df3 = df3[df3['COMP']==False].copy()
        df3['Borrar'] = (df3['Mpura']==True)&(df3['To']==False)
        df4 = df3[df3['Borrar']==False].copy()
        return df4
    except:
        print('NO SE ENCONTRARON ADGROUPS FILTRANDO POR COMP Y MPURA')

#Validaciones
def adgroupsCambiarCount(df2):
    """Contar cuantos adgroup tienen Marca Pura y no tienen TO ||contar cuantas comp hay """

    tot = len(df2.index)
    comp= (len(df2[df2['COMP']==True]))
    aux = df2.copy()  
    aux['Borrar'] = (aux['Mpura']==True)&(aux['To']==False)
    MpurayTo = len(aux[aux['Borrar']==True])
    cantBorrar = comp + MpurayTo
    cantQuedarse = tot - comp - MpurayTo

    print('Total de adgroups'+ " " + str(tot))
    print('Total de adgroups que deberían borrarse por ser Pura y no TO'+" "+str(MpurayTo))
    print('Total de adgroups que deberían borrarse por competencia' + " " +str(comp))
    print('Cantidad de adgroups totales a borrar' + " " +str(cantBorrar))
    print('AdGroups que deberían cambiarse - cantidad de filas que debería tener el archivo final')
    print('Cantidad de adgroups a cambiar' +str(cantQuedarse))



# %%
# 2) EJECUCIÓN
# 2.1) Leemos el archivo
file_path = 'Informe de palabras clave de búsqueda (6).csv'
file = readFile(file_path)
# 2.2) Seleccionamos las columnas de interes
reducido = colsToUse(file)
# 2.3) Limpiamos los caracteres relacionados al matchtype
reducidoNoMatchType = cleanKwMatchType(reducido)
# 2.5) Arma lista de combinaciones agregando espacios antes después y ambas
combinacionesExcluir = armarCombinaciones(palabrasExcluir)
# 2.6) con la lista generada en 2.5) limpiamos las kw y reemplazamos espacio por -
reducidoLimpio = cleanKwGeneral(reducidoNoMatchType, combinacionesExcluir)
# 2.8) Armamos la url asociada a cada KW
reducidoLimpio['preUrl'] = UrlPais
reducidoLimpio['urlArmada'] = reducidoLimpio['preUrl'] + reducidoLimpio['kwCleanSlash']
# 3) OUTPUT : Van a ser dos archivos, uno de control, dónde podemos comparar cada kw original con la final. Y otro archivo directo para cargar con las columnas necesarias
control = reducidoLimpio.dropna().copy()
#%%
filtrosControl = armarFiltros(control)
#cargar = reducidoLimpio[['Campaña', 'Grupo de anuncios','Palabra clave', 'urlArmada']].dropna().copy()


filtrosControl.head()
revisar = adgroupsCambiar(filtrosControl)
cargar = revisar[['Campaña','Grupo de anuncios', 'Palabra clave','urlArmada']].copy()

#%%
cargarFinal = cargar.rename(columns={'Campaña':'Campaign','Grupo de anuncios':'Ad Group', 'Palabra clave':'Keyword','urlArmada':'Final URL'}).copy()


# 3.1) Para usar en colab :
# 3.4) Nos descarga el archivo
#cargarFinal.to_excel(nombreDescarga)
# files.download(nombreDescarga)
#revisar.to_excel(nombreDescargaControl)
# files.download(nombreDescargaControl)


#Celda control 
adgroupsCambiarCount(filtrosControl)






