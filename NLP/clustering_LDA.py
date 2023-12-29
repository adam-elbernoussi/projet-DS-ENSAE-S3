"""In this file, we will implement the clustering algorithm. More precisely, we will implement a K-means method.
   The input of this algorithm is a list of vectors (the vectors are the word embeddings of the words in the corpus).
   More precisely, the algorithm is a pipeline that transorms a list words (article scleaned by lemmatization) in vector by counting the words and then applying the K-means algorithm.
   The output is a list of clusters, where each cluster is a label/category
   
   For the vizualisation we add a PCA step.
   And then we plot the 2D PCA of the articles with the color of the cluster.
   """

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.decomposition import LatentDirichletAllocation


#usefull
pipeline = make_pipeline(CountVectorizer(), KMeans(n_clusters=3, random_state=0, n_init="auto"))
colors  = ["navy", "turquoise", "darkorange"]


if __name__ == "__main__":
    df = pd.read_csv("data/AIP_cleanarticles.csv")
    corpus = df['content']

    vectorizer = CountVectorizer()
    vectorizedCorpus = vectorizer.fit_transform(corpus.apply(lambda s: ' '.join(s)))
    print(vectorizedCorpus)
    

    #number_topics = 5
    # number_words = 10# Create and fit the LDA model
    # lda = LatentDirichletAllocation(n_components=11, max_iter=5,
    #                                 learning_method = 'online',
    #                                 learning_offset = 50.,
    #                                 random_state = 0,
    #                                 n_jobs = 1)
    # lda.fit(df['content_vectorized'])
    #print(df)

    # X = np.array(df['content_vectorized'].tolist())
    # kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(X)
    # df['label'] = kmeans.labels_

    # pca = PCA(n_components=2)
    # pca.fit(X)
    # df['PCA2D'] = pca.transform(X).tolist()

    # plt.figure()
    # for color, i in zip(colors, [0, 1, 2]):
    #     plt.scatter(df[df['label'] == i]['PCA2D'].apply(lambda x: x[0]), df[df['label'] == i]['PCA2D'].apply(lambda x: x[1]), color=color,label=i)
    # plt.legend(loc='best', shadow=False, scatterpoints=1)
    # plt.title('KMeans clustering of the articles PCA')
    # #plt.savefig("output/PCA_clustering.png")
    # plt.show()