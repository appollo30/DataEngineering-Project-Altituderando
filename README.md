# DataEngineering-Project-Altituderando
By Noureddine BOUDALI et Léo LASNIER

Bienvenue sur la page Github du projet AltitudeRando dans le cadre de l'unité DataEngineering.

Il s'agit d'un moteur de recherche qui va scraper les données depuis le site https://www.altituderando.com/, puis les afficher dans une webapp.

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

#### Pour lancer l'appli directement :
- Pareil mais faites l'opération inverse (commentez la ligne 20 et décommentez la ligne 22)


Placez-vous à la racine du projet dans un terminal, puis lancer la commande ```docker build -t altituderando .```
Cela crééra l'image docker du projet. Cela peut prendre un peu de temps (2-3mn) si vous lancez cette commande pour la première fois car l'image a besoin de charger toutes les dépendances du projet.

Ensuite, toujours à la racine du projet, lancez la commande ```docker-compose up```. Cela lancera le docker-compose.
Même sans effectuer de scraping, cela prend quelques temps (~2mn), le temps d'initialiser le service Elasticsearch.

une fois que c'est fait
