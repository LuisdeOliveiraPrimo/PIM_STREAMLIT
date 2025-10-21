import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from auth_utils import show_custom_menu
import os
from datetime import datetime

# --- AUTENTICAÇÃO E MENU ---
show_custom_menu()

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide")

# --- ESTILO CSS PARA OS CARTÕES ---
st.markdown("""
<style>
.metric-card {
    background-color: #FAFAFA; padding: 1.5rem; border-radius: 10px; border: 1px solid #E0E0E0;
    text-align: center; color: #1E1E1E; height: 100%; display: flex; flex-direction: column; justify-content: center;
}
.metric-card .label { font-size: 1rem; color: #555555; margin-bottom: 0.5rem; }
.metric-card .value { font-size: 2.5rem; font-weight: 600; color: #000000; }
</style>
""", unsafe_allow_html=True)

st.title("🧑‍🏫 Painel do Professor")
st.write(f"Olá, Prof(a). *{st.session_state.user_info['nome_completo']}*!")

try:
    # --- CARREGAMENTO DE TODOS OS DADOS ---
    # CORREÇÃO: Caminhos absolutos e nomes de arquivo corretos
    df_usuarios = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\usuarios.csv')

    df_turmas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\turmas.csv')

    df_disciplinas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\diciplinas.csv') 

    df_matriculas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\matriculas.csv')

    df_notas = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\notas.csv')

    df_frequencia = pd.read_csv('C:\\Users\\luiso\\OneDrive\\Desktop\\PIM\\data\\frequencia.csv')
    
    # --- FILTRO PRINCIPAL: SELEÇÃO DE TURMA ---
    # CORREÇÃO: 'id_usuario'
    professor_id = st.session_state.user_info['id_usuario']
    
    # CORREÇÃO: 'id_professor'
    turmas_professor = df_turmas[df_turmas['id_professor'] == professor_id]
    
    # CORREÇÃO LÓGICA: Revertido para a lógica original que agora está correta
    turmas_professor = pd.merge(turmas_professor, df_disciplinas, on='id_disciplina')
    turmas_professor['turma_display'] = turmas_professor['nome_disciplina'] + " (" + turmas_professor['semestre'].astype(str) + ")"

    if turmas_professor.empty:
        st.warning("Você não está alocado em nenhuma turma.")
    else:
        turma_selecionada_display = st.selectbox(
            "Selecione uma de suas turmas para gerenciar:",
            turmas_professor['turma_display']
        )
        
        # CORREÇÃO: 'id_turma'
        id_turma_selecionada = turmas_professor[turmas_professor['turma_display'] == turma_selecionada_display].iloc[0]['id_turma']
        # CORREÇÃO: 'nome_disciplina'
        nome_disciplina_selecionada = turmas_professor[turmas_professor['turma_display'] == turma_selecionada_display].iloc[0]['nome_disciplina']

        st.markdown("---")

        # --- PREPARAÇÃO DOS DADOS DA TURMA SELECIONADA ---
        # CORREÇÃO: 'id_turma'
        matriculas_da_turma = df_matriculas[df_matriculas['id_turma'] == id_turma_selecionada]
        
        # CORREÇÃO: 'id_aluno' e 'id_usuario'
        alunos_na_turma = pd.merge(matriculas_da_turma, df_usuarios, left_on='id_aluno', right_on='id_usuario')
        
        # CORREÇÃO: 'id_matricula'
        notas_da_turma = df_notas[df_notas['id_matricula'].isin(matriculas_da_turma['id_matricula'])]
        
        # CORREÇÃO: 'id_matricula'
        frequencia_da_turma = df_frequencia[df_frequencia['id_matricula'].isin(matriculas_da_turma['id_matricula'])]

        # --- ABAS COM AS FUNCIONALIDADES ---
        tab1, tab2, tab3 = st.tabs(["Visão Geral", "Frequência", "Painel de Desempenho"])

        # --- ABA 1: VISÃO GERAL ---
        with tab1:
            st.subheader(f"Resumo da Turma: {nome_disciplina_selecionada}")
            
            n_alunos = len(alunos_na_turma)
            
            # CORREÇÃO: 'valor_nota'
            media_turma = notas_da_turma['valor_nota'].mean() if not notas_da_turma.empty else 0.0
            
            # CORREÇÃO: 'status_presenca'
            taxa_presenca_turma = ((frequencia_da_turma['status_presenca'] == 'Presente').sum() / len(frequencia_da_turma) * 100) if not frequencia_da_turma.empty else 0.0
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f'<div class="metric-card"><div class="label">Nº de Alunos</div><div class="value">{n_alunos}</div></div>', unsafe_allow_html=True)
            with c2:
                st.markdown(f'<div class="metric-card"><div class="label">Média da Turma</div><div class="value">{media_turma:.2f}</div></div>', unsafe_allow_html=True)
            with c3:
                st.markdown(f'<div class="metric-card"><div class="label">Taxa de Presença</div><div class="value">{taxa_presenca_turma:.1f}%</div></div>', unsafe_allow_html=True)

            st.markdown("---")
            
            st.subheader("Comparativo de Desempenho (P1 vs. P2)")
            # CORREÇÃO: 'tipo_avaliacao'
            notas_p1_p2 = notas_da_turma[notas_da_turma['tipo_avaliacao'].str.strip().str.lower().isin(['p1', 'p2'])]
            
            if len(notas_p1_p2['tipo_avaliacao'].str.strip().str.lower().unique()) > 1:
                # CORREÇÃO: 'tipo_avaliacao' e 'valor_nota'
                media_p1 = notas_p1_p2[notas_p1_p2['tipo_avaliacao'].str.strip().str.lower() == 'p1']['valor_nota'].mean()
                media_p2 = notas_p1_p2[notas_p1_p2['tipo_avaliacao'].str.strip().str.lower() == 'p2']['valor_nota'].mean()
                media_p1 = media_p1 if pd.notna(media_p1) else 0.0
                media_p2 = media_p2 if pd.notna(media_p2) else 0.0

                g1, g2 = st.columns(2)
                with g1:
                    fig_gauge_p1 = go.Figure(go.Indicator(
                        mode = "gauge+number", value = media_p1,
                        title = {'text': "Média P1", 'font': {'size': 24}},
                        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#636EFA"}},
                        number={'font': {'size': 40}}
                    ))
                    fig_gauge_p1.update_layout(height=250, margin=dict(l=10, r=10, t=80, b=10))
                    st.plotly_chart(fig_gauge_p1, use_container_width=True)
                with g2:
                    fig_gauge_p2 = go.Figure(go.Indicator(
                        mode = "gauge+number", value = media_p2,
                        title = {'text': "Média P2", 'font': {'size': 24}},
                        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#00CC96"}},
                        number={'font': {'size': 40}}
                    ))
                    fig_gauge_p2.update_layout(height=250, margin=dict(l=10, r=10, t=80, b=10))
                    st.plotly_chart(fig_gauge_p2, use_container_width=True)
            else:
                st.info("O comparativo P1 vs P2 estará disponível quando ambas as notas forem lançadas.")

            st.markdown("---")

            st.subheader("Ranking de Alunos")
            if not notas_da_turma.empty:
                # CORREÇÃO: 'id_matricula' e 'valor_nota'
                media_por_aluno = pd.merge(
                    notas_da_turma.groupby('id_matricula')['valor_nota'].mean().reset_index(), 
                    alunos_na_turma[['id_matricula', 'nome_completo']], 
                    on='id_matricula'
                )
                # CORREÇÃO: 'valor_nota'
                media_por_aluno = media_por_aluno.sort_values('valor_nota', ascending=False)
                
                # Renomeando para exibição
                media_por_aluno_display = media_por_aluno.rename(columns={'valor_nota': 'Média', 'nome_completo': 'Aluno'})
                
                r1, r2 = st.columns(2)
                with r1:
                    st.write("🏆 *Top 5 Alunos (Melhores Médias)*")
                    st.dataframe(media_por_aluno_display.head(5), use_container_width=True, hide_index=True, 
                                 column_config={"Média": st.column_config.NumberColumn(format="%.2f")})
                with r2:
                    st.write("⚠️ *Alunos que Precisam de Atenção*")
                    st.dataframe(media_por_aluno_display.tail(5).sort_values('Média', ascending=True), use_container_width=True, hide_index=True, 
                                 column_config={"Média": st.column_config.NumberColumn(format="%.2f")})
            else:
                st.info("As análises de ranking estarão disponíveis após o lançamento de notas.")
            
            st.markdown("---")
            
            st.subheader("Perfil Rápido do Aluno")
            aluno_selecionado = st.selectbox("Selecione um aluno para análise individual:", options=sorted(alunos_na_turma['nome_completo'].unique()))
            if aluno_selecionado:
                # CORREÇÃO: 'id_matricula'
                id_matricula_aluno = alunos_na_turma[alunos_na_turma['nome_completo'] == aluno_selecionado].iloc[0]['id_matricula']
                
                # CORREÇÃO: 'id_matricula'
                notas_do_aluno = notas_da_turma[notas_da_turma['id_matricula'] == id_matricula_aluno]
                
                # CORREÇÃO: 'valor_nota'
                media_aluno = notas_do_aluno['valor_nota'].mean() if not notas_do_aluno.empty else 0.0
                
                col_perfil1, col_perfil2 = st.columns(2)
                with col_perfil1:
                    fig_gauge_aluno = go.Figure(go.Indicator(
                        mode = "gauge+number", value = media_aluno,
                        title = {'text': f"Média de {aluno_selecionado.split()[0]}", 'font': {'size': 24}},
                        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#00CC96"}},
                        number={'font': {'size': 40}}
                    ))
                    fig_gauge_aluno.update_layout(height=250, margin=dict(l=10, r=10, t=80, b=10))
                    st.plotly_chart(fig_gauge_aluno, use_container_width=True)
                with col_perfil2:
                    fig_gauge_turma = go.Figure(go.Indicator(
                        mode = "gauge+number", value = media_turma,
                        title = {'text': "Média da Turma", 'font': {'size': 24}},
                        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "lightgray"}},
                        number={'font': {'size': 40}}
                    ))
                    fig_gauge_turma.update_layout(height=250, margin=dict(l=10, r=10, t=80, b=10))
                    st.plotly_chart(fig_gauge_turma, use_container_width=True)
        
        # --- ABA 2: GESTOR DE FREQUÊNCIA ---
        with tab2:
            st.header("Gestão de Frequência")
            st.write("Esta seção ainda está em desenvolvimento.")
            st.info("Aqui você poderá lançar e editar as frequências dos alunos para esta turma.")
            # ...

        # --- ABA 3: PAINEL DE DESEMPENHO ---
        with tab3:
            st.header("Gestão de Notas (Desempenho)")
            st.write("Esta seção ainda está em desenvolvimento.")
            st.info("Aqui você poderá lançar e editar as notas (P1, P2, Trabalhos) dos alunos.")
            # ...

except FileNotFoundError as e:
    st.error(f"Arquivo de dados não encontrado: {e}. Verifique se o caminho e o nome do arquivo estão corretos (ex: 'usuarios.csv', 'disciplinas.csv').")
except KeyError as e:
    st.error(f"Erro de Coluna: Uma coluna esperada não foi encontrada: {e}. Verifique se os seus CSVs têm todas as colunas necessárias (ex: 'id_usuario', 'id_aluno', 'id_matricula', 'valor_nota', 'status_presenca', etc.).")
except Exception as e:
    st.error(f"Ocorreu um erro ao processar os dados: {e}")