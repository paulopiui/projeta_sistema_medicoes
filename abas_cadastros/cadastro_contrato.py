import streamlit as st
from utils.conexao_supabase import supabase
from utils import format
import pandas as pd

def aba_cadastro_contrato():
    
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
        cliente_selecionado = st.selectbox("Cliente*", sorted(mapa_clientes.keys()),key="selecao_cliente")

    with col2:
        # Carregar empresas
        empresas = supabase.table("tb_empresas").select("id, empresa_grupo_projeta").execute()
        mapa_empresas = {e["empresa_grupo_projeta"]: e["id"] for e in empresas.data}
        empresa_selecionada = st.selectbox("Empresa Grupo Projeta*", sorted(mapa_empresas.keys()),key="selecao_empresa")

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
    
    format.formatar_data_brasil(df_contratos_filtrados, "Data de Assinatura")
    format.configurar_valor_moeda(df_contratos_filtrados, "Valor Inicial")
    df_contratos_filtrados = df_contratos_filtrados[["Contrato/Ata", "Ano", "Tipo", "Data de Assinatura", "Prazo (dias)", "Valor Inicial", "Empresa do Grupo"]]     
    st.write("Lista de Contratos Cadastrados")
    
    # Ajusta a altura da tabela
    altura_final = format.altura_tabela(df_contratos_filtrados, 8)        
    st.dataframe(df_contratos_filtrados, use_container_width=True, height=altura_final)       