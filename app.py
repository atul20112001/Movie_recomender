import streamlit as st
import pickle
import pandas as pd
import requests
import bz2


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=39b079713a590994f67911b70b0438ae&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Loading the compressed pickle data

compressed_pickle_file = 'data.pkl.bz2'
with bz2.open(compressed_pickle_file, 'rb') as f:
    similarity = pickle.load(f)


compressed_pickle_file = 'movie_dict.pkl.bz2'
with bz2.open(compressed_pickle_file, 'rb') as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)




# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)






# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select the movie you would like to watch',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write(" ")

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write(" ")
    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write(" ")
    with col5:
        st.text(names[4])
        st.image(posters[4])

