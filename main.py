import pandas as pd
from Scrapping import scrapping
from NLP import cleaning_text
from NLP import clustering
import matplotlib.pyplot as plt
from wordcloud import WordCloud

ticker = "AIP"
link = f"https://www.abcbourse.com/marches/news_valeur/{ticker}"

if __name__ == '__main__':
    # First, constructon of the DataBase of articles
    scrappingResult = scrapping.scrapOnSite(link)
    df = pd.DataFrame(scrappingResult)
    #df.to_csv(f"data/{ticker}_articles.csv")

    #Then preprocessing the text
    df = df.dropna()
    df["content"] = df["content"].apply(cleaning_text.cleaningText)
    print(df)
    #df.to_csv(f"data/{ticker}_cleanarticles.csv")