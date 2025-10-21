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
from datetime import date
from auth_utils import show_custom_menu
from config import get_csv_path

# --- Configuração da Página ---
# CORREÇÃO: st.set_page_config() deve ser o primeiro comando Streamlit
st.set_page_config(layout="wide")

# --- Autenticação e Menu ---
show_custom_menu()

# Define o nome do arquivo CSV

# ==========================================================
# FUNÇÃO DE CONSULTA (CSV RELACIONAL)
# ==========================================================

def get_prazos_aluno(aluno_id):
    """
    Recupera as atividades com prazos futuros para as turmas do aluno.
    Retorna um DataFrame processado ou None em caso de erro.
    """
    
    hoje = date.today().isoformat()
    
    try:
        # 1. Carregar todos os dados necessários
        df_atividades = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\atividades.csv')
        df_turmas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\turmas.csv')
        df_disciplinas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\diciplinas.csv') 
        df_matriculas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\matriculas.csv')

        # 2. Encontrar as turmas do aluno
        turmas_do_aluno = df_matriculas[df_matriculas['id_aluno'] == aluno_id]['id_turma'].unique()
        
        if len(turmas_do_aluno) == 0:
            return pd.DataFrame() # Aluno não está matriculado

        # 3. Filtrar atividades apenas para essas turmas e que sejam futuras
        df_atividades_aluno = df_atividades[
            (df_atividades['id_turma'].isin(turmas_do_aluno)) &
            (df_atividades['data_entrega'] >= hoje)
        ]
        
        if df_atividades_aluno.empty:
            return pd.DataFrame() # Nenhuma atividade futura para este aluno

        # 4. Enriquecer com nomes das disciplinas
        df_merged = pd.merge(df_atividades_aluno, df_turmas, on='id_turma')
        df_merged = pd.merge(df_merged, df_disciplinas, on='id_disciplina')
        
        # 5. Ordenar por data
        df_merged = df_merged.sort_values(by='data_entrega', ascending=True)
        return df_merged
            
    except (FileNotFoundError, pd.errors.EmptyDataError):
        st.error(f"ERRO: Um arquivo de dados (como 'atividades.csv') não foi encontrado.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao acessar os dados: {e}")
        return None

# ==========================================================
# FUNÇÃO PRINCIPAL DE EXIBIÇÃO
# ==========================================================

def exibir_calendario_streamlit():
    st.title("📚 Calendário de Prazos (Visão do Aluno)")
    st.markdown("Veja todas as atividades com prazos a partir de hoje.")
    
    aluno_id = st.session_state.user_info['id_usuario']
    df_atividades = get_prazos_aluno(aluno_id)
    
    if df_atividades is None:
        return # Erro já foi mostrado pela função get_prazos_aluno

    if df_atividades.empty:
        st.info("🎉 Nenhuma atividade ou prazo futuro agendado para suas turmas no momento. Aproveite!")
        return

    # Processa os dados para exibição (cálculo de dias restantes)
    dados_processados = []
    
    for _, row in df_atividades.iterrows():
        try:
            data_entrega = date.fromisoformat(row['data_entrega'])
            hoje = date.today()
            dias_restantes_int = (data_entrega - hoje).days
            
            if dias_restantes_int == 0:
                dias_restantes = "HOJE (Dia da Entrega!)"
            elif dias_restantes_int == 1:
                dias_restantes = "1 dia"
            else:
                dias_restantes = f"{dias_restantes_int} dias"
        except ValueError:
            dias_restantes = "Data Inválida"

        dados_processados.append({
            "Disciplina": row['nome_disciplina'],
            "Título da Atividade": row['titulo'],
            "Prazo de Entrega": row['data_entrega'],
            "Dias Restantes": dias_restantes,
            "Detalhes": row['descricao'] or "Sem detalhes"
        })

    df_display = pd.DataFrame(dados_processados)
    
    st.subheader(f"Total de {len(df_display)} Atividades Futuras Encontradas")
    st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader("Visualização Detalhada por Atividade")
    
    for _, row in df_display.iterrows():
        with st.expander(f"**{row['Título da Atividade']}** - {row['Disciplina']} (Prazo: **{row['Prazo de Entrega']}** - Faltam: {row['Dias Restantes']})"):
            st.markdown(f"**Detalhes da Atividade:**")
            st.info(row['Detalhes'])
            
# --- Iniciar a Aplicação ---
exibir_calendario_streamlit()