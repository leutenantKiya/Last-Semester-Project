import streamlit as st
import script as sc
from registration import register
import app 

if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'page' not in st.session_state:
    st.session_state['page'] = 'login' 
    
st.set_page_config(
    page_title="Duta Comic - Login", # Beri judul halaman login
    page_icon="📚",
    layout="centered"
)

#login if no user 
def display_login_page():
    st.markdown(
        """
        <h2>Welcome to Duta Comic🖐️</h2>
        <p>Please Login before proceed any further</p>
        """,
        unsafe_allow_html=True
    )
    username_input = st.text_input("Username", key="username_login") 
    password_input = st.text_input("Password", type="password", key="password_login")

    login, register_col = st.columns([1, 0.4])
    with login:
        if st.button("Login", key="login_btn", type="primary"):
            if not username_input or not password_input:
                st.warning("Please enter your username and password first")
            else:
                is_correct = sc.check_user(username_input, password_input)
                if is_correct:
                    #change state
                    st.success("Login Berhasil!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username_input
                
                    st.rerun() 
                else:
                    st.error("Username atau password salah.")
                    
    with register_col:
        st.markdown("Don't have an account?")
        if st.button("Register"):
            st.session_state['page'] = 'register'
            st.rerun()

sc.create_table() 
#login succeeded
if st.session_state['logged_in']:
    app.main()
 # if we press register button   
elif st.session_state['page'] == 'register':
    register()
# default 
else:
    display_login_page()