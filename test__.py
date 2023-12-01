from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

corpus = [
    'Un premier document à propos des chats.',
    'Un second document qui parle des chiens.'
]

vectorizer = CountVectorizer()
vectorizer.fit(corpus)

vectorizer.get_feature_names_out()

X = vectorizer.transform(corpus)
print(X.toarray())

cv_bow = fit_vectorizers(CountVectorizer)