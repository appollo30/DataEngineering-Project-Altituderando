import streamlit as st
import queries
from elasticsearch import Elasticsearch
from os import environ
from utils import restrict_str

#Connexion à ES

es_host = environ.get("ELASTICSEARCH_HOST")
es_port = environ.get("ELASTICSEARCH_PORT")

es_client = Elasticsearch(hosts=["localhost" if es_host == None else es_host],timeout = 120)
print(es_client)


#On vérifie que ES est bien connecté
es_connexion = es_client.ping()

#Pour trouver tous les différents endroits

result_location_values = es_client.search(index="altituderando",body=queries.QUERY_LOCATION)
unique_locations = [elt['key'] for elt in result_location_values['aggregations']['unique_locations']['buckets']]

#Début de la page streamlit
st.title('DataEngineering: Altituderando')
st.markdown('Connexion à Elasticsearch: **'+str(es_connexion)+"**")

#Input de l'utilisateur
user_input_prompt = st.text_input(label="Recherchez un article dans Altituderando",placeholder="Recherche")

colonne1,colonne2 = st.columns([0.4,0.6])

with colonne1:
     st.markdown("**Affichage des résultats :**")
     size = st.slider("Nombre de résultats",min_value=1,max_value=30,value=10)
     number_of_cols = st.slider("Nombre de colonnes", min_value=1,max_value=3,value=1)

with colonne2:
     keywords = st.multiselect("Localisation", options=unique_locations)
     difficulty = st.selectbox("Difficulté",["","Facile","Moyen","Difficile"])
     tri = st.radio("Trier par :", ["Pertinence","Dénivelé (Croissant)", "Dénivelé (Décroissant)"])
     


#Creation d'une requête puis recherche dans ES
query = queries.generate_query(user_input_prompt,size=int(size),sorting_type=tri,keywords=keywords,difficulty=difficulty)
result = es_client.search(index="altituderando",body=query)
#st.markdown(str(result))
st.markdown("Votre recherche a pris **" + str(result["took"]) + "** millisecondes et a trouvé **" + str(result["hits"]["total"]) + "** randonnées correspondantes !")
content = [elt['_source'] for elt in result["hits"]["hits"]]
for i in range(len(content)):
    row_index = i%number_of_cols
    if row_index==0:
        st.write("---")
        cols = st.columns(number_of_cols, gap="large")
    with cols[row_index]:
        #Infos principales
        if content[i]["date"] != None:
            st.caption(content[i]["date"].split("T")[0])
        else:
            st.caption("")
        st.header(restrict_str(content[i]['page_title'],150/number_of_cols))
        st.subheader("Auteur : "+ content[i]["author"])
        st.markdown("**"+content[i]['activity']+"**")
        st.markdown("**📍: "+" - ".join(content[i]['location'])+"**")
        st.markdown("**🥵: "+content[i]['difficulty']+"**")
        if content[i]['height_difference'] != None:
             st.markdown("**Dénivelé ⛰️: " + str(int(content[i]['height_difference'])) + "**")
        st.image(str(content[i]['image_url']))
        st.markdown("* " + restrict_str(str(content[i]['description']),200/number_of_cols))
        #Infos supplémentaires
        with st.expander("Plus d'infos : "):
            if content[i]['keywords'] != None:
                st.markdown("* Mots-clés : " + str(content[i]['keywords']))
            if content[i]['access'] != None:
                st.markdown("* Accès : "+ restrict_str(content[i]['access'],300/number_of_cols))
            if content[i]['itinerary'] != None:
                st.markdown("* Itinéraire : "+ restrict_str(content[i]['itinerary'],500/number_of_cols))
            #Photos de la rando
            if content[i]['all_photos_url'] != None:
                 st.link_button("Photos de la randonnée",url=content[i]['image_url'])
            #Section commentaires
            if content[i]['comments_author'] == None:
                 st.subheader("Commentaires : Aucun")
            else:
                st.subheader("Commentaires : "+str(len(content[i]['comments_author'])))
                for j in range(len(content[i]['comments_date'])):
                            if content[i]['comments_author'][j] == None:
                                 st.markdown("**Auteur Inconnu :**")
                            else:
                                st.markdown("**"+content[i]['comments_author'][j]+" :**")
                            st.markdown("   " +restrict_str(content[i]['comments_content'][j],200/number_of_cols))
                            if content[i]['comments_date'][j] != None:
                                st.caption(content[i]["comments_date"][j].split("T")[0])
                            else:
                                st.caption("")
                            st.markdown("")
                           
        st.link_button(label="Aller sur la page",url=str(content[i]['url']))