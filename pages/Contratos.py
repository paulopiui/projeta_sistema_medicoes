import pandas as pd
import streamlit as st
import utils.utils as utils
from utils.conexao_supabase import supabase

# Configuração da Página e Cabeçalho
utils.config_pagina()
utils.exibir_cabecalho()
utils.validar_login()
utils.validar_nivel_acesso("usuario")

# Carregar contratos
df_contratos = utils.carregar_contratos()

st.subheader("Medições por Contrato")   

col1, col2, col3, col4, col5 = st.columns([0.25, 0.15, 0.25, 0.20, 0.15])

with col1:
    cliente_opcoes = df_contratos["cliente"].dropna().unique().tolist()
    cliente_selecionado = st.selectbox("Cliente", [""] + cliente_opcoes)

with col2:

    if cliente_selecionado != "":
        df_filtrado_clientes = df_contratos[df_contratos["cliente"] == cliente_selecionado]
        contrato_opcoes = df_filtrado_clientes["numero_contrato_ata"].dropna().unique().tolist()
    else:
        contrato_opcoes = df_contratos["numero_contrato_ata"].dropna().unique().tolist()
    
    contrato_selecionado = st.selectbox("Contrato", [""] + contrato_opcoes)

with col5:
    if st.button("Cadastrar Medição", key="cadastrar_medicao"):
        
        if contrato_selecionado == "":
            utils.dialogo_alerta("Selecione um contrato antes de cadastrar a medição.")            
        else:
            utils.cadastrar_medicao(contrato_selecionado)


# Aplicação dos filtros
df_filtrado = df_contratos.copy()

st.write("")
st.write("")

if cliente_selecionado != "":
    df_filtrado = df_filtrado[df_filtrado["cliente"] == cliente_selecionado]
else:
    df_filtrado = df_filtrado[df_filtrado["cliente"].isnull()]

if contrato_selecionado:
    df_filtrado = df_filtrado[df_filtrado["numero_contrato_ata"] == contrato_selecionado]    

    col1, col2, col3, col4 = st.columns([0.3, 0.25, 0.20, 0.20])

    with col1:

        if df_filtrado.empty:
            st.info("Nenhum contrato encontrado.")
            st.stop()

        cliente = df_filtrado.iloc[0]["cliente"]
        st.subheader(f"{cliente}")

    with col2:    
        ano = df_filtrado.iloc[0]["ano"]
        st.write(f"Ano Contrato: {ano}")

    with col3:
        tipo = df_filtrado.iloc[0]["tipo"]
        st.write(f"Tipo: {tipo}")
    
    with col4:
        status = df_filtrado.iloc[0]["status"]
        st.write(f"Status: {status}")    

    id_contrato = df_filtrado.iloc[0]["id"]
    query = (
        supabase
        .table("tb_medicoes")
        .select("id, id_contrato, numero_medicao, mes_referencia, valor_medido, status")
        .eq("id_contrato", id_contrato)
        .execute()
    )
    
    data = query.data if query.data else []
    df_medicoes = pd.DataFrame(data)        

    query_itens = (
        supabase
        .table("tb_itens_medidos")
        .select("id_medicao, id_item, quantidade_medida, unidade_medida, valor_medido, valor_unitario")
        .execute()
    )
    data_itens = query_itens.data if query_itens.data else []
    df_itens_medidos = pd.DataFrame(data_itens)    

    if not df_medicoes.empty:        
        
        for _, row in df_medicoes.iterrows():
            mes_ano = row["mes_referencia"][:7] if "mes_referencia" in row else "N/A"
            id_medicao = row["id"]
            titulo_expander = f'**Medição** {row["numero_medicao"]} - **Mês:** {mes_ano} - **Valor:** R$ {row["valor_medido"]:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")

            with st.expander(titulo_expander):
                
                if df_itens_medidos.empty:
                    st.info("Sem itens medidos")
                    st.stop()
                else:
                    df_filtrado_itens = df_itens_medidos[df_itens_medidos["id_medicao"] == id_medicao]

                    df_itens_exibicao = df_filtrado_itens[["id_item", "valor_unitario", "quantidade_medida", "unidade_medida", "valor_medido"]]  # Selecionando colunas específicas

                    df_itens_exibicao = df_itens_exibicao.rename(columns={
                            "id_item": "Item",
                            "valor_unitario": "Valor Unitário",
                            "quantidade_medida": "Quantidade",
                            "unidade_medida": "Unidade",
                            "valor_medido": "Valor (R$)"
                    })

    
    else:
        st.warning("Sem medições")  
