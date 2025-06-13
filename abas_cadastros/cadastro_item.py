import streamlit as st
from utils.conexao_supabase import supabase
from utils import format, dialogs
import pandas as pd

def aba_cadastro_item():

    st.write("")
    
    cadastro_realizado = False
    
    with st.form(key="cadastro_item_form"):
        
        col1, col2 = st.columns(2)
        with col1:

            nome_item = st.text_input("Nome do Item*").strip().title()

        with col2:
            
            grupos = supabase.table("tb_grupos_itens").select("id, grupo").execute().data
            
            mapa_grupos = {g["grupo"]: g["id"] for g in grupos}
            
            grupo_item = st.selectbox("Grupo do Item*", options=[""] + sorted(mapa_grupos.keys()))      
            
            id_grupo = mapa_grupos.get(grupo_item)

        submit_button=st.form_submit_button("Cadastrar Item")

        if submit_button:

            if nome_item:
                # Verificar duplicidade
                item_existe = (
                    supabase.table("tb_itens")
                    .select("id")
                    .eq("item", nome_item)
                    .execute()
                )

                if item_existe.data:
                    st.warning("⚠️  ATENÇÃO: Já existe um item com este nome.")
                else:               

                    try:
                        data = {"item": nome_item, "id_grupo":id_grupo}
                        
                        with st.spinner("Cadastrando item..."):
                            supabase.table("tb_itens").insert(data).execute() 
                        
                        cadastro_realizado = True                                                                                 
                                                        
                    except Exception as e:
                        st.error("Erro ao cadastrar item.")
                        st.write(f"Detalhes técnicos: {e}")
    
    if cadastro_realizado:
        dialogs.show_success_dialog()
        
    consulta = supabase.table("tb_itens").select("item, tb_grupos_itens(grupo), created_at").execute()
    
    if consulta.data:
        df_itens = pd.DataFrame(consulta.data)
        df_itens = df_itens.rename(columns={"item": "Item", "created_at": "Criado em", "tb_grupos_itens": "Grupo"})
        
        df_itens["Grupo"] = df_itens["Grupo"].apply(lambda x: x["grupo"].strip() if isinstance(x, dict) and "grupo" in x else "")

        format.formatar_data_hora_brasil(df_itens, "Criado em")
        st.write("Lista de Itens Cadastrados")
        
        # Ajusta a altura da tabela
        altura_final = format.altura_tabela(df_itens, 8)        
        st.dataframe(df_itens, use_container_width=True, height=altura_final)  