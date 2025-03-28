import streamlit as st
import os

# ==============================
# CONFIGURAÇÃO GLOBAL
# ==============================

def configurar_pagina():
    st.set_page_config(
        page_title="Data Fake",
        page_icon="📊",
        layout="centered"
    )
    st.title("📊 Data Fake")
    st.markdown("---")

# ==============================
# GERAÇÃO SIMPLES
# ==============================

def interface_geracao_simples(presets_disponiveis: list[str]):
    st.subheader("🧪 Geração Simples")
    st.markdown("Configure rapidamente um dataset com base em um preset.")

    col1, col2 = st.columns(2)

    with col1:
        preset = st.selectbox("🔧 Escolha a categoria (preset)", presets_disponiveis)
        tipo_analise = st.selectbox("🎯 Tipo de Análise", ["EDA", "Regressão", "Classificação", "Cluster"])
    
    with col2:
        qtd_linhas = st.slider("📏 Quantidade de Linhas", min_value=100, max_value=500_000, value=1000, step=100)
        # A quantidade máxima de colunas será ajustada dinamicamente com base no preset
        qtd_colunas = st.slider("🔢 Quantidade de Colunas", min_value=2, max_value=15, value=8)

    return {
        "modo": "simples",
        "preset": preset,
        "tipo_analise": tipo_analise,
        "qtd_linhas": qtd_linhas,
        "qtd_colunas": qtd_colunas
    }

# ==============================
# GERAÇÃO CUSTOMIZADA
# ==============================

def interface_geracao_customizada(presets_disponiveis: list[str]):
    st.subheader("🧪 Geração Customizada")
    st.markdown("Controle total sobre a geração de dados.")

    col1, col2 = st.columns(2)

    with col1:
        preset = st.selectbox("🔧 Escolha a categoria (preset)", presets_disponiveis, key="preset_custom")
        tipo_analise = st.selectbox("🎯 Tipo de Análise", ["EDA", "Regressão", "Classificação", "Cluster"], key="analise_custom")
    
    with col2:
        qtd_linhas = st.slider("📏 Quantidade de Linhas", min_value=100, max_value=500_000, value=1000, step=100, key="linhas_custom")
        qtd_colunas = st.slider("🔢 Quantidade de Colunas", min_value=2, max_value=15, value=8, key="colunas_custom")

    st.markdown("#### 🧬 Integridade dos Dados (global)")
    with st.expander("Configurações de Integridade"):
        duplicados = st.checkbox("🔁 Permitir Duplicados", value=False)
        missings = st.checkbox("📉 Permitir Missing Values", value=False)
        outliers = st.checkbox("🚨 Permitir Outliers", value=False)
        distribuicao = st.selectbox("📊 Distribuição dos Dados Numéricos", ["Normal", "Left-Skewed", "Right-Skewed", "Uniforme", "Aleatória"])

    st.markdown("#### 🎯 Target (dependente da análise)")
    with st.expander("Configuração da Target"):
        if tipo_analise == "Regressão":
            integridade_target = st.slider("🔧 Dificuldade de previsão (ruído)", 0, 100, 30)
            target_missing = st.checkbox("Permitir missing na target", value=False)
            target_outliers = st.checkbox("Permitir outliers na target", value=False)
        elif tipo_analise == "Classificação":
            balanceamento = st.selectbox("⚖️ Balanceamento", ["Balanceado (50/50)", "Aleatório", "Desbalanceado"])
            dummies = st.checkbox("🔢 Dummyficar classes?", value=False)
        elif tipo_analise == "EDA":
            st.info("No modo EDA, as configurações globais serão aplicadas.")
        elif tipo_analise == "Cluster":
            st.info("Cluster não utiliza target explícita.")

    return {
        "modo": "customizado",
        "preset": preset,
        "tipo_analise": tipo_analise,
        "qtd_linhas": qtd_linhas,
        "qtd_colunas": qtd_colunas,
        "integridade": {
            "duplicados": duplicados,
            "missings": missings,
            "outliers": outliers,
            "distribuicao": distribuicao
        },
        "target": {
            "modo_regressao": {
                "ruido": integridade_target if tipo_analise == "Regressão" else None,
                "missings": target_missing if tipo_analise == "Regressão" else None,
                "outliers": target_outliers if tipo_analise == "Regressão" else None,
            },
            "modo_classificacao": {
                "balanceamento": balanceamento if tipo_analise == "Classificação" else None,
                "dummies": dummies if tipo_analise == "Classificação" else None
            }
        }
    }

# ==============================
# FUNÇÃO PRINCIPAL DE EXIBIÇÃO
# ==============================

def exibir_interface(presets_disponiveis: list[str]):
    configurar_pagina()

    modo = st.radio("🔄 Escolha o Modo de Geração", ["Geração Simples", "Geração Customizada"])

    if modo == "Geração Simples":
        config_usuario = interface_geracao_simples(presets_disponiveis)
    else:
        config_usuario = interface_geracao_customizada(presets_disponiveis)

    gerar = st.button("🚀 Gerar Dataset")

    if gerar:
        return config_usuario  # Isso será passado ao constructor.py
    return None
