import re

def process_typed_request(search_query): # splits and lowers cases, removes symbols
  cleaned = re.sub(r"[^\w\s]", "", search_query)
  return [w.lower() for w in cleaned.split()]