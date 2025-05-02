#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from utils import *

URL_EP = "http://localhost:5555/get_results"

print("haciendo petición, resultados scrapping...")

posts = {}

respuesta = requests.get(URL_EP)
if respuesta.status_code == 200:
    posts = respuesta.json()
    posts = posts["data"]
    
print("Cantidad de posts encontrados: ", len(posts))

termino_busqueda = input("Ingrese termino de búsqueda: ")
termino_busqueda = termino_busqueda.lower()

resultados = []
for post in posts:
    data_post = posts[post]
    titulo = data_post["data"]["titulo"].lower()
    cuerpo = data_post["data"]["texto"].lower()

    if (titulo.find(termino_busqueda) != -1 or cuerpo.find(termino_busqueda) != -1):
        resultados.append(data_post["data"])
        

print("Se encontraron " + str(len(resultados)) + " resultados, se genera json con resultados...")
with open('resultados_busqueda.json', 'w') as file:
    json.dump(resultados, file)