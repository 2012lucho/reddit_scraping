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

    enlace_info = []
    enlaces = soup.find_all("a")
    
    dir_base = 'post_data/'+id
    os.makedirs(dir_base, exist_ok=True)

    #Se obtienen las respuestas
    enlace_comentarios = BASE_URL + enlaces[0]['href']
    try:
        driver.get(enlace_comentarios)
    except:
        continue

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

    scroll_hasta_el_final(driver)
    mas_info = True
    while mas_info:
        mas_info = hacer_clic_por_texto(driver, 'Ver más comentarios')
        time.sleep(5)


    contenido_resp = driver.page_source
    soup_resp = BeautifulSoup(contenido_resp, 'html.parser')

    #se obtienen los chats
    chats = soup_resp.find_all("shreddit-comment")
    all_chats_0 = []
    for chat in chats:
        chat_info = {
            "header": {
                "autor": chat.get("author"),
                "permalink": chat.get("permalink"),
                "score": chat.get("score"),
                "depth": chat.get("depth"),
                "parentid": chat.get("parentid"),
                "postid": chat.get("postid"),
                "thingid": chat.get("thingid"),
                "content-type": chat.get("content-type"),
                "moderation-verdict": chat.get("moderation-verdict"),
                "comentario": "",
            },
            "respuestas": []
        }

        #se obtienen respuestas inmediatas
        resp_0 = chat.find("p")
        if (resp_0 != None):
            print(resp_0)
            chat_info["header"]["comentario"] = resp_0.text
        print(chat_info)
        all_chats_0.append(chat_info)
        
    nombre_arch = dir_base + '/' + fecha + '.json'
    try:
        with open( nombre_arch ) as archivo_json:
            data_post = json.load(archivo_json)
            data_post['chats'] = all_chats_0

            with open(nombre_arch, 'w') as file:
                json.dump(data_post, file)
                print("post data actualizado nivel 0 de conversaciones: ",nombre_arch)

    except:
        print("Archivo de posts no encontrado")