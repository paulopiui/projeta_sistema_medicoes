import streamlit as st
from conexao_supabase import supabase
from utils import dialogs
import pandas as pd

def aba_cadastro_item_contrato():
    
    def atualizar_itens_grupo(contrato_id, grupo_id, itens):
        
        # Buscar os itens já cadastrados no contrato
        vinculados = supabase.table("tb_itens_por_contrato") \
            .select("id_item, valor_unitario, quantidade_contratada") \
            .eq("id_contrato", contrato_id) \
            .execute().data

        itens_ja_cadastrados = {
            v["id_item"]: {
                "valor_unitario": v["valor_unitario"],
                "quantidade_contratada": v["quantidade_contratada"]
            }
            for v in vinculados
        }

        # Criar dataframe com base nos itens do grupo
        df = pd.DataFrame([
            {
                "ID": i["id"],
                "Item": i["item"],
                "Valor Unitário": itens_ja_cadastrados[i["id"]]["valor_unitario"] if i["id"] in itens_ja_cadastrados else 0.0,
                "Quantidade Contratada": itens_ja_cadastrados[i["id"]]["quantidade_contratada"] if i["id"] in itens_ja_cadastrados else 0.0,
                "Cadastrar": i["id"] in itens_ja_cadastrados
            }
            for i in itens if i["id_grupo"] == grupo_id
        ])    
    
    
    
    st.write("")

    # Buscar contratos, grupos e itens
    contratos = supabase.table("tb_contratos").select("id, numero_contrato_ata").execute().data
    grupos = supabase.table("tb_grupos_itens").select("id, grupo").execute().data
    itens = supabase.table("tb_itens").select("id, item, id_grupo").execute().data

    # Mapas de apoio
    # Mapa de Contratos | Número do Contrato e ID do Contrato
    map_contratos = {f"{c['numero_contrato_ata']}": c["id"] for c in contratos}
    # Mapa de Grupos | Nome do Grupo e ID do Grupo
    map_grupos = {g["grupo"]: g["id"] for g in grupos}

    col1, col2, col3, col4 = st.columns([1, 2, 0.5, 0.5])
    
    # Seleção do contrato e grupo
    with col1:    
        contrato_nome = st.selectbox("Contrato", map_contratos.keys())
    
    with col2:
        grupo_nome = st.selectbox("Grupo de Itens", map_grupos.keys())

    with col4:
        if st.button("Atualizar Itens"):            
            st.rerun()
    
    if "itens_grupo_df" not in st.session_state:
        st.session_state.itens_grupo_df = pd.DataFrame()

    # Baseado na seleção do usuário, captura o ID do grupo e do contrato
    grupo_id = map_grupos[grupo_nome]
    contrato_id = map_contratos[contrato_nome]
    
    # Criação de abas para Cadastro e Exclusão de itens
    aba_cadastro, aba_exclusao = st.tabs(["Cadastro\Edição", "Exclusão"])
    
    # ADCIONAR\EDITAR itens ##################################################################################
    with aba_cadastro:

        # Itens do grupo
        # Percorre os itens e filtra apenas os do grupo selecionado
        itens_grupo = [i for i in itens if i["id_grupo"] == grupo_id]
        
        # Se o grupo selecionado não possuir itens, mostra uma mensagem de aviso
        # Caso contrário, atualiza o session_state com os itens do grupo
        if not itens_grupo:
            st.warning("Nenhum item encontrado neste grupo.")
        else:
            st.session_state.itens_grupo_df = atualizar_itens_grupo(contrato_id, grupo_id, itens)

        # Editor de tabela
        if not st.session_state.itens_grupo_df:  
            
            st.markdown("""
                <div style="background-color:#e6f2ff; padding:1px; border-radius:5px; height:50px; display:flex; align-items:center; justify-content:center;">
                    <h3 style="margin:0; color:#003366;">✏️ Adicionar/Editar</h3>
                </div>
            """, unsafe_allow_html=True)

            edited_df = st.data_editor(
                st.session_state.itens_grupo_df,
                use_container_width=True,
                num_rows=10,
                key="editor_grupo",
                column_config={
                    "Item": st.column_config.Column(disabled=True),
                    "ID": st.column_config.Column(disabled=True),
                    "Valor Unitário": st.column_config.NumberColumn("Valor Unitário (R$)", min_value=0.0, step=0.01),
                    "Quantidade Contratada": st.column_config.NumberColumn("Qtd. Contratada", min_value=0.0, step=0.01),
                    "Cadastrar": st.column_config.CheckboxColumn("Cadastrar")  # nova coluna
                }
            )


            # Botão para salvar os itens (excluindo os marcados)
            if st.button("Salvar Itens no Contrato"):
                
                contrato_id = map_contratos[contrato_nome]
                novos = []
                atualizacoes = []

                for _, row in edited_df.iterrows():
                    if row["Cadastrar"]:
                        dados = {
                            "id_contrato": contrato_id,
                            "id_item": row["ID"],
                            "valor_unitario": row["Valor Unitário"],
                            "quantidade_contratada": row["Quantidade Contratada"]
                        }

                        if row["ID"] in itens_ja_cadastrados:
                            atualizacoes.append(dados)
                        else:
                            novos.append(dados)

                # Inserir novos
                if novos:
                    supabase.table("tb_itens_por_contrato").insert(novos).execute()

                # Atualizar existentes
                for item in atualizacoes:
                    supabase.table("tb_itens_por_contrato") \
                        .update({
                            "valor_unitario": item["valor_unitario"],
                            "quantidade_contratada": item["quantidade_contratada"]
                        }) \
                        .eq("id_contrato", item["id_contrato"]) \
                        .eq("id_item", item["id_item"]) \
                        .execute()

                st.success("Itens atualizados com sucesso!")
                st.session_state.itens_grupo_df = atualizar_itens_grupo(contrato_id, grupo_id, itens)
                st.rerun()    

# EXCLUIR itens ##########################################################################################
    with aba_exclusao:
        
        st.markdown("""
            <div style="background-color:#ffcccc; padding:1px; border-radius:5px; height:50px; display:flex; align-items:center; justify-content:center;">
                <h3 style="margin:0; color:#800000;">❌ Excluir Itens</h3>
            </div>
        """, unsafe_allow_html=True)        
        
        if "df_exclusao" not in st.session_state:
            
            # Buscar os itens já cadastrados no contrato
            vinculados = supabase.table("tb_itens_por_contrato") \
                .select("id, id_item, valor_unitario, quantidade_contratada") \
                .eq("id_contrato", contrato_id) \
                .execute().data

            if vinculados:
                
                dados_vinculados = []
                for v in vinculados:
                    item_nome = next((i["item"] for i in itens if i["id"] == v["id_item"]), "Desconhecido")
                    dados_vinculados.append({
                        "ID": v["id"],
                        "Item": item_nome,
                        "Valor Unitário": v["valor_unitario"],
                        "Quantidade Contratada": v["quantidade_contratada"],
                        "Excluir": False  # Coluna para marcar exclusão
                    })
                st.session_state.df_exclusao = pd.DataFrame(dados_vinculados)
            
            else:
                st.session_state.df_exclusao = pd.DataFrame(columns=["ID", "Item", "Valor Unitário", "Quantidade Contratada", "Excluir"])
                    
        if st.session_state.df_exclusao.empty:
            st.info("ℹ️  Nenhum item vinculado ao Contrato para exclusão.")       
        else:
            df_excluir = st.data_editor(
            st.session_state.df_exclusao,
            use_container_width=True,
            key="editor_excluir_itens",
            num_rows=10
            )
        
            if st.button("Excluir Itens Selecionados"):
                
                if df_excluir.empty:
                    st.info("ℹ️  Nenhum item encontrado para exclusão.")
                else:                
                    dialogs.confirmacao_exclusao()                