#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from utils import *

BASE_URL  = "https://www.reddit.com/r/devsarg/"
fecha     = datetime.datetime.now().strftime("%Y%m%d")

driver = get_driver()

driver.get(BASE_URL)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

ciclar = True

diccio_posts = {}

while ciclar:
    scroll_hasta_el_final(driver, True)

    contenido = driver.page_source
    soup = BeautifulSoup(contenido, 'html.parser')
    posts = soup.find_all("article")
    for post in posts:
        id = post.find("shreddit-post").get("id")
        if (id in diccio_posts):
            continue
        
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
            except Exception as e:
                print("Error al descargar la imagen", e)

        response = requests.post('http://localhost:5555/post_html', json={
            "html": post.decode_contents(), 
            "data": {
                "id": id,
                "enlaces": enlace_info,
                "enlace_comentarios": enlace_info[0],
                "texto": soup.text,
                "imagenes": imagenes_info,
                "html": post.decode_contents()
            },
            "id": id
        })
        if response.status_code == 200:
            print("Enviado!")
        else:
            print("Error en la petición POST:", response.status_code)
    time.sleep(2)