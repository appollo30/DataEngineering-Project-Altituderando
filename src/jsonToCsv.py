import pandas as pd

#Il s'agit juste d'un programme pour convertir le résultat du scraping du json au csv (cela évite de devoir faire en plus scrapy crawl altituderando -O ../data/results.csv qui prendrait aussi 30mn a scraper, et en plus selon les permissions du site, le site peut refuser l'accès lors d'un scraping et pas un autre)
#Note: Ici cela n'est vraisemblablement pas le cas, puisque pour avoir testé, sur chaque scraping on scrape précisement 10365 pages.

df = pd.read_json('../data/results.json')


df.to_csv('../data/results.csv', index=False)