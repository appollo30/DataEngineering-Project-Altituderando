import streamlit as st
import queries
from elasticsearch import Elasticsearch
from os import environ
from datetime import date

#Connexion à ES

es_host = environ.get("ELASTICSEARCH_HOST")
es_port = environ.get("ELASTICSEARCH_PORT")

es_client = Elasticsearch(hosts=["localhost" if es_host == None else es_host],timeout = 120)
print(es_client)
#Début de la page streamlit
st.title('DataEngineering: Altituderando')

#On vérifie que ES est bien connecté
es_connexion = es_client.ping()
st.markdown('Connexion à Elasticsearch: **'+str(es_connexion)+"**")

#Input de l'utilisateur
user_input = st.text_input(label="Recherchez un article dans Altituderando",placeholder="Recherche")

if user_input:
    #Creation d'une requête puis recherche dans ES
    query = queries.generate_query(user_input)
    result = es_client.search(index="altituderando",body=query)
    #st.markdown(str(result))
    st.markdown("Votre recherche a pris **" + str(result["took"]) + "** millisecondes et a trouvé **" + str(result["hits"]["total"]) + "** randonnées correspondantes!")
    content = [elt['_source'] for elt in result["hits"]["hits"]]
    number_of_cols = 3
    for i in range(len(content)):
        row_index = i%number_of_cols
        if row_index==0:
            st.write("---")
            cols = st.columns(number_of_cols, gap="large")
        with cols[row_index]:
            if content[i]["date"] != None:
                st.caption(content[i]["date"].split("T")[0])
            st.markdown("**"+str(content[i]['page_title'])+"**")
            st.image(str(content[i]['image_url']))
            st.markdown(str(content[i]['url']))