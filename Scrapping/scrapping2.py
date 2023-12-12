"""In this file, we will scrap some information about a company given its ticker."""
"""We will use the website Wikipedia"""

#Importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import datetime
import time
from urllib import request


url_airliquide = "https://fr.wikipedia.org/wiki/Air_liquide"
request_text = request.urlopen(url_airliquide).read()
type(request_text)
page = BeautifulSoup(request_text, "html.parser")
#print(str(page))
#fichier = open("res.txt", "w")
#fichier.write(str(page))
#fichier.close()
tableau_general = page.find('table')
#print(tableau_general)
table_body = tableau_general.find('tbody')
rows = table_body.find_all('tr')
#print(rows[5])
# On crée un dictionnaire avec les infos

dico = {}
i = -1
for row in rows:
    try :
        _key = row.find("th").contents[0].string
        _key = re.findall("\S*", _key)[0]
        print(_key)
        dico[_key] = list(row.find("td").strings)
    except AttributeError :
        pass

print("test : ", rows[4].find("th").contents[0].string)

print(dico)