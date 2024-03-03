FROM python:3.8

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY src/. ./src
COPY data/. ./data


#Choix du scraping ou non:
#Pour la ligne 20 et 22, si vous souhaitez effectuer le scraping avant de lancer l'app, 
#il suffit de décommenter la ligne 20 et de commenter la ligne 22
#Si vous souhaitez directement lancer l'app sans scraping (les donnees sont disponibles dans le fichier /data/results.json), 
#décommentez la ligne 22 et commentez la ligne 20

##Avec scraping
#CMD ["/bin/bash", "-c", "cd ./src && scrapy crawl altituderando -O results.json && cd .. && python ./src/insertion.py"]
##Pas de scraping
CMD ["python", "./src/insertion.py"]
