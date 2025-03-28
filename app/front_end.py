import streamlit as st

# --- Modo Geração Simples ---
def interface_geracao_simples(presets_disponiveis: list):
    st.subheader("Geração Simples")
    st.markdown("""Configure um dataset simples com base em um preset.""")
    st.markdown('')

    preset = st.selectbox('Escolha uma categoria (preset):', presets_disponiveis,
                              help="""O preset vai definir qual é o tipo dos dados que você quer gerar e quais colunas esses dados terão.""")
    tipo_analise = st.selectbox("Tipo de Análise", ["EDA", "Regressão", "Classificação", "Cluster", "Inferência"],
                                    index=0,
                                    help="""
                                    O tipo de análise vai determinar alguns elementos importantes, como a estrutura geral dos dados, se ele vai ter uma variável resposta, etc.
                                    """)
    
    qtd_linhas = st.slider("Quantidade de Linhas", min_value=10, max_value=500_000, value=1000, step=100)
    # A quantidade máxima de colunas será ajustada dinâmicamente com base no preset, mas usaremos um valor padrão por enquanto.
    qtd_colunas = st.slider("Quantidade de Colunas", min_value=2, max_value=15, value=8)

    return { # Retorna um dicionário, que usaremos no constructor.py depois
    "modo": "simples",
    "preset": preset,
    "tipo_analise": tipo_analise,
    "qtd_linhas": qtd_linhas,
    "qtd_colunas": qtd_colunas # qtd_colunas é definida pelo preset.
}

# -- Modo Geração Customizada ---
def interface_geracao_customizada(presets_disponiveis: list):
    st.subheader("Geração Customizada")
    st.markdown("""
            Configure um dataset customizado. Em caso de dúvidas, utilize os valores padrão pré-definidos com base no tipo de análise que vocẽ escolheu.
            """)
    st.markdown('')
    
    col_1, col_2 = st.columns(2)


    preset = st.selectbox('Escolha uma categoria (preset):', presets_disponiveis,
                              help="""O preset vai definir qual é o tipo dos dados que você quer gerar e quais colunas esses dados terão.""")
        
    tipo_analise = st.selectbox("Tipo de Análise", ["EDA", "Regressão", "Classificação", "Cluster", "Inferência"],
                                    index=0,
                                    help="""
                                    O tipo de análise vai determinar alguns elementos importantes, como a estrutura geral dos dados, se ele vai ter uma variável resposta, etc.
                                    """,
                                    key='analise_custom')

    qtd_linhas = st.slider("Quantidade de Linhas", min_value=10, max_value=500_000, value=1000, step=100, key='linhas_custom') 

    # A quantidade máxima de colunas será ajustada dinâmicamente com base no preset, mas usaremos um valor padrão por enquanto.
    qtd_colunas = st.slider("Quantidade de Colunas", min_value=2, max_value=15, value=8, key='colunas_custom')

    st.markdown("#### Integridade dos Dados (global)")
    with st.expander('Configurações da Integridade Geral dos Dados'): # FILTRAR PARA ACONSIDERAR o tipo_analise
        duplicados = st.checkbox("Permitir Duplicados", value=False)
        missings = st.checkbox("Permitir Valores Faltantes (Nulos)", value=False)
        outliers = st.checkbox("Permitir Outliers", value=False)
        distribuicao = st.selectbox("Distribuição dos Dados Numéricos", ["Normal", "Desvio pra Esquerda", "Desvio pra Direita", "Uniforme", "Aleatória"],
                                    index=0)
            
    st.markdown("#### 🎯 Target (dependente da análise)")
    with st.expander("Configuração da Target"):
        if tipo_analise == "Regressão":
            integridade_target = st.slider("Dificuldade de previsão (ruído)", 0, 100, 30)
            target_missing = st.checkbox("Permitir valores faltantes (Nulos)", value=False)
            target_outliers = st.checkbox("Permitir outliers", value=False)
        elif tipo_analise == "Classificação":
            balanceamento = st.selectbox("Balanceamento", ["Balanceado (50/50)", "Aleatório", "Desbalanceado"])
            dummies = st.checkbox("Converter classes em numéricos?", value=False)
        elif tipo_analise == "EDA":
            st.info("Sem target") # TEMPORÁRIO
        elif tipo_analise == "Inferência":
            st.info("Sem target")
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


# Função principal com a interface do projeto
def main_interface():

    # -- Interface Básica --
    st.title('📊 Data Fake')
    st.markdown("**Desenvolvido por:**") # Créditos dos criadores

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "[![Daniel](https://img.shields.io/badge/LinkedIn-Daniel_Castro-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-casthro/)",
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "[![Bruno](https://img.shields.io/badge/LinkedIn-Bruno_Rocha-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/brsrochapi/)",
            unsafe_allow_html=True
        )

    # Banner
    # INSERIR BANNER AQUI.

    # Descrição
    st.info("""
                🎉 **Bem-vindo ao Data Fake!**  
                Gere datasets sintéticos de forma rápida e prática para simulações, testes e análises exploratórias.

                Você pode escolher entre dois modos de geração:  
                    - **Geração Simples**: ideal para criar dados rapidamente, com configurações automáticas.  
                    - **Geração Customizada**: controle total sobre os tipos de colunas e características dos dados.

                Selecione a categoria desejada, defina o número de linhas e colunas e clique em **Gerar Dataset**.
            """)

    st.markdown("---")
    
    # -- Seleção do Modo de Geração --
    modo = st.sidebar.selectbox("🔄 Escolha o Modo de Geração", ['Geração Simples', 'Geração Customizada'])

    if modo == 'Geração Simples':
        interface_geracao_simples(['Teste 1', 'Teste 2', 'Teste 3'])
    else:
        interface_geracao_customizada(['Teste 1', 'Teste 2', 'Teste 3'])

    gerar = st.button('Gerar Dataset') # Botão apenas simbólico por enquanto.
