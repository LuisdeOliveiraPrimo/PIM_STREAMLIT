# auth_utils.py
import streamlit as st

def show_custom_menu():
<<<<<<< HEAD
    # Esconde o menu de navegação padrão do Streamlit
=======
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] > ul {
                display: none;
            }
        </style>
        """, unsafe_allow_html=True)

<<<<<<< HEAD
    # Verifica se o usuário está logado, se não, chuta para a página principal
    if not st.session_state.get('logged_in', False):
        st.switch_page("main.py")

    # Mostra as informações do usuário logado
    st.sidebar.info(f"Usuário: *{st.session_state.user_info['nome_completo']}*")
    st.sidebar.info(f"Perfil: *{st.session_state.user_info['role']}*")
    
    # Botão de Logout
    if st.sidebar.button("Logout"):
        # Limpa toda a sessão
=======
    if not st.session_state.get('logged_in', False):
        st.switch_page("main.py")

    st.sidebar.info(f"Usuário: **{st.session_state.user_info['nome_completo']}**")
    st.sidebar.info(f"Perfil: **{st.session_state.user_info['role']}**")
    
    if st.sidebar.button("Logout"):
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("main.py")

    st.sidebar.header("Navegação")
    
<<<<<<< HEAD
    # Menus de navegação dinâmicos baseados no perfil ('role')
=======
>>>>>>> 2c890c1dde41bf62524c09774854234b3a8644dd
    role = st.session_state.user_info['role']

    if role == 'Aluno':
        if st.sidebar.button("🎓 Meu Painel"):
            st.switch_page("pages/painel_aluno.py")

    if role == 'Professor':
        if st.sidebar.button("🧑‍🏫 Meu Painel"):
            st.switch_page("pages/painel_professor.py")

    if role == 'Coordenação':
        if st.sidebar.button("📊 Painel de Coordenação"):
            st.switch_page("pages/painel_cordenação.py")
        if st.sidebar.button("🧑‍🏫 Painel do Professor"):
            st.switch_page("pages/painel_professor.py")
        if st.sidebar.button("🎓 Painel do Aluno"):
            st.switch_page("pages/painel_aluno.py")

    if role == 'Administração':
        if st.sidebar.button("👑 Painel de Administração"):
            st.switch_page("pages/painel_administração.py")
        if st.sidebar.button("📊 Painel de Coordenação"):
            st.switch_page("pages/painel_cordenação.py")
        if st.sidebar.button("🧑‍🏫 Painel do Professor"):
            st.switch_page("pages/painel_professor.py")
        if st.sidebar.button("🎓 Painel do Aluno"):
            st.switch_page("pages/painel_aluno.py")