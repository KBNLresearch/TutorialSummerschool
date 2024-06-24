import pandas as pd
import spacy
import pickle

from spacy.lang.nl.examples import sentences

def process_text(text):
    return nlp(text)

rows_to_keep = range(0, 100)
vaderland = pd.read_csv("HetVaderland_1873_fixed.csv", index_col=0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0, skiprows = lambda x: x not in rows_to_keep)
standaard = pd.read_csv("DeStandaard_1873.csv", index_col = 0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0, skiprows = lambda x: x not in rows_to_keep)
tijd = pd.read_csv("DeTijd_1873_fixed.csv", index_col = 0, delimiter=',', encoding='utf-8', quotechar='"', quoting=0, skiprows = lambda x: x not in rows_to_keep)

data = pd.concat([vaderland, standaard, tijd])

data["date"] = pd.to_datetime(data["date"])

data['month'] = data['date'].dt.strftime("%B")
data['day'] = data['date'].dt.strftime("%A")

data = data.sort_values(by='date')

data = data.dropna(subset=['content'])

# Specify the relative path to the model directory
model_path = "../model/nl_core_news_sm"

# Load the model from the relative path
nlp = spacy.load(model_path)

data["doc"] = data["content"].apply(process_text)

# Serialize
with open('processed_docs.pkl', 'wb') as f:
    pickle.dump(data, f)

# # Deserialize
# with open('processed_docs.pkl', 'rb') as f:
#     processed_docs = pickle.load(f)
