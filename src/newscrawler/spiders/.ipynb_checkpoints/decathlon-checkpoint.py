import scrapy
import random
from datetime import date


class DecathlonSpider(scrapy.spiders.SitemapSpider):
    name = 'decathlon'
    allowed_domains = ['altituderando.com']
    sitemap_urls = [
        'https://www.altituderando.com/sitemap-rando-topo.xml'
    ]
    custom_settings = {
        'USER_AGENT': 'MyCustomUserAgent'+ str(random.randint(0,1e6)) +'/1.0'
    }
    mois = {
        "janvier": 1,
        "février": 2,
        "mars": 3,
        "avril": 4,
        "mai": 5,
        "juin": 6,
        "juillet": 7,
        "août": 8,
        "septembre": 9,
        "octobre": 10,
        "novembre": 11,
        "décembre": 12
    }
    


    def parse(self, response):
        yield {
            'page_title' : response.css('title::text').extract_first(),
            'description' : response.css('meta[name="description"]::attr(content)').extract_first(),
            'url' : response.url,
            'image_url' : response.css('div[class="col-lg-8"]').css('img::attr(src)').extract_first(),
            'difficulty' : response.css('dd[title="Difficulté"]::text').extract_first(),
            'author' : response.css('a[rel="author"]::text').extract_first(),
            'location' : response.css('li[id="localisation-entete"]').css('a::text').extract(),
            'activity' : response.css('li[id="type"]::text').extract_first(),
            'keywords' : response.css('li[id="mot-cle"]').css('span::text').extract(),
            'all_photos_url' : response.urljoin(response.css('a[id="toutes-les-photos"]::attr(href)').extract_first()),
            'height_difference' : self.convertir_int(response.css('dd[title="Dénivelé"]::text').extract_first()),
            'access' : response.css('div[id="acces"]').css('p::text').extract_first(),
            'difficulty_precisions' : response.css('div[id="difficulte-prevision"]').css('p::text').extract(),
            'itinerary' : "".join(response.css('div[id="itineraire"]').css('div[class="ctexte"]').css('p::text').extract()),
            'additional_info' : self.traiter_infos_supplementaires(response),
            'comments' : response.css('div[id="commentaires"]').css('ul').css('div[class="contenu-msg"]').css('p::text').extract(),
            'date' : self.nettoyer_et_convertir_date(self.trouver_date_modification(response.css('div[class="metadates"]').css('p::text').extract()))
        }
        pass

    def trouver_date_modification(self,result_list):
        for elt in result_list:
            if elt[0] == '.':
                return elt
        return None

    def nettoyer_et_convertir_date(self,str_date):
        # Supprimer les caractères non nécessaires et diviser la chaîne par des espaces
        cleaned_str = str_date.replace('. Dernière modification :', '').replace('\r\n', '').replace('(','').strip()
        cleaned_str_split = cleaned_str.split(" ")
        try:
            accurate_month = self.mois[cleaned_str_split[1]]
            date_obj = date(int(cleaned_str_split[2]), accurate_month, int(cleaned_str_split[0]))
        except (ValueError, KeyError) as error:
            # Gérer le cas où le format de date est différent
            date_obj = None
        return date_obj

    def convertir_int(self,str_result):
        try:
            result = int(str_result)
        except ValueError:
            result = None
        return result

    def traiter_infos_supplementaires(self,response):
        r1 = response.css('div[id="bloc-carte"]').css('strong::text').extract()
        r2 = [elt for elt in response.css('div[id="bloc-carte"]').css('li::text').extract() if elt != ' ' ]
        if len(r1) == len(r2):
            return [str(r1[i]) + str(r2[i]) for i in range(len(r1))]
        return r2
