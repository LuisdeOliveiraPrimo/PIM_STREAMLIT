# pages/painel_administração.py
import streamlit as st
import pandas as pd
from auth_utils import show_custom_menu

show_custom_menu()

st.title("👑 Painel de Administração")
st.warning("Área com acesso total ao sistema.")

try:
    df_usuarios = pd.read_csv('data/usuarios.csv')
    
    st.header("Gerenciamento de Usuários")
    
    filtro_nome = st.text_input("Filtrar usuários por nome:")
    
    if filtro_nome:
        usuarios_filtrados = df_usuarios[df_usuarios['nome_completo'].str.contains(filtro_nome, case=False, na=False)]
    else:
        usuarios_filtrados = df_usuarios
        
    st.dataframe(usuarios_filtrados, use_container_width=True)
    
    with st.expander("Ações Administrativas"):
        st.button("Criar Novo Usuário")
        st.button("Exportar Lista de Usuários")
        st.info("Em uma aplicação real, estes botões teriam funcionalidades para modificar a base de usuários.")

except FileNotFoundError:
    st.error("Arquivos de dados não encontrados. Execute o script de geração de dados.")