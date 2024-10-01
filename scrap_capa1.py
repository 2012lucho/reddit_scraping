#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
from utils import *
import random

BASE_URL  = "https://www.reddit.com/r/devsarg/new/"

driver = get_driver()

TIEMPO_INTERCONSULTA = 150

ciclar = True

diccio_posts = {}

while ciclar:
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))
    #scroll_hasta_el_final(driver, True)

    contenido = driver.page_source
    soup = BeautifulSoup(contenido, 'html.parser')
    posts = soup.find_all("article")
    for post in posts:
        id = post.find("shreddit-post").get("id")
        if (id in diccio_posts):
            continue
        
        enlace_info = []
        enlaces = post.find_all("a")
        for enlace in enlaces:
            enlace_info.append({ "href": enlace.get("href") })
        
        imagenes_info = []
        imagenes = post.find_all("img")
        id_img = 0

        dir_base = 'post_data/'+id
        os.makedirs(dir_base, exist_ok=True)
        os.makedirs(dir_base+'/img', exist_ok=True)
            
        for img in imagenes:
            url_imagen = img.get("src")        
            descargar_imagen(url_imagen, dir_base,id + '_' + str(id_img))
            path_img = dir_base + '/img/' + id + '_' + str(id_img)
            imagenes_info.append({ "src": url_imagen, "path": path_img })
            id_img = id_img + 1

        id_title = "post-title-"+id
        id_post_cont = id + "-post-rtjson-content"
        
        try:
            response = requests.post('http://localhost:5555/post_html', json={
                "html": post.decode_contents(), 
                "data": {
                    "id": id,
                    "url": post.find("shreddit-post").get("content-href"),
                    "titulo": post.find(id=id_title).text.strip(),
                    "texto": post.find(id=id_post_cont).text.replace("\n", "").strip(),
                    "timestamp": post.find("shreddit-post").get("created-timestamp"),

                    "score": post.find("shreddit-post").get("score"),
                    "author-id": post.find("shreddit-post").get("author-id"),
                    "author": post.find("shreddit-post").get("author"),

                    "enlaces": enlace_info,  
                    "comment-count": post.find("shreddit-post").get("comment-count"),
                    "domain": post.find("shreddit-post").get("domain"),
                    "post-language": post.find("shreddit-post").get("domain"),
                    "imagenes": imagenes_info
                },
                "id": id
            })
            if response.status_code == 200:
                print("Enviado!")
            else:
                print("Error en la petición POST:", response.status_code)
        except Exception as e:
            print("Error al obtener datos del post", e, post)
            continue

    print("esperando para prox ciclo")
    time.sleep(random.randint(1, TIEMPO_INTERCONSULTA/5))
    time.sleep(TIEMPO_INTERCONSULTA)