import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample Movie Dataset
movies = pd.DataFrame({
    'title': [
        'Avatar',
        'Titanic',
        'Avengers',
        'Iron Man',
        'The Notebook',
        'Interstellar',
        'Inception',
        'Doctor Strange',
        'The Martian',
        'Guardians of the Galaxy'
    ],
    'genre': [
        'Action Adventure Sci-Fi',
        'Romance Drama',
        'Action Adventure Superhero',
        'Action Superhero Sci-Fi',
        'Romance Drama',
        'Sci-Fi Adventure Drama',
        'Sci-Fi Thriller Action',
        'Action Fantasy Sci-Fi',
        'Sci-Fi Adventure',
        'Action Adventure Sci-Fi'
    ]
})

# Convert genres into numerical features
cv = CountVectorizer()
count_matrix = cv.fit_transform(movies['genre'])

# Calculate similarity scores
similarity = cosine_similarity(count_matrix)

# Recommendation function
def recommend(movie_name):
    
    if movie_name not in movies['title'].values:
        print("Movie not found!")
        return
    
    movie_index = movies[movies['title'] == movie_name].index[0]
    
    scores = list(enumerate(similarity[movie_index]))
    
    sorted_scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )
    
    print(f"\nMovies similar to '{movie_name}':\n")
    
    count = 0
    
    for movie in sorted_scores[1:]:
        index = movie[0]
        print(movies.iloc[index]['title'])
        
        count += 1
        
        if count == 5:
            break

# Main Program
print("Available Movies:")
for movie in movies['title']:
    print("-", movie)

choice = input("\nEnter a movie you like: ")

recommend(choice)
