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

# We make a request on the Wikipedia page of the company.
url_airliquide = "https://fr.wikipedia.org/wiki/Air_liquide"

def scrapInfo(link):
    #request_text = request.urlopen(url_airliquide).read()
    request_text = requests.get(url_airliquide).text
    page = BeautifulSoup(request_text, "html.parser")

    """
    To view the entire HTML code, we execute the following code, which copies it into a new file :
    print(str(page))
    fichier = open("res.txt", "w")
    fichier.write(str(page))
    fichier.close()
    """
    # This code allows us to observe that to retrieve the table of interest, we need to search for the word 'table'
    tableau_general = page.find('table')

    table_body = tableau_general.find('tbody')
    # We name 'row' the list of rows (in HTML) of the table :
    rows = table_body.find_all('tr')

    # We create a dictionary with the information, cleaning them up (for example, removing the \n) so that they are usable

    infos_generales = {}
    i = -1
    for row in rows:
        try :
            _key = row.find("th").contents[0].string
            _key = re.findall("\S*", _key)[0]
            infos_generales[_key] = (row.find("td").contents[0].string).strip('\n')
            
        except AttributeError :
            pass

    return infos_generales

