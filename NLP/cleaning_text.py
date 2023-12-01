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

#Coding functions
def tokenization(text : str):
    words = nltk.word_tokenize(text, language='french')
    print(words)
    words = [word for word in words if word.isalpha()]
    return words


