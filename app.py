import streamlit as st
import pickle
import requests

def fetch_poster_path(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=002f35e47887e75b9582198cd5f7b1e8#'.format(movie_id))
    movie_data = response.json()
    poster_path = movie_data['poster_path']
    return "https://image.tmdb.org/t/p/w500"+poster_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]
    for j in movies_list_indices:
        movie_index = movies.iloc[j[0]].movie_id
        recommended_movies.append(movies.iloc[j[0]].title)
        recommended_movies_posters.append(fetch_poster_path(movie_index))
    return recommended_movies,recommended_movies_posters



movies = pickle.load(open('movies.pkl','rb'))
movies_list = movies['title'].values


similarity = pickle.load(open('similarity.pkl','rb'))


## Website
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select the movie",movies_list)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
    cols = st.columns(len(names))
    for i in range(len(names)):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])



