# DataEngineering-Project-Altituderando
By Noureddine BOUDALI et Léo LASNIER

Bienvenue sur la page Github du projet AltitudeRando dans le cadre de l'unité DataEngineering.

Il s'agit d'un moteur de recherche qui va scraper les données depuis le site https://www.altituderando.com/, puis les afficher dans une webapp.
Nous utilisons principalement Scrapy, MongoDB et pymongo, Elasticsearch, Pandas, Streamlit, Docker, Docker-compose.

Le site Altituderando est un site qui répertorie un certain nombre de chemins de randonnée, alpinisme, spéléologie, etc. principalement en France. Chaque chemin dispose d'une page postée par un utilisateur du site, n'importe qui peut devenir utilisateur. 
Chaque page montre des informations telles que la localisation de la rando, sa difficulté, son dénivelé, des photos, l'accès et l'itinéraire, des cartes, etc. Les utilisateurs peuvent également poster des commentaires.

<img width="2559" alt="Capture d’écran 2024-03-07 à 01 32 07" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/ea5ab725-8a52-4a77-89d9-7779c04acec3">
<img width="2559" alt="Capture d’écran 2024-03-07 à 01 31 42" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/64c182ba-2b78-4be8-827e-923f356e571b">

Il s'agit d'un site avec une communauté plutôt active, puisque l'on peut voir tous les jours de nouveaux articles apparaitre sur le site.

## Installation
Pour installer et lancer le projet, il faut tout d'abord cloner le présent repo avec
```git clone git@github.com:appollo30/DataEngineering-Project-Altituderando.git```
dans le répertoire de votre choix.

Le projet utilise Docker-compose, donc il faut avoir accès à Docker Desktop, qui peut être installé sur https://www.docker.com/products/docker-desktop/.

Avant de créer l'image du projet, il vous faudra choisir entre 2 options que nous avons laissé délibérément, le choix de faire un scraping ou non. En effet, les données de scraping peuvent être disponibles dans les fichiers ```./data/results.json```et ```./data/results.csv```. Néanmoins, vous pouvez directement récupérer les données du site via un scraping. C'est une opération qui prend du temps (~20mn) et si vous souhaitez ne pas avoir à attendre trop longtemps on laisse l'option.

#### Pour effectuer le scraping :
- Rendez-vous dans le fichier ```./Dockerfile``` qui contient toutes les infos pour générer l'image Docker. 
- Décommentez la ligne 20 si ce n'est pas déjà fait
- Recommentez la ligne 22

<img width="643" alt="Capture d’écran 2024-03-07 à 02 18 41" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/c2a8cd4c-12c1-4384-b257-ea796f5faa28">


#### Pour lancer l'appli directement :
- Pareil mais faites l'opération inverse (commentez la ligne 20 et décommentez la ligne 22)

<img width="643" alt="Capture d’écran 2024-03-07 à 02 18 29" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/70653d2c-fa2d-4ef7-9851-d933452420aa">

Placez-vous à la racine du projet dans un terminal, puis lancer la commande ```docker build -t altituderando .```
Cela crééra l'image docker du projet. Cela peut prendre un peu de temps (2-3mn) si vous lancez cette commande pour la première fois car l'image a besoin de charger toutes les dépendances du projet.

Ensuite, toujours à la racine du projet, lancez la commande ```docker-compose up```. Cela lancera le docker-compose.
Même sans effectuer de scraping, cela prend quelques temps (~2mn), le temps d'initialiser le service Elasticsearch en partie.

une fois que c'est fait, attendez jusqu'à voir ceci sur le terminal :

<img width="732" alt="Capture d’écran 2024-03-07 à 02 20 56" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/5ae640b8-a25f-4376-a914-b9e1a4c4a321">

Cela signifie que l'app est en ligne, vous pouvez vous y rendre en tapant ```localhost:8501``` sur votre navigateur.
Vous devriez vous retrouver face à cette page : 

Vous pouvez donc tester l'app!

# Fonctionnement :

Le projet fonctionne en 3 parties principales:
- Le scraping
- L'insertion
- L'app

## Le Scraping

Nous utilisons les outils de Scrapy pour scraper le site. En particulier, pour trouver les ressources à scraper, nous avons examiné le ```robots.txt```du site que l'on peut trouver à https://www.altituderando.com/robots.txt. 

Il s'agit d'un document qu'on peut trouver sur la majourité des sites, et qui donne des infos sur les permissions d'accès au site pour les crawlers et là où on peut retrouver les pages du site, via la Sitemap. Celle d'Altituderando se situe à https://www.altituderando.com/altituderando-sitemap.xml. Elle répertorie entre autres l'ensemble des adresses des pages d'articles que nous allons scraper. 
Scrapy possède une classe qui gère le crawling de sitemaps, ```SitemapSpider```. 

On a donc créé une clesse héritant de ```SitemapSpider```que l'on peut retrouver dans ```./src/newscrawler/spiders/altituderando.py```. On a utilisé les outils de développement pour trouver les endroits dans le html des pages où on pouvait avoir les informations, et on a formulé des requêtes scrapy dans ```parse```pour récupérer ces infos lors du scraping.
Puis on a lancé la spider et stocké les informations dans un fichier json  avec ```scrapy crawl altituderando -O ./data/results.json```.

On a également créé le fichier ```./src/jsonToCsv.py```pour pouvoir convertir les résultats du scraping du json au csv sans avoir besoin de relancer un scraping.

## L'Insertion

On insère ensuite les données scrapées dans une base Mongo et un index Elasticsearch, pour cela on utilise Docker-compose, et on utilise les servieces mongo, elasticsearch, kibana, et celui qui est défini dans notre Dockerfile. On effectue notamment un mapping des ports pour que les services soient bien connectés entre eux et on utilise des variables d'environnement pour les ports et les hôtes de Elasticsearch et mongo.

#### Pourquoi ES et Mongo?
Tout d'abord un prtit mot sur pourquoi est-ce qu'on a choisi d'utiliser les 2 systèmes de bases de données alors que cela pourrait être redondant? Nous avons fait ce choix car certains problèmes d'Elasticsearch sont comblés par Mongo. En effet la méthode d'indexation inversée de Elasticsearch fait que chaque terme individuel est stocké sur la base, et c'est les endroits où apparaissent les termes qui sont stockés. Ainsi, si on souhaite ajouter des documents 1 par 1 dans un index Elasticsearch, cela prendrait beaucoup plus de temps par rapport à une base Mongo où il faudrait juste ajouter le document à la suite de la collection. On garde donc mongo au cas où il faudrait updater l'index plusieurs fois par minute, ce qui serait inefficient (cela ne risque pas d'arriver vu le trafic généré par Altituderando, mais on sait jamais ;) ).

![inverse-index](https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/850b2a20-894d-4dae-bb7c-d1b39f14b20c)

Maintenant pour l'insertion, tout se passe dans ```./src/insertion.py```. On a choisi de le séparer en 2 fonctions distinctes, une pour mongo, une pour Elasticsearch. Pour mongo c'est relativement simple puisque le service se lance quasi instantanément dans docker-compose, tandis que Elasticsearch met plus de temps. On doit donc effectuer des tentatives de connexion à répétition au client Elasticsearch pour y avoir accès. Pour éviter le timeout, on l'a modifié à 120 secondes dans le client.

## L'App
On a décidé d'utiliser la librairie streamlit pour l'app. C'est une librairie python utilisée pour créer des app web légères. 
