import streamlit as st
import utils

utils.validar_login()
utils.validar_nivel_acesso("gerente")

st.write(st.session_state)