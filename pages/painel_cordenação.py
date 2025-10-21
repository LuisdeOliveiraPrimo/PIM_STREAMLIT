# pages/painel_cordenação.py
import streamlit as st
import pandas as pd
<<<<<<< HEAD
import plotly.express as px
import plotly.graph_objects as go 

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide")

st.title("📊 Painel de Coordenação")
st.write("Uma ferramenta para análise e apoio à decisão acadêmica.")


# --- ESTILO CSS PARA OS CARTÕES (COM AJUSTE DE ALTURA) ---
st.markdown("""
<style>
.metric-card {
    background-color: #FAFAFA;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #E0E0E0;
    text-align: center;
    color: #1E1E1E;
    /* --- NOVAS PROPRIEDADES PARA ALTURA IGUAL --- */
    height: 100%; /* Força o cartão a preencher a altura da coluna */
    display: flex; /* Habilita o flexbox para alinhamento interno */
    flex-direction: column; /* Empilha os itens verticalmente */
    justify-content: center; /* Centraliza o conteúdo verticalmente */
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
.metric-card .delta {
    font-size: 1rem;
    font-weight: 500;
    margin-top: 0.5rem;
}
.delta-positive {
    color: #28a745; /* Verde */
}
.delta-negative {
    color: #dc3545; /* Vermelho */
}
</style>
""", unsafe_allow_html=True)


# --- CARREGAMENTO E PROCESSAMENTO DOS DADOS ---
try:
    # --- CAMINHOS ABSOLUTOS CONFORME SOLICITADO ---
    # NOTA: O nome 'usuario.csv' (singular) foi mantido 
    # com base nos dados que você enviou anteriormente (usuario / user_id...).
    df_usuarios = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\usuarios.csv')
    df_turmas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\turmas.csv')
    df_disciplinas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\diciplinas.csv')
    df_matriculas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\matriculas.csv')
    df_notas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\notas.csv')
    df_frequencia = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\frequencia.csv')


    # --- INICIALIZAÇÃO DO ESTADO DA SESSÃO ---
    if 'turma_selecionada' not in st.session_state:
        st.session_state.turma_selecionada = "Selecione uma turma..."

    # --- SEÇÃO 1: MÉTRICAS GERAIS ---
    st.header("Métricas Gerais")
    
    df_usuarios['role_tratado'] = df_usuarios['role'].str.strip().str.lower()
    total_alunos = df_usuarios[df_usuarios['role_tratado'] == 'aluno'].shape[0]
    total_professores = df_usuarios[df_usuarios['role_tratado'] == 'professor'].shape[0]
    total_turmas = df_turmas.shape[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="label">Total de Alunos</div><div class="value">{total_alunos}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="label">Total de Professores</div><div class="value">{total_professores}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="label">Total de Turmas</div><div class="value">{total_turmas}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # --- SEÇÃO 2: VISÃO GERAL DA INSTITUIÇÃO ---
    st.header("Visão Geral da Instituição")
    st.write("Os indicadores mais importantes sobre o engajamento e sucesso dos alunos.")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        total_presentes = (df_frequencia['status'] == 'Presente').sum()
        total_aulas_registradas = len(df_frequencia)
        taxa_presenca = (total_presentes / total_aulas_registradas) * 100 if total_aulas_registradas > 0 else 0

        fig_gauge_presenca = go.Figure(go.Indicator(
            mode = "gauge+number", value = taxa_presenca,
            title = {'text': "Taxa de Presença Geral", 'font': {'size': 24}},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#28a745"}},
            number={'suffix': "%", 'font': {'size': 40}}
        ))
        fig_gauge_presenca.update_layout(height=300)
        st.plotly_chart(fig_gauge_presenca, use_container_width=True)

    with col_graf2:
        NOTA_DE_CORTE_APROVACAO = 6.0
        aprovados = (df_notas['nota'] >= NOTA_DE_CORTE_APROVACAO).sum()
        total_notas = len(df_notas)
        taxa_aprovacao = (aprovados / total_notas) * 100 if total_notas > 0 else 0
        
        fig_gauge_aprovacao = go.Figure(go.Indicator(
            mode = "gauge+number", value = taxa_aprovacao,
            title = {'text': "Taxa de Aprovação Geral", 'font': {'size': 24}},
            gauge = {'axis': {'range': [None, 100]}, 'bar': {'color': "#4285F4"}},
            number={'suffix': "%", 'font': {'size': 40}}
        ))
        fig_gauge_aprovacao.update_layout(height=300)
        st.plotly_chart(fig_gauge_aprovacao, use_container_width=True)


    st.markdown("---")
    
    # --- SEÇÃO 3: ANÁLISE DE FREQUÊNCIA POR TURMA ---
    # CORREÇÃO LÓGICA: Alterado de "Matéria" para "Turma", pois o CSV 'turmas'
    # não possui mais a chave 'id_disciplina' para fazer a junção.
    st.header("Análise de Frequência por Turma")
    frequencia_com_turma = pd.merge(df_frequencia, df_matriculas, on='matricula_id')
    frequencia_com_turma = pd.merge(frequencia_com_turma, df_turmas, on='turma_id')
    
    # Usamos 'nome_turma' que já é descritivo
    lista_turmas_freq = sorted(frequencia_com_turma['nome_turma'].unique())
    turma_selecionada_freq = st.selectbox("Selecione a Turma para análise de frequência:", options=lista_turmas_freq)

    if turma_selecionada_freq:
        dados_filtrados_turma_freq = frequencia_com_turma[frequencia_com_turma['nome_turma'] == turma_selecionada_freq]
        frequencia_turma_counts = dados_filtrados_turma_freq['status'].value_counts().reset_index()
        frequencia_turma_counts.columns = ['status', 'contagem']
        fig_donut_turma = px.pie(frequencia_turma_counts, names='status', values='contagem', 
                                   title=f'Taxa de Presença em {turma_selecionada_freq}', 
                                   color='status', color_discrete_map={'Presente': '#4285F4', 'Ausente': '#EA4335'}, hole=0.4)
        st.plotly_chart(fig_donut_turma, use_container_width=True)

    st.markdown("---")
    
    # --- SEÇÃO 4: ANÁLISE DE NOTAS (P1 & P2) POR TURMA ---
    st.header("Análise de Notas (P1 e P2) por Turma")
    
    # CORREÇÃO LÓGICA: O 'nome_turma' do seu CSV já é o nome de exibição.
    # Removemos o merge com 'disciplinas' e a concatenação com 'semestre'
    # pois essas colunas não existem mais no 'turmas.csv'.
    turmas_com_disciplinas = df_turmas.copy()
    turmas_com_disciplinas['turma_display'] = turmas_com_disciplinas['nome_turma']
    lista_turmas_notas = sorted(turmas_com_disciplinas['turma_display'].unique())

    st.selectbox("Selecione uma turma para ver as médias e analisar os alunos:", options=["Selecione uma turma..."] + lista_turmas_notas, key="turma_selecionada")

    if st.session_state.turma_selecionada != "Selecione uma turma...":
        turma_id_selecionada = turmas_com_disciplinas[turmas_com_disciplinas['turma_display'] == st.session_state.turma_selecionada]['turma_id'].iloc[0]
        matriculas_da_turma = df_matriculas[df_matriculas['turma_id'] == turma_id_selecionada]
        
        if not matriculas_da_turma.empty:
            notas_da_turma = df_notas[df_notas['matricula_id'].isin(matriculas_da_turma['matricula_id'])]
            
            # CORREÇÃO: 'tipo_avaliacao' -> 'avaliacao'
            # Ajustado para os nomes das avaliações que você enviou ('Prova 1', 'Trabalho Final')
            media_p1 = notas_da_turma[notas_da_turma['avaliacao'].str.strip().str.lower() == 'prova 1']['nota'].mean()
            media_p2 = notas_da_turma[notas_da_turma['avaliacao'].str.strip().str.lower() == 'trabalho final']['nota'].mean()
            
            media_p1 = media_p1 if pd.notna(media_p1) else 0.0
            media_p2 = media_p2 if pd.notna(media_p2) else 0.0
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(f'<div class="metric-card"><div class="label">Média Prova 1 da Turma</div><div class="value">{media_p1:.2f}</div></div>', unsafe_allow_html=True)
            with col_p2:
                st.markdown(f'<div class="metric-card"><div class="label">Média Trab. Final da Turma</div><div class="value">{media_p2:.2f}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Não há alunos matriculados nesta turma para calcular as médias.")

    st.markdown("---")

    # --- SEÇÃO 5: ESTUDO DE PERFIL DE ALUNO ---
    st.header("Estudo de Perfil de Aluno")
    NOME_CORRETO_DA_COLUNA = 'nome_completo' # Esta coluna existe no 'usuario.csv'

    if st.session_state.turma_selecionada != "Selecione uma turma...":
        st.info(f"Analisando alunos da turma: *{st.session_state.turma_selecionada}*")
        turma_id_perfil = turmas_com_disciplinas[turmas_com_disciplinas['turma_display'] == st.session_state.turma_selecionada]['turma_id'].iloc[0]
        alunos_na_turma = df_matriculas[df_matriculas['turma_id'] == turma_id_perfil]
        
        # CORREÇÃO: 'id_aluno' -> 'aluno_id' (em matriculas)
        # CORREÇÃO: 'id_usuario' -> 'user_id' (em usuarios)
        alunos_info = pd.merge(alunos_na_turma, df_usuarios, left_on='aluno_id', right_on='user_id')
        
        if NOME_CORRETO_DA_COLUNA not in alunos_info.columns:
            st.error(f"Erro: A coluna '{NOME_CORRETO_DA_COLUNA}' não foi encontrada em 'usuario.csv'. Verifique o nome da coluna.")
        else:
            lista_alunos_perfil = sorted(alunos_info[NOME_CORRETO_DA_COLUNA].unique())
            aluno_selecionado_perfil = st.selectbox("Selecione o(a) aluno(a) para gerar o relatório:", options=["Selecione..."] + lista_alunos_perfil, key="aluno_perfil")

            if aluno_selecionado_perfil != "Selecione...":
                # CORREÇÃO: 'id_aluno' -> 'aluno_id'
                id_aluno_selecionado = alunos_info[alunos_info[NOME_CORRETO_DA_COLUNA] == aluno_selecionado_perfil]['aluno_id'].iloc[0]
                
                with st.container(border=True):
                    st.subheader(f"Relatório de Desempenho: {aluno_selecionado_perfil}")
                    
                    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
                    matriculas_do_aluno = df_matriculas[df_matriculas['aluno_id'] == id_aluno_selecionado]
                    notas_do_aluno_geral = df_notas[df_notas['matricula_id'].isin(matriculas_do_aluno['matricula_id'])]
                    media_geral_aluno = notas_do_aluno_geral['nota'].mean()
                    media_geral_aluno = media_geral_aluno if pd.notna(media_geral_aluno) else 0.0
                    
                    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
                    matricula_id_na_turma = alunos_info[(alunos_info['aluno_id'] == id_aluno_selecionado) & (alunos_info['turma_id'] == turma_id_perfil)]['matricula_id'].iloc[0]
                    notas_aluno_na_turma = df_notas[df_notas['matricula_id'] == matricula_id_na_turma]
                    media_aluno_na_turma = notas_aluno_na_turma['nota'].mean()
                    media_aluno_na_turma = media_aluno_na_turma if pd.notna(media_aluno_na_turma) else 0.0
                    
                    matriculas_da_turma_perfil = df_matriculas[df_matriculas['turma_id'] == turma_id_perfil]
                    notas_da_turma_geral = df_notas[df_notas['matricula_id'].isin(matriculas_da_turma_perfil['matricula_id'])]
                    media_geral_turma = notas_da_turma_geral['nota'].mean()
                    media_geral_turma = media_geral_turma if pd.notna(media_geral_turma) else 0.0
                    
                    frequencia_aluno = df_frequencia[df_frequencia['matricula_id'] == matricula_id_na_turma]
                    if not frequencia_aluno.empty:
                        faltas = (frequencia_aluno['status'] == 'Ausente').sum()
                        total_aulas = len(frequencia_aluno)
                        percentual_faltas = (faltas / total_aulas) * 100 if total_aulas > 0 else 0
                    else:
                        percentual_faltas = 0
                    
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.markdown(f'<div class="metric-card"><div class="label" title="Média de notas do aluno em todas as disciplinas.">Média Geral do Aluno ⓘ</div><div class="value">{media_geral_aluno:.2f}</div></div>', unsafe_allow_html=True)
                    with col_m2:
                        delta = media_aluno_na_turma - media_geral_turma
                        delta_color_class = "delta-positive" if delta >= 0 else "delta-negative"
                        arrow = "▲" if delta >= 0 else "▼"
                        help_text = f"A média da turma é {media_geral_turma:.2f}. O valor abaixo indica a diferença."
                        st.markdown(f'''<div class="metric-card"><div class="label" title="{help_text}">Média na Matéria vs. Turma ⓘ</div><div class="value">{media_aluno_na_turma:.2f}</div><div class="delta {delta_color_class}">{arrow} {delta:.2f}</div></div>''', unsafe_allow_html=True)
                    with col_m3:
                        st.markdown(f'<div class="metric-card"><div class="label">Taxa de Ausência na Matéria</div><div class="value">{percentual_faltas:.1f}%</div></div>', unsafe_allow_html=True)

                    st.markdown("---")
                    
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        st.write("*Notas Detalhadas na Matéria*")
                        # CORREÇÃO: 'tipo_avaliacao' -> 'avaliacao'
                        notas_display = notas_aluno_na_turma[['avaliacao', 'nota']].rename(columns={'avaliacao': 'Avaliação', 'nota': 'Nota'})
                        st.dataframe(notas_display, use_container_width=True, hide_index=True)
                    with col_t2:
                        st.write("*Frequência Detalhada na Matéria*")
                        if not frequencia_aluno.empty:
                            detalhes_frequencia = frequencia_aluno['status'].value_counts().reset_index()
                            detalhes_frequencia.columns = ['Status', 'Total de Aulas']
                            st.dataframe(detalhes_frequencia, use_container_width=True, hide_index=True)
                        else:
                            st.info("Nenhum registro de frequência encontrado.")
    else:
        st.info("👆 Selecione uma turma na seção 'Análise de Notas' para começar a analisar o perfil dos alunos.")
    
    st.markdown("---")

    # --- SEÇÃO 6: ALUNOS QUE PRECISAM DE ATENÇÃO ---
    st.header("Alunos que Precisam de Atenção")
    st.write("Use os filtros para identificar proativamente alunos com baixo desempenho e alta taxa de ausência.")

    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
    media_geral_por_aluno = pd.merge(df_notas, df_matriculas, on='matricula_id').groupby('aluno_id')['nota'].mean().reset_index()
    media_geral_por_aluno.rename(columns={'nota': 'media_geral'}, inplace=True)
    
    freq_com_alunos = pd.merge(df_frequencia, df_matriculas, on='matricula_id')
    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
    ausencias = freq_com_alunos[freq_com_alunos['status'] == 'Ausente'].groupby('aluno_id').size()
    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
    total_aulas = freq_com_alunos.groupby('aluno_id').size()
    
    taxa_ausencia = ((ausencias / total_aulas) * 100).fillna(0).reset_index(name='taxa_ausencia_%')
    
    # CORREÇÃO: 'id_aluno' -> 'aluno_id'
    df_risco = pd.merge(media_geral_por_aluno, taxa_ausencia, on='aluno_id', how='outer').fillna(0)
    
    # CORREÇÃO: 'id_aluno' -> 'aluno_id' (em df_risco)
    # CORREÇÃO: 'id_usuario' -> 'user_id' (em df_usuarios)
    df_risco = pd.merge(df_risco, df_usuarios, left_on='aluno_id', right_on='user_id')

    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        nota_corte = st.slider("Mostrar alunos com média abaixo de:", min_value=0.0, max_value=10.0, value=6.0, step=0.5)
    with col_filtro2:
        ausencia_corte = st.slider("E com taxa de ausência acima de (%):", min_value=0, max_value=100, value=25, step=5)

    alunos_em_risco = df_risco[(df_risco['media_geral'] < nota_corte) & (df_risco['taxa_ausencia_%'] > ausencia_corte)]
    
    if not alunos_em_risco.empty and NOME_CORRETO_DA_COLUNA in alunos_em_risco.columns:
        st.dataframe(alunos_em_risco[[NOME_CORRETO_DA_COLUNA, 'media_geral', 'taxa_ausencia_%']].rename(columns={NOME_CORRETO_DA_COLUNA: 'Nome do Aluno', 'media_geral': 'Média Geral', 'taxa_ausencia_%': 'Taxa de Ausência (%)'}), use_container_width=True)
    else:
        st.success("Nenhum aluno encontrado com os critérios de risco selecionados.")

# --- TRATAMENTO DE ERROS ---
except FileNotFoundError as e:
    st.error(f"Arquivo de dados não encontrado: {e}. Verifique se o caminho e o nome do arquivo estão corretos.")
except KeyError as e:
    st.error(f"Erro de Coluna: Uma coluna esperada não foi encontrada: {e}. Verifique se os seus CSVs (ex: 'usuario.csv', 'notas.csv') têm todas as colunas necessárias ('user_id', 'aluno_id', 'avaliacao', etc.).")
except Exception as e:
    st.error(f"Ocorreu um erro ao processar os dados: {e}")
=======
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
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd
