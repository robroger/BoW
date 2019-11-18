import nltk
from nltk.tokenize import RegexpTokenizer
import re
# from unidecode import unidecode
import collections
import string
from spellchecker import SpellChecker


# TODO: biblioteca UNIDECODE
# TODO: arrumar os retornos
# TODO: palavras com hífen deveriam ficar com hífen?


def text_tokenize(text):
    """
    Separa as palavras de um texto.
    :param text: 'Isso é um texto!'
     :return: tokens: ['Isso', 'é', 'um', 'texto','!']
    """
    # text = unidecode(text)
    text = re.sub(r'-(?:me|te|se|nos|vos|o|os|a|as|lo|los|la|las|lhe|lhes|lha|lhas|lho|lhos|no|na|nas|mo|ma|mos'
                  r'|mas|to|ta|tos|tas)\b', '', text)
    tokenizer = RegexpTokenizer(
        r'(R\$\s?(?:\d{1,3}.?)+,\d{2})|'
        r'(\d+/\d+)|'
        r'(\w+)', gaps=True)
    tokens = tokenizer.tokenize(text)
    return tokens


def remove_specialchar(tokens):
    """
    Retira as palavras (tokens) que são caracteres especiais de uma lista de palavras.
    Mantém pontos e vírgulas de números.
    :param tokens: ['Isso', 'é', 'um', 'texto','!']
    :return filtered_tokens: ['Isso', 'é', 'um', 'texto']
    """
    pattern_decimal = re.compile(r"(R\$\s)?(\d{1,3}\.?)+(,\d{2})")
    # pattern_enclise = re.compile(r"\b(\w+)-(me|te|se|nos|vos|o|os|a|as|lo|los|la|las|lhe|lhes|lha|lhas|lho|lhos|no|na"
    #                              r"|nas|mo|ma|mos|mas|to|ta|tos|tas)\b")
    decimals = [token for token in tokens if pattern_decimal.match(token)]
    # enclises = [token for token in tokens if pattern_enclise.match(token)]
    # tokens = [token for token in tokens if token not in (decimals + enclises)]
    tokens = [token for token in tokens if token not in decimals]
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    tokens = [pattern.sub('', token) for token in tokens]
    # tokens.extend(decimals + enclises)
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
    # TODO: adicionar dicionário com siglas de órgãos públicos
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
    return spellcheck_tokens, output_corrected_list


sp = 'EXTRATO DE TERMO ADITIVO Nº 4/2017 - UASG 133003'
tp = 'teste testa-la testa-lo R$ 5.000,00'
print(text_tokenize(sp))
print(list(remove_specialchar(text_tokenize(sp))))
