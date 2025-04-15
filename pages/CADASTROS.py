import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase

utils.config_pagina_centralizada()
utils.exibir_cabecalho_centralizado()

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
        # strip é usado para remover espaços em branco no início e no final do texto
        municipio = st.text_input("Município*").title().strip() # title é usado para que o texto tenha a primeira maiuscula e demais minusculas
        uf = st.text_input("UF*", max_chars=2).upper().strip() # upper é usado para que o texto tenha todas as letras maiusculas
        submit_button = st.form_submit_button("Cadastrar")

        if submit_button:
            if len(uf) == 2 and len(municipio) > 2:
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
                        with st.spinner("Cadastrando..."):
                            response = supabase.table("tb_municipios").insert(data).execute()
                        st.success("Cadastro realizado com sucesso!")
                    except Exception as e:
                        st.error("Erro inesperado ao tentar cadastrar. Tente novamente mais tarde.")
                        st.write(f"Detalhes técnicos (debug): {e}")

            else:
                st.error("Por favor, preencha todos os campos corretamente.")

with aba_cadastro_cliente:
    st.write("")

    # Buscar municípios existentes para popular o selectbox
    municipios = supabase.table("tb_municipios").select("id, municipio, uf").execute()

    lista_municipios = [f"{m['uf']} - {m['municipio']}" for m in municipios.data]
    mapa_municipios = {f"{m['uf']} - {m['municipio']}": m["id"] for m in municipios.data}

    with st.form(key='cadastro_cliente_form'):
        cliente = st.text_input("Nome do Cliente*").strip().title()
        municipio_selecionado = st.selectbox("Município*", sorted(lista_municipios))
        submit_button_cliente = st.form_submit_button("Cadastrar")

        if submit_button_cliente:
            id_municipio = mapa_municipios[municipio_selecionado]

            # Verifica se cliente já está cadastrado no mesmo município
            cliente_existe = (supabase.table("tb_clientes")
                .select("*")
                .eq("cliente", cliente)
                .eq("id_municipio", id_municipio)
                .execute())

            if cliente_existe.data:
                st.warning("⚠️  ATENÇÃO: Este cliente já está cadastrado para este município.")
            else:
                dados = {"cliente": cliente, "id_municipio": id_municipio}
                try:
                    with st.spinner("Cadastrando cliente..."):
                        supabase.table("tb_clientes").insert(dados).execute()
                    st.success("Cliente cadastrado com sucesso!")
                except Exception as e:
                    st.error("Erro ao cadastrar cliente.")
                    st.write(f"Detalhes técnicos (debug): {e}")

  
with aba_cadastro_contrato:
    st.write("")

with aba_cadastro_item_medido:
    st.write("")