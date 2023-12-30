"""In this file, we will implement another version of the clustering algorithm. More precisely, we will implement a K-means method.
   The algorithm is a pipeline that transorms a list words (article cleaned by lemmatization) in vector by counting the words, then applying a LDA (latent dirichlet allocation) and then applying the K-means algorithm.
   The output is a list of clusters, where each cluster is a label/category
   
   For the vizualisation we add a PCA step.
   And then we plot the 2D PCA of the articles with the color of the cluster.

   Then we finish the file by implementing a grid search in order to fine tune the number of topics in the LDA
   We try to find the number of components that maximizes the difference between the means of the variations (stock price) of each cluster
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
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV


#usefull
pipeline_LDA = make_pipeline(CountVectorizer(), 
                            LatentDirichletAllocation(n_components=32),
                            KMeans(n_clusters=3, random_state=0, n_init="auto"))

colors = ["navy", "turquoise", "darkorange"]


if __name__ == "__main__":
    df = pd.read_csv("data/AIP_cleanarticles.csv", index_col=0)

    vectorizer = CountVectorizer()
    vectorizedCorpus = vectorizer.fit_transform(df['cleaned_article_lemmatization'])

    number_topics = 30
    lda = LatentDirichletAllocation(n_components=number_topics, max_iter=5,
                                    learning_method = 'online',
                                    learning_offset = 50.,
                                    random_state = 0,
                                    n_jobs = 1)
    lda.fit(vectorizedCorpus)

    df['content_vectorized'] = lda.transform(vectorizedCorpus).tolist()

    X = np.array(df['content_vectorized'].tolist())
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(X)
    df['label'] = kmeans.labels_

    pca = PCA(n_components=2)
    pca.fit(X)
    df['PCA2D'] = pca.transform(X).tolist()

    plt.figure()
    for color, i in zip(colors, [0, 1, 2]):
        plt.scatter(df[df['label'] == i]['PCA2D'].apply(lambda x: x[0]), df[df['label'] == i]['PCA2D'].apply(lambda x: x[1]), color=color,label=i)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('KMeans clustering of the articles PCA')
    #plt.savefig("output/PCA_clustering_LDA.png")
    plt.show()

    #We will now use the pipeline to fine-tune the number of topics in the LDA asking for clusters that maximize the difference between the means of the variations of the clusters

    #Firstly we have to compute here as it is done into the main.py the variation of the stock price and the benchmark
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x.split(' ')[0]))
    df.set_index('date', inplace=True)
    
    df_bench = pd.read_csv(f"data/^FCHI.csv", index_col=0)
    df_bench['variation bench'] = df_bench['Close'].pct_change(fill_method=None)
    df_bench.dropna(inplace=True)
    df_bench = df_bench.drop(columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df_bench.index = pd.to_datetime(df_bench.index)

    df_var = pd.read_csv(f"data/AI.PA.csv", index_col=0)
    df_var = df_var.drop(columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df_var['variation'] = df_var['Close'].pct_change(fill_method=None)
    df_var = df_var.dropna()
    df_var.index = pd.to_datetime(df_var.index)
    df_var = df_var.drop(columns=['Close'])

    df = df.merge(df_var, how='inner', left_index=True, right_index=True)
    df = df.merge(df_bench, how='inner', left_index=True, right_index=True)

    reglin = LinearRegression()
    reglin = reglin.fit(df['variation bench'].values.reshape(-1, 1), df['variation'].values.reshape(-1, 1))
    intercept, beta = reglin.intercept_, reglin.coef_[0]

    df['Adj variation'] = df['variation'] - beta*df['variation bench']

    df = df.reset_index()

    #Implementing the grid search for the number of topics

    #the idea here is to implement a grid search for the number of topics in the LDA that maximizes the difference between the means of the variations of each cluster
    #thus we have to code a scoring function that computes the distance between the means of the clusters

    def _wider_scorer(estimator, X):
        """
        This function computes the distance between the means of the variations of each cluster
        This is an auxiliary function that computes a custom score for the grid search.
        
        Parameters
        ----------
        estimator : sklearn estimator
            The estimator to use.
        X : array
            The data to fit.
        
        Returns
        -------
        np.sum(np.array([means[0]-means[1], means[0]-means[2], means[1]-means[2]])**2) : float
            The distance between the means of the clusters
        """
        _df = df.copy()
        _df = _df.loc[X.index]
        #transform the data
        vectorized = estimator.named_steps['countvectorizer'].transform(X)
        lda_transformed = estimator.named_steps['latentdirichletallocation'].transform(vectorized)
        labels = estimator.named_steps['kmeans'].fit_predict(lda_transformed)

        _df['cluster_label'] = labels
        #computing the mean on each cluster
        means = _df.groupby('cluster_label')['Adj variation'].mean().values
        
        return np.sum(np.array([means[0]-means[1], means[0]-means[2], means[1]-means[2]])**2)

    #Now the grid search
    params = {'latentdirichletallocation__n_components': list(range(5, 70))}

    grid = GridSearchCV(pipeline_LDA, 
                        param_grid = params, 
                        scoring = _wider_scorer)
    grid.fit(df['content'])

    print("The best number of components is :", grid.best_params_)