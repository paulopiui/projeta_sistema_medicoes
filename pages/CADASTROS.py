import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase

utils.config_pagina_centralizada()
utils.exibir_cabecalho_centralizado()

# Título da Aplicação
st.title("Cadastro de Dados")

# Seção de Abas
aba_cadastro_municipio,aba_cadastro_cliente, aba_cadastro_contrato, aba_cadastro_item = st.tabs(
    ["Município", "Cliente", "Contrato", "Item Medição"]
)

with aba_cadastro_municipio:

    st.write("")

    # Formulário de Cadastro
    with st.form(key='cadastro_municipio_form'):
        # strip é usado para remover espaços em branco no início e no final do texto
        municipio = st.text_input("Município*", placeholder="Informe um município").title().strip() # title é usado para que o texto tenha a primeira maiuscula e demais minusculas
        uf = st.text_input("UF*", max_chars=2, placeholder="Informe uma UF").upper().strip() # upper é usado para que o texto tenha todas as letras maiusculas
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

with aba_cadastro_cliente:
    st.write("")

    # Buscar municípios existentes para popular o selectbox
    municipios = supabase.table("tb_municipios").select("id, municipio, uf").execute()

    lista_municipios = [f"{m['uf']} - {m['municipio']}" for m in municipios.data]
    mapa_municipios = {f"{m['uf']} - {m['municipio']}": m["id"] for m in municipios.data}

    with st.form(key='cadastro_cliente_form'):
        cliente = st.text_input("Nome do Cliente*", placeholder="Insira o nome do cliente").strip().title()
        
        municipio_selecionado = st.selectbox(
            "Município*",
            [""] + sorted(lista_municipios))
        
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

with aba_cadastro_contrato:    

    col1, col2 = st.columns(2)

    with col1:
        # Carregar clientes
        clientes = supabase.table("tb_clientes").select("id, cliente").execute()
        mapa_clientes = {c["cliente"]: c["id"] for c in clientes.data}
        cliente_selecionado = st.selectbox("Cliente*", sorted(mapa_clientes.keys()))

    with col2:
        # Carregar empresas
        empresas = supabase.table("tb_empresas").select("id, empresa_grupo_projeta").execute()
        mapa_empresas = {e["empresa_grupo_projeta"]: e["id"] for e in empresas.data}
        empresa_selecionada = st.selectbox("Empresa Grupo Projeta*", sorted(mapa_empresas.keys()))

    with st.form(key="cadastro_contrato_form"):

        col1, col2, col3 = st.columns(3)

        with col1:
            numero_contrato = st.text_input("Número do Contrato/Ata*").strip().upper()
        
        with col2:        
            ano = st.number_input("Ano*", min_value=2000, max_value=2100, step=1)
        
        with col3:
            tipos_contrato = supabase.rpc("get_enum_values", {
                "table_name": "tb_contratos",
                "column_name": "tipo"
            }).execute()

        
            lista_tipos = tipos_contrato.data or []
        
            tipo = st.selectbox("Tipo de Contrato*", lista_tipos)  # Ajuste conforme enum

        col4, col5, col6 = st.columns(3)                  
        
        with col4:
            dt_assinatura = st.date_input("Data da Assinatura*")
        
        with col5:
            prazo_dias = st.number_input("Prazo (em dias)*", min_value=1)
        
        with col6:
            valor_inicial = st.number_input("Valor Inicial*", min_value=0.0, format="%.2f")
        
        submit_button_contrato = st.form_submit_button("Cadastrar Contrato")

        if submit_button_contrato:
            id_cliente = mapa_clientes[cliente_selecionado]
            id_empresa = mapa_empresas[empresa_selecionada]

            # Verificar duplicidade
            contrato_existe = (
                supabase.table("tb_contratos")
                .select("id")
                .eq("numero_contrato_ata", numero_contrato)
                .execute()
            )

            if contrato_existe.data:
                st.warning("⚠️  ATENÇÃO: Já existe um contrato com este número.")
            else:
                dados_contrato = {
                    "id_cliente": id_cliente,
                    "id_empresa_grupo_projeta": id_empresa,
                    "numero_contrato_ata": numero_contrato,
                    "ano": ano,
                    "tipo": tipo,
                    "status": status,
                    "dt_assinatura": dt_assinatura.isoformat(),
                    "prazo_dias": prazo_dias,
                    "valor_inicial": valor_inicial                    
                }

                try:
                    with st.spinner("Cadastrando contrato..."):
                        supabase.table("tb_contratos").insert(dados_contrato).execute()
                    st.success("Contrato cadastrado com sucesso!")
                except Exception as e:
                    st.error("Erro ao cadastrar contrato.")
                    st.write(f"Detalhes técnicos: {e}")

with aba_cadastro_item:
    
    with st.form(key="cadastro_item_form"):

        nome_item = st.text_input("Nome do Item*").strip().title()
    
        st.form_submit_button("Cadastrar Item")

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
                        with st.spinner("Cadastrando item..."):
                            supabase.table("tb_itens").insert(nome_item).execute()
                    except Exception as e:
                        st.error("Erro ao cadastrar item.")
                        st.write(f"Detalhes técnicos: {e}")

            st.success("Item cadastrado com sucesso!")

