from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd
import streamlit as st

# 🔹 Carregar variáveis de ambiente
def load_env_variables():
    load_dotenv("config.env")
    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY")
    }

# 🔹 Verificar se todas as variáveis foram carregadas corretamente
def check_env_variables(env_vars):
    if not all(env_vars.values()):
        st.error("❌ Erro: Variáveis de ambiente ausentes!")
        st.stop()

def connect_to_database(env_vars) -> Client:
    return create_client(env_vars["supabase_url"], env_vars["supabase_key"])

# 🔹 Carregar dados da tabela
def load_data(supabase):
    response = supabase.table("tb_teste").select("*").execute()
    data = response.data if response.data else []
    if not data:
        st.warning("⚠ Nenhum dado encontrado na tabela `tb_teste`.")
    return pd.DataFrame(data)

# 🔹 Interface do Streamlit
def main():

    st.set_page_config(page_title="📊 Medições Projeta", layout="wide")
    st.title("📊 Dashboard - Banco de Dados Supabase") 

    # Carregar e validar credenciais do .env
    env_vars = load_env_variables()
    check_env_variables(env_vars)    

    # Conectar ao Supabase
    supabase = connect_to_database(env_vars)

    # 🔹 Exibir dados
    st.subheader("📊 Dados da Tabela `tb_teste`")
    df = load_data(supabase)
    st.dataframe(df)

# 🔹 Executar Streamlit
if __name__ == "__main__":
    main()