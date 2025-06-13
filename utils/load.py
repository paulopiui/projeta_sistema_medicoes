import streamlit as st
from utils.conexao_supabase import supabase
import pandas as pd

# Função para carregar contratos do Supabase
def carregar_contratos():
    query = (
        supabase
        .table("tb_contratos")
        .select("id, numero_contrato_ata, ano, tb_clientes(id, cliente), tipo, status")
        .execute()
    )
    
    data = query.data if query.data else []
    df = pd.DataFrame(data)

    if not df.empty:
        df["cliente"] = df["tb_clientes"].apply(lambda x: x["cliente"] if isinstance(x, dict) else None)
        df.drop(columns=["tb_clientes"], inplace=True)  # Remover coluna aninhada
    
    return df

def carregar_medicoes(id_contrato):
    query = (
        supabase
        .table("tb_medicoes")
        .select("id, id_contrato, numero_medicao, mes_referencia, valor_medido, status")
        .eq("id_contrato", id_contrato)
        .execute()
    )
        
    data = query.data if query.data else []
    df_medicoes = pd.DataFrame(data)         

    return df_medicoes

def carregar_itens_medidos():
    query = (
        supabase
        .table("tb_itens_medidos")
        .select("id, id_medicao, id_item, quantidade_medida, unidade_medida, valor_medido, valor_unitario")        
        .execute()
    )
    
    data = query.data if query.data else []
    df_itens = pd.DataFrame(data)         

    return df_itens