import streamlit as st
from utils.conexao_supabase import supabase

@st.dialog("Cadastro realizado com sucesso!")
def show_success_dialog():    
    st.write("")

@st.dialog("⚠️  Atenção - Exclusão de Itens")
def confirmacao_exclusao():
    st.write("Esta ação não poderá ser desfeita, confirma a exclusão dos itens selecionados?")
    
    col1, col2, col3, col4, col5 = st.columns([1,2,1,2,1])
    
    with col2:
        if st.button("Confirmar"):

            ids_para_excluir = [
                row["ID"] for _, row in df_excluir.iterrows() if row["Excluir"]
            ]
            if ids_para_excluir:
                supabase.table("tb_itens_por_contrato").delete().in_("id", ids_para_excluir).execute()
            st.success("Itens excluídos com sucesso!")
            del st.session_state["df_exclusao"]
            st.rerun()
            
    
    with col4:
        if st.button("Cancelar"):            
            del st.session_state["df_exclusao"]
            st.rerun()
            
@st.dialog("⚠️  Alerta")
def dialogo_alerta(texto):
    st.write(texto)    

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