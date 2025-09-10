import streamlit as st
import pandas as pd

# Verificar se o usuário está logado e se é um professor
if not st.session_state.get('logged_in') or st.session_state.user_info['role'] != 'Professor':
    st.error("Acesso negado. Por favor, faça o login como professor.")
    st.stop()

# --- CARREGAR DADOS ---
# É uma boa prática carregar os dados dentro de funções com cache para performance
@st.cache_data
def load_data():
    turmas_df = pd.read_csv('data/turmas.csv')
    matriculas_df = pd.read_csv('data/matriculas.csv')
    usuarios_df = pd.read_csv('data/usuarios.csv')
    return turmas_df, matriculas_df, usuarios_df

turmas_df, matriculas_df, usuarios_df = load_data()

# --- PÁGINA DO PROFESSOR ---
user_info = st.session_state.user_info
st.title(f"Bem-vindo(a) ao seu Painel, Prof. {user_info['nome_completo'].split(' ')[0]}!")

# Filtrar para encontrar as turmas do professor logado
professor_id = user_info['user_id']
minhas_turmas = turmas_df[turmas_df['professor_id'] == professor_id]

if minhas_turmas.empty:
    st.warning("Você não está alocado em nenhuma turma no momento.")
    st.stop()

# --- INTERFACE ---
st.header("Minhas Turmas")
turma_selecionada_nome = st.selectbox(
    "Selecione uma turma para gerenciar:",
    options=minhas_turmas['nome_turma'].unique()
)

# Obter ID da turma selecionada
turma_id_selecionada = minhas_turmas[minhas_turmas['nome_turma'] == turma_selecionada_nome]['turma_id'].iloc[0]

st.markdown("---")
st.subheader(f"Gerenciando a Turma: {turma_selecionada_nome}")

# Abas para Diário, Atividades, etc.
tab1, tab2 = st.tabs(["📊 Diário de Classe", "📝 Gestão de Atividades"])

with tab1:
    st.header("Alunos Matriculados e Desempenho")
    
    # Encontrar os alunos matriculados na turma selecionada
    matriculas_turma = matriculas_df[matriculas_df['turma_id'] == turma_id_selecionada]
    alunos_na_turma = usuarios_df[usuarios_df['user_id'].isin(matriculas_turma['aluno_id'])]
    
    if alunos_na_turma.empty:
        st.info("Nenhum aluno matriculado nesta turma ainda.")
    else:
        st.write(f"Total de alunos: {len(alunos_na_turma)}")
        
        # Aqui você implementaria a lógica para exibir/editar notas e frequência
        st.dataframe(alunos_na_turma[['nome_completo', 'username']])
        st.info("Funcionalidade de lançamento de notas e faltas será implementada aqui.")

with tab2:
    st.header("Publicar e Visualizar Atividades")
    st.info("Funcionalidade para publicar novas atividades e ver as entregas será implementada aqui.")