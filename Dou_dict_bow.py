import Text_normalization
import datetime
import json
from pathlib import *

dict_dou = []
spellcheck_words_dou = {}


def create_dict_dou(path_data):
    """
    Cria novo dicionário no diretório dicts_dou do projeto a partir dos arquivos em um diretório.
    :param path_data: caminho do diretório com arquivos para criar o dicionário
    """
    i = 0
    filelist = []
    for f in path_data.iterdir():
        filelist.append(f)

    for file in filelist:
        with file.open() as data_file:
            json_data = json.load(data_file)
            for publicacao in json_data:
                i += 1
                print(i)
                # publicacao_text = publicacao_text_join(publicacao)
                publicacao_tokens = publicacao_normalization(publicacao)
                update_dict_dou(publicacao_tokens)

    dump_jsonfile('./dicts_dou/dict_dou', dict_dou)
    dump_jsonfile('./spellcheck/spellcheck_dou', spellcheck_words_dou)


## TODO: não preciso mais dessa função?
def publicacao_text_join(publicacao):
    """
    Junta os campos de uma publicação.
    :param publicacao: {'title': 'Isso', 'body': 'é um texto'}
    :return: puclicacao_text: 'Isso é um texto'
    """
    publicacao_text = ' '.join(map(str, publicacao.values()))
    return publicacao_text


def publicacao_normalization(publicacao):
    """
    Junta os campos de dict de uma publicacao, separa em tokens e remove os caracteres especiais.
    :param publicacao: Uma publicacao de um arquivo json
    :return: filtered_tokens: Palavras da publicação separadas sem caracteres especiais
    """
    publicacao_text = ' '.join(map(str, publicacao.values()))
    tokens = Text_normalization.text_tokenize(publicacao_text)
    filtered_tokens = Text_normalization.remove_specialchar(tokens)
    return filtered_tokens


def update_dict_dou(publicacao_tokens, dict_toupdate=None):
    """
    Atualiza o dicionário do dou (variável global dict_dou[]) com uma nova lista de palavras passadas pela correção
    ortográfica.
    :param publicacao_tokens: iter de palavras
    :param dict_toupdate: caminho para atualizar um dicionário já existente caso a função seja utilizada depois que já
    existir um dicionário previamente criado
    """
    # filtered_tokens = publicacao_normalization(publicacao)
    spell = Text_normalization.spell_check_define_dict('./pt_BR_out.txt')
    # spellcheck_tokens, spellcheck_dict_publicacao = Text_normalization.spell_check(filtered_tokens, spell)
    spellcheck_tokens, spellcheck_dict_publicacao = Text_normalization.spell_check(publicacao_tokens, spell)
    new_words = [token for token in spellcheck_tokens if token not in dict_dou]
    dict_dou.extend(new_words)
    spellcheck_words_dou.update(spellcheck_dict_publicacao)
    if dict_toupdate is not None:
        with open(dict_toupdate, 'r') as data_file:
            json_data = json.load(data_file)
            json_data.extend(dict_dou)
        dump_jsonfile(dict_toupdate, json_data)


def create_bow(publicacao, dict_path):
    """
    Cria o BoW de uma publicação depois de corrigir a publicação utilizando o dicionário indicado.
    :param publicacao: Uma publicacao de um arquivo json
    :param dict_path: caminho do dicionário a ser utilizado
    :return: word_counts: BoW
    """
    filtered_tokens = publicacao_normalization(publicacao)
    spell = Text_normalization.spell_check_define_dict(dict_path, None)
    spellcheck_tokens, corrected_words_list = Text_normalization.spell_check(filtered_tokens, spell)
    filtered_text = Text_normalization.remove_stopwords(spellcheck_tokens)
    stemmed_tokens = Text_normalization.stemming(filtered_text)
    word_counts = Text_normalization.count_word(stemmed_tokens)
    return word_counts


def dump_jsonfile(file_name, file_content):
    """
    Cria e escreve um arquivo json
    :param file_name: nome do arquivo com caminho
    :param file_content: conteúdo a ser escrito
    """
    with open(file_name, 'w') as outfile:
        json.dump(file_content, outfile)


def date_from_string(string):
    """
    Define uma data no formato datetime aa/mm/dd a partir de uma string 'aammdd'
    :param string: String com ano, mês e dia juntos como 'aammdd'
    :return: aa-mm-dd
    """
    date = str(datetime.date(int(string[:4]), int(string[4:6]), int(string[6:8])))  # date: ano, mês, dia
    return date


path_d = Path('./data')
create_dict_dou(path_d)
# fil = publicacao_normalization({'tittle': 'qualquercoisa', 'body': 'qualquercoisa2'})
# update_dict_dou(fil, './dicts_dou/dict_dou')
# create_bow('teste firmado', './dicts_dou/dict_dou')


