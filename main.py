import pandas as pd
import streamlit as st
import neo4j_functions

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
