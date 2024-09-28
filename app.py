import streamlit as st
import pickle
import pandas as pd
import requests as req
from dotenv import load_dotenv
import os

load_dotenv()

tmdb_api_keys = os.getenv('tmdb_API_KEYS')


movie_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_posters(movie_id):
    res = req.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_keys}&languale=en-us')
    data = res.json()
    # print(data['success'])
    if 'success' in data.keys():
        # print(data['success'])
        return -1
    else:
        return 'https://image.tmdb.org/t/p/w185' + data['poster_path'],'https://www.imdb.com/title/' + data['imdb_id']
        # print(data['poster_path'])
    # poster = data['poster_path']
    # print(poster)

def recommend_movie(movie_name):
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    recommended_movies = []
    posters = []
    imdb_page = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # print(new_df.iloc[i[0]].title)
        # posters.append(fetch_posters(movie_id))
        poster_link,imdb_link = fetch_posters(movie_id)
        posters.append(poster_link)
        imdb_page.append(imdb_link)
    return recommended_movies,posters,imdb_page

st.title("movie recommender system")

selected_movie_name = st.selectbox('Which movie do you like',movies['title'].values)

if st.button("recommend"):
    names,posters,imdb_pages = recommend_movie(selected_movie_name)
    columns = st.columns(5)
    for i, col in enumerate(columns):
        with col:
            st.text(names[i])
            # Create clickable images
            st.markdown(
                f'<a href="{imdb_pages[i]}" target="_blank">'
                f'<img src="{posters[i]}" alt="{names[i]}" style="width:100%;">'
                '</a>',
                unsafe_allow_html=True
            )