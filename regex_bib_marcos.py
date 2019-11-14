import re
import nltk
from unidecode import unidecode

re_dict = {
	'contrato': '((CT\s\d{1,4})|contrat.{1,10}(.de.empreitada)?(administrativo)?(de.presta..o.de.servi.os)?\s?(n|N)?.{1,3}?(\d(\.|-)?){1,10}?((\/|-)(\d{4}|\d{2}))?)',
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

sub_contr = '(prefeitura\s(d.\smunic.pio\sd..?\s|municipal\sd..?\s|d..?\s)?|munic.pio\sd..?\s|estado|governo(\sestadual|do\sestado)?\sd.\s|departamento|secretaria|divis.o|instituto)'

not_numbers = '[^\d]'
leading_zeros = '^0+'
numbers = '(\S+)?\d+(\S+)?'
com_num = ['convenio', 'licitacao', 'contrato']

estados = ['ac', 'al', 'ap', 'am', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mt', 'ms', 'mg', 'pa', \
		   'pb', 'pr', 'pe', 'pi', 'rj', 'rn', 'rs', 'ro', 'rr', 'sc', 'sp', 'se', 'to']


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
	return [i for i in list(set(tokens)) if (len(i) > 2 or i in estados)]


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

	blocos = {'contratante': [], 'concedente': [], 'convenio': [], 'licitacao': [], 'contratado': [], 'contrato': []}
	blocos_num = {'convenio': [], 'licitacao': [], 'contrato': []}

	for kw in kw_lst:
		cat = kw_category(kw)
		if cat == 'contratante':
			# informação mais importante
			nome_contr = re.sub(sub_contr, '', kw.lower())
			nome_contr = re.sub('(\/|-)\D\D', '', nome_contr)
			blocos[cat].extend([nome_contr])
		elif cat in blocos:
			blocos[cat].extend(kw_tokens(kw))
			if cat in blocos_num:
				try:
					blocos_num[cat].extend(checa_num(kw))
				except:
					pass

	return blocos, blocos_num


if __name__ == '__main__':
	a = ['prefeitura municipal de aldeias altas/AA','município de Tuneiras do Oeste/PR', 'CT 0237.101-27/2007', 'CT 0242.083-00/2007', \
		 'CT 0247.481-35/2007', 'CT 0247.415-25/2007', 'CONSTRUTORA GAV LTDA CAMPUS MORÃO CONSTRUÇÃO LTDA']
	print(block_builder(a))
