import streamlit as st

def exibir_cabecalho():

    """Exibe o cabeçalho padrão em todas as páginas."""
    col1, col2, col3 = st.columns([0.1, 0.2 ,0.6])

    with col1:
        # Exibir logo no topo
        st.image("img/logo.png", width=300,  use_container_width=True)  # Substitua pelo caminho da sua logo

    with col3:
        #st.markdown('<h2 class="custom-subheader">Gerenciamento de Contratos</h2>', unsafe_allow_html=True)
        st.title("Gerenciamento de Contratos")

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

    st.divider()

def config_pagina_centralizada():
    # Configuração da página
    st.set_page_config(        
        page_icon="img/favicon2.png",
        layout="centered"
    )