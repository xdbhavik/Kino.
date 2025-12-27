from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import difflib

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
    # 0. Safety Check
    if movies is None or similarity is None:
        return ["System Error: Data files missing."]
    
    # --- STEP 1: NORMALIZE INPUT ---
    # Convert to lowercase and strip whitespace
    query = movie_title.lower().strip()
    
    # Get all titles and make a lowercase version for searching
    all_titles = movies['Title'].tolist()
    lower_titles = [t.lower() for t in all_titles]
    
    # --- STEP 2: SUBSTRING SEARCH (For "Half Names") ---
    # Looks for the user's query INSIDE the movie title
    # e.g., "dark knight" will match "The Dark Knight"
    substring_matches = [
        title for title, lower in zip(all_titles, lower_titles) 
        if query in lower
    ]
    
    # If we found substring matches, use the shortest one (usually the most accurate)
    if substring_matches:
        # Sort by length so "Iron Man" comes before "Iron Man 3"
        closest_match = sorted(substring_matches, key=len)[0]
    
    else:
        # --- STEP 3: FUZZY SEARCH (For "Typos") ---
        # Only runs if Substring Search failed.
        # e.g., "Avengrs" won't be a substring, but difflib will find it.
        # cutoff=0.4 allows for "loose" matching
        fuzzy_matches = difflib.get_close_matches(query, lower_titles, n=1, cutoff=0.4)
        
        if not fuzzy_matches:
            return ["Movie not found. Please check spelling."]
        
        # We need to map the lowercase fuzzy match back to the original Title
        # (Because 'fuzzy_matches' gives us the lowercase version)
        match_index = lower_titles.index(fuzzy_matches[0])
        closest_match = all_titles[match_index]

    # --- STEP 4: RETRIEVE RECOMMENDATIONS ---
    try:
        # Find the index of the closest match
        index = movies[movies['Title'] == closest_match].index[0]
        
        # Get similarity scores
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        
        # Get top 6 recommendations
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

