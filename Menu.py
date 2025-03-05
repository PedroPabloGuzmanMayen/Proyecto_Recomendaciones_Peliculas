import streamlit as st
import API
from datetime import datetime

def recomendar_peliculas():
    """Sistema de recomendación basado en ítems"""
    st.header("Recomendaciones Personalizadas")

    username = st.session_state.username
    recomendaciones = API.get_recommendations_based_on_similarity(username)

    if recomendaciones:
        st.subheader("Películas recomendadas:")
        for pelicula in recomendaciones:
            st.write(f"- {pelicula['title']} (Similitud: {pelicula['score']:.2f})")
    else:
        st.info("No se encontraron recomendaciones. Intenta calificar más películas.")


def calificar_peliculas():
    """Permite al usuario calificar cualquier película disponible en la base de datos"""
    st.header("🎥 Califica las Películas")
    
    username = st.session_state.username
    peliculas = API.get_movies()  

    if peliculas:
        st.subheader("Selecciona una película para calificar:")

        peliculas_dict = {pelicula["n.title"]: pelicula for pelicula in peliculas}
        seleccion = st.selectbox("📌 Películas disponibles:", list(peliculas_dict.keys()))

        if seleccion:
            pelicula = peliculas_dict[seleccion]

            # Verificar si el póster es una URL válida
            poster_url = pelicula.get("n.poster", "")
            if poster_url and poster_url.startswith("http"):
                try:
                    response = requests.get(poster_url, timeout=5)
                    if response.status_code == 200:
                        st.image(poster_url, width=200)
                    else:
                        st.warning("⚠️ No se pudo cargar la imagen.")
                except requests.exceptions.RequestException:
                    st.warning("⚠️ No se pudo cargar la imagen.")
            else:
                st.warning("⚠️ No hay póster disponible.")

            st.write(f"📅 **Estreno:** {pelicula['n.releaseDate']}")
            st.write(f"⭐ **Rating General:** {pelicula['n.rating']}")
            st.write(f"📝 **Sinopsis:** {pelicula['n.overview']}")

            with st.form(key=f"form_{seleccion}"):
                rating = st.slider("Calificación:", min_value=0.0, max_value=10.0, value=5.0)
                comentario = st.text_area("Comentario sobre la película:")
                fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                submit_button = st.form_submit_button(label="✅ Guardar Calificación")

                if submit_button:
                    rel_props = {"rating": rating, "comment": comentario, "date": fecha_actual}
                    API.create_movie_review(username, seleccion, rel_props)
                    st.success(f"Calificación guardada para **{seleccion}** ✅")

def recomendaciones_similaridad():
    """Sistema de recomendación basado en similaridad de películas"""
    st.header("Recomendaciones Basadas en Similaridad")

    username = st.session_state.username
    recomendaciones = API.get_recommendations_based_on_similarity(username)

    if recomendaciones:
        st.subheader("Te recomendamos estas películas:")
        for pelicula in recomendaciones:
            st.write(f"- 🎬 {pelicula['title']} (Similitud: {pelicula['score']})")
    else:
        st.info("No se encontraron recomendaciones. Intenta calificar más películas.")
