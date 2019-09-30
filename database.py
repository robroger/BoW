from pymongo import MongoClient
import json


# json_file = './output/test.json'
# Campos de cada publicação: _id, bow: {dict}, data, risco, texto_completo
# bow: {dict} > dict: bow de cada publicação

def post_publicacoes(json_file):
    client = MongoClient('localhost', 27017)
    db = client['publicacoes_db']
    collection_publicacoes = db['publicacoes']
    with open(json_file) as post_data:
        json_data = json.load(post_data)

    collection_publicacoes.insert_many(json_data)
    client.close()
