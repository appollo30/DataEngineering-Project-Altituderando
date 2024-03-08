from itertools import chain

def generate_query(str_prompt,size,sorting_type,keywords,difficulty):
    prompt_split = str_prompt.lower().split(" ")
    QUERY = {
        "query": {
            "bool": {
                "should": 
                list(chain.from_iterable(
                [
                     [{ "term": { "page_title": term }},
                     { "term": { "location": term }},
                     { "term": { "acces": term }},
                     { "term": { "description": term }},
                     { "term": { "itinerary": term }}]
                    for term in prompt_split
                ]
                )),
		"must":
		[
                    { "match": { "location": kw.lower() }}
                    for kw in keywords
                ]
            }
        },
        "size" : size
    }
    if difficulty != "":
        QUERY["query"]["bool"]["should"].append({ "match": { "difficulty": difficulty.lower() }})

    if sorting_type == "Dénivelé (Croissant)":
        QUERY['sort'] = [
            { "height_difference": "asc" }
        ]
    elif sorting_type == "Dénivelé (Décroissant)":
        QUERY['sort'] = [
            { "height_difference": "desc" }
        ]
    return QUERY

QUERY_LOCATION = {
  "size": 0,
  "aggs": {
    "unique_locations": {
      "terms": {
        "field": "location.keyword",
        "size": 10000
      }
    }
  }
}
