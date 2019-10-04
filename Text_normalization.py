import nltk
import re  # regular expression
import collections
import string
from spellchecker import SpellChecker


# Separa todas os elementos do texto
def text_tokenize(text):
    """

    :param text:
    :return:
    """
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


# Retira os caracteres especiais
def remove_specialchar(tokens):
    """

    :param tokens:
    :return:
    """
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens])
    return filtered_tokens


# Retira stop words
def remove_stopwords(tokens):
    """

    :param tokens:
    :return:
    """
    stopwords = nltk.corpus.stopwords.words('portuguese')
    filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


# Stemming
def stemming(filtered_text):
    """

    :param filtered_text:
    :return:
    """
    stemmer = nltk.stem.RSLPStemmer()
    stemmed_text = stemmer.stem(filtered_text)
    stemmed_tokens = text_tokenize(stemmed_text)
    return stemmed_tokens


# Conta as palavras e suas frequencias
def count_word(tokens):
    """

    :param tokens:
    :return:
    """
    word_counts = collections.Counter(tokens)
    return word_counts


def spell_check(tokens):
    """

    :param tokens:
    :return:
    """
    corrected_dict = {}
    output_corrected_list = {}
    corrected_tokens = list(tokens)
    spell = SpellChecker(distance=2, language='pt')  # recomendada para palavras grandes
    spell.word_frequency.load_text_file('./romans_up_to_3999.txt')
    misspelled = spell.unknown(corrected_tokens)
    for word in misspelled:
        if word != spell.correction(word):
            corrected_tokens.append(spell.correction(word))
        else:
            misspelled = [token for token in misspelled if token != word]
        corrected_dict[word] = spell.correction(word)
        output_corrected_list.update(corrected_dict)
    corrected_tokens = [token for token in corrected_tokens if token not in misspelled]
    return corrected_tokens, output_corrected_list


# cor, out = spell_check(remove_specialchar(text_tokenize('agricuura qulquer agricuura qlquer XXII')))
# print(cor)
# print(out)
