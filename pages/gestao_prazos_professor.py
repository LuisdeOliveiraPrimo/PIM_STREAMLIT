# Bloco de código para o topo de CADA ARQUIVO EM 'pages/'
import sys
import os
import streamlit as st

pages_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(pages_dir)
if project_root not in sys.path:
    sys.path.append(project_root)
# Fim do bloco

import pandas as pd
from datetime import date, datetime
from auth_utils import show_custom_menu
from config import get_csv_path

# --- Configuração da Página ---
# CORREÇÃO: st.set_page_config() deve ser o primeiro comando Streamlit
st.set_page_config(layout="wide")

# --- Autenticação e Menu ---
show_custom_menu()

# Define o nome do arquivo CSV
ATIVIDADES_CSV = get_csv_path('atividades.csv')
HEADERS_CSV = ['id_atividade', 'id_turma', 'titulo', 'descricao', 'data_entrega']

# ==========================================================
# 1. FUNÇÕES DE INFRAESTRUTURA (CSV)
# ==========================================================

def get_todas_atividades():
    """Recupera todas as atividades do arquivo CSV."""
    try:
        df = pd.read_csv(ATIVIDADES_CSV)
        if df.empty and list(df.columns) != HEADERS_CSV:
             return pd.DataFrame(columns=HEADERS_CSV)
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        if not os.path.exists(ATIVIDADES_CSV):
            pd.DataFrame(columns=HEADERS_CSV).to_csv(ATIVIDADES_CSV, index=False)
        return pd.DataFrame(columns=HEADERS_CSV)

def adicionar_atividade(id_turma, titulo, data_entrega_dt, descricao=""):
    """Adiciona a atividade ao CSV."""
    df = get_todas_atividades()
    if df.empty or 'id_atividade' not in df.columns:
        new_id = 1
    else:
        new_id = df['id_atividade'].max() + 1
        
    data_entrega_str = data_entrega_dt.isoformat()
    nova_atividade = {
        'id_atividade': new_id,
        'id_turma': id_turma,
        'titulo': titulo,
        'descricao': descricao,
        'data_entrega': data_entrega_str
    }
    df_nova = pd.DataFrame([nova_atividade])
    df_final = pd.concat([df, df_nova], ignore_index=True)
    
    try:
        df_final.to_csv(ATIVIDADES_CSV, index=False)
        return f"SUCESSO! Atividade '{titulo}' adicionada."
    except Exception as e:
        return f"Ocorreu um erro ao salvar o CSV: {e}"

def deletar_atividade(atividade_id):
    """Deleta uma atividade do CSV usando o seu ID."""
    df = get_todas_atividades()
    
    if 'id_atividade' not in df.columns or atividade_id not in df['id_atividade'].values:
        return f"ERRO: Nenhuma atividade encontrada com o ID {atividade_id}."
        
    df_filtrado = df[df['id_atividade'] != atividade_id]
    
    try:
        df_filtrado.to_csv(ATIVIDADES_CSV, index=False)
        return f"SUCESSO! Atividade com ID {atividade_id} foi deletada."
    except Exception as e:
        return f"Ocorreu um erro ao salvar o CSV após deletar: {e}"

# ==========================================================
# 2. INTERFACE STREAMLIT
# ==========================================================

def menu_professor_streamlit():
    st.title("👨‍🏫 Plataforma de Gerenciamento de Prazos")
    st.caption("Visão do Professor: Publicação e Exclusão de Atividades.")

    # Carregar dados relacionais
    try:
        professor_id = st.session_state.user_info['id_usuario']
        df_turmas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\turmas.csv')
        df_disciplinas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\diciplinas.csv') 
    except Exception as e:
        st.error(f"Não foi possível carregar os dados das turmas: {e}")
        return

    # Filtrar turmas do professor logado
    turmas_professor = df_turmas[df_turmas['id_professor'] == professor_id]
    turmas_professor = pd.merge(turmas_professor, df_disciplinas, on='id_disciplina')
    turmas_professor['turma_display'] = turmas_professor['nome_disciplina'] + " (" + turmas_professor['semestre'].astype(str) + ")"
    
    if turmas_professor.empty:
        st.warning("Você não está alocado em nenhuma turma e não pode publicar atividades.")
        return

    # Recupera todas as atividades
    df_atividades_todas = get_todas_atividades()
    
    # Junta atividades com as turmas do professor para exibir
    if not df_atividades_todas.empty:
        df_atividades_visivel = pd.merge(df_atividades_todas, turmas_professor, on='id_turma')
    else:
        df_atividades_visivel = pd.DataFrame(columns=HEADERS_CSV + ['turma_display', 'nome_disciplina']) # Cria DF vazio com colunas
        
    st.markdown("---")
    tab_ver, tab_publicar, tab_deletar = st.tabs(["Visualizar Prazos", "Publicar Nova Atividade", "Deletar Atividade"])

    # --- ABA DE VISUALIZAÇÃO ---
    with tab_ver:
        st.subheader("📋 Atividades Publicadas por Você")
        if df_atividades_visivel.empty:
            st.warning("Nenhuma atividade encontrada para suas turmas. Publique a primeira!")
        else:
            df_exibicao = df_atividades_visivel.rename(columns={
                'id_atividade': 'ID',
                'turma_display': 'Turma',
                'titulo': 'Título',
                'data_entrega': 'Prazo',
                'descricao': 'Detalhes'
            })
            st.dataframe(df_exibicao[['ID', 'Turma', 'Título', 'Prazo', 'Detalhes']], use_container_width=True, hide_index=True)

    # --- ABA DE PUBLICAÇÃO ---
    with tab_publicar:
        st.subheader("📝 Publicar Nova Atividade")
        with st.form("form_publicacao", clear_on_submit=True):
            turma_selecionada_display = st.selectbox("Selecione a Turma:", options=turmas_professor['turma_display'])
            titulo = st.text_input("Título da Atividade:")
            data_entrega = st.date_input("Data de Entrega:", min_value=date.today(), value=date.today())
            descricao = st.text_area("Descrição Detalhada (Opcional):", height=100)
            publicar_button = st.form_submit_button("Publicar no Calendário")
            
            if publicar_button:
                if not titulo or not turma_selecionada_display:
                    st.error("Título e Turma são obrigatórios!")
                else:
                    id_turma_selecionada = turmas_professor[turmas_professor['turma_display'] == turma_selecionada_display].iloc[0]['id_turma']
                    resultado = adicionar_atividade(id_turma_selecionada, titulo, data_entrega, descricao)
                    if "SUCESSO" in resultado:
                        st.success(resultado)
                    else:
                        st.error(resultado)

    # --- ABA DE DELEÇÃO ---
    with tab_deletar:
        st.subheader("🗑️ Deletar Atividade")
        if df_atividades_visivel.empty:
            st.info("Nenhuma atividade publicada por você para ser deletada.")
        else:
            df_atividades_visivel['id_atividade'] = df_atividades_visivel['id_atividade'].astype(int)
            opcoes_delecao = [f"{row['id_atividade']} - {row['titulo']} (Turma: {row['turma_display']})" 
                              for index, row in df_atividades_visivel.iterrows()]
            selecao = st.selectbox("Selecione a atividade para deletar:", options=opcoes_delecao)
            
            # Garante que há uma seleção antes de tentar extrair o ID
            if selecao: 
                id_para_deletar = int(selecao.split(' - ')[0])
                if st.button(f"Confirmar Deleção do ID {id_para_deletar}", type="primary"):
                    resultado = deletar_atividade(id_para_deletar)
                    if "SUCESSO" in resultado:
                        st.success(resultado)
                        st.rerun() 
                    else:
                        st.error(resultado)
            else:
                 st.info("Nenhuma atividade selecionada para deleção.")


# --- Iniciar a Aplicação ---
menu_professor_streamlit()