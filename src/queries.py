def generate_query(str_prompt):
    QUERY = {
        "query": {
            "term": {
                "page_title": str_prompt
            }
        }
    }
    return QUERY



