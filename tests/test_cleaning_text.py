import sys

import unittest
sys.path.append("NLP/")

from urllib import request

url = "https://www.gutenberg.org/files/17989/17989-0.txt"
response = request.urlopen(url)
raw = response.read().decode('utf8')

dumas = raw.split("*** START OF THE PROJECT GUTENBERG EBOOK LE COMTE DE MONTE-CRISTO, TOME I ***")[1].split("*** END OF THE PROJECT GUTENBERG EBOOK LE COMTE DE MONTE-CRISTO, TOME I ***")[0]

import re

def clean_text_(text):
    text = text.lower() # mettre les mots en minuscule
    text = " ".join(text.split())
    return text

dumas = clean_text_(dumas)



# test
from cleaning_text import tokenization, remove_stop_words, stemming

class Test_tokenization(unittest.TestCase):
    def test_tokenization_type(self):
        res = tokenization("Ce matin, je me suis baladé dans la forêt. J'ai vu un lapin, et un écureuil. J'ai mangé une pomme.")
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

    def test_tokenization_content(self):
        res = tokenization("Ce matin, je me suis baladé dans la forêt. J'ai vu un lapin, et un écureuil. J'ai mangé une pomme.")
        self.assertEqual(res, ['Ce', 'matin', 'je', 'me', 'suis', 'baladé', 'dans', 'la', 'forêt', 'vu', 'un', 'lapin', 'et', 'un', 'écureuil', 'mangé', 'une', 'pomme'])

    def test_tokenisation_other(self):
        res = tokenization("J'apprécie fortement le poulet sauce moutarde avec le riz rond et la sauce champignons.")
        self.assertEqual(res, ['fortement', 'le', 'poulet', 'sauce', 'moutarde', 'avec', 'le', 'riz', 'rond', 'et', 'la', 'sauce', 'champignons'])
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

class Test_remove_stop_words(unittest.TestCase):
    def test_remove_stop_words_type(self):
        res = remove_stop_words(['Ce', 'matin', 'je', 'me', 'suis', 'baladé', 'dans', 'la', 'forêt', 'vu', 'un', 'lapin', 'et', 'un', 'écureuil', 'mangé', 'une', 'pomme'])
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

    def test_remove_stop_words_content(self):
        res = remove_stop_words(['Ce', 'matin', 'je', 'me', 'suis', 'baladé', 'dans', 'la', 'forêt', 'vu', 'un', 'lapin', 'et', 'un', 'écureuil', 'mangé', 'une', 'pomme'])
        self.assertEqual(res, ['Ce', 'matin', 'baladé', 'forêt', 'vu', 'lapin', 'écureuil', 'mangé', 'pomme'])

    def test_remove_stop_words_other(self):
        res = remove_stop_words(['fortement', 'le', 'poulet', 'sauce', 'moutarde', 'avec', 'le', 'riz', 'rond', 'et', 'la', 'sauce', 'champignons'])
        self.assertEqual(res, ['fortement', 'poulet', 'sauce', 'moutarde', 'riz', 'rond', 'sauce', 'champignons'])
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

class Test_stemming(unittest.TestCase):
    def test_stemming_type(self):
        res = stemming(['Ce', 'matin', 'baladé', 'forêt', 'vu', 'lapin', 'écureuil', 'mangé', 'pomme'])
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

    def test_stemming_content(self):
        res = stemming(['Ce', 'matin', 'baladé', 'forêt', 'vu', 'lapin', 'écureuil', 'mangé', 'pomme'])
        self.assertEqual(res, ['ce', 'matin', 'balad', 'forêt', 'vu', 'lapin', 'écureuil', 'mang', 'pomm'])

    def test_stemming_other(self):
        res = stemming(['fortement', 'poulet', 'sauce', 'moutarde', 'riz', 'rond', 'sauce', 'champignons'])
        self.assertEqual(res, ['fort', 'poulet', 'sauc', 'moutard', 'riz', 'rond', 'sauc', 'champignon'])
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)


if __name__ == "__main__":
    unittest.main()