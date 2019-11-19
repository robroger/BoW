import re
import json
import nltk
from nltk import RegexpTokenizer
from unidecode import unidecode
import unicodedata


def create_dict_orgaos():
    dict_orgaos = {}
    with open('orgaos.txt', 'r', encoding='utf8') as r_file:
        orgaos = r_file.readlines()
        print(orgaos)
        for orgao in orgaos:
            orgao = unidecode(orgao.lower())
            orgao = re.sub('\-\s', '', orgao)
            tokenizer = RegexpTokenizer(r'(^[a-zA-Z]+)', gaps=True)
            tokens = tokenizer.tokenize(orgao)
            tokens[1] = re.sub('^\s', '', tokens[1])
            tokens[1] = re.sub('\n', '', tokens[1])
            dict_orgaos.update({tokens[0]: tokens[1]})

    print(dict_orgaos)
    with open('sigla_orgao.txt', 'w') as w_file:
        w_file.write(json.dumps(dict_orgaos))


def create_dict_orgaos_clean():
    orgaos_possiveis = ['ENGEVIX', 'ALPAV', 'GESTÃODE', 'FUNAI', 'CONSTRUTÉCNICA', 'MPS', 'PREÇOS', 'SANEAMENTO',
                        'PARTICIPAÇÕES', '(SETUR)', 'BRASIL', '(MDS)', 'ENGELEC', 'PROSERVES', 'EPG', 'HIDROSONDA',
                        'GTEC', 'DEFESA', 'MAIO', 'STATUS', 'SRP', 'VISÃO', 'AGUIAR', 'LTDA', 'ALMEIDA', 'SOS', 'INSS',
                        'PMO', 'VITÓRIA', 'INCORPORADORA', 'S/A.', 'TOMADA', 'MVA', 'VIÁRIA', 'CAPIM', 'OAP', 'SENA',
                        'VALEC', 'SANTOS', 'FLÔR', 'UNIVERSIDADE', 'IMOBILIÁRIA', 'CODESA', 'REMARC', 'CETESB', 'TCC',
                        'CROS', 'INCORPORAÇÃO', 'COBI', 'YTAMIRIM', 'CARNEIRO', 'GERAR', 'CONSTRUTORA', 'SOLUTION.COM',
                        'SERVIÇOS', 'JAL', 'COMPRES.', 'COFRUVALE', 'MILLENIUM', 'PARCAN', 'EST', 'CONSTRAN', 'PEREIRA',
                        'POLYEFE', 'C.T.', 'SETOP', 'CONTERRA/SCL', 'AQUARELA', 'ATEMAC', 'IAPA', 'SPEL', 'EMCONSEL',
                        'SOLUÇÕES', 'FONTE', 'PREFISAN', 'RAMOS', 'TRIMEC', 'TABOCÃO', '(AGESUL)', 'ENGIPEC', 'CARIRI',
                        'PMVV', 'VETORIAL', 'ITAPAJEENSE', 'FEDERAL', 'EMPRENGE', 'DEPASA', '(IFG)', 'GPV', 'PERCAMP',
                        'DCS-CL', 'JAM', 'CCS', 'PRODUÇÃO', 'CCR', 'SOUZA', 'PIETC-', 'CONST', 'SPAGNOL',
                        'ACREPREVIDENCIA', 'SEP', 'ADMINISTRAÇÃO', 'RENZO', 'CONCRETOS', 'REGO', 'OAS', 'ALPLAN',
                        '(SRP)', 'ROCHA', 'A.S.', 'LOTE', 'CIC', 'FOME', 'GAV', 'ENGEFIX', 'CNO', 'COESA', 'SOCIAL',
                        'UFPB', 'IMPERMEABILIZAÇÕES', 'ANA', 'EGE', 'SEPROR', 'DEMOP', 'CAMTER', 'CCD', 'CONSTRUÇOES',
                        'FLAMAC', 'ABACOL-ABATEDOURO', 'DEC', 'CMSG', 'RDC', 'CARTA', 'ENGENHEIROS', 'CORSAN',
                        'ITAQUARA/BA', 'AVM', 'CENTRAL', 'QUALITEC', 'NBR', 'TESCON', 'INTEGRAÇÃO', 'PAVINPAR',
                        'HELENO', 'PRIMOS', 'ELÉTRICA', 'PAVEN', 'SPA', 'MIRANDA', 'IGARASSU/PE', 'AMERICANA',
                        'FOMENGE', 'IBAMA', 'MIN', 'DESENVOLVIMENTO', 'CONCORRÊNCIA', 'CRT/MS/Nº', 'SIGILOSO', 'SOSP',
                        'ENS', 'JRJ', 'ASB', 'ATLANTA', 'RAIAR', 'SENAT', 'D.O.U.', 'COMPECC', 'ECOPLAN–MAGNA',
                        'SETRE/BA', 'CONSBEM', 'W.A.G.', 'IHGT', 'IN-LOCO', 'FUNASA', 'PAC', 'LOC', 'PRESTACOES', 'AML',
                        'ENGEWAL', 'INFRAERO', 'IESA', 'ELECTRA', 'CAMOZZATO', 'PRECAST', 'RADIER', 'EXTERIOR',
                        'PAESAN', 'ESTADUAL', 'S.J.L.', 'SMS', 'COLARES', 'ALFA', 'IZABEL', 'UFPB/CFT', 'DNIT', 'COLA',
                        'SESAU/TO', 'MFM', 'DERTINS', 'CAVALCA', 'SERPREL', 'SERVICE', 'CARDOSO', 'CICAL', 'GTA', 'SUL',
                        'CONSPAV-CONSTRUÇÕES', 'PARNAÍBA', 'PRONAF', 'MSJ', 'TRN', 'COMASE', 'CONPAC', 'INCORPORAÇÕES',
                        'TRIPOLONI', 'SETA', 'SECRETARIA', 'BASE', 'FNDE', 'CONDER', 'EIRELI', 'INDÚSTRIA', 'COMBATE',
                        'TELES', 'TRENA', 'PABR', 'URB', 'DNER', 'BOMBAS', 'CAIXA', 'MUNICIPAL', 'SEC', 'BTA',
                        'PAVSANTOS', 'TECCOS', 'PARANÁ', 'IZAIAS', 'FNP', 'SESEF', 'TSA', 'ATS', 'UNICON', 'TÉKNICA',
                        'BESSA', 'LUNYS', 'GERAIS', 'MACHADO', 'CONVÊNIO', 'DNIT/TT', 'TRANSPORTADORA', 'MARTIFER',
                        'CONCREMAX', 'SIQUEIRA', 'CMT/GETEL', 'SEINFRA/CMT-GETEL', 'DOU', 'GAE', 'EMPRESA', 'RDS',
                        'CONVITE', 'DER-ES', 'CATINGUEIRA/PB', 'CEGELEC', 'MINERAÇÃO', 'CMT/EGESA', 'VEGA', 'C.S.P.',
                        'FEC', 'URBANISMO', 'SEOP/AC', 'COOPBUGGY', 'GALVÃO', 'LINK', 'ECONTEC', 'CONSVAL', 'R.R.',
                        'ACR', 'RECÔNCAVO', 'ABO', 'SEV', 'RODRIGUES', 'GONÇALVES', 'DAS', 'CRT/MT', 'LAGOA/PB',
                        'REGIONAL', 'M.D.', 'COMERCIO', 'AGÊNCIA', 'OPF', 'VILLENA', 'ALVENARIA', 'POÇOS',
                        'CARBONITA/MG', 'ENCO', 'SEP/PR', 'CIVIS', 'SUFRAMA', 'MINISTÉRIO', 'TÉCNICA', 'PERCOL',
                        'GIORDANI', 'NORDESTE', 'ARENA', 'PERNAMBUCO', 'MAV', 'UFPB/PU', 'G&F', 'TCU', 'ESTADO',
                        'LIMPEZA', 'SEMARH/RN', 'CONSTRUMAR', 'CODEVASF', 'LUSTOZA', 'GCM', 'ESTRUTURAIS', 'SEMOGEL',
                        'EPP', 'CONSTRUÇÃO', 'FERREIRA', 'GLOBAL', 'IMPERTEC', 'PERF.', 'ECON', 'DUCK’S', 'FKC',
                        'FOMENTO', 'COGUETTO', 'CAMPUSMORÃO', 'PROJETO', 'ENCALSO', 'CNPAF', 'AMBIENTAIS', 'DERACRE',
                        'TCE', 'CAMARGO', 'LTDA.', 'NORTE', 'PAVIMENTAÇÃO', 'AIROLDI', 'BRAMAC', 'ALB', 'SANE',
                        'URTIGA', 'QUEIROZ', 'SERRÃO', 'E.S.O.', 'SERVICOS', 'JDE', 'BARIZON', 'ECOP', 'CONSTRUTERRA',
                        'AGETRANS', 'PAULA', 'CAROLINO', 'COOMPRAM', 'CONSTRUTURA', 'CHAVES', 'DORNELAS', 'GIMA', 'CMS',
                        'EVB', 'NIOAQUE/MS', '(CP)', 'MONTAGENS', 'PMR', 'CONSTRULIX', 'DOURADO', 'WDC', 'BAHIA',
                        'H.M.', 'SAMA', 'ODEBRAN', 'SILGRAN', 'BONACCI', 'ALTA', 'SILVA', 'NOBRE', 'TRANSPORTES',
                        'SOARES', 'SEST', 'GONZAGA', 'CONTRUÇÕES', 'IMDC', 'CONAB', 'ADVANCE', 'PROJETOS', 'RURAL',
                        'MELLO', 'MARTS', 'SANCHES', 'C.R.', 'UT-', 'CAXA', 'INSTEC', 'CASA', 'CELCOM', 'COMÉRCIO',
                        'OSV', 'B.L.', 'SEGURANÇA', 'S/A', 'PREFEITURA', 'FIDENS', 'CAMPUS', 'TANAKA', 'STJ', 'FCK',
                        'CONTRATO', 'ECOS', '(DOM)', 'IFB', 'G.P.', 'CREA-MS', 'ENGENOR', 'S.A', 'CONFER', 'TERRABRAS',
                        'SEDUC/TP', 'CONSERGE', 'ESPECIALIZADOS', 'GESTÃO', 'SIAFI', 'OLIVEIRA', 'MLNG', 'BASECOM',
                        'INC', 'FNS', 'LAJEAÇO', 'DELTA', 'SEMAR', 'CANARANA/MT', 'PRESTAÇÕES', 'ARAÚJO', 'PÓRTICO',
                        'MEC', 'V.C.', 'JADILSON', 'CARAM', 'PIEMTUR', 'TERRAPLANAGEM', 'ROJEP', 'PAV.', 'SMA/DLC',
                        'LIBERTY', 'VENEZA', 'PIETC-RMC', 'CIDADES/CAIXA', 'PETROBRÁS', 'CSC', 'ANEEL', 'STE-DYNATEST',
                        'MMA', 'RIBEIRO', 'DNOCS', 'DUDUZÃO', 'EPENG', 'CIA.', 'EMPREITEIRA', 'ELETRICIDADE', '/RN',
                        'COENCO', 'BNDES', 'RMC', 'ETEC', 'N°.', 'CIVIL', 'RDO', 'BRAVA', 'ÁGAPE', 'EMPREENDIMENTOS',
                        'SEOP/PA', 'CIA', 'ENGEPAR', 'M.P.', 'AGESUL', 'LOCAÇÕES', 'FIOCRUZ', 'COENGE', 'IFES',
                        'CONSERVAÇÃO', 'TC/PAC', 'AGT', 'REDRAM', 'INVESTIMENTOS', 'CENTRO', 'HZO', 'SEPLAN', 'FONSECA',
                        'KGW', 'SELT', 'SANEAGO', 'SEINF/AM', 'IFG', 'NOVACAP', 'AGECON', 'BIRD', 'TROP', 'GETEL',
                        'UEX', 'DISTRIBUIÇÃO', 'ULUSCAR', 'EIT', 'CMC', 'CONSTRUCOES', 'CREA/MG', 'STE', 'EMPARSANCO',
                        'VITORIA', 'MORÃO', 'GAID', 'VEP', 'FUNDEB', 'PRESTADORA', 'INCRA', 'PROJETUS', 'CIDADES',
                        'SOBRADO', 'CONAP', 'Nº.', 'RBS', 'SEMARH', 'CONTER', 'NOGUEIRA', 'UASG', 'ENG.', 'UAUÁ/BA',
                        'CONSULTORIA', 'HUERO', 'PONTE', 'CALÇAMENTO', 'TROP-COMEXPORT', 'CONSTRUMASTER', 'SICONV',
                        'JPN', 'ITATIAIA', 'SCAMVIAS', 'DINIZ-CONSTRUÇÃO', 'NACIONAL', 'LAGOA', 'PPV', 'IDENE',
                        'CONSTRUAL', 'TERRAPLENAGEM', 'TUFÃO', 'LTDA.-ME', 'CONSULTORES', 'SIMELO', 'VGS', 'DIRETRIZ',
                        'ENTERPA/KEPLER', 'EMSA', 'DEGEC/SUSUP', 'ALEXANDRE', '/CAMIL', 'TT-', 'ENGEDELP', 'CANA',
                        'AVANTE', 'GOIANA', 'COCENO', 'EDIFIC', 'S.A.', 'SUDAM', 'CELTA', 'CAMPOS', 'CAENGE',
                        'TRANSPORTE', 'OBRAS', 'EHL', 'TURISMO', 'INTERNACIONAL', 'ARQUITETURA', '(SIAFI', 'MARIA',
                        'CONSTRUÇÕES', 'ALBUQUERQUE', 'SEDUOP', 'OUTRO', 'KMS', 'CRIFEN', 'SANTANA', 'ASSESSORIA',
                        'CPL', 'METACON', 'OPC', 'FERTILTEC', 'SIMEC', 'BARBOSA', 'BRAGA', 'ENGECOL', 'DURAN', 'PGE',
                        'NEGÓCIOS', 'CJS', 'AMG', 'CORREIOS', 'MUNICÍPIO', 'CONSERV', 'CAMAT', 'SOEBE', 'EMEC',
                        'CONSTAL', 'BOA', 'ENGEMAT', 'CMT', 'KAKI', 'ENGENHARIA', 'EMBRATUR', 'ARS', 'UFPB/UGCG/PU',
                        'VANGUARDA', 'CAGEO', 'COM.', 'JRN', 'EIRELLI', 'LTDA-ME', 'ADINN', 'MMA/FNMA', 'URB-TOPO',
                        'PERFIL', 'PROTECO']

    dict_orgaos_clean = {}
    list_orgaos = []
    with open('sigla_orgao.txt', 'r') as r_sigla:
        siglas_orgaos = json.load(r_sigla)
        for orgao in siglas_orgaos:
            list_orgaos.append(orgao.lower())

        for orgao in orgaos_possiveis:
            orgao = orgao.lower()
            if orgao in list_orgaos:
                dict_orgaos_clean.update({orgao: siglas_orgaos[orgao]})

    with open('siglas_orgaos_clean.txt', 'w') as w_file:
        w_file.write(json.dumps(dict_orgaos_clean))


texto = 'isso e um texto com uma funai sigla fundacao nacional do indio de estado aldeias altas 07.825.451/0001-07  mt tuneiras do oeste'
public = {
    'contratante': ['aldeias altas', 'tuneiras do oeste'],
    'concedente': ['isso', 'e', 'um', 'texto', 'com', 'uma', 'sigla', 'de', 'estado'],
    'estado': ['minas gerais', 'mg', 'mt', 'mato grosso'],
    'orgao': [],
    'CNPJs': ['04.480.157/0001-12', '07.825.451/0001-07']}
texto_slipt = texto.split()

# TODO: E SE CONCEDENTE NÃO EXISTIR
# check_estado = [texto for i in (public['estado']['concedente'] + public['estado']['contratante']) if(i in texto)]
# check_orgao = [texto for i in (public['orgao']['concedente'] + public['orgao']['contratante']) if(i in texto)]


if all([i in texto for i in public['concedente']]) and all(
                        [i in texto for i in public['contratante']]) and len(public['concedente']) + len(
                    public['contratante']) > 0:
    if any([i in texto for i in public['estado']]) and len(public['estado']) > 0:
        if any([i in texto for i in public['orgao']]) or len(public['orgao']) == 0:
            if any([i in texto for i in public['CNPJs']]) and len(public['CNPJs']) > 0:
                print('found')

kws = []
for i in [public['estado'], public['orgao'], public['CNPJs']]:
    for j in i:
        if j in texto:
            kws.append(j)

print(kws)
# if all([i in texto for i in public['contratante']]) and [texto for i in public['estado']['contratante'] if(i in texto)]:
#    print('found2')

# if all([i in texto for i in public['concedente']]) and len(public['concedente']) > 0:
    # if len(public['estado']) > 0:
    #     for estado in public['estado']:
    #         if estado in texto:

public2 = {'contratante': ['aldeias altas', 'tuneiras do oeste parana']}


# def post_publicacoes(json_file):
#     client = MongoClient('localhost', 27017)
#     db = client['deep-vacuity']
#     collection_publicacoes = db['publications']
#     with open(json_file) as post_data:
#         json_data = json.load(post_data)

#     collection_publicacoes.insert_many(json_data)
#     client.close()


# post_publicacoes(pub)
