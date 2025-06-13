import streamlit as st
from utils.conexao_supabase import supabase
from utils import format
import pandas as pd

def aba_cadastro_municipio():    
    
    st.write("")

    # Formulário de Cadastro
    with st.form(key='cadastro_municipio_form'):
        
        col1, col2 = st.columns(2)
        
        with col1:
            uf = st.text_input(
                "UF*",
                max_chars=2,
                placeholder="Informe uma UF",
                help="Campo obrigatório. Deve conter 2 letras maiúsculas"
            ).upper().strip() # upper é usado para que o texto tenha todas as letras maiusculas            
        
        with col2:
            municipio = st.text_input(
                "Município*",
                placeholder="Informe um município",
                help="Campo obrigatório. Deve conter pelo menos 3 caracteres"
            ).title().strip() # title é usado para que o texto tenha a primeira maiuscula e demais minusculas
        
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

    tabela_municipios = supabase.table("tb_municipios").select("id, municipio, uf, dt_cadastro").execute()
    if tabela_municipios.data:
        df_municipios = pd.DataFrame(tabela_municipios.data)
        df_municipios = df_municipios.rename(columns={"municipio": "Município", "uf": "UF", "dt_cadastro": "Data de Cadastro"})
        df_municipios["Data de Cadastro"] = pd.to_datetime(df_municipios["Data de Cadastro"], format="mixed")
        df_municipios["Data de Cadastro"] = df_municipios["Data de Cadastro"].dt.strftime("%Y-%m-%d %H:%M:%S")
        format.formatar_data_hora_brasil(df_municipios, "Data de Cadastro")        
        df_municipios = df_municipios[["Município", "UF", "Data de Cadastro"]]
        st.write("Lista de Municípios Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = format.altura_tabela(df_municipios, 8)        
        st.dataframe(df_municipios, use_container_width=True, height=altura_final)
        
    else:
        st.warning("Nenhum município cadastrado até o momento.")