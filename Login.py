import streamlit as st
import utils
from conexao_supabase import supabase
from unidecode import unidecode

utils.config_pagina_centralizada()
utils.exibir_cabecalho_centralizado()

# Seção de Abas
aba_login, aba_cadastro = st.tabs(["LOGIN", "CADASTRO"])

# === Login ===
with aba_login:
    st.subheader("🔐 Login")
    
    if "auth_user" in st.session_state and st.session_state.auth_user is not None:
        st.info("Você já está logado como: " + st.session_state.auth_user.email)
        
        if st.button("Sair"):
            
            try:
                supabase.auth.sign_out()
                st.session_state.auth_user = None                
                st.info("Logout realizado!") 
                st.rerun()  # Atualiza a página para refletir o estado de logout
            except Exception as e:
                st.error("Erro ao fazer logout: " + str(e))
    else:
        st.session_state.auth_user = None

        email = st.text_input("E-mail", key="email_login")
        senha = st.text_input("Senha", type="password", key="senha_login")

        if st.button("Entrar"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": senha
                })
                
                st.session_state.auth_user = res.user                
                st.session_state["session"] = res.session                
                st.success("Login realizado!")   
                st.rerun()  # Atualiza a página para refletir o estado de login                                              
            except Exception as e:
                
                if "Invalid login credentials" in str(e):
                    st.warning("⚠️  Atenção: E-mail ou senha inválidos.")
                else:
                    st.error("Erro ao fazer login: " + str(e))


# === Cadastro ===
with aba_cadastro:
    st.subheader("📝 Cadastro")    
    
    utils.validar_login()        
    utils.validar_nivel_acesso("administrador")
        
    nome = st.text_input("Nome completo", key="nome_cadastro")
    nivel_acesso = unidecode(st.selectbox("Nível de Acesso", ["Usuário", "Administrador"], key="nivel_acesso_cadastro")).lower()
    email = st.text_input("E-mail", key="email_cadastro")
    senha = st.text_input("Senha", type="password", key="senha_cadastro")
    st.info("ℹ️  A senha deve possuir no míninmo 6 caracteres, letras e números.")
    
    if st.button("Cadastrar"):
        try:            
            res = supabase.auth.sign_up({    
                "nome": nome,                                                     
                "email": email,
                "password": senha
            })        
            
            if res.user:                
            
                user_id = res.user.id                
                
                # Exemplo de dados adicionais
                dados_perfil = {   
                    "id": user_id,                                                      
                    "nivel_acesso": nivel_acesso
                }

                supabase.table("user_perfil").insert(dados_perfil).execute()
                
                st.success("Cadastro realizado! Verifique seu e-mail.")
                
        except Exception as e:
            if "Password" in str(e):
                st.warning("⚠️  Atenção: A senha digitada não atende aos requisitos exigidos")
            elif "User already registered" in str(e):
                st.warning("⚠️  Atenção: O e-mail informado já está cadastrado.")
            else:
                st.error("Erro ao cadastrar: " + str(e))