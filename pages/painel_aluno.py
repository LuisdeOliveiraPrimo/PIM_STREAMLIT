<<<<<<< HEAD
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar # Importa a nova biblioteca
from auth_utils import show_custom_menu
import os

# --- AUTENTICAÇÃO E MENU ---
# Isso verifica se o usuário está logado e mostra o menu lateral
show_custom_menu()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide")

# --- ESTILO CSS PARA OS CARTÕES ---
st.markdown("""
<style>
.metric-card {
    background-color: #FAFAFA;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #E0E0E0;
    text-align: center;
    color: #1E1E1E;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.metric-card .label {
    font-size: 1rem;
    color: #555555;
    margin-bottom: 0.5rem;
}
.metric-card .value {
    font-size: 2.5rem;
    font-weight: 600;
    color: #000000;
}
</style>
""", unsafe_allow_html=True)


st.title("🎓 Meu Painel")
st.write(f"Bem-vindo(a), *{st.session_state.user_info['nome_completo']}*!")

try:
    # --- CARREGAMENTO DE TODOS OS DADOS ---
    # CORREÇÃO: Caminhos absolutos e nome 'usuario.csv' (singular)
    df_usuarios = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\usuarios.csv')
    df_turmas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\turmas.csv')
    df_disciplinas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\diciplinas.csv')
    df_matriculas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\matriculas.csv')
    df_notas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\notas.csv')
    df_frequencia = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\frequencia.csv')
    
    # --- FILTRAGEM INICIAL DOS DADOS DO ALUNO LOGADO ---
    # CORREÇÃO: 'id_usuario' -> 'user_id' (do st.session_state)
    aluno_id = st.session_state.user_info['user_id'] 
    
    # CORREÇÃO: 'id_aluno' -> 'aluno_id' (do matriculas.csv)
    matriculas_aluno = df_matriculas[df_matriculas['aluno_id'] == aluno_id]
=======
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
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd

    if matriculas_aluno.empty:
        st.warning("Você não está matriculado em nenhuma turma.")
    else:
<<<<<<< HEAD
        # --- SEÇÃO 1: MEU RESUMO ---
        st.header("Meu Resumo")
        
        # CORREÇÃO: 'id_matricula' -> 'matricula_id'
        notas_aluno_geral = df_notas[df_notas['matricula_id'].isin(matriculas_aluno['matricula_id'])]
        # CORREÇÃO: 'valor_nota' -> 'nota'
        media_geral = notas_aluno_geral['nota'].mean() if not notas_aluno_geral.empty else 0.0
        
        disciplinas_cursando = len(matriculas_aluno)
        
        # CORREÇÃO: 'id_matricula' -> 'matricula_id'
        frequencia_aluno_geral = df_frequencia[df_frequencia['matricula_id'].isin(matriculas_aluno['matricula_id'])]
        
        if not frequencia_aluno_geral.empty:
            # CORREÇÃO: 'status_presenca' -> 'status'
            presente_geral = (frequencia_aluno_geral['status'] == 'Presente').sum()
            taxa_presenca_geral = (presente_geral / len(frequencia_aluno_geral)) * 100
        else:
            taxa_presenca_geral = 0.0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="label">Média Geral</div><div class="value">{media_geral:.2f}</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="label">Disciplinas Cursando</div><div class="value">{disciplinas_cursando}</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="label">Taxa de Presença Geral</div><div class="value">{taxa_presenca_geral:.1f}%</div></div>', unsafe_allow_html=True)

        st.markdown("---")

        # --- SEÇÃO 2: ANÁLISE POR DISCIPLINA ---
        st.header("Análise por Disciplina")
        
        # CORREÇÃO LÓGICA:
        # 1. 'id_turma' -> 'turma_id'
        # 2. Removemos a junção com 'df_disciplinas', pois 'df_turmas' já tem 'nome_turma'
        disciplinas_do_aluno = pd.merge(matriculas_aluno, df_turmas, on='turma_id')
        
        disciplina_selecionada = st.selectbox(
            "Selecione uma disciplina para ver os detalhes:",
            # CORREÇÃO: 'nome_disciplina' -> 'nome_turma'
            options=disciplinas_do_aluno['nome_turma'].unique()
        )

        if disciplina_selecionada:
            # CORREÇÃO: 'nome_disciplina' -> 'nome_turma'
            info_disciplina = disciplinas_do_aluno[disciplinas_do_aluno['nome_turma'] == disciplina_selecionada].iloc[0]
            # CORREÇÃO: 'id_matricula' -> 'matricula_id'
            id_matricula_selecionada = info_disciplina['matricula_id']
            # CORREÇÃO: 'id_turma' -> 'turma_id'
            id_turma_selecionada = info_disciplina['turma_id']

            col_d1, col_d2 = st.columns([1, 2])
            
            with col_d1:
                st.write("*Sua Frequência*")
                # CÓDIGO RESTAURADO E CORRIGIDO
                frequencia_disciplina = df_frequencia[df_frequencia['matricula_id'] == id_matricula_selecionada]
                if not frequencia_disciplina.empty:
                    frequencia_counts = frequencia_disciplina['status'].value_counts().reset_index()
                    frequencia_counts.columns = ['status', 'contagem']
                    fig_donut_disciplina = px.pie(frequencia_counts, names='status', values='contagem',
                                                  title=f'Frequência',
                                                  color='status', color_discrete_map={'Presente': '#4285F4', 'Ausente': '#EA4335'}, hole=0.4)
                    fig_donut_disciplina.update_layout(margin=dict(t=30, b=0, l=0, r=0))
                    st.plotly_chart(fig_donut_disciplina, use_container_width=True)
                else:
                    st.info("Nenhum registro de frequência para esta matéria.")

            with col_d2:
                st.write("*Suas Notas*")
                # CÓDIGO RESTAURADO E CORRIGIDO
                # CORREÇÃO: 'id_matricula' -> 'matricula_id'
                notas_disciplina = df_notas[df_notas['matricula_id'] == id_matricula_selecionada]
                if not notas_disciplina.empty:
                    # CORREÇÃO: 'tipo_avaliacao' -> 'avaliacao', 'valor_nota' -> 'nota'
                    notas_display = notas_disciplina[['avaliacao', 'nota']].rename(columns={'avaliacao': 'Avaliação', 'nota': 'Nota'})
                    st.dataframe(notas_display, use_container_width=True, hide_index=True)
                else:
                    st.info("Nenhuma nota lançada para esta matéria.")

        st.markdown("---")

        # --- SEÇÃO 3: HORÁRIOS E PROFESSORES ---
        with st.expander("Ver meus horários e professores"):
            # CÓDIGO RESTAURADO E CORRIGIDO
            # Juntamos com df_usuarios para pegar o nome do professor
            prof_info = pd.merge(disciplinas_do_aluno, df_usuarios, left_on='professor_id', right_on='user_id', suffixes=('_aluno', '_prof'))
            
            display_cols = ['nome_turma', 'nome_completo']
            st.dataframe(
                prof_info[display_cols].rename(columns={'nome_turma': 'Turma', 'nome_completo': 'Professor'}),
                use_container_width=True,
                hide_index=True
            )
            st.info("Informações de horários e salas serão adicionadas em breve.")

        
        st.markdown("---")

        # ######################################################################
        # ### NOVA SEÇÃO: CALENDÁRIO DE AULAS ###
        # ######################################################################
        st.header("Meu Calendário de Aulas")

        # Preparar os dados para o formato que o calendário espera
        # CORREÇÃO: 'id_matricula' -> 'matricula_id'
        aulas_do_aluno = df_frequencia[df_frequencia['matricula_id'].isin(matriculas_aluno['matricula_id'])]
        
        # CORREÇÃO: Ajuste na junção para usar as colunas corretas
        aulas_com_disciplina = pd.merge(
            aulas_do_aluno, 
            disciplinas_do_aluno[['matricula_id', 'nome_turma']], 
            on='matricula_id'
        )
        
        eventos_calendario = []
        for index, row in aulas_com_disciplina.iterrows():
            eventos_calendario.append({
                # CORREÇÃO: 'nome_disciplina' -> 'nome_turma'
                "title": row['nome_turma'], 
                "start": row['data_aula'],
                "end": row['data_aula'], # Para eventos de dia inteiro, start e end são iguais
            })

        # Configurações de aparência do calendário
        opcoes_calendario = {
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,timeGridWeek,timeGridDay",
            },
            "initialView": "dayGridMonth",
            "height": "700px", # Define a altura para o calendário ficar grande
        }

        # Renderiza o calendário
        calendar(events=eventos_calendario, options=opcoes_calendario)

except KeyError as e:
    st.error(f"ERRO DE COLUNA (KeyError): A coluna {e} não foi encontrada. Verifique os nomes das colunas nos seus arquivos CSV (ex: 'user_id', 'aluno_id', 'matricula_id', 'nota', 'status') e no código.")
=======
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
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd
except Exception as e:
    st.error(f"Ocorreu um erro: {e}")