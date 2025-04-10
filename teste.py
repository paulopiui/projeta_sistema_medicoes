import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase


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

        if "uf_selecionado" not in st.session_state:
            st.session_state.uf_selecionado = uf_opcoes[0]        

        uf_selecionado = st.selectbox("UF",uf_opcoes)  

        if uf_selecionado != st.session_state.uf_selecionado:
                st.session_state.uf_selecionado = uf_selecionado
                st.session_state.municipio_selecionado = "Selecione um município"        

        if uf_selecionado != "Todos":
            municipios_filtrado = df_municipios[df_municipios["uf"] == uf_selecionado].copy()                  
        else:
            municipios_filtrado = df_municipios.copy()
        
        municipios_opcoes = sorted(municipios_filtrado["municipio"].dropna().unique().tolist())            

        # **Salvar município no session_state para evitar seleção incorreta**
        if "municipio_selecionado" not in st.session_state:
            st.session_state.municipio_selecionado = "Selecione um município"

        municipio_selecionado = st.selectbox("Município", ["Selecione um município"] + municipios_opcoes, 
                                                key="municipio_selectbox",
                                                index=0 if st.session_state.municipio_selecionado not in municipios_opcoes else municipios_opcoes.index(st.session_state.municipio_selecionado) + 1)

    
    else:
        st.warning("Nenhum município encontrado.")

    st.write(f"Seleção de UF: {uf_selecionado}")
    
    st.dataframe(municipios_filtrado)        

    st.form_submit_button("Cadastrar")