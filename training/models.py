import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# from google.colab import files

# 1. Load your uploaded file

df = pd.read_csv('IMDbMovies-Clean.csv')

# 2. Preprocessing - Fill empty values to prevent errors
text_columns = ['Title', 'Summary', 'Director', 'Writer', 'Main Genres']
for col in text_columns:
    df[col] = df[col].fillna('')

# 3. Create a 'Soup' of metadata for better similarity matching
# This combines all key text into one searchable string per movie
def create_soup(x):
    return x['Title'] + " " + x['Summary'] + " " + x['Director'] + " " + x['Writer'] + " " + x['Main Genres']

df['soup'] = df.apply(create_soup, axis=1)

# 4. Vectorization using TF-IDF
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['soup'])

# 5. Calculate Cosine Similarity
similarity = cosine_similarity(tfidf_matrix)

# 6. Export for your Flask App
# We save the cleaned dataframe and the similarity matrix
pickle.dump(df, open('movie_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

