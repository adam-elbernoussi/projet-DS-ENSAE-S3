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
print(tableau_general)
