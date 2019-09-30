import nltk
import re  # regular expression
import collections
import string


# Separa todas os elementos do texto
def text_tokenize(text):
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


# Retira os caracteres especiais
def remove_specialchar(tokens):
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    return filtered_tokens


# Retira stop words
def remove_stopwords(tokens):
    stopwords = nltk.corpus.stopwords.words('portuguese')
    filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


# Stemming
def stemming(filtered_text):
    stemmer = nltk.stem.RSLPStemmer()
    stemmed_text = stemmer.stem(filtered_text)
    stemmed_tokens = text_tokenize(stemmed_text)
    return stemmed_tokens


# Conta as palavras e suas frequencias
def count_word(tokens):
    word_counts = collections.Counter(tokens)
    return word_counts
