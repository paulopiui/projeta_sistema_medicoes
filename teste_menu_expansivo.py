import streamlit as st

# Simula um popup usando um expander
with st.expander("📌 **Formulário**", expanded=True):
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
    opcao = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])

    # Botão para enviar os dados
    if st.button("Enviar"):
        st.success(f"Dados enviados: {nome}, {idade}, {opcao}")