import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import os

# 🔹 Carregar variáveis de ambiente
def load_env_variables():
    load_dotenv("config/config.env")
    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY")
    }

# 🔹 Conectar ao Supabase com sessão autenticada, se existir
def connect_to_supabase(env_vars) -> Client:
    client = create_client(env_vars["supabase_url"], env_vars["supabase_key"])

    # Verifica se a sessão foi armazenada após o login
    if "session" in st.session_state:
        session = st.session_state["session"]
        access_token = session.access_token
        refresh_token = session.refresh_token
        if access_token and refresh_token:
            client.auth.set_session(access_token, refresh_token)

    return client

# Carregar variáveis de ambiente e conectar ao Supabase
env_vars = load_env_variables()
supabase = connect_to_supabase(env_vars)
