#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from utils import *

BASE_URL = "https://www.reddit.com"

driver = get_driver()

while True:
    print("Obteniendo post...")
    post = ''
    headers_ = {
        "Accept": "application/json",
    }

    comentarios = ''
    id_post = ''
    while comentarios == '':
        respuesta = requests.get('http://localhost:5555/get_process_2',headers=headers_)
        post = respuesta.json()
        post = post['item']
        id_post = post['id']
        if (post == ''):
            print("No hay post, reintentando en 10 segundos")
            time.sleep(10)

        if (not "comentarios" in post):
            print("No hay comentarios, reintentando en 10 segundos")

        comentarios = post["data"]["comentarios"]

    id_img = 0

    for id_comment in comentarios:
        print("")
        comentario = comentarios[id_comment]
        print("comentario ",comentario)

        try:
            url_info = BASE_URL + comentario['data']['permalink']
            print("\n Consultando : ", url_info)
            driver.get(url_info)
        except:
            continue

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
        scroll_hasta_el_final(driver)
        mas_info = True
        while mas_info:
            mas_info = hacer_clic_por_texto(driver, 'Ver más respuestas')
            time.sleep(1)

        contenido_resp = driver.page_source
        soup_resp = BeautifulSoup(contenido_resp, 'html.parser')

        comentarios_l_1 = soup_resp.find_all("shreddit-comment")
        dir_base = 'post_data/'+id_post

        for coment in comentarios_l_1:
            imagenes = coment.find_all("img")
            img_info = []
            text = ''
            if (coment.find("p") != None):
                text = coment.find("p").text

            os.makedirs(dir_base+'/img', exist_ok=True)

            for img in imagenes:
                url_imagen = img.get("src")        

                path_img = dir_base+'/img/'+str(id_img)
                try:
                    respuesta = requests.get(url_imagen)
                    if respuesta.status_code == 200:
                        with open(path_img, "wb") as archivo:
                            archivo.write(respuesta.content)
                        print("Imagen descargada")
                        img_info.append({ "src": url_imagen, "path": path_img })
                        os.makedirs('all_images', exist_ok=True)
                        os.symlink(os.path.relpath(path_img, os.path.dirname('all_images/post_'+str(id)+'_'+str(id_img))), 'all_images/post_'+str(id)+'_'+str(id_img))
                    else:
                        print("Error al descargar la imagen:", respuesta.status_code)
                    id_img = id_img + 1
                except Exception as e:
                    print("Error al guardar la imagen", e)

            send_data = {
                    "data": {
                        "autor": coment.get("author"),
                        "permalink": coment.get("permalink"),
                        "score": coment.get("score"),
                        "depth": coment.get("depth"),
                        "parentid": coment.get("parentid"),
                        "postid": coment.get("postid"),
                        "thingid": coment.get("thingid"),
                        "content-type": coment.get("content-type"),
                        "moderation-verdict": coment.get("moderation-verdict"),
                        "ts": coment.find("time").get("datetime"),
                        'imagenes': img_info,
                    },
                    "comentario": text,
                    "respuestas": [],
                    "id_post": id_post
                }
            response = requests.post('http://localhost:5555/post_process_2_msg', 
                json=send_data)
            if response.status_code == 200:
                print("Enviado!")
            else:
                print("Error en la petición POST:", response.status_code)
            print("")

