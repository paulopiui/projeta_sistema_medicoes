import streamlit as st
import pandas as pd
from utils import utils
from conexao_supabase import supabase
from abas_cadastros import cadastro_cliente, cadastro_municipio, cadastro_contrato

utils.config_pagina()
utils.validar_login()
utils.validar_nivel_acesso("gerente")
                               
col1, col2, col3 = st.columns(3)

with col2:
    # Título da Aplicação
    st.title("Cadastro de Dados")

# Seção de Abas
aba_cadastro_municipio, aba_cadastro_cliente, aba_cadastro_contrato, aba_cadastro_itens_contrato, aba_cadastro_aditivo, aba_cadastro_item = st.tabs(
    ["Município", "Cliente", "Contrato", "Itens do Contrato", "Aditivo","Item Medição"]
)

with aba_cadastro_municipio:
    cadastro_municipio.aba_cadastro_municipio()       

with aba_cadastro_cliente:  
    cadastro_cliente.aba_cadastro_cliente()   

with aba_cadastro_contrato:  
    cadastro_contrato.aba_cadastro_contrato()     

with aba_cadastro_itens_contrato:
    cadastro_contrato.aba_cadastro_contrato()
    


with aba_cadastro_aditivo:

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        # Carregar clientes
        clientes = supabase.table("tb_clientes").select("id, cliente").execute()
        mapa_clientes = {}
        for c in clientes.data:
            cliente_nome = c["cliente"].strip()
            if cliente_nome not in mapa_clientes:
                mapa_clientes[cliente_nome] = c["id"]
        cliente_selecionado = st.selectbox("Cliente*", key="cliente_aditivo",options=sorted(mapa_clientes.keys()))

    with col2:
        
        cliente_id = mapa_clientes.get(cliente_selecionado)
        
        # Carregar contratos
        contratos = (
            supabase.table("tb_contratos")
            .select("id, numero_contrato_ata")
            .eq("id_cliente",cliente_id)
            .execute()
            )
        
        mapa_contratos = {}
        for c in contratos.data:
            contrato_nome = c["numero_contrato_ata"].strip()
            if contrato_nome not in mapa_contratos:
                mapa_contratos[contrato_nome] = c["id"]      
        
        contrato_selecionado = st.selectbox(
           "Contrato*", key="contrato_aditivo", options=sorted(mapa_contratos.keys())
        )

with aba_cadastro_item:
    
    st.write("")
    
    cadastro_realizado = False
    
    with st.form(key="cadastro_item_form"):
        
        col1, col2 = st.columns(2)
        with col1:

            nome_item = st.text_input("Nome do Item*").strip().title()

        with col2:
            
            grupos = supabase.table("tb_grupos_itens").select("id, grupo").execute().data
            
            mapa_grupos = {g["grupo"]: g["id"] for g in grupos}
            
            grupo_item = st.selectbox("Grupo do Item*", options=[""] + sorted(mapa_grupos.keys()))      
            
            id_grupo = mapa_grupos.get(grupo_item)

        submit_button=st.form_submit_button("Cadastrar Item")

        if submit_button:

            if nome_item:
                # Verificar duplicidade
                item_existe = (
                    supabase.table("tb_itens")
                    .select("id")
                    .eq("item", nome_item)
                    .execute()
                )

                if item_existe.data:
                    st.warning("⚠️  ATENÇÃO: Já existe um item com este nome.")
                else:               

                    try:
                        data = {"item": nome_item, "id_grupo":id_grupo}
                        
                        with st.spinner("Cadastrando item..."):
                            supabase.table("tb_itens").insert(data).execute() 
                        
                        cadastro_realizado = True                                                                                 
                                                        
                    except Exception as e:
                        st.error("Erro ao cadastrar item.")
                        st.write(f"Detalhes técnicos: {e}")
    
    if cadastro_realizado:
        show_success_dialog()
        
    consulta = supabase.table("tb_itens").select("item, tb_grupos_itens(grupo), created_at").execute()
    
    if consulta.data:
        df_itens = pd.DataFrame(consulta.data)
        df_itens = df_itens.rename(columns={"item": "Item", "created_at": "Criado em", "tb_grupos_itens": "Grupo"})
        
        df_itens["Grupo"] = df_itens["Grupo"].apply(lambda x: x["grupo"].strip() if isinstance(x, dict) and "grupo" in x else "")

        utils.formatar_data_hora_brasil(df_itens, "Criado em")
        st.write("Lista de Itens Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = utils.altura_tabela(df_itens, 8)        
        st.dataframe(df_itens, use_container_width=True, height=altura_final)    