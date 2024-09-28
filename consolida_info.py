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
info_posts = {}

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
        
        chats_info = {}

        if ("chats" in data_post):
            for chat in data_post["chats"]:
                print("chat: ", chat)
                if (chat['header']['depth'] == '0'):
                    chats_info[chat['header']['thingid']] = chat['header']
                    for resp in chat['respuestas']:
                        print("resp: ", resp)
                        if (resp['header']['depth'] == '1'):
                            if (not resp['header']['parentid'] in chats_info):
                                chats_info[resp['header']['parentid']] = {  "respuestas": [] }
                            chats_info[resp['header']['parentid']]["respuestas"].append(resp['header'])
                            

                print("")

        data_ = {
            "id": id,
            "url": BASE_URL + data_post["enlace_comentarios"]['href'],
            "enlaces": data_post["enlaces"],
            "text": data_post["texto"],
            "imagenes": data_post["imagenes"],
            "chats": chats_info
        }

        info_posts[id] = data_
        
        print('procesando', id)
        print("")

with open( "consolidado_"+fecha+".json", 'w') as file:
    json.dump(info_posts, file)
    print('se actualiza el archivo: ', "consolidado_"+fecha+".json")
    print('')