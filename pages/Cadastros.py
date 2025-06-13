import streamlit as st
from utils import format, validate
from abas_cadastros import cadastro_cliente, cadastro_item_contrato, cadastro_municipio, cadastro_contrato, cadastro_item, cadastro_aditivo

format.config_pagina()
validate.validar_login()
validate.validar_nivel_acesso("gerente")
                               
col1, col2, col3 = st.columns(3)
with col2:
    # Título da Aplicação
    st.title("Cadastro de Dados")

# Seção de Abas
aba_cadastro_municipio, aba_cadastro_cliente, aba_cadastro_contrato, aba_cadastro_itens_contrato, aba_cadastro_aditivo, aba_cadastro_item = st.tabs(
    ["Município", "Cliente", "Contrato", "Itens do Contrato", "Aditivo","Item Medição"]
)

with aba_cadastro_municipio:
    cadastro_municipio.aba_cadastro_municipio()       

with aba_cadastro_cliente:  
    cadastro_cliente.aba_cadastro_cliente()   

with aba_cadastro_contrato:  
    cadastro_contrato.aba_cadastro_contrato()     

with aba_cadastro_itens_contrato:
    cadastro_item_contrato.aba_cadastro_item_contrato()    

with aba_cadastro_aditivo:
    cadastro_aditivo.aba_cadastro_aditivo()

with aba_cadastro_item:
    cadastro_item.aba_cadastro_item()      