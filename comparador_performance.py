#!/usr/bin/env python
import os
import time
import gc
import numpy as np
import pandas as pd
import polars as pl
from faker import Faker
import random
from concurrent.futures import ThreadPoolExecutor

# Limita o uso de threads do Polars para evitar gargalos
os.environ["POLARS_MAX_THREADS"] = "4"

# Instancia o Faker
fake = Faker("pt_BR")

# Classe otimizada de geração de strings com cache
class CachedFaker:
    def __init__(self, func, cache_size=1000):
        self.cache = [func() for _ in range(cache_size)]
        
    def sample(self, n):
        return np.random.choice(self.cache, size=n)

# 🔹 Modo OTIMIZADO: NumPy + Polars + CachedFaker + threading
def generate_optimized(n_rows=1_000_000, n_numeric=50, n_string=50):
    print("\n🔹 Modo OTIMIZADO (Polars + NumPy + CachedFaker + Threading)")
    start_total = time.perf_counter()

    # Geração numérica vetorizada com NumPy
    print("Gerando colunas numéricas...")
    numeric_cols = {
        f'num_{j}': (
            np.random.randint(0, 1000, size=n_rows)
            if j % 2 == 0 else
            np.random.uniform(0, 1000, size=n_rows)
        ) for j in range(n_numeric)
    }

    # Geração de strings paralelizada e com cache
    print("Gerando colunas de strings com cache e threads...")
    string_cols = {}
    funcs = [fake.name, fake.city, fake.company, fake.job, fake.color_name]
    with ThreadPoolExecutor() as executor:
        futures = {
            f'str_{j}': executor.submit(CachedFaker(funcs[j % len(funcs)]).sample, n_rows)
            for j in range(n_string)
        }
        for k, fut in futures.items():
            string_cols[k] = fut.result()

    print("Criando DataFrame com Polars...")
    df_opt = pl.DataFrame({**numeric_cols, **string_cols})

    end_total = time.perf_counter()
    print(f"✅ OTIMIZADO concluído em {end_total - start_total:.2f} segundos — shape {df_opt.shape}")
    del df_opt
    gc.collect()

# 🔸 Modo BASE: sem otimizações (Pandas + Faker direto, sem cache)
def generate_baseline(n_rows=1_000_000, n_numeric=50, n_string=50):
    print("\n🔸 Modo BASE (Pandas + Faker padrão)")
    start_total = time.perf_counter()
    funcs = [fake.name, fake.city, fake.company, fake.job, fake.color_name]

    data = []
    for _ in range(n_rows):
        row = {}
        for j in range(n_numeric):
            row[f'num_{j}'] = random.randint(0, 1000) if j % 2 == 0 else random.uniform(0, 1000)
        for j in range(n_string):
            row[f'str_{j}'] = funcs[j % len(funcs)]()
        data.append(row)

    print("Criando DataFrame com Pandas...")
    df_base = pd.DataFrame(data)

    end_total = time.perf_counter()
    print(f"✅ BASE concluído em {end_total - start_total:.2f} segundos — shape {df_base.shape}")
    del df_base
    gc.collect()

# Execução
def main():
    print("🚀 Comparando performance: OTIMIZADO vs. BASE")
    generate_optimized()
    generate_baseline()
    print("\n🏁 Fim do teste.")

if __name__ == "__main__":
    main()
