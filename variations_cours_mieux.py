"""Ce code est une amélioration du code variations_cours précédent, car il permet de modifier
la date à partir de laquelle on collecte les données. Je n'ai pas pu le tester parfaitement (pb 
d'interpréteur python), mais ça devrait être bon (si ça ne marche pas, ça devrait être l'affaire
de 2-3 lignes de codes).
Je pense qu'on peut exporter ce code sans trop de difficultés sur Yahoo Finances, j'essaierai une prochaine
fois."""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import pandas as pd
from urllib import request
import lxml
import html

driver = webdriver.Chrome("W:\Bureau\Projet Python 2A\projet-DS-ENSAE-S3\chromedriver.exe")

driver.get("https://www.abcbourse.com/download/valeur/AIp")

date_à_changer = driver.find_element_by_id("datefrom")
date_à_changer.send_keys("18/08/2023")
date_à_changer.send_keys(Keys.RETURN)

page_source = driver.page_source

page = bs4.BeautifulSoup(page_source, "lxml")

#on identifie le tableau qui nous intéresse

tableau = page.find("table", {"id" : "tabQuotes"})

tableau_body = tableau.find("tbody")

lignes = tableau_body.find_all("tr")

#on récupère les en-têtes

en_tete = tableau.find("thead")

liste_en_tete = []
for titre in en_tete.find_all("th"):
    liste_en_tete.append(titre.text.strip())
    
#on prépare la récupération des lignes, ici la méthode est un peu différente de celle du prof, puisqu'on crée un dico ou chaque clé est un en-tête et les valeurs sont
#celles des colonnes directement

liste_ligne = [[] for i in range(len(liste_en_tete))]

for ligne in lignes:
    colonne = ligne.find_all("td")
    i = 0
    for element in colonne :
        liste_ligne[i].append(element.text.strip())
        i += 1
        

#on réunit les titres des en-têtes et le contenu des colonnes 

dico_final = {}
j = 0
for titre in liste_en_tete : 
    dico_final[titre] = liste_ligne[j]
    j += 1

#On crée le tableau
tableau_cours = pd.DataFrame.from_dict(dico_final)

#On l'allège en ne conservant que les informations qui nous intéressent (étape pas obligatoire au demeurant)
tableau_cours = tableau_cours.drop(columns=["Ouverture", "Plus Haut", "Plus Bas", "Volume", "Dernier"])