from flask import Flask, render_template, request
import pickle
import pandas as pd
import os

app = Flask(__name__)

# --- FILE LOADING LOGIC ---
def load_data():
    # 1. Name of the file we want to create/load in the end
    reconstructed_filename = 'similarity_reconstructed.pkl'
    
    # 2. Check if we already reconstructed it (so we don't do it every request)
    if not os.path.exists(reconstructed_filename):
        print("Reconstructing similarity matrix from parts...")
        
        # Create the new empty file
        with open(reconstructed_filename, 'wb') as outfile:
            part_num = 1
            while True:
                # Look for similarity.pkl.part1, part2, etc.
                part_name = f"similarity.pkl.part{part_num}"
                
                if not os.path.exists(part_name):
                    break # Stop when we run out of parts
                
                print(f"Merging {part_name}...")
                with open(part_name, 'rb') as infile:
                    outfile.write(infile.read())
                part_num += 1
                
        print("Reconstruction complete.")
                
    # 3. Load the final reconstructed pickle file
    return pickle.load(open(reconstructed_filename, 'rb'))

# --- GLOBAL DATA LOADING ---
try:
    # Load movies (Small file, usually exists directly)
    movies = pickle.load(open('movie_list.pkl', 'rb'))
    
    # Load similarity (Big file, uses the reconstruction logic above)
    similarity = load_data()
    
except FileNotFoundError as e:
    print(f"Critical Error: {e}")
    movies = None
    similarity = None

# --- RECOMMENDATION LOGIC ---
def recommend(movie_title):
    if movies is None or similarity is None:
        return ["System Error: Data files missing or corrupted."]
    
    try:
        # 1. Find the index of the movie (case-insensitive)
        matches = movies[movies['Title'].str.lower() == movie_title.lower()]
        
        if matches.empty:
            return ["Movie not found. Please check the spelling."]
            
        index = matches.index[0]
        
        # 2. Get similarity scores
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # 3. Get top 6 recommendations (skip index 0, which is the movie itself)
        recommended_movie_names = []
        for i in distances[1:7]:
            recommended_movie_names.append(movies.iloc[i[0]].Title)
            
        return recommended_movie_names

    except Exception as e:
        return [f"An error occurred: {str(e)}"]

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    user_input = ""
    
    if request.method == 'POST':
        user_input = request.form.get('movie_name')
        if user_input:
            recommendations = recommend(user_input)
    
    return render_template('index.html', recommendations=recommendations, query=user_input)

if __name__ == '__main__':
    app.run(debug=True)