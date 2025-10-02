# pages/painel_cordenação.py
import streamlit as st
import pandas as pd
from auth_utils import show_custom_menu

show_custom_menu()

st.title("📊 Painel de Coordenação")
st.write("Visão geral dos dados acadêmicos.")

try:
    df_usuarios = pd.read_csv('data/usuarios.csv')
    df_turmas = pd.read_csv('data/turmas.csv')
    df_disciplinas = pd.read_csv('data/disciplinas.csv')
    df_matriculas = pd.read_csv('data/matriculas.csv')
    df_notas = pd.read_csv('data/notas.csv')
    
    st.header("Métricas Gerais")
    total_alunos = df_usuarios[df_usuarios['role'] == 'Aluno'].shape[0]
    total_professores = df_usuarios[df_usuarios['role'] == 'Professor'].shape[0]
    total_turmas = df_turmas.shape[0]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Alunos", total_alunos)
    col2.metric("Total de Professores", total_professores)
    col3.metric("Total de Turmas", total_turmas)
    
    st.header("Desempenho Médio por Turma")
    
    notas_com_turmas = pd.merge(df_notas, df_matriculas, on='id_matricula')
    media_por_turma = notas_com_turmas.groupby('id_turma')['valor_nota'].mean().reset_index()
    media_por_turma = pd.merge(media_por_turma, df_turmas, on='id_turma')
    media_por_turma = pd.merge(media_por_turma, df_disciplinas, on='id_disciplina')
    media_por_turma.rename(columns={'valor_nota': 'Média da Turma'}, inplace=True)
    
    st.dataframe(media_por_turma[['nome_disciplina', 'semestre', 'Média da Turma']], use_container_width=True)
    st.bar_chart(media_por_turma.set_index('nome_disciplina')['Média da Turma'])

except FileNotFoundError:
    st.error("Arquivos de dados não encontrados. Execute o script de geração de dados.")