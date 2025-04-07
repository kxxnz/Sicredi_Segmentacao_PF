import numpy as np
import pandas as pd

def gerar_dados(n=1000, seed=42):
    np.random.seed(seed)
    data = {
        'ID': range(1, n+1),
        'Renda_Mensal': np.round(np.random.uniform(1000, 15000, n), 2),
        'Investimentos': np.round(np.random.uniform(0, 300000, n), 2),
        'Regiao': np.random.choice(['PR', 'SP', 'RJ'], n, p=[0.35, 0.4, 0.25])
    }
    df = pd.DataFrame(data)
    return df
