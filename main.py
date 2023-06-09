# librerias y modulos a utilizar
from fastapi import FastAPI
import pandas as pd, numpy as np
from statistics import mode
from collections import Counter
import RecomendacionML as R

#objeto de la clase
app = FastAPI()
# datos a utilizar
data = pd.read_csv('datasets/movies.csv')
# nombre de las plataformas
webs=['amazon','disney','hulu','netflix']

#rura inicial
@app.get('/')
def index():
    return {'saludo': 'bienbenido a la api de peliculas y series por Elmer Daza',
    'contacto':'elmer-daza@hotmail.com',
    'redes':{'linkedin': 'linkedin.com/in/elmer-daza-207a02171/',
            'github':'github.com/ElmerDaza'
        }
    }

#devuelve cantidad de peliculas de acuerdo con los filtros
@app.get('/get_score_count/{platform}/{scored}/{year}')
def get_score_count(platform, scored, year):
    """Cantidad de películas por plataforma con un puntaje 
    mayor a XX en determinado año 
    """
    #verificar que los datos sean validos
    try:
        scored=float(scored)
        year = int(year)
    except:
        #en caso que los datos sean incorectos se envia el mensaje
        resp={'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
        return resp
    #validar que la plataforma sea correcta para hacer el filtro
    if platform in webs:
        #filtro
        respuesta = data.query(
            'score > @scored and release_year == @year and type == "movie" and ID.str.split().str.get(0).str[0] == @platform[0]')
        #remplazar valores nulos por ''
        respuesta = respuesta.replace(np.nan, '')
        #respuesta
        resp = {platform: int(respuesta['ID'].count())}
        
    else:
        #si la plataforma no es correcta devuelve el siguiente mensaje
        resp={'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
    return resp

# cantidad de peliculas por
@app.get('/get_count_platform/{platform}')
def get_count_platform(platform):
    """
    Cantidad de películas por plataforma con filtro de PLATAFORMA. 
    """
    #verificar que la plataforma sea correcta
    if platform in webs:
        #registros correspondientes a platform y que su type sea movie
        cantidad=data.query(
            'ID.str.split().str.get(0).str[0] == @platform[0] and type == "movie"')
    else:
        #se retorna el error en caso de no existir la plataforma
        return {'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
    #retornar la cantidad de registros
    return {platform:int(cantidad['ID'].count())}


@app.get('/get_actor/{platform}/{year}')
def get_actor(platform, year):
    """
    Actor que más se repite según plataforma y año. 
    """
    #comprobar que el año sea entro
    try:
        year=int(year)
    except:
        # de no ser un numero entro re retorna el siguiente mensaje
        return {'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
    # verificar que la plataforma sea correcta
    if platform in webs:
        #obtener todos los actores de ese año de la plataforma
        actores = data.query('ID.str.split().str.get(0).str[0] == @platform[0] and release_year == @year')
        #seleccionar solo la columna ''cast' eliminando los valores nulos
        actores= actores['cast'].dropna()
    else:
        #en caso de no ser correcta la plataforma se envia el siguiente mensaje
        return {'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}

    #colocar todos los actores en una lista
    full_list = []
    for  i in actores:
        lista = [elemento.strip() for elemento in i.split(',')]
        full_list+=lista
    #frecuencia de cada actor
    frecuencias = Counter(full_list).most_common()
    print(frecuencias[0])
    #verificar si hay mas de un valor frecuente
    if len(frecuencias) > 1 and frecuencias[0][1] == frecuencias[1][1]:
        return {'mensajes':"Hay varios valores que se repiten la misma cantidad de veces, se muestran los primeros 2",
                'data 1':frecuencias[0][0],
                'data 2':frecuencias[1][0]}
    #verificar que exista una respuesta
    elif len(frecuencias)==0:
        return {'mensaje':'No existen datos para estos filtros'}
    else:
        #se retorna el actor que mas aparece en la lista
        return{'common_actor':frecuencias[0][0]}

@app.get('/get_max_duration/{year}/{platform}/{duration_type}')
def get_max_duration(year = None, 
                    platform = None, 
                    duration_type= None):
    """Película con mayor duración con filtros opcionales de
    AÑO, PLATAFORMA Y TIPO DE DURACIÓN. 
    """

    #verificamos que coinsida la plataforma
    if platform not in webs:
        platform=None
        return {'Mensaje':f"esta plataforma '{platform}' no coincide en la base de datos"}
    
    #esta funcion realiza el filtro
    columns, filtrado = filtrar_max_duration(year,platform,duration_type)
    resp={}
    #se pasa el resultado a un diccionario
    for index, i in filtrado.iterrows():
        for j in columns:
            resp.update({j:i[j]})
    #resp.update({'platform':platform})
    #entregar respuesta
    return resp
    
@app.get('/recomendacion/{userid}/{movieid}')
def recomendacion(userid,movieid):
    #validar datos
    try:
        userid = int(userid)
    except:
        return {'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
    #consultar el registro para movieid
    movie = data.query('title == @movieid or ID == @movieid')
    #la consulta debe tener contenido
    if len(movie)==0:
        return {'mensaje':'no es posible dar una respuesta, verifica los datos e intenta nuevamente'}
    else:
        #ejecutar funcion de recomendacion y dar respuesta
        print(movie['ID'].values)
        return {'recomendar':R.predecir(userid,movie['ID'].values[0])}

@app.get('/prod_per_county/{tipo}/{pais}/{anio}')
def prod_per_county(tipo,pais,anio):

    """La cantidad de contenidos/productos 
    (todo lo disponible en streaming) que se publicó por país y año.
    por favor usar en tipo estas dos opciones (movie, serie)"""

    tip=['movie','serie']
    try:
        anio = int(anio)
    except:
        return {'mesage':'los datos no son correctos revise la informacion e intenta nuevamente'}

    if tipo not in tip:
        return {'mesage':'los datos no son correctos revise la informacion e intenta nuevamente'}
    else:
        resultado = data[data['country'] == pais & data['type'] & data['date_added'].dt.year==anio]
        #data.query(
        #    'country == @pais and type == @tipo and date_added.dt.year == @anio')
        return{
            'pais':pais,
            'año':anio,
            'productos':len(resultado)
        }
        

def filtrar_max_duration(year = None, 
            platform = None, 
            duration_type= None):

    type_duration = ['min','season']
    if duration_type not in type_duration:
        duration_type = None
    #filtrar por año
    try:
        year=int(year)
    except:
        year=''
    if type(year) == int:
        respuesta= (data[data['release_year']==int(year) ])
    else:
        respuesta= (data)
    #filtrar por plataforma
    if platform != None:
        respuesta = respuesta[respuesta['ID'].str.split().str.get(0).str[0]==platform[0]]
    else:
        ...
    #maxima duracion
    if duration_type in type_duration:
        respuesta = respuesta[respuesta['duration_type']== duration_type]
        respuesta = respuesta[respuesta['duration_int']==respuesta['duration_int'].max()]
    else:
        respuesta = respuesta[respuesta['duration_int']==respuesta['duration_int'].max()]

    #seleccionar la columnas de interes
    columns= respuesta.columns.tolist()
    respuesta= (respuesta[columns])
    respuesta= respuesta.replace(np.nan,'')
    return columns, respuesta