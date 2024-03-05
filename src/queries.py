def generate_query(str_prompt):
    QUERY = {
        "query": {
            "term" : { 
                "page_title" : str_prompt} 
        }
    }
    return QUERY


def query_result(es_client,idx,query):
    result = es_client.search(index=idx, body=query)
    return result
