import streamlit as st
import API

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



