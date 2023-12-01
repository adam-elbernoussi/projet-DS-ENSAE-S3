"""In this file, we will scrap some articles about a company given its ticker."""
"""Firstly, on the website abcbourse.com"""

#Importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import datetime
import time
import tqdm


#Coding functions
def scrap_article_CF(link : str):
    """
    This function scraps an article from a given link.

    Parameters
    ----------
    link : str
        The link of the article.

    Returns
    -------
    title : str
        The title of the article.
    date : str
        The date of the article.
    content : str
        The content of the article.
    """
    #Getting the page
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    #for title
    res_title = soup.title.string
    #for date
    stringForDate = soup.find("span", {"class": "co_g2"}).string
    stringForHour = re.findall(r"\d+/\d+/\d+ \d+:\d+", stringForDate)[0]
    res_date = datetime.datetime.strptime(stringForHour, r"%d/%m/%y %H:%M")
    #for content
    article_body = soup.find("div", {"class": "txtbig content_news"})
    if res_date >= datetime.datetime.strptime("12/08/2019", r"%d/%m/%Y"):
        article_body = article_body.p
    listSentence = article_body.strings
    res_content = ""
    for sentence in listSentence:
        res_content += sentence.string
    res_content = re.sub(r"\.(?=[a-zA-Z]|')", ". ", res_content)
    try:
        res_content = re.findall(r"- (.*) (?:Copyright|'Copyright)", res_content)[0]
        res_content = res_content.replace("  ", " ")
    except:
        return {"title": res_title, "date": str(res_date), "content": None}
    return {"title": res_title, "date": str(res_date), "content": res_content}



# à voir si utile, en fait les article de CF suffisent probablement
def scrap_article_gen(link : str):
    """
    This function scraps an article from a given link.

    Parameters
    ----------
    link : str
        The link of the article.

    Returns
    -------
    title : str
        The title of the article.
    date : str
        The date of the article.
    content : str
        The content of the article.
    """
    #Getting the page
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    #for title
    res_title = soup.title.string
    #for date
    stringForDate = soup.find("span", {"class": "co_g2"}).string
    stringForHour = re.findall(r"\d+/\d+/\d+ \d+:\d+", stringForDate)[0]
    res_date = datetime.datetime.strptime(stringForHour, r"%d/%m/%y %H:%M")
    #for content
    article_body = soup.find("div", {"class": "txtbig content_news"})
    article_body = article_body.p
    listSentence = article_body.strings
    res_content = ""
    for sentence in listSentence:
        res_content += sentence.string
    res_content = re.sub(r"\.(?=\D)", ". ", res_content)
    return {"title": res_title, "date": str(res_date), "content": res_content}



def scrapOnePage(link : str):
    """
    This function scraps all the articles of a page by applying scrap_article_CF to each of them.

    Parameters
    ----------
    link : str
        The link of the page.
    
    Returns
    -------
    dataset : list
        The list of all the articles of the page.
    """
    dataset = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    listOfLink = soup.find("div", {"class":"newslft"})
    listOfLink = listOfLink.findAll("div")
    for div_class in listOfLink:
        if "(CF)" in div_class.contents[-1]:
            dataset.append(scrap_article_CF(f"""https://www.abcbourse.com{div_class.a.get("href")}"""))
    return dataset


# à recoder en plus propre (ou pas)
def scrapOnSite(link, limite : int = 4, iter : int = 0, res = None):
    """
    This function scraps some articles of a site by looking into every page and applying scrapOnePage.
    This function is recursive.
    
    Parameters
    ----------
    link : str
        The link of the site.
    limite : int
        The maximum number of pages to scrap.
    iter : int
        The number of pages already scrapped.
    res : list
        The list of all the articles scrapped (the result).

    Returns
    -------
    res : list
        The list of all the articles scrapped. 
        Each article is a dictionary with the keys "title", "date" and "content".
    """
    if res is None:
        res = []
    iter +=1
    queue = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    listOfLink = soup.find("ul", {"class":"pagin"})
    listOfLink = listOfLink.findAll("li")
    for link in listOfLink:
        queue.append(f"https://www.abcbourse.com{link.a.get('href')}")
    while queue and iter < limite:
        if len(queue) == 1:
            scrapOnSite(queue[0], limite, iter, res)
            res += scrapOnePage(queue.pop(0))
        else:
            res += scrapOnePage(queue.pop(0))
    return res



# main
if __name__ == "__main__": 
    print(scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216"))
    print(scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-va-decarboner-une-cimenterie-d-holcim_594182"))
    print(scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-blackrock-detient-moins-d-actions_476418"))
    print(scrapOnePage("https://www.abcbourse.com/marches/news_valeur/AIp/10"))
    print(scrapOnSite("https://www.abcbourse.com/marches/news_valeur/AIp"))