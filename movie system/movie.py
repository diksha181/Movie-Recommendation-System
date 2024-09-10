import streamlit as st
import pandas as pd
import pickle
import requests


def fetch_poster(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=70c3d81da1bef397e2a609a8c9644101&language=en-US".format(movie_id)
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


movies_dict = pickle.load(open("movies.pkl", "rb"))

similarity = pickle.load(open("similarity.pkl", "rb"))


def recommend(movie):
    movie_index = movies_list[movies_list["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_listed = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_listed:
        movie_id = movies_list.iloc[i[0]].id
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


global movies_list
movies_list = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "What would you like to watch?", (movies_list["title"].values),index=None,placeholder="Search similar"
)

def movie_component(index):
    st.text(names[index])
    st.image(posters[index])

if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    tab1,tab2 = st.tabs(["Most Similar","Others you might like"])
    with tab1:
        st.text(names[0])
        st.image(posters[0])
    with tab2:
        col1,col2,col3 = st.columns(3)
        for i in range(1,4):
            with col1:
                movie_component(i)
        for i in range(4, 7):
            with col2:
                movie_component(i)
        for i in range(7, 10):
            with col3:
                movie_component(i)
    
