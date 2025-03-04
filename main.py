import pandas as pd
import streamlit as st
import API
import Menu

def main():
    st.title("Sistema de Recomendación de Películas")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Aqui se manejan las pantallas por si esta o no con sesion iniciada
    if not st.session_state.logged_in:
        login_page()
    else:
        menu_principal()

def login_page():
    st.header("Bienvenido")

    opcion = st.radio("Seleccione una opción", ["Iniciar Sesión", "Registrarse"])

    if opcion=="Iniciar Sesión":
        st.subheader("Login")
        username_login = st.text_input("Usuario", key="login_user")
        password_login = st.text_input("Contraseña", type="password", key="login_password")
        # Se actualizan los estados de login
        if st.button("Iniciar Sesion"):
            st.session_state.logged_in = True
            st.session_state.username = username_login

    elif opcion=="Registrarse":
        st.subheader("Registro")
        username_registro = st.text_input("Nuevo Usuario", key="registro_user")
        password_registro = st.text_input("Contraseña", type="password", key="registro_password")

        if st.button("Registrarse"):
            user_props={
                    "username": username_registro,
                    "password": password_registro
            }
            API.create_User(user_props)
            st.success("Usuario registrado correctamente, por favor inicie sesión")

def menu_principal():
    menu = st.sidebar.radio(
        "Menú", 
        [
            "Perfil", 
            "Mis Preferencias", 
            "Recomendaciones"
        ]
    )
    
    if menu == "Perfil":
        st.header(f"Bienvenido, {st.session_state.username}")
        st.subheader("Verificando usuario en la base de datos...")
        if API.check_user_exists(st.session_state.username):
            st.success("✅ El usuario existe en la base de datos.")
        else:
            st.error("❌ El usuario NO existe. Revisa la creación del usuario.")

    
    elif menu == "Mis Preferencias":
        Menu.preferencias_usuario()
    
    elif menu == "Recomendaciones":
        Menu.recomendar_peliculas()

main()
