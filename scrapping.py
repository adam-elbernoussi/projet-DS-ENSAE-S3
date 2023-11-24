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

ticker = "BNPP"
name = "bnp-paribas"

#Coding functions
def scrap_article(link : str):
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






# main
if __name__ == "__main__": 
    print(scrap_article("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216"))

