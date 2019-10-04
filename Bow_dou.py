import json
import Text_normalization
from pathlib import *
import datetime
import database


def main():
    path_data = Path('./data')  # se não for colocar os arquivos de leitura nessa pasta, trocar para o caminho absoluto
    filelist = []  # lista de arquivos .json da pasta no caminho acima
    output_list = []
    publicacao_dict = {}
    output_dict = {}
    for f in path_data.iterdir():
        filelist.append(f)

    for file in filelist:
        print(datetime.datetime.now().time())
        with file.open() as data_file:
            json_data = json.load(data_file)
            output_file = './output/' + file.name  # caminho da pasta para os arquivos de saida
            data = str(datetime.date(int(file.name[:4]), int(file.name[4:6]), int(file.name[6:8])))  # ano, mês, dia
            i = 0
        for publicacao in json_data:
            i += 1
            print(i)
            title_string = publicacao['title']
            body_string = publicacao['body']
            publicacao_text = ' '.join([title_string, body_string])

            # Normalização do texto de uma publicação
            tokens = Text_normalization.text_tokenize(publicacao_text.lower())
            filtered_tokens = Text_normalization.remove_specialchar(tokens)
            corrected_tokens, corrected_words = Text_normalization.spell_check(filtered_tokens)
            filtered_text = Text_normalization.remove_stopwords(corrected_tokens)
            stemmed_tokens = Text_normalization.stemming(filtered_text)
            word_counts = Text_normalization.count_word(stemmed_tokens)
            publicacao_dict['date'] = data
            publicacao_dict['bow'] = word_counts
            publicacao_dict['text'] = publicacao_text
            # publicacao_dict['risco'] =
            output_list.append(publicacao_dict.copy())  # sem o copy a última publicação sobrescreve todas as anteriores
            output_dict.update(corrected_words)

        with open(output_file, 'w') as outfile:
            json.dump(output_list, outfile)
            output_list.clear()
            print(datetime.datetime.now().time())

    # database.post_publicacoes(output_file)

    with open('output_dict', 'w') as outfile:
        json.dump(output_dict, outfile)


        # como pesquisar as publicacoes com risco no mongodb


if __name__ == '__main__':
    main()
