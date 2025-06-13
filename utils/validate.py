import streamlit as st
from utils.conexao_supabase import supabase

def validar_login():
    if "auth_user" not in st.session_state or st.session_state["auth_user"] is None:
        st.warning("⚠️ Acesso restrito. Faça login primeiro.")
        st.stop()

def validar_nivel_acesso(nivel_acesso_necessario):
    
    NIVEIS_ACESSO = {
        "usuario": 1,
        "gerente": 2,
        "administrador": 3
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