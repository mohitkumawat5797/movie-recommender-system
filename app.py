import streamlit as  st
import pickle 
import pandas as pd
import requests

#st.title('Movie Recommendor system')

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5b255e37dba6b2d0415f83821d27678a&language=en-US".format(movie_id)
    try:
        response = requests.get(url, timeout=5) # Add timeout to prevent hanging
        response.raise_for_status() # Check if request was successful
        data = response.json()
        poster_path = data.get('poster_path')
        
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
            
    except requests.exceptions.RequestException as e:
        # If network fails, print error to console but don't crash the app
        print(f"Error fetching poster: {e}") 
        return "https://via.placeholder.com/500x750?text=Network+Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse = True,key=lambda x:x[1])[1:6]

    recommended_movies = [] 
    recommended_movies_posters = []
    for i in movies_list:

        movie_id = movies.iloc[i[0]]['id']

        recommended_movies.append(movies.iloc[i[0]]['title'])
        # fetching poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters
  




movies_dict = pickle.load(open("movie_dict.pkl",'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl",'rb')) 

selected_movies = st.selectbox(
    'Search',movies['title'].values)



if st.button('Recommend'):
    names, posters = recommend(selected_movies)

    # Dynamically create columns based on how many recommendations you have
    cols = st.columns(5) 
    
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])