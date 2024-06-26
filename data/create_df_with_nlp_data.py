import pandas as pd
import spacy
import pickle

from spacy.lang.nl.examples import sentences

nlp = spacy.load("../model/nl_core_news_sm")
print("spacy geladen", flush=True)

def process_text(text):
    # Load the model from the relative path
    return nlp(text)

vaderland = pd.read_csv("HetVaderland_1873.csv", index_col=0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0)
print("vaderland ingelezen: " + str(len(vaderland)), flush=True)
standaard = pd.read_csv("DeStandaard_1873.csv", index_col = 0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0)
print("standaard ingelezen: " + str(len(standaard)), flush=True)
tijd = pd.read_csv("DeTijd_1873.csv", index_col = 0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0)
print("tijd ingelezen:      " + str(len(tijd)), flush=True)

data = pd.concat([vaderland, standaard, tijd])
print("data geplakt", flush=True)

data["date"] = pd.to_datetime(data["date"])
data['month'] = data['date'].dt.strftime("%B")
data['day'] = data['date'].dt.strftime("%A")

data = data.sort_values(by='date')
print("data gesorteerd", flush=True)

data = data.dropna(subset=['content'])
print("data gerefinet", flush=True)

data["doc"] = data["content"].apply(process_text)

# Serialize
with open('processed_docs.pkl', 'wb') as f:
    pickle.dump(data, f)

print("klaar met dumpen", flush=True)
# # Deserialize
# with open('processed_docs.pkl', 'rb') as f:
#     processed_docs = pickle.load(f)
