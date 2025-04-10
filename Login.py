import streamlit as st
from conexao_supabase import supabase
import time

# Configuração da página
st.set_page_config(
    page_title="Gerenciador de Contratos",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="img/favicon2.png"
    )

try:
    st.image("img/logo.png", width=150,  use_container_width=True)
except:
    st.write("Logo Projeta")

# Criar sessão para armazenar usuário
if "user" not in st.session_state:
    st.session_state["user"] = None

# Evita consultas automáticas ao iniciar
if st.session_state["user"] is None:
    supabase.auth.sign_out()  # Garante que não há sessão ativa

# Se o usuário não estiver logado, exibir formulário de login
if "user" in st.session_state and st.session_state["user"] is not None:

    st.switch_page("VISUALIZAR")

else:

    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        st.markdown('<p style="text-align: center; font-size: 30px; font-weight: bold;">Gerenciador de Contratos</p>', unsafe_allow_html=True)

        # Campos de email e senha
        email = st.text_input("Email", placeholder="Digite seu email")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

        # Botão de login
        if st.button("Entrar"):
            try:
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})

                # 🔹 O Supabase retorna um objeto do tipo User, então pegamos corretamente o email
                if response.user:
                    st.session_state["user"] = response.user  # Armazena o objeto User corretamente
                    st.success(f"✅ Bem-vindo, {st.session_state['user'].email}!")  # Acessa o email corretamente
                    time.sleep(1)
                    st.switch_page("VISUALIZAR.py")                    
            except Exception as e:
                st.error(f"❌ Erro no login: {e}")