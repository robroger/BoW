import json
from pathlib import *
import Dou_dict_bow
import database


def main():
    path_data = Path('./data')  # caminho da pasta dos arquivos de entrada
    filelist = []  # lista de arquivos .json da pasta no caminho acima
    output_list = []  # lista a ser escrita no arquivo json [{date: '', bow: '', text: ''}]
    publicacao_dict = {}  # dict que compõe a lista -output_list- {date: '', bow: '', text: ''}

    # Dou_dict_bow.create_dict_dou(path_data)

    for f in path_data.iterdir():
        filelist.append(f)

    for file in filelist:
        with file.open() as data_file:
            json_data = json.load(data_file)
            output_file = './output/' + file.name  # caminho da pasta para os arquivos de saida
            date = Dou_dict_bow.date_from_string(file.name)
        for publicacao in json_data:
            publicacao_dict['date'] = date
            publicacao_dict['bow'] = Dou_dict_bow.create_bow(publicacao, './dicts_dou/dict_dou')
            publicacao_dict['text'] = Dou_dict_bow.publicacao_text_join(publicacao)
            output_list.append(publicacao_dict.copy())

        Dou_dict_bow.dump_jsonfile(output_file, output_list)
        output_list.clear()

    # database.post_publicacoes(output_file)
    # dump_jsonfile('output_dict', output_dict)


if __name__ == '__main__':
    main()
