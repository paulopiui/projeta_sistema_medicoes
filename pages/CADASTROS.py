import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase

utils.config_pagina_centralizada()
utils.exibir_cabecalho_centralizado()

def on_change():
    st.session_state.tipologia_opcoes = lista_opcoes_tipologia(st.session_state.area_atuacao_cad)

# Título da Aplicação
st.title("Cadastro de Dados")

# Seção de Abas
aba_cadastro_municipio,aba_cadastro_cliente, aba_cadastro_contrato, aba_cadastro_item_medido = st.tabs(
    ["Município", "Cliente", "Contrato", "Item"]
)

with aba_cadastro_municipio:

    st.write("")

    # Formulário de Cadastro
    with st.form(key='cadastro_municipio_form'):
        municipio = st.text_input("Município*").title() # title é usado para que o texto tenha a primeira maiuscula e demais minusculas
        uf = st.text_input("UF*", max_chars=2).upper()
        submit_button = st.form_submit_button("Cadastrar")

        if submit_button and len(uf) == 2 and len(municipio) > 2:
            existing_municipio = (
                supabase.table("tb_municipios")
                .select("municipio, uf")
                .eq("municipio", municipio)
                .eq("uf", uf)
                .execute()
            )

            if existing_municipio.data:
                st.warning("⚠️  ATENÇÃO: Este município já está cadastrado.")
            else:
                data = {"municipio": municipio, "uf": uf}
                try:
                    response = supabase.table("tb_municipios").insert(data).execute()
                    st.success("Cadastro realizado com sucesso!")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {str(e)}")

        else:
            st.error("Por favor, preencha todos os campos corretamente.")

with aba_cadastro_cliente:
    st.write("")

 
  
with aba_cadastro_contrato:
    st.write("")

with aba_cadastro_item_medido:
    st.write("")