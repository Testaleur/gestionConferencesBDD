import re

def process_keywords(search_query): # splits and lowers cases, removes symbols
  cleaned = re.sub(r"[^\w\s]", "", search_query)
  words = [w.lower() for w in cleaned.split()]
  return words

def process_profile(profile): # splits and lowers cases, removes symbols
  words = [w.lower().trim() for w in profile.split(",")]
  return words