import streamlit as st
import queries
from elasticsearch import Elasticsearch
from os import environ

#Connexion à ES

es_host = environ.get("ELASTICSEARCH_HOST")
es_port = environ.get("ELASTICSEARCH_PORT")

es_client = Elasticsearch(hosts=["localhost" if es_host == None else es_host],timeout = 120)

#Début de la page streamlit
st.title('DataEngineering: Altituderando')

#On vérifie que ES est bien connecté
es_connexion = es_client.ping()
st.markdown('Connexion à Elasticsearch: **'+str(es_connexion)+"**")

user_input = st.text_input(label="Recherchez un article dans Altituderando")

query = queries.generate_query(user_input)
