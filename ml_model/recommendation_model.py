import os
import pandas as pd
import requests
import zipfile
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from fuzzywuzzy import process

# Check if the dataset directory exists
if not os.path.exists('ml-latest'):
    # Download and unzip the dataset
    url = "https://files.grouplens.org/datasets/movielens/ml-latest.zip"
    response = requests.get(url)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        z.extractall()

# Load data
movies = pd.read_csv('ml-latest-small/movies.csv')

# Use TF-IDF to convert text data into numerical data
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(movies['genres'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

def get_recommendations(query_title, cosine_sim=cosine_sim):
    # Use fuzzywuzzy to find the most similar title in the dataset
    title, score, index = process.extractOne(query_title, movies['title'])
    
    # Check if the similarity score meets a threshold (e.g., 80)
    if score < 80:
        return f"No similar movie found for '{query_title}'."
    
    idx = movies.index[movies['title'] == title].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]
user_movie = input("Enter the name of a movie: ")

# Get and print recommendations based on user's input
print(get_recommendations(user_movie))
