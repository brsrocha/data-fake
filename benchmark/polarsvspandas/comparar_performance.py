import os, time, gc
import numpy as np
import pandas as pd
import polars as pl
from faker import Faker
from concurrent.futures import ThreadPoolExecutor

# Inicializa a instância do Faker
faker = Faker("pt_Br")

## Variaveis globais -- USE COM CUIDADO!
# Quantidade de threads
os.environ['POLARS_MAX_THREADS'] = '2' # Aumentar se quiser mais processamento, pode crashar.
qtd_linhas = 100_000 # Quantidade de linhas do dataset
qtd_colunas_numericas = 50 # quantidade de colunas de numeros (NumPy)
qtd_colunas_texto = 50 # quantidade de colunas de texto (faker)
funcoes_faker = [faker.name, faker.city, faker.company, faker.job, faker.color_name] # lista de funcoes do faker para aplicar as colunas de texto

# Classe para gerar strings do faker em CACHE
class GeradorCacheado:
    """
    Com cache, nós vamos limitar os dados a um tamanho específico e vamos gerar os mesmos dados com uma seleção aleatória.
    Isso fará com que os dados se repitam ao longo das colunas. 
    Para esse teste de performance, isto é ok, e acelera MUITO o desempenho. Arrisco dizer que essa é a feature
    desse código que mais traz desempenho. Porém, essa medida NÃO SE SUSTENTARÁ no projeto final, por que o usuário pode desejar
    valores verdadeiramente únicos. 
    Para o projeto final, usaremos uma outra abordagem usando Rust e batcheamento. O usuário poderá escolher se quer que todos
    os valores sejam únicos (mais lento, porém vamos otimizar no Rust) ou se ele quer x valores únicos (extremamente rápido).
    Cacheamento também será utilizado se o usuário quiser incluir duplicados no dataset.
    
    O exemplo abaixo seria o caso do usuário escolher mil valores únicos, ou seja, o faker irá criar 1000 valores e repetir
    esses valores aleatoriamente ao longo das 1 milhão de linhas selecionadas no exemplo.
    """
    def __init__(self, func, tamanho_cache=1000): # 'func' é a função do faker
        self.cache = [func() for _ in range(tamanho_cache)] # Pré-carrega o cache
        
    def gerar(self, n): # Método para gerar amostras do cache sob demanda
        return np.random.choice(self.cache, size=n) # sorteia n valores do cache
    
# Funcao para gerar dados de forma OTIMIZADA, usando Numpy, polars, cache e threads
def gerar_dados_otimizado(
    qtd_linhas=qtd_linhas, 
    qt_coluna_numericas=qtd_colunas_numericas, 
    qtd_colunas_texto=qtd_colunas_texto):
    print("\n MODO Otimizado usando Polars, NumPy, cache e threads:")
    
    inicio = time.perf_counter() # inicia a contagem de tempo da funcao
    
    # -- COLUNAS NUMÉRICAS --
    print(f"Gerando colunas numéricas...")
    colunas_numericas = {
        f"numero_{i}": # CHAVE do dicionário (nome da coluna)
            (np.random.randint(0, 1000, size=qtd_linhas)) for i in range (qt_coluna_numericas) # Valor da coluna
    }
    
    # -- COLUNAS DE TEXTO --
    # Usamores a classe de Cache e também paralelismo
    print(f"Gerando colunas de texto...")
    colunas_texto = {}
    with ThreadPoolExecutor() as executor: # multithreading
        tarefas = {
            f"texto_{i}": # CHAVE do dicionário (nome da coluna)
                executor.submit(GeradorCacheado(funcoes_faker[i % len(funcoes_faker)]).gerar, qtd_linhas)
                for i in range(qtd_colunas_texto) # Valor da coluna, submitado para o executar fazer multithreading, gerando varias colunas ao mesmo tempo
        }
        for nome_coluna, tarefa in tarefas.items():
            colunas_texto[nome_coluna] = tarefa.result # chama o método .result da instância do executor, que vai criar as colunas
            
    
    # -- MONTANDO O DATAFRAME --
    print(f"Montando dataframe com Polars...")
    dados = pd.DataFrame(
        {**colunas_numericas, **colunas_texto}
    )
    
    fim = time.perf_counter()
    print(f"Concluído em {fim - inicio:.2f} segundos.\n tamanho do dataset (linhas x colunas): {dados.shape}")
    
def gerar_dados_lento(
    qtd_linhas=qtd_linhas, 
    qt_coluna_numericas=qtd_colunas_numericas, 
    qtd_colunas_texto=qtd_colunas_texto
):
    print("\n MODO lento usando single-thread, loops padrao e pandas")
    
    inicio = time.perf_counter()
    linhas = []  # Lista que conterá todos os dicionários (cada um representando uma linha)
    
    for _ in range(qtd_linhas):
        linha = {}
        
        # Adiciona as colunas numéricas
        for i in range(qt_coluna_numericas):
            linha[f"num_{i}"] = np.random.randint(0, 1000)
        
        # Adiciona as colunas de texto (chamando as funções do faker)
        for j in range(qtd_colunas_texto):
            # Cada elemento em funcoes_faker é uma função, então chamamos com ()
            linha[f"texto_{j}"] = funcoes_faker[j % len(funcoes_faker)]()
        
        # Agora sim, inserimos o dicionário pronto dentro da lista 'linhas'
        linhas.append(linha)
    
    print("Montando dataframe no pandas...")
    dados = pd.DataFrame(linhas)
    
    fim = time.perf_counter()
    print(f"Concluído em {fim - inicio:.2f} segundos.\n tamanho do dataset (linhas x colunas): {dados.shape}")
    
    # Limpando da memória
    del dados
    gc.collect()

    
# FUNÇÃO PRINIPAL PARA EXECUTAR OS MODOS, segundo input do usuario
def main():
    print("Escolha o modo de geração de dados:")
    print("1 - Otimizado (rápido, usa cache e multithreading)")
    print("2 - Lento (mais simples, sem otimizações)")

    escolha = input("Digite 1 ou 2: ").strip()

    if escolha == "1":
        gerar_dados_otimizado()
    elif escolha == "2":
        gerar_dados_lento()
    else:
        print("Opção inválida. Digite 1 ou 2.")

if __name__ == "__main__":
    main()