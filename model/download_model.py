import spacy

# python -m spacy download nl_core_news_sm
nlp = spacy.load("nl_core_news_sm")
nlp.to_disk('nl_core_news_sm')