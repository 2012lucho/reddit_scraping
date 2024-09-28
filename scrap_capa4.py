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
    id = soup.find("shreddit-post").get("id")
    print("Post ID: ",id)
    id_img = 0
    dir_base = 'post_data/'+id
    nombre_arch = dir_base + '/' + fecha + '.json'
    #try:
    with open( nombre_arch ) as archivo_json:
        try:
            data_post = json.load(archivo_json)
        except:
            print("archivo_json", archivo_json)
            continue

        if (data_post['chats'] == None):
            print("No hay chats registrados")
            continue

        chats = data_post['chats']
        for chat in chats:
            try:
                url_info = BASE_URL + chat['header']['permalink']
            
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
            all_chats_1 = []
            for coment in comentarios_l_1:
                imagenes = coment.find_all("img")
                chat_info = {
                    "header": {
                        "autor": coment.get("author"),
                        "permalink": coment.get("permalink"),
                        "score": coment.get("score"),
                        "depth": coment.get("depth"),
                        "parentid": coment.get("parentid"),
                        "postid": coment.get("postid"),
                        "thingid": coment.get("thingid"),
                        "content-type": coment.get("content-type"),
                        "moderation-verdict": coment.get("moderation-verdict"),
                        "comentario": "",
                    },
                    "respuestas": [],
                    'enlaces': coment.find_all("a"),
                    'imagenes': imagenes,
                    'image': coment.find_all("image")
                }

                os.makedirs(dir_base+'/img', exist_ok=True)

                for img in imagenes:
                    url_imagen = img.get("src")        

                    path_img = dir_base+'/img/'+str(id_img)
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

                #se obtienen respuestas inmediatas
                resp_1 = coment.find("p")
                if (resp_1 != None):
                    print(resp_1)
                    chat_info["header"]["comentario"] = resp_1.text
                print(resp_1)
                all_chats_1.append(chat_info)
            
            chat['respuestas'] = all_chats_1
            print(len(all_chats_1))
            print('')
        
        data_post['chats'] = chats
        print(data_post)
        try:
            with open( nombre_arch, 'w') as file:
                json.dump(data_post, file)
                print('se actualiza el archivo: ', nombre_arch)
                print('')
        except:
            print("Error al actualizar el archivo: ", nombre_arch)
        
    #except:
    #    print("Archivo de post no encontrado")