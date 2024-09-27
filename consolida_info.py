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