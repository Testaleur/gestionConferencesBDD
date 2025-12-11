import random

# Vocabulaire scientifique
domains = [
  "Neural Networks",
  "Quantum Computing",
  "Machine Learning",
  "Cybersecurity",
  "Data Mining",
  "Bioinformatics",
  "Robotics",
  "Climate Modeling",
  "Artificial Intelligence",
  "Software Engineering",
  "Spatial Data Bases"
]

verbs = [
  "Analysis of",
  "Advances in",
  "Applications of",
  "Challenges in",
  "Evaluation of",
  "Optimization of",
  "Exploring",
  "Modeling of"
]

adjectives = ["Efficient", "Robust", "Novel", "Scalable", "High-Performance", "Adaptive"]

def generate_scientific_title():
  verb = random.choice(verbs)
  domain = random.choice(domains)
  adj = random.choice(adjectives) if random.random() < 0.5 else ""
  title = f"{verb} {adj} {domain}".strip()
  return " ".join(title.split())  # remove double spaces if adj is empty

def generate_scientific_intro():
  # Simple template-based intro
  intro_templates = [
    "This study presents the latest research on {domain}.",
    "We explore novel methodologies in {domain} for improved performance.",
    "In this work, we investigate the challenges of {domain}.",
    "Our research focuses on developing robust solutions for {domain}.",
    "This paper provides an in-depth analysis of {domain} applications."
  ]
  domain = random.choice(domains)
  template = random.choice(intro_templates)
  return template.format(domain=domain)
