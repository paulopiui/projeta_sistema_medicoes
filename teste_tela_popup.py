import streamlit as st
from streamlit_modal import Modal

# Criar o modal
modal = Modal(key="form_modal", title="📌 Formulário")

# Botão para abrir o popup
if st.button("Abrir Popup"):
    modal.open()

# Exibir o modal se estiver aberto
if modal.is_open():
    with modal.container():
        nome = st.text_input("Nome:")
        idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
        opcao = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])

        # Botão para enviar os dados
        if st.button("Enviar"):
            st.success(f"Dados enviados: {nome}, {idade}, {opcao}")
            modal.close()

        # Botão para fechar o modal
        if st.button("Fechar"):
            modal.close()
