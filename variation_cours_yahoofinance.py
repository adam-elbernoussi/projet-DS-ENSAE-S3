"""Voici une fonction permettant de récupérer un tableau contenant les variations des cours d'une action donnée (ici 
Air Liquide) à partir de la date souhaitée sur le site Yahoo Finance.
Ce code est très semblable  la version sur ABC Bourse, car le principe est le même.
Nous avons souhaité scrapper le site de Yahoo Finance car ABC Bourse ne permettait de récupérer les variations des cours 
uniquement depuis 6 mois, ce qui ne nous paraissait pas suffisant pour une base de données."""

def variation_cours_yf(date_dd_mm_yyyy) :

    #on importe les modules nécessaires
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import bs4
    import pandas as pd
    from urllib import request
    import lxml
    import html 

    #on définit le webdriver dont on se sert
    driver = webdriver.Chrome("W:\Bureau\Projet Python 2A\projet-DS-ENSAE-S3\chromedriver.exe")

    #on ouvre la page souhaitée
    driver.get("https://finance.yahoo.com/quote/AI.PA/history?p=AI.PA") 

    #on localise la date à changer
    changement_date = driver.find_element_by_name("startDate")

    #on rentre la date souhaitée
    changement_date.send_keys(date_dd_mm_yyyy)

    #on affiche la page avec la nouvelle date
    changement_date.send_keys(Keys.RETURN)

    #On récupère le code source de la page
    page_source = driver.page_source

    #On rend ce code exploitable avec Beautifoul Soup
    page = bs4.BeautifulSoup(page_source, "lxml")

    #on identifie le tableau qui nous intéresse
    tableau = page.find("table", {"class" : "W(100%) M(0)"})
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

    #On créer une nouvelle colonne qui évalue la différence du cours de l'action entre l'ouvertur et la fermeture de la bourse
    liste_open = tableau_cours["Open"]
    liste_close = tableau_cours["Close*"]
    liste_variation = []

    for i in range(len(liste_open)):
        liste_variation.append(liste_open[i] - liste_close[i])
        i += 1
    
    tableau_cours["Variation"] = liste_variation

    #On allège le tableau
    tableau_cours = tableau_cours.drop(columns=["Open", "High", "Low", "Volume", "Close*", "Adj Close**", "Volume"])

    return tableau_cours
