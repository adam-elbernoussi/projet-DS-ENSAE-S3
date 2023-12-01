"""In this file, we will clean the text of the articles scrapped in scrapping.py"""

"""
In order to clean the text we will proceed in 3 steps :
- Tokenization
- Stop words removal
- Stemming
"""

#Importing libraries
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

#Coding functions
def tokenization(text : str):
    words = nltk.word_tokenize(text, language='french')
    print(words)
    words = [word for word in words if word.isalpha()]
    return words

def remove_stop_words(words : list):
    stop_words = set(stopwords.words('french'))
    wordsNoStopWords = [word for word in words if word not in stop_words]
    return wordsNoStopWords

def stemming(words : list):
    stemmer = SnowballStemmer("french")
    wordsStemmed = [stemmer.stem(word) for word in words] 
    return wordsStemmed

if __name__ =="__main__":
    text = """Air Liquide a annoncé mardi avoir signé de nouveaux contrats de long terme avec le sud-africain Sasol portant sur des capacités d'électricité renouvelable de 100 MW au niveau du site de Secunda. Le partenariat a été conclu avec le fournisseur d'énergie éolienne et solaire Mainstream Renewable Power, qui a été chargé de construire une ferme solaire qui devrait être opérationnelle en 2025. Il s'agit de la troisième série de 'PPA' conclus par Air Liquide et Sasol, après ceux déjà annoncés en début d'année avec Enel Green Power et avec TotalEnergies et son partenaire Mulilo. Ces accords doivent contribuer à l'objectif d'Air Liquide de réduire de 30% à 40% les émissions de CO2 liées à la production d'oxygène d'ici 2031 à Secunda, où le groupe exploite le plus grand site de production d'oxygène au monde. Pour mémoire, Air Liquide a racheté à Sasol les 16 unités de production d'oxygène de ce dernier à Secunda, qu'il exploite désormais depuis juin 2021. En tenant compte d'une autre unité de séparation des gaz de l'air (ASU) que le groupe opérait déjà pour Sasol, Air Liquide exploite un total de 17 ASU à Secunda, pour une capacité totale de 47.000 tonnes d'oxygène par jour."""
    tokenList = tokenization(text)
    tokenListNoStopWords = remove_stop_words(tokenList)
    stemmedTokenList = stemming(tokenListNoStopWords)
    print(tokenList)
    print(tokenListNoStopWords)
    print(stemmedTokenList)

