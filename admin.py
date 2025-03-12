import streamlit as st
import API

def administrar_datos():
    st.header("Administración de Datos")
    
    # Menú de administración
    opcion = st.selectbox(
        "Seleccione qué desea administrar",
        ["Películas", "Actores", "Directores", "Reviews"]
    )
    
    if opcion == "Películas":
        administrar_peliculas()
    elif opcion == "Actores":
        administrar_actores()
    elif opcion == "Directores":
        administrar_directores()
    elif opcion == "Reviews":
        admin_reviews()

def administrar_peliculas():
    st.subheader("Administración de Películas")
    
    # Seleccionar operación CRUD
    operacion = st.radio(
        "Seleccione la operación",
        ["Ver películas", "Crear película", "Actualizar película", "Eliminar película"]
    )
    
    if operacion == "Ver películas":
        # Obtener y mostrar todas las películas
        movies = API.get_movies()
        if movies:
            df_movies = []
            for movie in movies:
                df_movies.append({
                    "Título": movie.get("n.title", ""),
                    "Fecha de lanzamiento": movie.get("n.releaseDate", ""),
                    "Calificación": movie.get("n.rating", ""),
                })
            
            st.dataframe(df_movies)
        else:
            st.info("No hay películas disponibles.")
    
    elif operacion == "Crear película":
        st.subheader("Crear nueva película")
        title = st.text_input("Título")
        release_date = st.date_input("Fecha de lanzamiento")
        overview = st.text_area("Descripción")
        rating = st.slider("Calificación", 0.0, 10.0, 5.0, 0.1)
        poster = st.text_input("URL del poster")
        
        if st.button("Crear película"):
            try:
                # Corrigiendo el método para crear película
                result = API.create_movie(
                    title=title, 
                    releaseDate=release_date.strftime("%Y-%m-%d"), 
                    overview=overview, 
                    rating=rating, 
                    poster=poster
                )
                st.success(f"Película '{title}' creada correctamente.")
            except Exception as e:
                st.error(f"Error al crear la película: {str(e)}")
    
    elif operacion == "Actualizar película":
        st.subheader("Actualizar película existente")
        
        # Obtener películas para seleccionar
        movies = API.get_movies()
        movie_titles = [movie.get("n.title", "") for movie in movies]
        
        if movie_titles:
            selected_movie = st.selectbox("Seleccione la película a actualizar", movie_titles)
            
            # Mostrar datos actuales para actualizar
            current_movie = API.get_movie(selected_movie)
            
            if current_movie:
                # Campos para actualizar
                new_title = st.text_input("Nuevo título", value=current_movie.get("title", ""))
                new_release_date = st.date_input("Nueva fecha de lanzamiento")
                new_overview = st.text_area("Nueva descripción", value=current_movie.get("overview", ""))
                new_rating = st.slider("Nueva calificación", 0.0, 10.0, float(current_movie.get("rating", 5.0)), 0.1)
                new_poster = st.text_input("Nueva URL del poster", value=current_movie.get("poster", ""))
                
                if st.button("Actualizar película"):
                    try:
                        updates = {
                            "title": new_title,
                            "releaseDate": new_release_date.strftime("%Y-%m-%d"),
                            "overview": new_overview,
                            "rating": new_rating,
                            "poster": new_poster
                        }
                        # Corrigiendo el método para actualizar película
                        result = API.update_movie(selected_movie, updates)
                        st.success(f"Película '{selected_movie}' actualizada correctamente.")
                    except Exception as e:
                        st.error(f"Error al actualizar la película: {str(e)}")
            else:
                st.warning("No se pudo obtener la información de la película seleccionada.")
        else:
            st.info("No hay películas disponibles para actualizar.")
    
    elif operacion == "Eliminar película":
        st.subheader("Eliminar película")
        
        # Obtener películas para seleccionar
        movies = API.get_movies()
        movie_titles = [movie.get("n.title", "") for movie in movies]
        
        if movie_titles:
            selected_movie = st.selectbox("Seleccione la película a eliminar", movie_titles)
            
            if st.button("Eliminar película", help="Esta acción no se puede deshacer"):
                try:
                    API.delete_movie(selected_movie)
                    st.success(f"Película '{selected_movie}' eliminada correctamente.")
                except Exception as e:
                    st.error(f"Error al eliminar la película: {str(e)}")
        else:
            st.info("No hay películas disponibles para eliminar.")

def administrar_actores():
    st.subheader("Administración de Actores")
    
    # Seleccionar operación CRUD
    operacion = st.radio(
        "Seleccione la operación",
        ["Ver actores", "Crear actor", "Actualizar actor", "Eliminar actor"]
    )
    
    if operacion == "Ver actores":
        # Obtener y mostrar todos los actores
        actors = API.get_actors()
        if actors:
            actor_names = [actor.get("n.name", "") for actor in actors]
            st.write("Actores populares (en películas con rating ≥ 8.0):")
            for actor in actor_names:
                st.write(f"- {actor}")
        else:
            st.info("No hay actores disponibles.")
    
    elif operacion == "Crear actor":
        st.subheader("Crear nuevo actor")
        name = st.text_input("Nombre del actor")
        gender = st.number_input("Género del actor o actriz: (0 para masculino, 1 para femenino)", min_value=0, max_value=1)
        photo = st.text_input("URL de la foto del actor (si tiene)")
        date_of_birth = st.date_input("Fecha de nacimiento")
        description = st.text_area("Descripción del actor")
        
        if st.button("Crear actor"):
            try:
                # Corrigiendo el método para crear actor
                props = {
                    'name': name,
                    'gender':gender,
                    'photo':photo,
                    'date_of_birth':date_of_birth.strftime("%Y-%m-%d"),
                    'description':description
                    }
                result = API.create_actor(props)
                st.success(f"Actor '{name}' creado correctamente.")
            except Exception as e:
                st.error(f"Error al crear el actor: {str(e)}")
    
    elif operacion == "Actualizar actor":
        st.subheader("Actualizar actor existente")
        
        # Para este caso necesitaríamos un método para obtener todos los actores
        # Ya que get_actors() solo devuelve actores populares
        old_name = st.text_input("Nombre del actor a actualizar")
        new_name = st.text_input("Nuevo nombre del actor")
        
        if st.button("Actualizar actor"):
            try:
                # Corrigiendo el método para actualizar actor
                result = API.update_actor(name=old_name, new_name=new_name)
                st.success(f"Actor '{old_name}' actualizado a '{new_name}' correctamente.")
            except Exception as e:
                st.error(f"Error al actualizar el actor: {str(e)}")
    
    elif operacion == "Eliminar actor":
        st.subheader("Eliminar actor")
        
        # De nuevo, necesitaríamos un método para obtener todos los actores
        name = st.text_input("Nombre del actor a eliminar")
        
        if st.button("Eliminar actor", help="Esta acción no se puede deshacer"):
            try:
                API.delete_actor(name=name)
                st.success(f"Actor '{name}' eliminado correctamente.")
            except Exception as e:
                st.error(f"Error al eliminar el actor: {str(e)}")

def administrar_directores():
    st.subheader("Administración de Directores")
    
    # Seleccionar operación CRUD
    operacion = st.radio(
        "Seleccione la operación",
        ["Ver directores", "Crear director", "Actualizar director", "Eliminar director"]
    )
    
    if operacion == "Ver directores":
        # Obtener y mostrar todos los directores
        directors = API.get_directors()
        if directors:
            director_names = [director.get("n.name", "") for director in directors]
            st.write("Directores populares (que dirigieron películas con rating ≥ 8.0):")
            for director in director_names:
                st.write(f"- {director}")
        else:
            st.info("No hay directores disponibles.")
    
    elif operacion == "Crear director":
        st.subheader("Crear nuevo director")
        name = st.text_input("Nombre del director")
        gender = st.number_input("Género del director o directora: (0 para masculino, 1 para femenino)", min_value=0, max_value=1)
        photo = st.text_input("URL de la foto del director (si tiene)")
        date_of_birth = st.date_input("Fecha de nacimiento")
        description = st.text_area("Descripción del director")
        
        if st.button("Crear director"):
            try:
                # Corrigiendo el método para crear director
                props = {
                    'name': name,
                    'gender':gender,
                    'photo':photo,
                    'date_of_birth':date_of_birth.strftime("%Y-%m-%d"),
                    'description':description
                    }
                result = API.create_director(props)
                st.success(f"Director '{name}' creado correctamente.")
            except Exception as e:
                st.error(f"Error al crear el director: {str(e)}")
    
    elif operacion == "Actualizar director":
        st.subheader("Actualizar director existente")
        
        # Para este caso necesitaríamos un método para obtener todos los directores
        # Ya que get_directors() solo devuelve directores populares
        old_name = st.text_input("Nombre del director a actualizar")
        new_name = st.text_input("Nuevo nombre del director")
        
        if st.button("Actualizar director"):
            try:
                # Corrigiendo el método para actualizar director
                result = API.update_director(name=old_name, new_name=new_name)
                st.success(f"Director '{old_name}' actualizado a '{new_name}' correctamente.")
            except Exception as e:
                st.error(f"Error al actualizar el director: {str(e)}")
    
    elif operacion == "Eliminar director":
        st.subheader("Eliminar director")
        
        # De nuevo, necesitaríamos un método para obtener todos los directores
        name = st.text_input("Nombre del director a eliminar")
        
        if st.button("Eliminar director", help="Esta acción no se puede deshacer"):
            try:
                API.delete_director(name=name)
                st.success(f"Director '{name}' eliminado correctamente.")
            except Exception as e:
                st.error(f"Error al eliminar el director: {str(e)}")



def admin_reviews():
    st.header("Eliminar reviews")

    username = st.session_state.username

    reviews = API.get_user_ratings(username)


    for review in reviews:
        st.write(f"🎬 **{review['title']}** - Rating: {review['rating']}")
        if st.button(f"Eliminar review de {review['title']}"):
            try:
                API.delete_user_ratings(username, review['title'])
                st.success(f"Review de {review['title']} eliminada correctamente.")
            except Exception as e:
                st.error(f"Error al eliminar la review: {str(e)}")

