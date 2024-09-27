#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from utils import *

fecha     = datetime.datetime.now().strftime("%Y%m%d")

nombre_arch = 'posts_' + fecha + '.json'
try:
    with open( nombre_arch ) as archivo_json:
        POSTS = json.load(archivo_json)
except:
    print("Archivo de posts no encontrado")

BASE_URL = "https://www.reddit.com"

driver = get_driver()

for post in POSTS:
    soup = BeautifulSoup(post, 'html.parser')
    print("Post ID: ",id)
    id = soup.find("shreddit-post").get("id")
    
    enlace_info = []
    enlaces = soup.find_all("a")
    for enlace in enlaces:
        enlace_info.append({ "href": enlace.get("href") })
    
    imagenes_info = []
    imagenes = soup.find_all("img")
    id_img = 0

    dir_base = 'post_data/'+id
    os.makedirs(dir_base, exist_ok=True)
    os.makedirs(dir_base+'/img', exist_ok=True)

    for img in imagenes:
        url_imagen = img.get("src")        

        path_img = dir_base+'/img/'+str(id_img)
        imagenes_info.append({ "src": url_imagen, "path": path_img })
        try:
            respuesta = requests.get(url_imagen)
            if respuesta.status_code == 200:
                with open(path_img, "wb") as archivo:
                    archivo.write(respuesta.content)
                print("Imagen descargada y guardada correctamente")

                os.makedirs('all_images', exist_ok=True)
                os.symlink(os.path.relpath(path_img, os.path.dirname('all_images/post_'+str(id)+'_'+str(id_img))), 'all_images/post_'+str(id)+'_'+str(id_img))
            else:
                print("Error al descargar la imagen:", respuesta.status_code)
            id_img = id_img + 1
        except:
            print("Error al descargar la imagen")
    
    #print("Enlaces: ", enlaces)
    #print("Imágenes: ", imagenes)

    post_data = {
        "id": id, "enlaces" : enlace_info, "enlace_comentarios": enlace_info[0], "texto": soup.text, "imagenes": imagenes_info, "html": post
    }
    
    
    nombre_arch = dir_base + '/' + fecha + '.json'
    with open(nombre_arch, 'w') as file:
        json.dump(post_data, file)
        print(nombre_arch)