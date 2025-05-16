import streamlit as st

# Estilos customizados
st.markdown("""
    <style>
    .stSelectbox > div > div {
        color: #ffffff !important;
    }
    .info-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 0.5rem;
    }
    .medicao-box {
        background-color: #1f1f1f;
        border-left: 5px solid #00c851;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
    }
    .item-list {
        margin-top: 0.5rem;
        padding-left: 1.5rem;
        color: #ffffff;
    }
    .item-list li {
        margin-bottom: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("## 🧾 Gerenciamento de Contratos")

# Filtros
col1, col2, col3 = st.columns([2, 2, 1])
with col1:
    cliente = st.selectbox("Cliente", ["Prefeitura de Nova Lima", "Outro Cliente"])
with col2:
    contrato = st.selectbox("Contrato", ["270/2023", "150/2022"])
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Cadastrar Medição"):
        st.success("Função de cadastro em desenvolvimento...")

# Dados do contrato
st.divider()
st.markdown(f"### {cliente}")
col1, col2, col3 = st.columns(3)
col1.markdown("📅 **Ano Contrato:** 2023")
col2.markdown("📎 **Tipo:** Adesão")
col3.markdown("📌 **Status:** _Não definido_")

# Simulação de dados da medição
medicoes = [{
    "id": 1,
    "mes": "2024-11",
    "valor": 165_146_584.00,
    "itens": ["Item 1 – Serviço X", "Item 2 – Serviço Y", "Item 3 – Serviço Z"]
}, {
    "id": 2,
    "mes": "2024-12",
    "valor": 123_456_789.00,
    "itens": []
}]

# Exibição das medições
for m in medicoes:
    with st.container():
        st.markdown(f"""
            <div class="medicao-box">
                <strong>Medição {m['id']}</strong> – Mês: {m['mes']} – Valor: R$ {m['valor']:,.2f}<br>
        """, unsafe_allow_html=True)

        if m["itens"]:
            st.markdown('<ul class="item-list">' + ''.join([f"<li>✅ {item}</li>" for item in m["itens"]]) + '</ul>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">⚠️ Nenhum item medido encontrado.</div>', unsafe_allow_html=True)

        col_edit, col_delete = st.columns([1, 1])
        with col_edit:
            if st.button("✏️ Editar", key=f"editar_{m['id']}"):
                st.info(f"Edição da Medição {m['id']} ainda não implementada.")
        with col_delete:
            if st.button("🗑️ Excluir", key=f"excluir_{m['id']}"):
                st.warning(f"Medição {m['id']} marcada para exclusão (simulação).")

        st.markdown("</div>", unsafe_allow_html=True)
