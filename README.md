# related-eventregistry-events
This script, mostly in Python, finds related events based on JSON data from EventRegistry

Begins by looking at events\events-00###000.JSON.

1. Run tfidf.py - assigns each word an idf value. Creates concept_hash_tables.json
2. Run concept_articles.py. Reads concept_hash_tables.json and gives each word => article => tfidf score.
3. Run lookup.py - looks at each word in the event and compares to words with similar tfidf scores.
