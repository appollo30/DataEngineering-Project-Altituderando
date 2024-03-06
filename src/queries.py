from itertools import chain

def generate_query(str_prompt,size):
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
                ]))
            }
        },
        "size" : size
    }
    return QUERY