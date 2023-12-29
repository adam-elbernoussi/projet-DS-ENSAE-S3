import pandas as pd
from Scrapping import scrapping
from NLP import cleaning_text
from NLP import clustering_counting
from NLP import clustering_LDA
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

ticker = "AIP"
link = f"https://www.abcbourse.com/marches/news_valeur/{ticker}"

if __name__ == '__main__':
    # First, constructon of the DataBase of articles
    #scrappingResult = scrapping.scrapOnSite(link) à remettre
    #df = pd.DataFrame(scrappingResult)
    #df.to_csv(f"data/{ticker}_articles.csv")

    #Then preprocessing the text
    #df = df.dropna()
    #df["content"] = df["content"].apply(cleaning_text.cleaningText)
    #print(df)
    #df.to_csv(f"data/{ticker}_cleanarticles.csv")

    df = pd.read_csv(f"data/{ticker}_cleanarticles.csv", index_col=0)
    df['date'] = df['date'].apply(lambda x: x.split(" ")[0])
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df = df.set_index('date')
    df.drop(columns=['title'], inplace=True)

    # We will now compute the variation of the stock price
    df_var = pd.read_csv(f"data/AI.PA.csv", index_col=0)
    df_var = df_var.drop(columns = ['Open', 'High', 'Low', 'Adj Close', 'Volume'])
    df_var['variation'] = df_var['Close'].pct_change(fill_method=None)
    df_var = df_var.dropna()
    df_var.index = pd.to_datetime(df_var.index)
    df_var = df_var.drop(columns=['Close'])

    # We will now compute the variation of the benchmark
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
    df['category'] = clustering_counting.pipeline.fit_predict(df['content'])

    # Printing and plotting the results
    print('moyenne des var adj :', df['Adj variation'].mean()*100)
    print('Moyenne des variations par cluster :', df.groupby('category')['Adj variation'].mean()*100) #first encouraging result

    fig, list_of_fig = plt.subplots(nrows=3, sharex=True, figsize=(7, 7))
    fig.suptitle("Distribution of the variations by cluster \n The mean of adjusted variations is : " + str(round(df['Adj variation'].mean()*100, 2)) + "%")

    for i in range(3):
        list_of_fig[i].hist(df[df['category']==i]['Adj variation']*100, bins=50)
        mean = round(df[df['category']==i]['Adj variation'].mean()*100, 2)
        list_of_fig[i].set_title('Cluster ' + str(i) + ' : ' + str(mean) + "%")
        list_of_fig[i].set_ylabel('Frequency')
        list_of_fig[i].axvline(x=mean, color='red', label = 'Mean : ' + str(mean) + "%")
        list_of_fig[i].legend()
    
    list_of_fig[2].set_xlabel('Variation (%)')
    plt.show()