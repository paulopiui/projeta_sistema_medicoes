import streamlit as st

# Função para carregar o CSS externo
def load_css(file_name):
    with open(file_name, "r") as f:
        css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Medições Projeta",  # Define o título da aba do navegador
    page_icon="📊",               # Ícone da aba do navegador (emoji ou URL de imagem)
    layout="wide",                # Layout da página: "centered" (padrão) ou "wide" (mais espaço)
    initial_sidebar_state="expanded",  # Estado inicial da barra lateral: "auto", "expanded" ou "collapsed"
)

# Aplicar o CSS externo
load_css("style.css")

# Seção com fundo verde
st.markdown('<div class="full-width-container">', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.title("Formulário com Abas")

tab1, tab2, tab3 = st.tabs(["📋 Dados Pessoais", "⚙️ Configurações", "📊 Resultados"])

with tab1:
    st.header("Dados Pessoais")
    nome = st.text_input("Nome:")
    idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
    opcao = st.selectbox("Escolha uma opção:", ["Opção 1", "Opção 2", "Opção 3"])

with tab2:
    st.header("Configurações")
    tema = st.radio("Escolha um tema:", ["Claro", "Escuro"])
    notificacoes = st.checkbox("Ativar notificações")

with tab3:
    st.header("Resultados")
    if st.button("Mostrar resumo"):
        st.write(f"Nome: {nome}, Idade: {idade}, Opção: {opcao}, Tema: {tema}, Notificações: {notificacoes}")