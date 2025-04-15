import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase

utils.config_pagina_centralizada()
utils.exibir_cabecalho_centralizado()

# Título da Aplicação
st.title("Cadastro de Medições")