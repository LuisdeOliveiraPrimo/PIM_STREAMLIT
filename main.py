# main.py
import streamlit as st
import pandas as pd
from auth_utils import show_custom_menu

st.set_page_config(page_title="SIGA-U Login", page_icon="🎓", layout="centered")

def authenticate(username, password):
    try:
        df_usuarios = pd.read_csv('data/usuarios.csv')
        user_data = df_usuarios[(df_usuarios['username'] == username) & (df_usuarios['password'] == str(password))]
        if not user_data.empty:
            return user_data.iloc[0]
        return None
    except FileNotFoundError:
        return "FILE_NOT_FOUND"

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None

if st.session_state['logged_in']:
    st.success(f"Login realizado com sucesso como **{st.session_state.user_info['nome_completo']}**!")
    st.write("Navegue para o seu painel usando o menu à esquerda.")
    show_custom_menu()
else:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.title("🎓 SIGA-U: Sistema Integrado de Gestão")
    st.header("Login")
    
    with st.form("login_form"):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            user = authenticate(username, password)
            if user is not None and not isinstance(user, str):
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = user
                st.rerun()
            elif user == "FILE_NOT_FOUND":
                st.error("Erro: Bases de dados não encontradas. Execute o script `python scripts/gerar_dados.py` primeiro.")
            else:
                st.error("Usuário ou senha inválidos.")