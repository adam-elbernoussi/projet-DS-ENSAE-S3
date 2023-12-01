"""Cette page a pour but de coder les éléments nécessaires à la récupération des indicateurs de variations des cours
Il s'agit d'un code provisoire, destiné à être étoffé. En effet, il scrape les données du site AbcBourse et sur une période de 2 mois.
On voudrait pouvoir faire cela sur le site Yahoo Finance sur des périodes plus longues, mais il semble y avoir un problème au moment
de la récupération des données html. A voir, donc."""

import bs4
import pandas as pd
from urllib import request
import lxml
import html

#on récupère la page web

url_ya_fi = "https://www.abcbourse.com/download/valeur/AIp"

text_page = request.urlopen(url_ya_fi).read()

page = bs4.BeautifulSoup(text_page, "lxml")

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

