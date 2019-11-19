from pymongo import MongoClient
from regex_bib import extrai_num
import re
import time
from fuzzywuzzy import fuzz

numbers = r'(\S+)?\d\d\d+(\S+)?'

commom_kw = ['concorrencia', 'construcoes', 'construtora', 'construcoes', 'consorcio', 'convite', 'convenio',
             'convenios', 'concorrencia', 'conselho', 'dispensa', 'edital', 'empresa', 'empresas', 'empreendimentos',
             'engenharia', 'instituto', 'licitacao', 'ltda', 'municipio', 'municipios', 'municipal', 'prefeitura',
             'pregao', 'secretaria', 'universidade', 'contrato', 'administrativo', 'prestacao', 'servicos', 'processo',
             'publica', 'internacional', 'tomada', 'precos', 'carta', 'presencial', 'eletronico', 'governo', 'estado',
             'estadual', 'departamento', 'instituto', 'universidade', 'participacoes', 'ministerio', 'fundacao',
             'companhia', 'apoio', 'empreitada', 'ndeg']


def create_num_dict(collection):
    """
    :param collection: MongoDB Collection with cases
    :return: Dict: Number string: list[category, id]
    """
    number_dict = {}

    lis = collection.find()

    for i, item in enumerate(lis):
        kw_num = item.get('kw_num', None)
        idt = item.get('_id')
        datas = item.get('datas', None)
        if datas:
            data_min = min(datas)
            data_max = max(datas)
        else:
            data_min = '1900-01-01'
            data_max = '2030-12-31'
        if kw_num:
            for cat in kw_num:
                for num in kw_num[cat]:
                    num2 = fix_year(num)
                    if num2 in number_dict:
                        number_dict[num2].extend([[cat, idt, data_min, data_max]])
                    else:
                        number_dict[num2] = [[cat, idt, data_min, data_max]]
    return number_dict


def fix_year(num):
    """
    Correção de ano no numero do doc
    strings com menos de 6 caracteres e com ultimos 4 digitos fora do intervalo 1990 - 2019
    :param num: string do numero do doc
    :return: string corrigida
    """
    year = int(num[-4:])
    if not (1990 < year < 2019) and len(num) < 6:
        year = year % 100
        if year > 90:
            return num[:-2] + str(1900 + year)
        elif year < 18:
            return num[:-2] + str(2000 + year)
    return num


def compute_pts(texto, tokens):
    if len(tokens) == 0:
        return -1
    tks_str = ' '.join(tokens)

    return ratios(texto, tks_str)


# pts = 0
# kwds = []
# for contr in tokens:
# 	if contr in texto:
# 		digitos = re.search(r'\d+', contr)
# 		if digitos:
# 			pass
# 		elif contr in commom_kw or len(contr) < 4:
# 			pts += 1
# 		else:
# 			pts += 10
# 			kwds.append(contr)
# if len(kwds) > 0:
# 	print(kwds)
# return pts


def test_terms(cat_id_list, texto, risco1, data_pub):
    """
    b1-contratante com concedente com convenio: Convênio
    b2-contratante com licitação : Aviso de Licitação
    b3-contratante com contratado com contrato : Contratos, Aditivos e Destratos
    blocos = {'contratante': [], 'concedente': [], 'convenio': [], 'licitacao': [], 'contratado': [], 'contrato': []}
    :param cat_id_list:
    :param texto:
    :param risco1:
    :param data_pub:
    :return:
    """
    pts_list = []
    for cat_id in cat_id_list:
        if data_pub < cat_id[2] or data_pub > cat_id[3]:
            pts_list.append(0)
        else:
            item = risco1.find_one({'_id': cat_id[1]})
            pts = 0
            kw_tokens = item.get('kw_tokens', '')
            # Caso Convênio
            if cat_id[0] == 'convenio' and re.search('conv.nio', texto):
                if all([i in texto for i in kw_tokens['concedente']]) and all(
                        [i in texto for i in kw_tokens['contratante']]) and len(kw_tokens['concedente']) + len(
                    kw_tokens['contratante']) > 0:
                    if any([i in texto for i in kw_tokens['estado']]) or len(kw_tokens['estado']) == 0:
                        if any([i in texto for i in kw_tokens['orgao']]) or len(kw_tokens['orgao']) == 0:
                            if any([i in texto for i in kw_tokens['CNPJs']]) or len(kw_tokens['CNPJs']) == 0:
                                kws = []
                                for i in ['contratante', 'concedente', 'convenio', 'CNPJs']:
                                    kws.extend(kw_tokens[i])

                                    for i in [kw_tokens['estado'], kw_tokens['orgao'], kw_tokens['CNPJs']]:
                                        for j in i:
                                            if j in texto:
                                                kws.append(j)

                                pts = compute_pts(texto, kws)
            # Caso Licitação
            elif cat_id[0] == 'licitacao' and re.search('(licitacao|edital)', texto):
                if all([i in texto for i in kw_tokens['contratante']]) and len(kw_tokens['contratante']) > 0:
                    if any([i in texto for i in kw_tokens['estado']]) or len(kw_tokens['estado']) == 0:
                        if any([i in texto for i in kw_tokens['orgao']]) or len(kw_tokens['orgao']) == 0:
                            if any([i in texto for i in kw_tokens['CNPJs']]) or len(kw_tokens['CNPJs']) == 0:
                                kws = []
                                for i in ['contratante', 'licitacao', 'CNPJs']:
                                    kws.extend(kw_tokens[i])

                                for i in [kw_tokens['estado'], kw_tokens['orgao'], kw_tokens['CNPJs']]:
                                    for j in i:
                                        if j in texto:
                                            kws.append(j)

                                pts = compute_pts(texto, kws)
            # Caso Contrato
            elif cat_id[0] == 'contrato' and re.search('(contrato|aditivo|rescis.o)', texto):
                # TODO: Colocar contratado?
                if all([i in texto for i in kw_tokens['contratante']]) and len(kw_tokens['contratante']) > 0:
                    if any([i in texto for i in kw_tokens['estado']]) or len(kw_tokens['estado']) == 0:
                        if any([i in texto for i in kw_tokens['orgao']]) or len(kw_tokens['orgao']) == 0:
                            if any([i in texto for i in kw_tokens['CNPJs']]) or len(kw_tokens['CNPJs']) == 0:
                                kws = []
                                for i in ['contratante', 'contratante', 'contrato', 'CNPJs']:
                                    kws.extend(kw_tokens[i])

                                for i in [kw_tokens['estado'], kw_tokens['orgao'], kw_tokens['CNPJs']]:
                                    for j in i:
                                        if j in texto:
                                            kws.append(j)

                                pts = compute_pts(texto, kws)
            pts_list.append(pts)
    return pts_list


def ratios(Str1, Str2):
    Str1 = Str1.lower()
    Token_Set_Ratio = fuzz.token_set_ratio(Str1, Str2)
    return max(-1, Token_Set_Ratio - 40)  # 40 veio de testes empiricos


def main():
    # n = int(input('n: '))

    start = time.time()
    print(start)

    # Start Mongo
    client = MongoClient('localhost', 27017)
    db = client['deep-vacuity']
    public = db['publications']
    risco1 = db['laudosR1']
    risco1temp = db['temp']


    number_dict = create_num_dict(risco1)

    lis = public.find()

    for i, item in enumerate(lis):
        texto = item.get('text', '')  # .lower()
        if len(
                texto) < 1700:  # licitação e contratos estão nesta categoria, outros textos com comprimentos maiores não tem relação
            texto = texto.lower()
            data_pub = item.get('date', '')
            with_num = re.finditer(numbers, texto)
            for num in with_num:
                clean_num = extrai_num(num.group())
                if clean_num in number_dict:
                    for ii, ptos in enumerate(test_terms(number_dict[clean_num], texto, risco1, data_pub)):
                        if ptos > 0:
                            idt = number_dict[clean_num][ii][1]
                            elem = risco1.find_one({'_id': idt})
                            kw = elem.get('keywords', [])
                            temp = risco1temp.find_one({'_id': idt})
                            if temp:
                                texto_list = temp.get('texto', [])
                                data_list = temp.get('data', [])
                            else:
                                texto_list = []
                                data_list = []
                            if len(texto_list) < 7:
                                texto_list.append(texto)
                                data_list.append(data_pub)
                                upd = {'$set': {'keywords': kw, 'texto': texto_list, 'data': data_list}}
                                risco1temp.update_one({'_id': idt}, upd, True)
                                print('Atualizado {}, Andamento {:.4f}% @ {}'.format(idt, i / 148000, time.time()))

    print('{} entradas depois:'.format(i))
    print('{} segundos'.format(time.time() - start))


if __name__ == '__main__':
    main()
