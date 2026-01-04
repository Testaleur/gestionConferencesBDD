def process_typed_request(search_query): # handles typed request (just lowers and splits cases right now)
  return [w.lower() for w in search_query.split()]