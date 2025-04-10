from supabase import create_client, Client
from dotenv import load_dotenv
import os

# 🔹 Carregar variáveis de ambiente
def load_env_variables():
    load_dotenv("config/config.env")
    return {
        "supabase_url": os.getenv("SUPABASE_URL"),
        "supabase_key": os.getenv("SUPABASE_KEY")
    }

# 🔹 Conectar ao Supabase
def connect_to_supabase(env_vars) -> Client:
    return create_client(env_vars["supabase_url"], env_vars["supabase_key"])

# Carregar variáveis de ambiente e conectar ao Supabase
env_vars = load_env_variables()
supabase = connect_to_supabase(env_vars)