"""This file is the main file of the project."""

"""
It is structured as follows :
    - First, we scrap the articles from the website abcbourse.com
    - Then we clean the text of the articles (tokenization, stop words removal, stemming/lemmatization)

    - Then we compute the variation of the stock price
    - Then we compute the variation of the benchmark
    - Then we compute the adjusted variation following the well known formula : var = alpha + beta*var_bench (adj_var is the residual thus the alpha)

    - Then we vectorize the cleaned text of the articles
    - Then we cluster the articles using K-means algorithm (those two last steps are done together with a pipeline)

    - Then we plot the distribution of the variations by cluster
The output of this file is the plot of the distribution of the variations by cluster
It also allows a comparison between the results of the clustering with and without LDA (Latent Dirichlet Allocation)
"""

import pandas as pd
from Scrapping import scrapping
from Scrapping import scrapping_data
from NLP import cleaning_text
from NLP import clustering_counting
from NLP import clustering_LDA
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import itertools

ticker = "AIP"
link = f"https://www.abcbourse.com/marches/news_valeur/{ticker}"
url_wiki_airliquide = "https://fr.wikipedia.org/wiki/Air_liquide"

if __name__ == '__main__':
    # First, construction of the DataBase of articles
    """
    Have a look at the module scrapping.py to see some examples of articles scrapped and how the algorithm seeks for the articles on the website
    """
    scrappingResult = scrapping.scrapOnSite(link) #à remettre
    df = pd.DataFrame(scrappingResult)
    df = df[df['date'] <= '2023-12-05'] # line added just to ensure the reproducibility
    df = df[df['date'] >= '2017-06-12'] # line added just to ensure the reproducibility
    df.to_csv(f"data/{ticker}_articles.csv") # this line has been run one time

    # # Then cleaning the text
    df = pd.read_csv(f"data/{ticker}_articles.csv", index_col=0) #emergency line
    df = df.dropna() # just in case
    """
    Have a look at the module cleaning_text.py to see how the text is cleaned step by step
    We also add (in this module) a nice wordcloud visualization of an article as an example
    """
    df["cleaned_article_stemming"] = df["content"].apply(cleaning_text.cleaningText)
    df["cleaned_article_stemming"] = df["cleaned_article_stemming"].apply(str)
    df["cleaned_article_lemmatization"] = df["content"].apply(cleaning_text.cleaningTextLDA)
    df["cleaned_article_lemmatization"] = df["cleaned_article_lemmatization"].apply(str)
    df.to_csv(f"data/{ticker}_cleanarticles.csv") # this line has been run one time

    #df = pd.read_csv(f"data/{ticker}_cleanarticles.csv", index_col=0) #emergency line
    df['date'] = df['date'].apply(lambda x: x.split(" ")[0])
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.set_index('date')
    df.drop(columns=['title'], inplace=True)

    #print(df['cleaned_article_stemming'][0])

    # We add here a step to construct a Database of informations about the company
    df_info = pd.DataFrame(scrapping_data.scrapInfo(url_wiki_airliquide), index=[0])
    df.to_csv(f"data/{ticker}_info.csv")

    # We will now compute the variation of the stock price
    """
    The data of the stock price were downloaded directly from Yahoo Finance as we have arlready scrapped the articles
    """
    df_var = pd.read_csv(f"data/AI.PA.csv", index_col=0)
    df_var = df_var.drop(columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df_var['variation'] = df_var['Close'].pct_change(fill_method=None)
    df_var = df_var.dropna()
    df_var.index = pd.to_datetime(df_var.index)
    df_var = df_var.drop(columns=['Close'])

    # We will now compute the variation of the benchmark
    """
    The data of the benchmark price were downloaded directly from Yahoo Finance too
    """
    df_var_bench = pd.read_csv(f"data/^FCHI.csv", index_col=0)
    df_var_bench = df_var_bench.drop(columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df_var_bench['variation bench'] = df_var_bench['Close'].pct_change(fill_method=None)
    df_var_bench = df_var_bench.dropna()
    df_var_bench.index = pd.to_datetime(df_var_bench.index)
    df_var_bench = df_var_bench.drop(columns=['Close'])

    # merging the three dataframes
    df = df.merge(df_var, how='inner', left_index=True, right_index=True)
    df = df.merge(df_var_bench, how='inner', left_index=True, right_index=True)

    # We will now compute the adjusted variation following the well known formula : var = alpha + beta*var_bench (adj_var is the residual)
    reglin = LinearRegression()
    reglin = reglin.fit(df['variation bench'].values.reshape(-1, 1), df['variation'].values.reshape(-1, 1))
    intercept, beta = reglin.intercept_, reglin.coef_[0]

    df['Adj variation'] = df['variation'] - beta*df['variation bench']


    # clustering
    """
    Have a look at the module clustering_counting.py to see how the clustering is done in the case of a simple counting vectorization
    In this module we also add a PCA step to vizualize the results of the clustering
    you can run the module directly to see it !
    """
    df['category no LDA'] = clustering_counting.pipeline.fit_predict(df['cleaned_article_stemming'])

    """
    Have a look at the module clustering_LDA.py to see how the clustering is done in the case of a LDA vectorization
    In this module too, we add a PCA 2D vizualization of the results
    we also add a gridsearch cross validation to find the best number of topics in the LDA
    we define the best number of topics as the number of topics that maximizes the difference between the means of the variations of the clusters in order to wide the clusters

    An area of improvement if we had more time would be to extend the gridsearch CV to other hyper-parameters of the model and to experiment several score functions

    We definitely encourage you to run this module to see the results !
    """
    df['category LDA'] = clustering_LDA.pipeline_LDA.fit_predict(df['cleaned_article_lemmatization'])


    # Printing and plotting the results
    print('moyenne des var adj :', df['Adj variation'].mean()*100)
    print('Moyenne des variations par cluster :', df.groupby('category no LDA')['Adj variation'].mean()*100) #first encouraging result

    """
    First encouraging result here :
    We can see in the means that we have the expected tilt of the variations.
    While the mean of the variations of the cluster 0 is almost 0% which corresponds to a neutral article category
    The mean of the variations of the cluster 1 is positive : 0.43% which is almost twice the mean of the daily variation of the stock
    And the mean of the variations of the cluster 2 is negative : -0.14%
    
    But when we plot the distribution of the variations by cluster, we can see that there are lots of mistakes in the classification.
    Thus the results are not satisfying.
    
    An idea here is to change the vectorization method. 
    We will try to add an LDA step before the K-means algorithm and plot the comparison.
    """

    fig, list_of_fig = plt.subplots(nrows=3, ncols=2, sharex=True, figsize=(7, 7))
    fig.suptitle("Distribution of the variations by cluster \n The mean of adjusted variations is : " + str(round(df['Adj variation'].mean()*100, 2)) + "%")

    type_vectorization = ["no LDA", "LDA"]
    color = ["steelblue", "darkorange"]

    for i, j in itertools.product(range(3), range(2)):
        list_of_fig[i, j].hist(df[df['category '+type_vectorization[j]]==i]['Adj variation']*100, bins=50, color=color[j])
        mean = round(df[df['category '+type_vectorization[j]]==i]['Adj variation'].mean()*100, 2)
        list_of_fig[i, j].set_title('Cluster '+ type_vectorization[j]+ " " + str(i) + ' : ' + str(mean) + "%")
        list_of_fig[i, j].set_ylabel('Frequency')
        list_of_fig[i, j].axvline(x=mean, color='red', label = 'Mean : ' + str(mean) + "%")
        list_of_fig[i, j].legend()
    
    list_of_fig[2, 0].set_xlabel('Variation (%)')
    list_of_fig[2, 1].set_xlabel('Variation (%)')
    plt.savefig("main_output.jpg")
    plt.show()

    """
    Now we can compare the two methods.
    As we can see and as we expected, the results are better with the LDA vectorization.
    More precisely, the tilt observed in the means of the variations is more pronounced. And errors are less likely to occur.

    Nevertheless, the classification is still not highly satisfying.
    As two categories seem to be pretty good, they contains only few datas and a third category seem to be a catch-all category.

    This can be explained by several reasons :
    - First, the number of articles may not be enough to have a good classification
    - Second, the link between the only news of the day and the variation of the stock price may not be as strong as assumed
    - Third, the vectorization method may not be the best one to discriminate the articles

    Thus an area of improvement would be to find a better way to vectorize the text in order to better discriminate the articles.
    Also we could think about a reverse process : 
    As we have the articles vectorized and the variations of the stock price that could act as a label (if we arbitraty define categories) we could train a classifier (such as a support vector machine classifier) to predict the category of the variation of the stock price.
    Another idea but probably less realistic is to use the variations of the stock price as a target and simply train a regressor to predict the variations of the stock price given a vectorized article.

    We would have tried this if we have had more time : work to do !
    """