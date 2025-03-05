import streamlit as st
import API
from datetime import datetime

def preferencias_usuario():
    """Selección de preferencias de géneros, actores y directores"""
    st.header("Cuéntanos tus preferencias")
    
    # Obtener datos de géneros, actores y directores
    generos = API.get_genres()
    actores = API.get_actors()
    directores = API.get_directors()
    
    # Checkboxes para selección
    st.subheader("Géneros que te gustan")
    generos_seleccionados = st.multiselect(
        "Elige tus géneros favoritos", 
        [g['n.name'] for g in generos]
    )
    
    st.subheader("Actores favoritos")
    actores_seleccionados = st.multiselect(
        "Elige tus actores favoritos", 
        [a['n.name'] for a in actores]
    )
    
    st.subheader("Directores favoritos")
    directores_seleccionados = st.multiselect(
        "Elige tus directores favoritos", 
        [d['n.name'] for d in directores]
    )
    
    if st.button("Guardar Preferencias"):
        username = st.session_state.username
        for genero in generos_seleccionados:
            API.create_user_like_relation(username, genero, 'Genre', {})
        
        for actor in actores_seleccionados:
            API.create_user_like_relation(username, actor, 'Actor', {})
        
        for director in directores_seleccionados:
            API.create_user_like_relation(username, director, 'Director', {})
        
        st.success("Preferencias guardadas")

def recomendar_peliculas():
    """Sistema de recomendación basado en items"""
    st.header("Recomendaciones Personalizadas")

    username = st.session_state.username
    recomendaciones = API.get_movie_recommendations(username)

    if recomendaciones:
        st.subheader("Te recomendamos estas películas:")
        for pelicula in recomendaciones:
            st.write(f"- 🎬 {pelicula}")
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
