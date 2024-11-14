import os
import pickle
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
st.write("API Key:", TMDB_API_KEY)


# Função para carregar os dados uma vez
def load_data():
    try:
        # Verifica a existência dos arquivos e carrega
        if not os.path.exists("parameter/model.pkl"):
            raise FileNotFoundError("Arquivo 'model.pkl' não encontrado.")

        model = pickle.load(open("parameter/model.pkl", "rb"))
        movie_pivot = pickle.load(open("parameter/movie_pivot.pkl", "rb"))
        movies = pickle.load(open("parameter/movies.pkl", "rb"))

        return model, movie_pivot, movies
    except FileNotFoundError as e:
        print(f"Erro ao carregar o modelo ou dados: {e}")
        return None, None, None


def get_movie_poster(title):
    """Busca a capa do filme pelo título usando a API TMDB."""
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"

    try:
        response = requests.get(url)
        data = response.json()

        # Verifique se há resultados e se a capa está disponível
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar a capa do filme: {e}")

    # Retorna uma imagem padrão se a capa não for encontrada
    return "https://via.placeholder.com/150x225?text=Capa+Indisponível"


# Função para obter recomendações de filmes
def get_recommendations(movie_name, model, movie_pivot):
    """Retorna uma lista de recomendações de filmes,
    ou uma lista vazia se o filme não for encontrado."""
    if model is None or movie_pivot is None:
        raise ValueError("Modelo ou dados não foram carregados corretamente.")

# Converter todos os títulos no índice para minúsculas
    movie_index_lower = {title.lower(): title for title in movie_pivot.index}

    # Verifica se o filme existe na base
    if movie_name not in movie_index_lower:
        return []

    # Obtém as recomendações usando o modelo carregado
    original_title = movie_index_lower[movie_name]
    distances, indices = (model.kneighbors(movie_pivot.loc[original_title]
                                           .values.reshape(1, -1),
                                           n_neighbors=6))
    recommended_movies = [
        {
            "title": movie_pivot.index[i],
            "poster_url": get_movie_poster(movie_pivot.index[i])
        }
        for i in indices.flatten()[1:]
    ]
    return recommended_movies


# Carrega os dados e modelo
model, movie_pivot, movies = load_data()
