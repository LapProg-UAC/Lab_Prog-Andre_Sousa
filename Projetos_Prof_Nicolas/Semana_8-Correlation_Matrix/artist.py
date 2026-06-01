import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List

def generate_formatted_heatmap() -> None:
    """
    Gera e exporta um heatmap com escala de cores ajustada e sem mascaramento.

    Returns
    -------
    None
    """
    
    data: np.ndarray = np.array([
        [1.0, 0.052],
        [0.052, 1.0]
    ])
    
    labels: List[str] = ['0', '1']
    df_corr: pd.DataFrame = pd.DataFrame(data, index=labels, columns=labels)

    plt.figure(figsize=(8, 6))
    sns.set_theme(style="white")
    
    heatmap = sns.heatmap(
        df_corr,
        annot=True,
        cmap='coolwarm',
        fmt=".3f",
        vmin=0.2,
        vmax=1.0,
        linewidths=0.5,
        square=True,
        cbar_kws={
            "ticks": [0.2, 0.4, 0.6, 0.8, 1.0],
            "shrink": 0.8
        }
    )

    plt.title("Correlation Matrix (Adjusted Scale)")
    plt.xlabel("Real Variables")
    plt.ylabel("Real Variables")
    
    plt.savefig('adjusted_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_formatted_heatmap()