import pandas as pd
import pymongo
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from os import environ
from time import sleep

print("fesses")

def insert_mongo(data):
    #Variables d'environnement
    mongo_host = environ.get("MONGO_HOST")
    mongo_port = environ.get("MONGO_PORT")
    #Instanciation du client Mongo
    global mongo_client
    mongo_client = pymongo.MongoClient("localhost" if mongo_host == None else mongo_host,27017 if mongo_port == None else int(mongo_port))
    print(mongo_host)
    print(mongo_port)
    print(mongo_client)
    database = mongo_client['altituderando']
    collection = database['pages']
    #Insertion
    data_dict_mongo = df.to_dict(orient="records")
    collection.delete_many({})
    collection.insert_many(data_dict_mongo)
    return True


def insert_es(data):
    #Variables d'environnement
    es_host = environ.get("ELASTICSEARCH_HOST")
    es_port = environ.get("ELASTICSEARCH_PORT")
    es_live = False
    #On essaie pendant une minute de se connecter à Elasticsearch
    retry_delay = 1
    number_of_retries = 120
    global es_client
    while not es_live and number_of_retries > 0:
        #Instanciation du client Elasticsearch
        #Avec docker-compose, les services sont lances simultanement donc il arrive que la base elasticsearch soit en ligne après l'exécution de insertion.py, donc elle n'a pas le temps de se lancer qu'on essaie déjà de s'y connecter
        #On y remédie en faisant une boucle où on essaie de se connecter a repetition jusqu'a se connecter. On met le delai entre les connexions à une seconde.
        es_client = Elasticsearch(hosts=["localhost" if es_host == None else es_host],timeout = 120)
        es_live = es_client.ping()
        sleep(retry_delay)
        number_of_retries += -1
    if not es_live:
        return False
    #Traitement de la donnée
    data_dict_es = df.fillna("").to_dict(orient="records")
    def generate_data(documents):
        for docu in documents:
            yield {
                "_index": "altituderando",
                "_type": "page",
                "_source": {k:v if v else None for k,v in docu.items()},
            }
    #Insertion dans Elasticsearch
    bulk(es_client, generate_data(data_dict_es))
    return True



#Traitement de la donnee depuis results.csv
def extract(comments,field):
    return [comment[field] for comment in comments]


df = pd.read_json("./data/results.json")
df['comments_author'] = df['comments'].apply(extract,field='author')
df['comments_content'] = df['comments'].apply(extract,field='content')
df['comments_date'] = df['comments'].apply(extract,field='date')
df['date'] = df['date'].astype(object).where(df['date'].notnull(), None)
df = df.drop('comments',axis=1)


print("Insertion dans Mongo: ", insert_mongo(df))
print("Insertion dans Elasticsearch: ", insert_es(df))