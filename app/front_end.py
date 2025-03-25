import streamlit as st
from app.middle_end import gerar_configuracao_final, get_presets_list, get_supported_analyses, get_max_colunas

def main_interface():
    st.title("📊 Data Fake – Geração de Datasets Sintéticos")

    modo = st.radio("Modo de Geração", ["Geração Simples", "Geração Customizada"])
    preset_nome = st.selectbox("Escolha o preset", get_presets_list())

    analise = st.selectbox("Tipo de análise", get_supported_analyses(preset_nome))
    max_colunas = get_max_colunas(preset_nome)
    n_colunas = st.slider("Número de colunas", 1, max_colunas, min(8, max_colunas))
    n_linhas = st.number_input("Número de linhas", 100, 1_000_000, step=1000)

    if modo == "Geração Customizada":
        st.markdown("⚙️ Customizações futuras aqui...")

    if st.button("Gerar Dataset"):
        config = gerar_configuracao_final(preset_nome, analise, n_colunas, n_linhas)
        st.json(config)
