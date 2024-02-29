import pandas as pd
import pymongo

print("fesses")


##Instanciation du client Mongo
client = pymongo.MongoClient("mongodb",27017)
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




