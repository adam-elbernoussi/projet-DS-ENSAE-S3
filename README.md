# projet-DS-ENSAE-S3

For this computer science project, we decided to explore the connections between published articles about companies and their stock prices.

To do this, we chose to focus on a major French company: Air Liquide, in order to collect a significant number of articles.

The aim of our work is to design an algorithm that, for a given article about Air Liquide, determines whether the impact of this article is positive, negative, or neutral on the company's stock price.

Firstly, we proceeded with data collection: the general information of the company, articles about it, and the fluctuations in its stock price. To achieve this, we employed web scraping. Then, we conducted a preprocessing step to transform the collected articles into vectors. Finally, to group the articles, we used clustering.

## Quick start
In order to run this project form the SSP cloud
You have to firstly set you terminal in the folder ie going from work to onyxia/home/projet-DS-ENSAE-S3, run :

cd onyxia/home/projet-DS-ENSAE-S3

once you are here you should install some packages, run :

pip3 install -r requirements.txt

Then, still in the folder of the project, you can run all the different files 