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
    # Formulário de Cadastro
    with st.form(key='cadastro_cliente_form'):
        cliente = st.text_input("Cliente*").title() # title é usado para que o texto tenha a primeira maiuscula e demais minusculas
        
        query = (
            supabase.table("tb_municipios")
            .select("municipio, uf")                        
            .execute()
        )

        data = query.data if query.data else []
        df_municipios = pd.DataFrame(data)          
        
        if not df_municipios.empty:

            df_municipios["uf"] = df_municipios["uf"].astype(str).str.strip()
            df_municipios["municipio"] = df_municipios["municipio"].astype(str).str.strip()

            uf_opcoes = df_municipios["uf"].dropna().unique().tolist() 
            uf_opcoes.insert(0, "Todos")

            uf_selecionado = st.selectbox("UF",uf_opcoes)  

            if uf_selecionado != "Todos":
                municipios_filtrado = df_municipios[df_municipios["uf"] == uf_selecionado].copy()                  
            else:
                municipios_filtrado = df_municipios.copy()
            
            municipios_opcoes = sorted(municipios_filtrado["municipio"].dropna().unique().tolist())            

            municipio_selecionado = st. selectbox("Município", municipios_opcoes)
        
        else:
            st.warning("Nenhum município encontrado.")

        st.write(f"Seleção de UF: {uf_selecionado}")
        
        st.dataframe(municipios_filtrado)        

        st.form_submit_button("Cadastrar")
   
with aba_cadastro_contrato:
    st.write("")

with aba_cadastro_item_medido:
    st.write("")

