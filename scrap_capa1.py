#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import time
import json
from bs4 import BeautifulSoup
import datetime
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scroll_hasta_el_final(driver):
    last_scroll_position = 0
    while True:
        # Mover el scroll hasta el final de la página actual
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        current_scroll_position = driver.execute_script("return window.pageYOffset")

        # Si no hay más contenido para mostrar (es decir, no se ha desplazado más), salir del bucle
        if current_scroll_position == last_scroll_position:
            break

        last_scroll_position = current_scroll_position

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    #options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def hacer_clic_por_texto(driver, texto):
    try:
        elemento = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{texto}')]")))
        elemento.click()
    except:
        print("No se pudo hacer clic en el elemento")

BASE_URL  = "https://www.reddit.com/r/devsarg/"
fecha     = datetime.datetime.now().strftime("%Y%m%d")

driver = get_driver()

driver.get(BASE_URL)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'html')))

ciclar = True

listado_posts = []
diccio_posts = {}

while ciclar:
    scroll_hasta_el_final(driver)

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