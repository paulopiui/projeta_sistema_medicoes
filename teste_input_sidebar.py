import streamlit as st

st.title("Formulário na Barra Lateral")

with st.sidebar:
    st.header("Preencha os dados:")
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
    opcao = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])

    if st.button("Enviar"):
        st.success(f"Dados enviados: {nome}, {idade}, {opcao}")

st.write("O formulário está na barra lateral. Isso libera mais espaço na tela principal.")
