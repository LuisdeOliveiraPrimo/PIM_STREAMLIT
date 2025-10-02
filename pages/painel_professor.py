# pages/painel_professor.py
import streamlit as st
import pandas as pd
from auth_utils import show_custom_menu

show_custom_menu()

st.title("🧑‍🏫 Painel do Professor")
st.write(f"Olá, Prof(a). **{st.session_state.user_info['nome_completo']}**!")

try:
    df_turmas = pd.read_csv('data/turmas.csv')
    df_disciplinas = pd.read_csv('data/disciplinas.csv')
    df_matriculas = pd.read_csv('data/matriculas.csv')
    df_usuarios = pd.read_csv('data/usuarios.csv')
    
    professor_id = st.session_state.user_info['id_usuario']
    turmas_professor = df_turmas[df_turmas['id_professor'] == professor_id]
    turmas_professor = pd.merge(turmas_professor, df_disciplinas, on='id_disciplina')

    if turmas_professor.empty:
        st.warning("Você não está alocado em nenhuma turma.")
    else:
        st.header("Minhas Turmas")
        turma_selecionada_nome = st.selectbox(
            "Selecione uma turma para ver os detalhes:",
            turmas_professor['nome_disciplina']
        )
        
        id_turma_selecionada = turmas_professor[turmas_professor['nome_disciplina'] == turma_selecionada_nome].iloc[0]['id_turma']
        
        st.subheader(f"Alunos Matriculados em {turma_selecionada_nome}")
        
        alunos_na_turma = pd.merge(df_matriculas, df_usuarios, left_on='id_aluno', right_on='id_usuario')
        alunos_na_turma = alunos_na_turma[alunos_na_turma['id_turma'] == id_turma_selecionada]
        
        st.dataframe(alunos_na_turma[['nome_completo']], use_container_width=True)
        st.info("Em uma aplicação real, aqui você teria botões para lançar notas e frequência.")

except FileNotFoundError:
    st.error("Arquivos de dados não encontrados. Execute o script de geração de dados.")