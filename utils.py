#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
from bs4 import BeautifulSoup
import time
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

def scroll_hasta_el_final(driver, solo_scroll=False):
    last_scroll_position = 0
    while True:
        # Mover el scroll hasta el final de la página actual
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        time.sleep(2)
        current_scroll_position = driver.execute_script("return window.pageYOffset")

        # Si no hay más contenido para mostrar (es decir, no se ha desplazado más), salir del bucle
        if current_scroll_position == last_scroll_position or solo_scroll:
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
        return True
    except:
        print("No se pudo hacer clic en el elemento")
        return False
    
def descargar_imagen(url_imagen, dir_base, name):
    os.makedirs(dir_base+'/img', exist_ok=True)

    path_img = dir_base+'/img/'+name
    try:
        respuesta = requests.get(url_imagen)
        if respuesta.status_code == 200:
            with open(path_img, "wb") as archivo:
                archivo.write(respuesta.content)
            print("Imagen descargada")
            
            os.makedirs('all_images', exist_ok=True)
            os.symlink(os.path.relpath(path_img, os.path.dirname('all_images/'+name)), 'all_images/'+name)
        else:
            print("Error al descargar la imagen:", respuesta.status_code)
        

    except Exception as e:
        print("Error al guardar la imagen", e)