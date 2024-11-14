import streamlit as st
from utilities import load_data, get_recommendations

# Carrega o modelo e dados
model, movie_pivot, movies = load_data()

st.set_page_config(page_title='Filmes Recomendados', layout='centered')

# Color settings
st.markdown(
    """
    <style>
    .main {
        background-color: #1a1a1a;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.write('# Qual seu próximo filme?')
st.write('### Insira seu filme favorito abaixo para receber recomendações '
         'personalizadas de filmes semelhantes!')
st.write("""---""")

# Input
movie_name = (st.text_input("Digite o seu filme favorito (em inglês):", "")
              .strip().lower())

# Search button
if st.button("Buscar Recomendações"):
    if movie_name:
        try:
            recommendations = get_recommendations(movie_name, model,
                                                  movie_pivot)
            if recommendations:
                st.subheader("Recomendações de Filmes:")
                for rec in recommendations:
                    st.write(f"- {rec}")
            else:
                st.write("Filme não encontrado ou sem recomendações.")
        except Exception as e:
            st.write("Ocorreu um erro. Tente novamente mais tarde.")
            st.write(f"Erro: {e}")
    else:
        st.write("Por favor, insira um filme para buscar recomendações.")
