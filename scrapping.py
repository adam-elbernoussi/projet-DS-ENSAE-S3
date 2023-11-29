"""In this file, we will scrap some articles about a company given its ticker."""
"""Firstly, on the website Investing.com"""

#Importing libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import datetime
import time



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
    article_body = article_body.p
    listSentence = article_body.strings
    res_content = ""
    for sentence in listSentence:
        res_content += sentence.string
    res_content = re.sub(r"\.(?=\D)", ". ", res_content)
    res_content = re.findall(r"- (.*) Copyright", res_content)[0]
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
    dataset = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    listOfLink = soup.find("div", {"class":"newslft"})
    listOfLink = listOfLink.findAll("div")
    for div_class in listOfLink:
        if "(CF)" in div_class.contents[-1]:
            dataset.append(scrap_article_CF(f"""https://www.abcbourse.com{div_class.a.get("href")}"""))
    return dataset

def scrapOnSite(link, limite : int = 3, iter : int = 0):
    iter +=1
    res = []
    queue = []
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')
    listOfLink = soup.find("ul", {"class":"pagin"})
    listOfLink = listOfLink.findAll("li")
    for link in listOfLink:
        queue.append(f"https://www.abcbourse.com{link.a.get('href')}")
    while queue and iter < limite:
        if len(queue) == 1:
            scrapOnSite(queue[0], limite, iter)
            #res.append(scrapOnePage(queue.pop(0)))
            queue.pop(0)
            res.append(1)
        else:
            #res.append(scrapOnePage(queue.pop(0)))
            queue.pop(0)
            res.append(1)
    return res

    

# main
if __name__ == "__main__": 
    # print(scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216"))
    # file = open("file.txt", "w")
    # file.write(str(scrapOnSite("ALP")))
    # file.close()
    print(scrapOnSite("https://www.abcbourse.com/marches/news_valeur/AIp"))
    #print(scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216"))
    # a = dict([['e', 5], ['r', 5]])
    # b = dict([['e', 6], ['r', 6]])
    # print(pd.DataFrame([a, b]))