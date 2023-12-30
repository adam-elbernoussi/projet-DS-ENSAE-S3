"""In this file, we will clean the text of the articles scrapped in scrapping.py"""

"""
In order to clean the text we will proceed in 3 steps :
- Tokenization
- Stop words removal
- Stemming
"""

#Importing libraries
import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer

#Coding functions
#tokenization
def tokenization(text : str):
    """
    This function tokenizes a text in french. And only keeps the words.

    Parameters
    ----------
    text : str
        The text to tokenize.

    Returns
    -------
    words : list
        The list of words (token) of the text.
    """
    words = nltk.word_tokenize(text, language='french')
    words = [word for word in words if word.isalpha()]
    return words

#stop words removal
def remove_stop_words(words : list):
    """
    This function removes the stop words from a list of words.
    
    Parameters
    ----------
    words : list
        The list of words.
        
    Returns
    -------
    wordsNoStopWords : list
        The list of words without stop words.
    """
    stop_words = set(stopwords.words('french'))
    wordsNoStopWords = [word for word in words if word not in stop_words]
    return wordsNoStopWords

#stemming
def stemming(words : list):
    """
    This function stems a list of words.
    
    Parameters
    ----------
    words : list
        The list of words.
    
    Returns
    -------
    wordsStemmed : list
        The list of stemmed words.
    """
    stemmer = SnowballStemmer("french")
    wordsStemmed = [stemmer.stem(word) for word in words] 
    return wordsStemmed

#alternative lemmatization
def lemmatization(words : list):
    """
    This function lemmatizes a list of words.
    
    Parameters
    ----------
    words : list
        The list of words.
    
    Returns
    -------
    wordsLemmatized : list
        The list of lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    wordsLemmatized = [lemmatizer.lemmatize(word) for word in words]
    return wordsLemmatized

#aggregation functions
def cleaningText(text : str):
    """
    This function cleans a text by applying the 3 previous functions (Tokenization, stop words removal, stemming). 
    It also removes some words that are not useful for our analysis.
    
    Parameters
    ----------
    text : str
        The text to clean.
    
    Returns
    -------
    list
        The list of cleaned words.
    """
    tokenList = tokenization(text)
    tokenListNoStopWords = remove_stop_words(tokenList)
    stemmedTokenList = stemming(tokenListNoStopWords)

    SetOfUnusefulWords = set(["air", "liquid"])
    
    return [word for word in stemmedTokenList if word not in SetOfUnusefulWords]


def cleaningTextLDA(text : str):
    """
    This function cleans a text by applying the 3 previous functions (Tokenization, stop words removal, lemmatization).

    Parameters
    ----------
    text : str
        The text to clean.

    Returns
    -------
    lemmatizedTokenList : list
        The list of cleaned words.
    """
    tokenList = tokenization(text)
    tokenListNoStopWords = remove_stop_words(tokenList)
    lemmatizedTokenList = lemmatization(tokenListNoStopWords)
    
    return lemmatizedTokenList



if __name__ =="__main__":
    text = """Air Liquide a annoncé mardi avoir signé de nouveaux contrats de long terme avec le sud-africain Sasol portant sur des capacités d'électricité renouvelable de 100 MW au niveau du site de Secunda. Le partenariat a été conclu avec le fournisseur d'énergie éolienne et solaire Mainstream Renewable Power, qui a été chargé de construire une ferme solaire qui devrait être opérationnelle en 2025. Il s'agit de la troisième série de 'PPA' conclus par Air Liquide et Sasol, après ceux déjà annoncés en début d'année avec Enel Green Power et avec TotalEnergies et son partenaire Mulilo. Ces accords doivent contribuer à l'objectif d'Air Liquide de réduire de 30% à 40% les émissions de CO2 liées à la production d'oxygène d'ici 2031 à Secunda, où le groupe exploite le plus grand site de production d'oxygène au monde. Pour mémoire, Air Liquide a racheté à Sasol les 16 unités de production d'oxygène de ce dernier à Secunda, qu'il exploite désormais depuis juin 2021. En tenant compte d'une autre unité de séparation des gaz de l'air (ASU) que le groupe opérait déjà pour Sasol, Air Liquide exploite un total de 17 ASU à Secunda, pour une capacité totale de 47.000 tonnes d'oxygène par jour."""
    tokenList = tokenization(text)
    tokenListNoStopWords = remove_stop_words(tokenList)
    stemmedTokenList = stemming(tokenListNoStopWords)
    cleantext = cleaningText(text)
    cleantextLDA = cleaningTextLDA(text)
    print(tokenList)
    print(tokenListNoStopWords)
    print(stemmedTokenList)
    print(cleantext)
    print(cleantextLDA)

    #We add a nice wordcloud that allows us to see the most used/important words in the article
    wordcloud = WordCloud().generate(" ".join(cleantext))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()