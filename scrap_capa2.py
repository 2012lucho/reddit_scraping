#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from utils import *

BASE_URL = "https://www.reddit.com"

driver = get_driver()

headers_ = {
    "Accept": "application/json",
}

while True:
    print("Obteniendo post...")
    post = ''
    while post == '':
        respuesta = requests.get('http://localhost:5555/get_process_1',headers=headers_)
        try:
            post = respuesta.json()
        except Exception as e:
            print(e)
            print("No hay post, reintentando en 10 segundos")
            time.sleep(10)
            continue
        post = post['item']
        if (post == ''):
            print("No hay post, reintentando en 10 segundos")
            time.sleep(10)

    print("post obtenido ",post)

    soup = BeautifulSoup(post['html'], 'html.parser')
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
        exit(0)

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
            "data": {
                "autor": chat.get("author"),
                "permalink": chat.get("permalink"),
                "score": chat.get("score"),
                "depth": chat.get("depth"),
                "parentid": chat.get("parentid"),
                "postid": chat.get("postid"),
                "thingid": chat.get("thingid"),
                "content-type": chat.get("content-type"),
                "moderation-verdict": chat.get("moderation-verdict"),
                "ts": chat.find("time").get("datetime"),
            },
            "comentario": "",
            "respuestas": []
        }

        resp_0 = chat.find("p")
        if (resp_0 != None):
            chat_info["comentario"] = resp_0.text.strip()
        print(chat_info)
        all_chats_0.append(chat_info)

    response = requests.post('http://localhost:5555/post_process_1_msg', json={
            "data": all_chats_0,
            "id_post": id
        })
    if response.status_code == 200:
        print("Enviado!")
    else:
        print("Error en la petición POST:", response.status_code)
        
