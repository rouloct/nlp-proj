import spacy

nlp = spacy.load("data_processing/output/model-best")
doc = nlp("eggs are gross")
print(doc.cats)