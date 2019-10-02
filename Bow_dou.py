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
    for f in path_data.iterdir():
        filelist.append(f)

    for file in filelist:
        print(datetime.datetime.now().time())
        with file.open() as data_file:
            json_data = json.load(data_file)
            output_file = './output/' + file.name  # caminho da pasta para os arquivos de saida
            data = str(datetime.date(int(file.name[:4]), int(file.name[4:6]), int(file.name[6:8])))  # ano, mês, dia

        for publicacao in json_data:
            title_string = publicacao['title']
            body_string = publicacao['body']
            publicacao_text = ' '.join([title_string, body_string])

            # Normalização do texto de uma publicação
            tokens = Text_normalization.text_tokenize(publicacao_text)
            filtered_tokens = Text_normalization.remove_specialchar(tokens)
            filtered_text = Text_normalization.remove_stopwords(filtered_tokens)
            # fazer o stemming só do plural regex
            stemmed_tokens = Text_normalization.stemming(
                filtered_text)  # stemmed_tokens = Texto final tratado em tokens
            word_counts = Text_normalization.count_word(stemmed_tokens)
            publicacao_dict['data'] = data
            publicacao_dict['bow'] = word_counts
            publicacao_dict['texto'] = publicacao_text
            # publicacao_dict['risco'] =
            output_list.append(publicacao_dict.copy())  # sem o copy a última publicação sobrescreve todas as anteriores

        with open(output_file, 'w') as outfile:
            json.dump(output_list, outfile)
            output_list.clear()
            print(datetime.datetime.now().time())

        database.post_publicacoes(output_file)

        # como pesquisar as publicacoes com risco no mongodb


if __name__ == '__main__':
    main()
