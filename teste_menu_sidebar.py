import streamlit as st

# Configuração da página
st.set_page_config(page_title="Sistema de Atestados", layout="wide")

# Função para carregar CSS externo
def load_css():
    with open("style.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

# Carregar o CSS
load_css()

# Inicializa o estado da página caso ainda não tenha sido definido
if "menu" not in st.session_state:
    st.session_state["menu"] = "home"

# Função para atualizar a página selecionada
def set_page(page):
    st.session_state["menu"] = page

# Criando o menu com botões estilizados no sidebar
st.sidebar.markdown('<div class="sidebar">', unsafe_allow_html=True)
st.sidebar.button("🏠 Página Inicial", on_click=set_page, args=("home",))
st.sidebar.button("➕ Adicionar Atestado", on_click=set_page, args=("add",))
st.sidebar.button("✏️ Editar Atestado", on_click=set_page, args=("edit",))
st.sidebar.button("📊 Visualizar Atestados", on_click=set_page, args=("view",))
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Obtém a página atual do estado da sessão
menu = st.session_state["menu"]

# Conteúdo de cada página
if menu == "home":
    st.title("🏠 Bem-vindo ao Sistema de Atestados")
    st.write("Utilize o menu lateral para navegar entre as funcionalidades.")

elif menu == "add":
    st.title("➕ Adicionar Atestado")
    with st.form("form_add"):
        nome = st.text_input("Nome do Paciente")
        data = st.date_input("Data do Atestado")
        dias = st.number_input("Quantidade de Dias", min_value=1, step=1)
        justificativa = st.text_area("Justificativa")
        submit_button = st.form_submit_button("Salvar")

        if submit_button:
            st.success("Atestado adicionado com sucesso!")

elif menu == "edit":
    st.title("✏️ Editar Atestado")
    st.write("Funcionalidade em desenvolvimento.")

elif menu == "view":
    st.title("📊 Visualizar Atestados")
    st.write("Aqui você pode visualizar os atestados armazenados.")
