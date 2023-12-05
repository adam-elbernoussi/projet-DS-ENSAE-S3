"""In this file, we will implement the clustering algorithm. More precisely, we will implement a K-means method.
   The input of this algorithm is a list of vectors (the vectors are the word embeddings of the words in the corpus).
   The output is a list of clusters, where each cluster is a label/category"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import seaborn as sns 
from sklearn.feature_extraction.text import CountVectorizer

def vectorize(corpus):
    vectorizer = CountVectorizer()
    vectorizedCorpus = vectorizer.fit_transform(corpus)
    return vectorizedCorpus



def clustering():
    pass


if __name__ == "__main__":
    df = pd.read_csv("data/AIP_cleanarticles.csv")
    print(df.head())
    corpus = ['This is the first document.', 'This document is the second document.', 'And this is the third one.', 'Is this the first document?']
    vectorizedCorpus = vectorize(corpus)
    print(vectorizedCorpus.toarray())
