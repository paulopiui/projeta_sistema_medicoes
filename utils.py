import streamlit as st
from conexao_supabase import supabase

def exibir_cabecalho():

    """Exibe o cabeçalho padrão em todas as páginas."""
    col1, col2, col3 = st.columns([0.1, 0.2 ,0.6])

    with col1:
        # Exibir logo no topo
        st.image("img/logo.png", width=300,  use_container_width=True)  # Substitua pelo caminho da sua logo

    with col3:
        #st.markdown('<h2 class="custom-subheader">Gerenciamento de Contratos</h2>', unsafe_allow_html=True)
        st.title("Gerenciamento de Contratos")

    st.divider()

def config_pagina():
    # Configuração da página
    st.set_page_config(        
        page_icon="img/favicon2.png",
        layout="wide"
    )

def exibir_cabecalho_centralizado():
        
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        st.image("img/logo.png", width=350)  # Substitua pelo caminho da sua logo

    st.divider()

def config_pagina_centralizada():
    
    # Configuração da página
    st.set_page_config(        
        page_icon="img/favicon2.png",
        layout="centered"
    )
    
def validar_login():
    if "auth_user" not in st.session_state or st.session_state["auth_user"] is None:
        st.warning("⚠️ Acesso restrito. Faça login primeiro.")
        st.stop()

def validar_nivel_acesso(nivel_acesso_necessario):
    
    NIVEIS_ACESSO = {
        "usuario": 1,
        "administrador": 2
    }
        
    user_id = st.session_state["auth_user"].id
    response = supabase.table("user_perfil").select("nivel_acesso").eq("id", user_id).single().execute()

    if not response.data:
        st.warning("⚠️ Usuário sem perfil definido.")
        st.stop()

    nivel_acesso_usuario = response.data["nivel_acesso"]
    
    if NIVEIS_ACESSO.get(nivel_acesso_usuario, 0) < NIVEIS_ACESSO.get(nivel_acesso_necessario, 0):
        st.warning("⚠️ Você não tem permissão para acessar esta página.")
        st.stop()

    