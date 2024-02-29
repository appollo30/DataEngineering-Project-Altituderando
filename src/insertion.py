import pandas as pd
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from os import environ
from time import sleep

print("fesses")

#Variables d'environnement

mongo_host = environ.get("MONGO_HOST")
mongo_port = environ.get("MONGO_PORT")
el_host = environ.get("ELASTICSEARCH_HOST")
el_port = environ.get("ELASTICSEARCH_PORT")


#Instanciation du client Mongo

mongo_client = pymongo.MongoClient("localhost" if mongo_host == None else mongo_host,27017 if mongo_port == None else int(mongo_port))
print("Connexion à MongoDB réussie")
database = mongo_client['altituderando']
collection = database['pages']
collection.delete_many({})

#Instanciation de la base Elasticsearch
#Avec docker-compose, les services sont lances simultanement donc il arrive que la base elasticsearch soit en ligne après l'exécution de insertion.py, donc elle n'a pas le temps de se lancer qu'on essaie déjà de s'y connecter
#On y remédie en faisant une boucle où on essaie de se connecter a repetition jusqu'a se connecter. On met le delai entre les connexions à 1 dixième de seconde.
el_live = False
retry_delay = 0.1

while not el_live:
    es_client = Elasticsearch(hosts=["localhost" if el_host == None else el_host])
    el_live = es_client.ping()
    sleep(retry_delay)
print("Connexion à Elasticsearch réussie")



#Traitement de la donnee depuis results.csv
def extract_content(comments):
    return [comment['content'] for comment in comments]


df = pd.read_json("./data/results.json")
df['comments'] = df['comments'].apply(extract_content)
df['date'] = df['date'].astype(object).where(df['date'].notnull(), None)



#Insertion dans la collection mongo
data_dict_mongo = df.to_dict(orient="records")
collection.insert_many(data_dict_mongo)
print("Insertion dans mongo réussie")

#Insertion dans Elasticsearch
data_dict_elasticsearch = df.fillna("").to_dict(orient="records")
def generate_data(documents):
    for docu in documents:
        yield {
            "_index": "altituderando",
            "_type": "page",
            "_source": {k:v if v else None for k,v in docu.items()},
        }

bulk(es_client, generate_data(data_dict_elasticsearch))
print("Insertion dans Elasticsearch réussie")