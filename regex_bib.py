import re
import nltk
from unidecode import unidecode
import json

re_dict = {
    'contrato': '(?:(?:CT)(?:\s)|(?:contrat(?:.{1,10})(?:.de.empreitada)?(.administrativo)?(.de.presta..o.de.servi.os)?\s?(?:n|N)?)).(?:\d{1,4})(?:(?:[.-]\d{1,3})?)(?:(?:[.-]\d{1,10})?)(?:(?:[./](?:\d{4}|\d{2}))?)',
    'convenio': '(contrato(s)?.de.repasse?|convênio)',
    'licitacao': '(processo.licitat.rio|concorrência(.pública)?(.internacional)?|licitação|TP-|Tomada\s+de\s+Preço(s)?|(Carta.)?Convite|C?onvite|edital|Dispensa|pregão(.presencial|.eletrônico)?)',
    'concedente': '(FUNAI|EMBRATUR|INCRA|FUNASA|FUNDEB|FNDE|DNOCS|Minist.rio\s(([A-Z]\S{1,15}|d.s?|,|e|–|em)\s?){1,15}|CODEVASF)',
    'contratante': ('(.{1,6}((\/|-)[A-Z]{2})|Prefeitura|Municipal|(M|m)unicípio'
                    '((\/|-)[A-Z]{2})?|((estado\s+d.|Governo\s+do\s+Estado|Governo\s+estadual|Departamento|Secretaria|Divisão|Instituto)'
                    '([A-Z]\S{1,15}|d.|D.|\s?){1,8})|UFPB|municíop|ANEEL|CEGELEC|ACREPREVIDENCI|AGETRANS|IFB|CODESA|DEPASA|AGETRANS|CETESB'
                    '|Conselho|Hemobr.s|Hipotecária|SEST|SENAT|IFG|STJ|DNER|DERTINS|SUDAM|IBAMA|IFES|CORSAN|Fiocruz|VALEC|Infraero|'
                    'Petrobrás|CONAB|Senado|SANEAGO|CODEVASF|DNIT|DERACRE|AGESUL|embrapa|NOVACAP|Correios|CREA|Universidade)'),
    'contratado': ('(.{1,50}(\sSA|(\s|-)ME|EPP|Ltda\.?|LTDA\.?|(\s|-)S(\.|\/)A\.?|EIRELI)(-ME)?|'
                   '(Consórcio|(E|e)mpresa|Construtora|participa..es|Empreendimentos|Engenharia|Constru..es|CR.Almeida))'),
    'dou': '(D\.?O\.?U\.?|Di.rio.Oficial).{1,50}(\d{1,2}º?(\/|-)\d{1,2}(\/|-)(\d{4}|\d{2})|\d{1,2}.?.de.\w{4,9}.de.(\d{4}|\d{2}))'
}

cnpj_pattern = r'((?:\d{2})[-.](?:\d{3})[-.](?:\d{3})\/(?:\d{4})[-.](?:\d{2}))'

estado_pattern = (
    r'(?i)\b(ac|al|ap|am|ba|ce|df|es|go|ma|mt|ms|mg|pa|pb|pr|pe|pi|rj|rn|rs|ro|rr|sc|sp|se|to|acre|alagoas'
    r'|amap[aá]|amazonas|bahia|cear[aá]|distrito federal|esp[ií]rito santo|goi[aá]s|maranh[aã]o|mato '
    r'grosso|mato grosso do sul|minas gerais|par[aá]|para[ií]ba|paran[aá]|pernambuco|piau[ií]|rio de '
    r'janeiro|rio grande do norte|rio grande do sul|roraima|rond[ôo]nia|santa catarina|s[aã]o '
    r'paulo|sergipe|tocantins)\b')

sigla_estado = {'ac': 'acre', 'al': 'alagoas', 'ap': 'amapa', 'am': 'amazonas', 'ba': 'bahia', 'ce': 'ceara',
                'df': 'distrito federal', 'es': 'espirito santo', 'go': 'goias', 'ma': 'maranhao',
                'mt': 'mato grosso', 'ms': 'mato grosso do sul', 'mg': 'minas gerais', 'pa': 'para',
                'pb': 'paraiba', 'pr': 'parana', 'pe': 'pernambuco', 'pi': 'piaui', 'rj': 'rio de janeiro',
                'rn': 'rio grande do norte', 'rs': 'rio grande do sul', 'ro': 'rondonia', 'rr': 'roraima',
                'sc': 'santa catarina', 'sp': 'sao paulo', 'se': 'sergipe', 'to': 'tocantins'}

# estado_sigla = dict sigla_estado com as keys e valores invertidos, ex: 'amazonas':'am'
estado_sigla = dict([(value, key) for key, value in sigla_estado.items()])

with open('siglas_orgaos_clean.txt', 'r') as r_sigla:
    sigla_orgao = json.load(r_sigla)

# orgao_sigla = dict orgao_sigla com as keys e valores invertidos, ex: 'fundacao nacional do indio':'funai'
orgao_sigla = dict([(value, key) for key, value in sigla_orgao.items()])

sub_contr = '(prefeitura\s(d.\smunic.pio\sd..?\s|municipal\sd..?\s|d..?\s)?|munic.pio\sd..?\s|estado|governo(\sestadual|do\sestado)?\sd.\s|departamento|secretaria|divis.o|instituto)'

not_numbers = '[^\d]'
leading_zeros = '^0+'
numbers = '(\S+)?\d+(\S+)?'
com_num = ['convenio', 'licitacao', 'contrato']


def kw_category(txt):
    """
    Search category of keyword
    :param txt: keywords in string format
    :return: category
    """
    kw_cat = None
    for cat in re_dict:
        if re.search(re_dict[cat], txt, re.IGNORECASE | re.M | re.S):
            return cat
    if not kw_cat:
        return 'outros'
    else:
        return kw_cat


def extrai_num(txt):
    """
    Only numbers for comparation
    :param txt: Any string
    :return: only numbers without leading zeros
    """
    return re.sub(leading_zeros, '', re.sub(not_numbers, '', txt))


def kw_tokens(text):
    """
    Tokiniza os keywords
    :param text: string
    :return: list of tokens
    """
    text = unidecode(text)
    text = re.sub('(\/|-)', ' ', text)
    tokens = nltk.word_tokenize(text.lower())

    tokens = [token.strip() for token in tokens]
    return [i for i in list(set(tokens)) if (len(i) > 2 or i in sigla_estado)]


def checa_num(kw):
    """
    Checa os KW por numeros
    :param kw: string
    :return: list of tokens
    """
    numeros = re.finditer(numbers, kw)
    if numeros:
        num_lst = []
        for i in numeros:
            num_lst.append(extrai_num(kw))
        return kw_tokens(' '.join(num_lst))
    return None

def findwholeword(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def block_builder(kw_lst):
    """
    Faz a lista de conjunto de nomes a ser procurado em uma publicação
    b1-contratante com concedente com convenio: Convênio
    b2-contratante com licitação : Aviso de Licitação
    b3-contratante com contratado com contrato : Contratos, Aditivos e Destratos
    :param kw_lst:
    :return: um dict de tokens de kw e uma lista numeros puros
    """
    ignore = ['SIGILOSO', 'OUTROS', 'Avaliação', ['OUTROS'], 'PULADO', ['Avaliação']]
    if kw_lst in ignore:
        return None, None

    blocos = {'contratante': [], 'concedente': [], 'convenio': [], 'licitacao': [], 'contratado': [], 'contrato': [],
              'estado': {}, 'orgao': {}, 'CNPJs': []}
    blocos_num = {'convenio': [], 'licitacao': [], 'contrato': []}

    for kw in kw_lst:
        cat = kw_category(kw)
        kw = kw.lower()
        kw = unidecode(kw)
        # Encontra as referência de cnpj em todos os kw (independente se já fazem parte de uma categoria ou não)
        cnpj = re.findall(cnpj_pattern, kw)
        blocos['CNPJs'].extend(cnpj)

        if cat == 'contratante':
            # informação mais importante
            nome_contr = re.sub(sub_contr, '', kw.lower())
            nome_contr = re.sub('(\/|-)\D\D', '', nome_contr)
            blocos[cat].extend([nome_contr])
        elif cat in blocos:
            if cat == 'contrato':
                num_contrato = [token for token in kw.split() if any(map(str.isdigit, token))]
                blocos['contrato'].extend(num_contrato)
                # num_contrato_pattern = re.search(
                #     r'((?:\d{1,4})[.-](?:\d{1,3})?(?:\d(?:[.-]))(?:\d{1,10})(?:[/-])(?:\d{4}|(\d{2}))|(?:\d{1,4})(?:[/-])(?:\d{4}|\d{2}))',
                #     kw).group(0)

            else:
                blocos[cat].extend(kw_tokens(kw))
                if cat in blocos_num:
                    try:
                        blocos_num[cat].extend(checa_num(kw))
                    except:
                        pass

        list_check = {'sigla_estado': sigla_estado, 'estado_sigla': estado_sigla, 'sigla_orgao': sigla_orgao, 'orgao_sigla': orgao_sigla}

        # Retira na análise de estados 'para's que não são precedidos de 'do', 'no', 'o', que não são o estado pará
        if findwholeword('para')(kw):
            # TODO: e se para for a primeira palavra?
            para_index = kw.split().index('para') - 1
            if kw.split()[para_index] not in 'do no o'.split():
                kw = re.sub('para', '', kw)
                kw = re.sub(r'(\s$)|(\s{2,})', '', kw)

        # Encontra as referências de estado e orgao, retira das suas cat originais e insere no campo correspondente de blocos
        if cat is not 'outros':
            for key in list_check:
                blocos_key = 'estado'
                check = list_check.get(key)
                if key is ('sigla_orgao' or 'orgao_sigla'):
                     blocos_key = 'orgao'
                for i in check:
                    if findwholeword(i)(kw):
                        if cat not in blocos[blocos_key]:
                            blocos[blocos_key].update({cat: []})
                        blocos[blocos_key][cat].append(i)
                        blocos[blocos_key][cat].append(check.get(i))
                        if cat is 'contratante':
                            blocos[cat][-1] = re.sub(i, '', blocos[cat][-1])
                            blocos[cat][-1] = re.sub(r'(^\s)|(\s$)|(\s{2,})', '', blocos[cat][-1])
                        else:
                            blocos[cat] = [word for word in blocos[cat] if word not in i]

    return blocos, blocos_num


if __name__ == '__main__':
    a = ['prefeitura municipal de goiás aldeias altas/AA', 'CT 0237.101-27/2007', 'Contrato no 4.08.030a mg',
         'CT 0242.083-00/2007', \
         'CT 0247.481-35/2007', 'CT 0247.415-25/2007', '4.08.030a',
         'CONSTRUTORA GAV LTDA CAMPUS MORÃO CONSTRUÇÃO LTDA',
         '04.480.157/0001-12 04.480.157/0001-13']
    b = ['município de Tuneiras do Oeste/PR']
    c = ['Governo Estadual do Goiás']
    print(block_builder(a))
