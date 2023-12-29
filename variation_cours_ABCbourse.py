"""Voici une fonction permettant de récupérer un tableau contenant les variations des cours d'une action donnée (ici 
Air Liquide) à partir de la date souhaitée sur le site ABC Bourse"""

def variation_cours(date_dd_mm_yyyy):

    #importation de tous les modules nécessaires
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import bs4
    import pandas as pd
    from urllib import request
    import lxml
    import html

    #choix du driver, ici on se sert du driver propre au navigateur Chrome
    driver = webdriver.Chrome("W:\Bureau\Projet Python 2A\projet-DS-ENSAE-S3\chromedriver.exe")

    #on se rend sur le site d'ABC Bourse
    driver.get("https://www.abcbourse.com/download/valeur/AIp")
    
    #on localise la date à changer
    date_à_changer = driver.find_element_by_id("datefrom")

    #on la modifie
    date_à_changer.send_keys(date_dd_mm_yyyy)

    #on lance la commande pour afficher la page avec la nouvelle date
    date_à_changer.send_keys(Keys.RETURN)

    #on récupère le code source de cette nouvelle page
    page_source = driver.page_source

    #on rend exploitable ce code source avec BeautifoulSoup
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
    
    #on prépare la récupération du contenu des colonnes en créant une liste de listes, où chaque sous-liste contient le contenu
    #d'une des colonnes du tableau

    liste_ligne = [[] for i in range(len(liste_en_tete))]

    #constitution des sous-listes
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

    #On l'allège en ne conservant que les informations qui nous intéressent 
    tableau_cours = tableau_cours.drop(columns=["Ouverture", "Plus Haut", "Plus Bas", "Volume", "Dernier"])

    return tableau_cours