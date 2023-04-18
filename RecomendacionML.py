import pickle, numpy as np

# cargar modelo
#with open('modelo_recomendacion.pkl', 'rb') as archivo:
#    modelo = pickle.load(archivo)
from keras.models import load_model
modelo = load_model('modelo_recomendacion.h5')

# funcion para predecir
def predecir(userid:int,movieid:str):
    #arrego de userid
    arreglo=np.array([userid])
    #transformacion de movieid
    if movieid[0]=='a':
        movieid= '19'+movieid[2:]
    elif movieid[0]=='d':
        movieid= '29'+movieid[2:]
    elif movieid[0]=='h':
        movieid= '39'+movieid[2:]
    elif movieid[0]=='n':
        movieid= '49'+movieid[2:]
    else:
        return {'mensaje':'este movieid '+movieid+' no es correcto'}
    #arreglo de movieid
    movieid=int(movieid)
    arr =np.array([movieid])
    #combinacion de los arreglos
    predic = np.stack((arreglo,arr),axis=1)
    #prediccion
    resultado=modelo.predict([predic])
    print(resultado)
    if resultado[0][0]>3.54:
        return True
    else:
        return False
    
#print(predecir(1,'ns3205'))