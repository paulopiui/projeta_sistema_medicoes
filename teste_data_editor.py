import streamlit as st
import pandas as pd
from conexao_supabase import supabase

@st.cache_data
def carregar_dados():
    """Busca os dados do banco"""
    response = supabase.table("tb_municipios").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=["id, uf", "municipio"])

st.subheader("Dados Cadastrados")

dados = carregar_dados()

# Campo de pesquisa por nome ou email
filtro = st.text_input("Filtrar por Município ou UF").lower()
dados_filtrados = dados[dados["municipio"].str.lower().str.contains(filtro) | dados["uf"].str.lower().str.contains(filtro)]

# Definir número de linhas por página
linhas_por_pagina = 10
total_linhas = len(dados)

# Criar controle de página
pagina = st.number_input("Página", min_value=1, max_value=(total_linhas // linhas_por_pagina) + 1, step=1)
inicio = (pagina - 1) * linhas_por_pagina
fim = inicio + linhas_por_pagina

# Exibir apenas os dados da página atual
dados_paginados = dados_filtrados.iloc[inicio:fim]

# Editor de Dados com paginação
dados_editados = st.data_editor(dados_paginados, num_rows="fixed")

if st.button("Salvar Alterações"):
    alteracoes = dados_editados.compare(dados.iloc[inicio:fim])
    if not alteracoes.empty:
        for index in alteracoes.index:
            id_municipio = dados_paginados.loc[index, "id_municipio"]
            novos_dados = dados_editados.loc[index].to_dict()
            supabase.table("tb_municipios").update(novos_dados).eq("id_municipio", id_municipio).execute()
        st.success("Alterações salvas com sucesso!")
        st.experimental_rerun()
    else:
        st.info("Nenhuma alteração detectada.")
