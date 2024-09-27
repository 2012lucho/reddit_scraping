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

listado_posts = []
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
        
        listado_posts.append(post.decode_contents())
        diccio_posts[id] = post
        
        nombre_arch = 'posts_' + fecha + '.json'
        with open(nombre_arch, 'w') as file:
            json.dump(listado_posts, file)
            print(nombre_arch)
        
    time.sleep(2)