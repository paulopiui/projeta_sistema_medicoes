import streamlit as st
import utils

utils.config_pagina()

# Função para carregar o CSS externo
def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Carregar CSS externo
load_css("style.css")

initial_sidebar_state="expanded"

utils.exibir_cabecalho()