import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="SIGA-U Login",
    page_icon="🎓",
    layout="centered"
)

# Função de autenticação
def authenticate(username, password):
    try:
        df_usuarios = pd.read_csv('data/usuarios.csv')
        user_data = df_usuarios[(df_usuarios['username'] == username) & (df_usuarios['password'] == str(password))]
        if not user_data.empty:
            return user_data.iloc[0]
        return None
    except FileNotFoundError:
        return "FILE_NOT_FOUND"

# Inicialização do estado da sessão
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_info'] = None

# Se o usuário já estiver logado, mostre uma mensagem e o link para o painel.
if st.session_state['logged_in']:
    st.success(f"Login realizado com sucesso como **{st.session_state.user_info['nome_completo']}**!")
    st.write("Navegue para o seu painel usando o menu à esquerda.")
    st.sidebar.info(f"Usuário: **{st.session_state.user_info['nome_completo']}**")
    st.sidebar.info(f"Perfil: **{st.session_state.user_info['role']}**")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Se não estiver logado, mostra o formulário de login
else:
    st.title("🎓 SIGA-U: Sistema Integrado de Gestão")
    st.header("Login")
    
    with st.form("login_form"):
        username = st.text_input("Usuário", key="login_username")
        password = st.text_input("Senha", type="password", key="login_password")
        submitted = st.form_submit_button("Entrar")

        if submitted:
            user = authenticate(username, password)
            if user is not None and not isinstance(user, str):
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = user
                st.rerun()
            elif user == "FILE_NOT_FOUND":
                st.error("Erro: Arquivo de usuários não encontrado. Execute o script de geração de dados.")
            else:
                st.error("Usuário ou senha inválidos.")