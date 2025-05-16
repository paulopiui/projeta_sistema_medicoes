import streamlit as st
from conexao_supabase import supabase
import pandas as pd
import pytz
from datetime import datetime
import time

def exibir_cabecalho():

    """Exibe o cabeçalho padrão em todas as páginas."""
    col1, col2, col3, col4 = st.columns([0.1, 0.2 ,0.6, 0.2])

    with col1:
        # Exibir logo no topo
        st.image("img/logo.png", width=300,  use_container_width=True)  # Substitua pelo caminho da sua logo

    with col3:
        #st.markdown('<h2 class="custom-subheader">Gerenciamento de Contratos</h2>', unsafe_allow_html=True)
        st.title("Gerenciamento de Contratos")
    
    with col4:                
            
        if "auth_user" not in st.session_state or st.session_state["auth_user"] is None:
            st.markdown(f'<h6 class="custom-subheader" style="text-align: right;">Usuário: Não logado</h6>', unsafe_allow_html=True)
        else:
            user_id = st.session_state["auth_user"].id
            res = supabase.table("user_perfil").select("nome").eq("id", user_id).single().execute()
            #st.markdown(f'<h6 class="custom-subheader">Usuário: {st.session_state["auth_user"].email}</h6>', unsafe_allow_html=True)
            st.markdown(f'<h6 class="custom-subheader" style="text-align: right;">Usuário: {res.data["nome"]}</h6>', unsafe_allow_html=True)
            
    st.divider()

def config_pagina():
    # Configuração da página
    st.set_page_config(        
        page_icon="img/favicon2.png",
        layout="wide"
    )

def exibir_cabecalho_centralizado():
        
    col1, col2, col3 = st.columns([0.2, 0.6, 0.2])

    with col2:
        st.image("img/logo.png", width=350)  # Substitua pelo caminho da sua logo    
      
    if "auth_user" not in st.session_state or st.session_state["auth_user"] is None:
        st.markdown(f'<h6 class="custom-subheader" style="text-align: right;">Usuário: Não logado</h6>', unsafe_allow_html=True)
    else:
        user_id = st.session_state["auth_user"].id
        res = supabase.table("user_perfil").select("nome").eq("id", user_id).single().execute()
        #st.markdown(f'<h6 class="custom-subheader" style="text-align: right;">Usuário: {st.session_state["auth_user"].email}</h6>', unsafe_allow_html=True)
        st.markdown(f'<h6 class="custom-subheader" style="text-align: right;">Usuário: {res.data["nome"]}</h6>', unsafe_allow_html=True)
            
    st.divider()

def config_pagina_centralizada():
    
    # Configuração da página
    st.set_page_config(        
        page_icon="img/favicon2.png",
        layout="centered"
    )
   
def validar_login():
    if "auth_user" not in st.session_state or st.session_state["auth_user"] is None:
        st.warning("⚠️ Acesso restrito. Faça login primeiro.")
        st.stop()

def validar_nivel_acesso(nivel_acesso_necessario):
    
    NIVEIS_ACESSO = {
        "usuario": 1,
        "gerente": 2,
        "administrador": 3
    }
        
    user_id = st.session_state["auth_user"].id
    response = supabase.table("user_perfil").select("nivel_acesso").eq("id", user_id).single().execute()

    if not response.data:
        st.warning("⚠️ Usuário sem perfil definido.")
        st.stop()

    nivel_acesso_usuario = response.data["nivel_acesso"]
    
    if NIVEIS_ACESSO.get(nivel_acesso_usuario, 0) < NIVEIS_ACESSO.get(nivel_acesso_necessario, 0):
        st.warning("⚠️ Você não tem permissão para acessar esta página.")
        st.stop()

def altura_tabela(df,linhas_max):

    altura_linha = 35  # altura aproximada por linha (em pixels)
    altura_max = altura_linha * (linhas_max + 1)  # altura máxima da tabela (em pixels)
    linhas = len(df)
    altura_final = min(altura_linha * (linhas + 1), altura_max)
    
    return altura_final

def configurar_valor_moeda(df, coluna):
    """Formata os valores de uma coluna como moeda brasileira."""
    df[coluna] = df[coluna].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if pd.notnull(x) else "R$ 0,00"
    )
    
    return df

def formatar_data_brasil(df, coluna):
    df[coluna] = pd.to_datetime(df[coluna], utc=True, format='mixed')    
    df[coluna] = df[coluna].dt.tz_convert("America/Sao_Paulo")       
    df[coluna] = df[coluna].dt.strftime('%d/%m/%Y')   
    return df

def formatar_data_hora_brasil(df, coluna):   
     
    df[coluna] = pd.to_datetime(df[coluna], utc=True, format='mixed')    
    df[coluna] = df[coluna].dt.tz_convert("America/Sao_Paulo")    
    df[coluna] = df[coluna].dt.strftime("%d-%m-%Y %H:%M:%S")
    return df

@st.dialog("Cadastrar Medição")
def cadastrar_medicao(contrato):
    
    resposta = supabase.table("tb_contratos").select("id, tb_clientes(id, cliente), dt_assinatura").eq("numero_contrato_ata", contrato).execute()
    id_contrato = resposta.data[0]["id"] if resposta.data else None
    
    mes_referencia_minimo = pd.to_datetime(resposta.data[0]["dt_assinatura"]).date() if resposta.data and resposta.data[0]["dt_assinatura"] else pd.to_datetime("today").date()
    
    meses = pd.date_range(start=mes_referencia_minimo, end=datetime.today(), freq='MS')
    opcoes = [d.strftime('%m/%Y') for d in meses]
    
    # Campos para cadastro
    mes_referencia = st.selectbox("Selecione o Mês de Referência", opcoes)
    valor = st.number_input("Valor da Medição", min_value=0.0, format="%.2f")
    
    if st.button("Cadastrar Medição", key="cadastrar_medicao_dialog"):
        if not mes_referencia or valor <= 0:
            st.warning("⚠️ Preencha todos os campos.")
        else:          
            mes_ref_date = datetime.strptime(mes_referencia, "%m/%Y").date()
            (supabase.table("tb_medicoes")
             .insert({"id_contrato": id_contrato, "mes_referencia": mes_ref_date.isoformat(), "valor_medido": valor})
             .execute()
             )
            st.success("✅ Medição cadastrada com sucesso!")
            time.sleep(1)
            st.rerun()

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

@st.dialog("⚠️  Alerta")
def dialogo_alerta(texto):
    st.write(texto)