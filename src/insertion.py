import pandas as pd
import pymongo
import os


print("fesses")


##Instanciation du client Mongo
var = os.environ
mongo_host = var.get("MONGO_HOST")
mongo_port = var.get("MONGO_PORT")

client = pymongo.MongoClient("localhost" if mongo_host == None else mongo_host,27017 if mongo_port == None else int(mongo_port))
database = client['altituderando']
collection = database['pages']
collection.delete_many({})

##Traitement de la donnee depuis results.csv
def extract_content(comments):
    return [comment['content'] for comment in comments]


df = pd.read_json("./data/results.json")
df['comments'] = df['comments'].apply(extract_content)
df['date'] = df['date'].astype(object).where(df['date'].notnull(), None)

data_dict = df.to_dict(orient="records")




collection.insert_many(data_dict)




