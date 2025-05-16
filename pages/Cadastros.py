import streamlit as st
import pandas as pd
import utils
from conexao_supabase import supabase

utils.config_pagina_centralizada()
#utils.exibir_cabecalho_centralizado_pequeno()
utils.validar_login()
utils.validar_nivel_acesso("gerente")

@st.dialog("Cadastro realizado com sucesso!")
def show_success_dialog():    
    st.write("")
    
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    # Título da Aplicação
    st.title("Cadastro de Dados")

# Seção de Abas
aba_cadastro_municipio, aba_cadastro_cliente, aba_cadastro_contrato, aba_cadastro_aditivo, aba_cadastro_item = st.tabs(
    ["Município", "Cliente", "Contrato", "Aditivo","Item Medição"]
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

    tabela_municipios = supabase.table("tb_municipios").select("id, municipio, uf, dt_cadastro").execute()
    if tabela_municipios.data:
        df_municipios = pd.DataFrame(tabela_municipios.data)
        df_municipios = df_municipios.rename(columns={"municipio": "Município", "uf": "UF", "dt_cadastro": "Data de Cadastro"})
        df_municipios["Data de Cadastro"] = pd.to_datetime(df_municipios["Data de Cadastro"], format="mixed")
        df_municipios["Data de Cadastro"] = df_municipios["Data de Cadastro"].dt.strftime("%Y-%m-%d %H:%M:%S")
        utils.formatar_data_hora_brasil(df_municipios, "Data de Cadastro")        
        df_municipios = df_municipios[["Município", "UF", "Data de Cadastro"]]
        st.write("Lista de Municípios Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = utils.altura_tabela(df_municipios, 8)        
        st.dataframe(df_municipios, use_container_width=True, height=altura_final)
        
        st.data_editor(
            df_municipios,
            use_container_width=True,
            hide_index=True,
            num_rows= "flexible")
        
    else:
        st.warning("Nenhum município cadastrado até o momento.")

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

with aba_cadastro_contrato:  
    
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

    df_contratos = (supabase.table("tb_contratos")
                    .select("id, numero_contrato_ata, ano, tipo, dt_assinatura, prazo_dias, valor_inicial, tb_clientes(cliente), tb_empresas(empresa_grupo_projeta)")                    
                    .execute())
    df_contratos = pd.DataFrame(df_contratos.data)    
    df_contratos["cliente"] = df_contratos["tb_clientes"].apply(lambda x: x["cliente"] if isinstance(x, dict) else None)
    df_contratos["empresa_grupo_projeta"] = df_contratos["tb_empresas"].apply(lambda x: x["empresa_grupo_projeta"] if isinstance(x, dict) else None)
    df_contratos.drop(columns=["tb_clientes", "tb_empresas"], inplace=True)
    df_contratos = df_contratos.rename(columns={
        "numero_contrato_ata": "Contrato/Ata",
        "ano": "Ano",
        "tipo": "Tipo",
        "dt_assinatura": "Data de Assinatura",
        "prazo_dias": "Prazo (dias)",
        "valor_inicial": "Valor Inicial",
        "cliente": "Cliente",
        "empresa_grupo_projeta": "Empresa do Grupo"
    })
    
    df_contratos_filtrados = df_contratos[df_contratos["Cliente"] == cliente_selecionado] 
    
    utils.formatar_data_brasil(df_contratos_filtrados, "Data de Assinatura")
    utils.configurar_valor_moeda(df_contratos_filtrados, "Valor Inicial")
    df_contratos_filtrados = df_contratos_filtrados[["Contrato/Ata", "Ano", "Tipo", "Data de Assinatura", "Prazo (dias)", "Valor Inicial", "Empresa do Grupo"]]     
    st.write("Lista de Contratos Cadastrados")
    
    # Ajusta a altura da tabela
    altura_final = utils.altura_tabela(df_contratos_filtrados, 8)        
    st.dataframe(df_contratos_filtrados, use_container_width=True, height=altura_final)    

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

        nome_item = st.text_input("Nome do Item*").strip().title()
    
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
                        data = {"item": nome_item}
                        
                        with st.spinner("Cadastrando item..."):
                            supabase.table("tb_itens").insert(data).execute() 
                        
                        cadastro_realizado = True                                                                                 
                                                        
                    except Exception as e:
                        st.error("Erro ao cadastrar item.")
                        st.write(f"Detalhes técnicos: {e}")
    
    if cadastro_realizado:
        show_success_dialog()
        
    consulta = supabase.table("tb_itens").select("item, created_at").execute()
    
    if consulta.data:
        df_itens = pd.DataFrame(consulta.data)        
        df_itens = df_itens.rename(columns={"item": "Item", "created_at": "Criado em"})
        utils.formatar_data_hora_brasil(df_itens, "Criado em")
        st.write("Lista de Itens Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = utils.altura_tabela(df_itens, 8)        
        st.dataframe(df_itens, use_container_width=True, height=altura_final)    