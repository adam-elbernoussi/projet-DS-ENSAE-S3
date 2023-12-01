import pandas as pd
import scrapping

ticker = "AIP"
link = f"https://www.abcbourse.com/marches/news_valeur/{ticker}"

if __name__ == '__main__':
    # First, constructon of the DataBase of articles
    scrappingResult = scrapping.scrapOnSite(link)
    df = pd.DataFrame(scrappingResult)
    df.to_csv(f"data/{ticker}_articles.csv")