import nltk
import re
import collections
import string
from spellchecker import SpellChecker


def text_tokenize(text):
    """
    Separa as palavras de um texto.
    :param text: 'Isso é um texto!'
    :return: tokens: ['Isso', 'é', 'um', 'texto','!']
    """
    tokens = nltk.word_tokenize(text)
    tokens = [token.strip() for token in tokens]
    return tokens


def remove_specialchar(tokens):
    """
    Retira as palavras (tokens) que são caracteres especiais de uma lista de palavras.
    Mantém pontos e vírgulas de números.
    :param tokens: ['Isso', 'é', 'um', 'texto','!']
    :return filtered_tokens: ['Isso', 'é', 'um', 'texto']
    """
    pattern_decimal = re.compile('^[0-9]+[.,][0-9]+[.,]?[0-9]+[.,]?[0-9]+[.,]?[0-9]+$')
    decimals = [token for token in tokens if pattern_decimal.match(token)]
    tokens = [token for token in tokens if token not in decimals]
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    # TODO: eu deveria deixar o $ para 'R$'?
    tokens = [pattern.sub('', token) for token in tokens]
    tokens.extend(decimals)
    filtered_tokens = filter(None, tokens)
    return filtered_tokens


def remove_stopwords(tokens):
    """
    Retira as stopwords de uma lista de palavras. Exemplo de stopwords: ['a', 'ao', 'aos', 'aquela', 'aquelas',
    'aquele', 'aqueles', 'aquilo', 'as', 'at\xe9']
    :param tokens: ['Isso', 'é', 'um', 'texto','!']
    :return: filtered_text: 'Isso texto !'
    """
    stopwords = nltk.corpus.stopwords.words('portuguese')
    filtered_tokens = [token for token in tokens if token not in stopwords]
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text


def stemming(text):
    """
    O Stemming remove variações de sufixo de palavras, como plural, feminino/masculino, gerúndio, diminutivo.
    Para processamento em português é utilizado o RSLP Stemmer.
    :param text: 'Isso é um textinho'
    :return: stemmed_tokens: ['isso', 'é', 'um', 'text']
    """
    stemmer = nltk.stem.RSLPStemmer()
    stemmed_text = stemmer.stem(text)
    stemmed_tokens = text_tokenize(stemmed_text)
    return stemmed_tokens


def count_word(tokens):
    """
    Conta a frequência das palavras de uma lista.
    :param tokens: ['Isso', 'é', 'é', 'é', 'um', 'texto', 'texto']
    :return: word_counts: Counter({'é': 3, 'texto': 2, 'Isso': 1, 'um': 1})
    """
    word_counts = collections.Counter(tokens)
    return word_counts


def spell_check_define_dict(spellcheck_dict, lang='pt'):
    """
    Configuração para a correção ortográfica utilizando pyspellcheck. Definição da distância utilizada para a comparação
    utilizando o algoritmo de Levenshtein (1: processamento mais rápido - melhor para palavras pequenas, 2:processamento
    mais lento - melhor para palavras maiores) e do dicionário adicional (além do padrão 'pt' do pyspellcheck)
    :param spellcheck_dict: Caminho do dicionário adicional
    :param lang: Por padrão ='pt'
    :return: spell: parâmetros de configuração do pyspellcheck
    """
    spell = SpellChecker(distance=1, language=lang)
    spell.word_frequency.load_text_file('./romans_up_to_3999.txt')  # adiciona dicionário de números romanos
    ## TODO: adicionar dicionário com siglas de órgãos públicos
    spell.word_frequency.load_text_file(spellcheck_dict)
    return spell


def spell_check(tokens, spell):
    """
    Corrige uma lista de palavras utilizando o pyspellcheck.
    (documentação: https://buildmedia.readthedocs.org/media/pdf/pyspellchecker/latest/pyspellchecker.pdf)
    :param tokens: ['Isso', 'é', 'um', 'texto', 'erado']
    :param spell: parâmetros de configuração definidos por spell_check_define_dict()
    :return: spellcheck_tokens: ['Isso', 'é', 'um', 'texto', 'errado']
             output_corrected_list: {'erado': 'errado'}
    """
    corrected_dict = {}
    output_corrected_list = {}
    spellcheck_tokens = list(tokens)
    misspelled = spell.unknown(spellcheck_tokens)
    misspelled = [token for token in misspelled
                  if any(map(str.isdigit, token)) is False]  # Retira da lista de misspeled expressões com números
    for word in misspelled:
        if word == spell.correction(word):
            misspelled = [token for token in misspelled if token != word]
        else:
            spellcheck_tokens.append(spell.correction(word))
        corrected_dict[word] = spell.correction(word)
        output_corrected_list.update(corrected_dict)
    spellcheck_tokens = [token for token in spellcheck_tokens if token not in misspelled]
    # TODO: Eu deveria fazer um interator ao invés de uma lista?
    # output_corrected_iter = iter(output_corrected_list)
    return spellcheck_tokens, output_corrected_list


# sp = '1.200, Roberta !'
# print(text_tokenize(sp))
# print(list(remove_specialchar(text_tokenize(sp))))

