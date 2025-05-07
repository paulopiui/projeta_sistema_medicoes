import streamlit as st
import utils
import pandas as pd

utils.config_pagina()
utils.exibir_cabecalho()
utils.validar_login()
utils.validar_nivel_acesso("gerente")
    
st.title("✏️ Editar Medição")