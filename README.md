# Api_Data_Movies

Este es el Proyecto individual para una api y un sistema de recomendacion de peliculas basado en puntajes

en este README podras encontrar toda la documentacion, e instrucciones para poder utilizar la api_data_mavies

▶ MENU: ◀
* Datasets -> archivos .csv donde esta almacenada la informacion
* __pycache__ -> carpeta de cache generada al ejecutar un archivo de python
* ETL.ipynb -> netebook con el paso a paso del ETL
* main.py -> archivo de codigo para la api
* README.md -> instrucciones y documentacion del proyecto
* requirements.txt -> dependencias necesarias para el proyecto

▶ Funciones que ejecuta la API ◀

1⃣ Película con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN.

2⃣ Cantidad de películas por plataforma con un puntaje mayor a ?? en determinado año

3⃣ Cantidad de películas por plataforma con filtro de PLATAFORMA.

4⃣ Actor que más se repite según plataforma y año.

▶ Como escribir las funciones en el navegador ◀

📌 https://pi-elmer-daza.onrender.com/get_max_duration/{year}/{platform}/{duration_type}

📌 https://pi-elmer-daza.onrender.com/get_score_count/{platform}/{scored}/{year}

📌 https://pi-elmer-daza.onrender.com/get_count_platform/{platform}

📌 https://pi-elmer-daza.onrender.com/get_actor/{platform}/{year}

▶ Ejemplo de queries para probar la API ◀

📌 https://pi-elmer-daza.onrender.com/get_max_duration/2021/disney/season

📌 https://pi-elmer-daza.onrender.com/get_score_count/hulu/3.5/2019

📌 https://pi-elmer-daza.onrender.com/get_count_platform/amazon

📌 https://pi-elmer-daza.onrender.com/get_actor/amazon/2021

🚫 ADVERTENCIA 🚫

❌ Las plataformas admitidas son: ['amazon','disney','hulu','netflix']

❌ Toda la query debe estar escrita en minuscula

❌ En caso que los datos de consulta sean erroneos se obtendra el siguiente mensaje: no es posible dar una respuesta, verifica los datos e intenta nuevamente

❌ Si ingresa una ruta no admitida recibira el siguiente mensaje: "detail":"Not Found"

▶ Funciones extra ◀

* funcion de bienvenida / -> esta se accede al no ingresar ninguna ruta: contiene un saludo y la forma de contactar con migo ademas de mis redes sociales
* funcion de docs: /docs -> esta muestra el menu principal de las funciones y ademas permite el test dede una interfaz intuitiva

▶ MUCHAS GRACIAS ◀

Agradesco por el tiempo que te has tomado para testear mi API y darme el feedback.
