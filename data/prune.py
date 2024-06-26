import pandas as pd
import pickle


# Deserialize
data = pd.read_pickle('processed_docs.pkl')
reduced_data = data.sample(frac = 0.005)

with open('reduced_docs.pkl', 'wb') as f:
    pickle.dump(reduced_data, f)