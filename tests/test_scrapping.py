import sys

import unittest
from Scrapping.scrapping import scrap_article_CF

class Test_scrap_article_CF(unittest.TestCase):
    def test_scrap_article_CF_title(self):
        res = scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216")
        self.assertEqual(res["title"], "Air Liquide: nouveaux PPA avec Sasol en Afrique du Sud")
    
    def test_scrap_article_CF_date(self):
        res = scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216")
        self.assertEqual(res["date"], "2023-11-21 09:23:00")
        
    def test_scrap_article_CF_content(self):
        #for recent articles
        res = scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216")
        self.assertEqual(res["content"], "Air Liquide a annoncé mardi avoir signé de nouveaux contrats de long terme avec le sud-africain Sasol portant sur des capacités d'électricité renouvelable de 100 MW au niveau du site de Secunda. Le partenariat a été conclu avec le fournisseur d'énergie éolienne et solaire Mainstream Renewable Power, qui a été chargé de construire une ferme solaire qui devrait être opérationnelle en 2025. Il s'agit de la troisième série de 'PPA' conclus par Air Liquide et Sasol, après ceux déjà annoncés en début d'année avec Enel Green Power et avec TotalEnergies et son partenaire Mulilo. Ces accords doivent contribuer à l'objectif d'Air Liquide de réduire de 30% à 40% les émissions de CO2 liées à la production d'oxygène d'ici 2031 à Secunda, où le groupe exploite le plus grand site de production d'oxygène au monde. Pour mémoire, Air Liquide a racheté à Sasol les 16 unités de production d'oxygène de ce dernier à Secunda, qu'il exploite désormais depuis juin 2021. En tenant compte d'une autre unité de séparation des gaz de l'air (ASU) que le groupe opérait déjà pour Sasol, Air Liquide exploite un total de 17 ASU à Secunda, pour une capacité totale de 47.000 tonnes d'oxygène par jour.")
        #for old ones
        res = scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-blackrock-detient-moins-d-actions_476418")
        self.assertEqual(res["content"], "La société BlackRock agissant pour le compte de clients et de fonds dont elle assure la gestion, a déclaré avoir franchi en baisse, le 15 juillet 2019, les seuils de 5% du capital et des droits de vote de la société Air Liquide et détenir, pour le compte desdits clients et fonds, 21 301 512 actions Air Liquide représentant autant de droits de vote, soit 4,97% du capital et des droits de vote de cette société. Ce franchissement de seuils résulte d'une cession d'actions Air Liquide sur le marché et d'une restitution d'actions Air Liquide détenues à titre de collatéral.")

    def test_scrap_article_CF_type(self):
        res = scrap_article_CF("https://www.abcbourse.com/marches/air-liquide-nouveaux-ppa-avec-sasol-en-afrique-du-sud_613216")
        self.assertIsInstance(res["title"], str)
        self.assertIsInstance(res["date"], str)
        self.assertIsInstance(res["content"], str)

if __name__ == "__main__":
    unittest.main()
