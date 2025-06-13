import streamlit as st
from conexao_supabase import supabase
import utils as utils
import pandas as pd

def aba_cadastro_cliente():
    
    st.write("")  

    # Buscar municípios existentes para popular o selectbox
    municipios = supabase.table("tb_municipios").select("id, municipio, uf").execute()

    lista_municipios = [f"{m['uf']} - {m['municipio']}" for m in municipios.data]
    mapa_municipios = {f"{m['uf']} - {m['municipio']}": m["id"] for m in municipios.data}

    with st.form(key='cadastro_cliente_form'):
        
        col1, col2 = st.columns(2)
        
        with col1:
            cliente = st.text_input(
                "Nome do Cliente*",
                placeholder="Insira o nome do cliente"
            ).strip().title()
            
        with col2:
            municipio_selecionado = st.selectbox(
                "Município*",
                [""] + sorted(lista_municipios)
            )

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

    df_clientes = supabase.table("tb_clientes").select("id, cliente, tb_municipios(municipio, uf), dt_cadastro").execute()
    if df_clientes.data: 
        df_clientes = pd.DataFrame(df_clientes.data)
        df_clientes["municipio"] = df_clientes["tb_municipios"].apply(lambda x: x["municipio"] if isinstance(x, dict) else None)
        df_clientes["uf"] = df_clientes["tb_municipios"].apply(lambda x: x["uf"] if isinstance(x, dict) else None)
        df_clientes.drop(columns=["tb_municipios"], inplace=True)
        df_clientes = df_clientes.rename(columns={"cliente": "Cliente", "municipio": "Município", "uf": "UF", "dt_cadastro": "Data de Cadastro"})
        df_clientes["Data de Cadastro"] = pd.to_datetime(df_clientes["Data de Cadastro"], format="mixed")
        df_clientes["Data de Cadastro"] = df_clientes["Data de Cadastro"].dt.strftime("%Y-%m-%d %H:%M:%S")
        df_clientes = df_clientes[["Cliente", "Município", "UF", "Data de Cadastro"]]
        utils.formatar_data_hora_brasil(df_clientes, "Data de Cadastro") 
        
        st.write("Lista de Clientes Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = utils.altura_tabela(df_clientes, 8)        
        st.dataframe(df_clientes, use_container_width=True, height=altura_final)                
    else:
        st.warning("Nenhum cliente cadastrado até o momento.")    