# .app.py

import streamlit as st
from app.front_end import main_interface

# Config inicial de pagina
st.set_page_config(
    page_title="Data Fake - Gerador de Dados Aleatórios",
    page_icon ="📊",
    layout="centered"
)

# Executa a interface principal no modulo front_end
main_interface()
