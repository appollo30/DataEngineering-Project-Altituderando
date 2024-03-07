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

<img width="732" alt="Capture d’écran 2024-03-07 à 17 27 12" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/dac6346f-81a4-4a7c-b1b1-dcf3e8079395">


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

Les inforamtions collectées dans le json sont:
- Le titre de la page
- Son url
- Une courte description
- L'image principale de l'article
- La difficulté
- L'auteur
- Les noms de massifs, département, commune
- La discipline (Randonnée, Alpinisme, Spéléo, etc.)
- Des mots-clés
- L'url où sont stockées toutes les photos de la rando postées par la communauté
- Le dénivelé
- L'accès à la rando
- L'itinéraire
- Des infos supplémentaires sur les endroits difficiles, l'équipement, etc.
- La date de publication
- Les commentaires avec leurs dates de publication et leurs auteurs

## L'Insertion

On insère ensuite les données scrapées dans une base Mongo et un index Elasticsearch, pour cela on utilise Docker-compose, et on utilise les servieces mongo, elasticsearch, kibana, et celui qui est défini dans notre Dockerfile. On effectue notamment un mapping des ports pour que les services soient bien connectés entre eux et on utilise des variables d'environnement pour les ports et les hôtes de Elasticsearch et mongo.

#### Pourquoi ES et Mongo?
Tout d'abord un prtit mot sur pourquoi est-ce qu'on a choisi d'utiliser les 2 systèmes de bases de données alors que cela pourrait être redondant? Nous avons fait ce choix car certains problèmes d'Elasticsearch sont comblés par Mongo. En effet la méthode d'indexation inversée de Elasticsearch fait que chaque terme individuel est stocké sur la base, et c'est les endroits où apparaissent les termes qui sont stockés. Ainsi, si on souhaite ajouter des documents 1 par 1 dans un index Elasticsearch, cela prendrait beaucoup plus de temps par rapport à une base Mongo où il faudrait juste ajouter le document à la suite de la collection. On garde donc mongo au cas où il faudrait updater l'index plusieurs fois par minute, ce qui serait inefficient (cela ne risque pas d'arriver vu le trafic généré par Altituderando, mais on sait jamais ;) ).

![inverse-index](https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/850b2a20-894d-4dae-bb7c-d1b39f14b20c)

Maintenant pour l'insertion, tout se passe dans ```./src/insertion.py```. On a choisi de le séparer en 2 fonctions distinctes, une pour mongo, une pour Elasticsearch. Pour mongo c'est relativement simple puisque le service se lance quasi instantanément dans docker-compose, tandis que Elasticsearch met plus de temps. On doit donc effectuer des tentatives de connexion à répétition au client Elasticsearch pour y avoir accès. Pour éviter le timeout, on l'a modifié à 120 secondes dans le client.

## L'App
On a décidé d'utiliser la librairie streamlit pour l'app. C'est une librairie python utilisée pour créer des app web légères et des dashboards. Les app streamlit se rechargent à chaque fois que l'input de l'utilisateur est changée donc c'est idéal dans notre cas. 

Quand l'user-input est changée, on génère une nouvelle requête Elasticsearch via la fonction ```generate_query```dans ```./src/queries.py```, puis on la recherche dans l'index, et on affiche les résultats et le temps que la recherche a pris.

Lorsqu'on ouvre l'app on a accès à la page suivante:

<img width="732" alt="Capture d’écran 2024-03-07 à 17 27 12" src="https://github.com/appollo30/DataEngineering-Project-Altituderando/assets/27921296/e343c092-2371-479e-b8cb-443f42ae28aa">

On nous indique si la connexion à Elasticsearch est bonne, puis on a la barre de recherche principale, où on peut taper des mots-clés pour avoir une recherche termwise de chaque mot-clé dans le titre de la page, dans le lieu, dans la description, dans l'accès et dans l'itinéraire. Ensuite on peut choisir des localisations précises, la difficulté, et l'ordre du tri des résultats. 

Enfin on peut regler l'affichage de la recherche avec le nombre de colonnes que l'on souhaite afficher et le nombre de résultats.


# Notes

Vous pouvez constater que le projet contient à la fois un ```requirements.txt```et un ```environment.yml```, c'est parce qu'à l'origine on utilisait une image miniconda, mais le fait d'avoir à la fois un conteneur docker et un environnement conda semblait redondant. De plus, l'image miniconda est beaucoup plus lourde que l'image officielle python. C'est pourquoi nous nous sommes rabattus sur l'image python. On a laissé le ```environment.yml``` au cas où, et parce que nous avions déjà un environnement déjà prêt sur nos machines en local lors du développement.

Vous constaterez qu'on utilise également un service Kibana, on s'en est surtout servis au cours du développement pour voir si l'insertion se déroulait bien et pour analyser nos données. Si vous souhaitez consulter les données vous pouvez également vous rendre sur ```localhost:5601``` pour consulter l'index ```altituderando*``` après avoir lancé le docker-compose.
