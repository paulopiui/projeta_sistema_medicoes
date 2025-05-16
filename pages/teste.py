import streamlit as st

@st.dialog("Cadastrar Medição")
def cadastrar_medicao():
    st.title("Cadastrar Medição")
    
    # Campos para cadastro
    cliente = st.text_input("Cliente")
    contrato = st.text_input("Contrato")
    data = st.date_input("Data da Medição")
    valor = st.number_input("Valor da Medição", min_value=0.0, format="%.2f")
    
# Botão para cadastrar
if st.button("Cadastrar Medição"):
    cadastrar_medicao()
