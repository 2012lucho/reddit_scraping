import json
from pymongo import MongoClient

def leer_configuracion():
    with open('config.json') as archivo:
        configuracion = json.load(archivo)
    return configuracion['mongodb']

def conectar_a_mongodb(configuracion):
    cliente = MongoClient(
        host=configuracion['host'],
        port=configuracion['port'],
        username=configuracion['username'],
        password=configuracion['password']
    )
    return cliente

def crear_base_de_datos_si_no_existe(cliente, configuracion):
    if configuracion['database'] not in cliente.list_database_names():
        db = cliente[configuracion['database']]
        print(f"Base de datos '{configuracion['database']}' creada vacía")
    else:
        db = cliente[configuracion['database']]
    return db

def crear_coleccion_si_no_existe(db, nombre_coleccion):
    if nombre_coleccion not in db.list_collection_names():
        db[nombre_coleccion]
        print(f"Colección '{nombre_coleccion}' creada vacía")

def main():
    configuracion = leer_configuracion()
    cliente = conectar_a_mongodb(configuracion)
    db = crear_base_de_datos_si_no_existe(cliente, configuracion)
    crear_coleccion_si_no_existe(db, 'reddit_scraping')
    print("Conexión establecida con éxito")

if __name__ == "__main__":
    main()