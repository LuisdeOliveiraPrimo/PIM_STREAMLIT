# pages/painel_aluno.py
import streamlit as st
import pandas as pd
from auth_utils import show_custom_menu
import os

show_custom_menu()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
def get_data_path(filename):
    return os.path.join(PROJECT_ROOT, "data", filename)

st.title("🎓 Painel do Aluno")
st.write(f"Bem-vindo(a), **{st.session_state.user_info['nome_completo']}**!")

try:
    df_matriculas = pd.read_csv(get_data_path('matriculas.csv'))
    df_turmas = pd.read_csv(get_data_path('turmas.csv'))
    df_disciplinas = pd.read_csv(get_data_path('disciplinas.csv'))
    df_usuarios = pd.read_csv(get_data_path('usuarios.csv'))
    df_notas = pd.read_csv(get_data_path('notas.csv'))

    aluno_id = st.session_state.user_info['id_usuario']
    matriculas_aluno = df_matriculas[df_matriculas['id_aluno'] == aluno_id]

    if matriculas_aluno.empty:
        st.warning("Você não está matriculado em nenhuma turma.")
    else:
        turmas_aluno = pd.merge(matriculas_aluno, df_turmas, on='id_turma')
        
        # --- FERRAMENTA DE DEPURAÇÃO ---
        # Verifique a saída disso na sua tela para encontrar o nome de coluna errado.
        with st.expander("🔍 Verificando Colunas Antes do Merge (Depuração)"):
            st.write("**Colunas na tabela `turmas_aluno`:**")
            st.write(turmas_aluno.columns.tolist())
            st.write("**Colunas na tabela `df_disciplinas`:**")
            st.write(df_disciplinas.columns.tolist())
        # --------------------------------

        # A linha abaixo é a que está causando o erro.
        # Compare a saída acima com a coluna 'id_disciplina' que estamos usando aqui.
        turmas_aluno = pd.merge(turmas_aluno, df_disciplinas, on='id_disciplina')
        
        turmas_aluno = pd.merge(turmas_aluno, df_usuarios, left_on='id_professor', right_on='id_usuario')

        st.header("Minhas Turmas e Horários")
        turmas_aluno.rename(columns={'nome_completo': 'Nome do Professor'}, inplace=True)
        st.dataframe(turmas_aluno[['nome_disciplina', 'Nome do Professor', 'horario_sala']], use_container_width=True)

        st.header("Minhas Notas")
        notas_aluno = pd.merge(matriculas_aluno, df_notas, on='id_matricula')
        notas_com_disciplina = pd.merge(notas_aluno, turmas_aluno[['id_turma', 'nome_disciplina']], on='id_turma')
        st.dataframe(notas_com_disciplina[['nome_disciplina', 'tipo_avaliacao', 'valor_nota']], use_container_width=True)

except KeyError as e:
    st.error(f"ERRO DE COLUNA (KeyError): A coluna {e} não foi encontrada. Verifique os nomes das colunas nos seus arquivos CSV e no código.")
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")