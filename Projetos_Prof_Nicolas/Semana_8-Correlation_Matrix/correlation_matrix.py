import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt  
import plotly.express as px
from bokeh.plotting import figure, show
from pathlib import Path


def main() -> None:  
    """Compute the correlation between trigonometric signals and render the heatmap."""  
    # NumPy variables
    t = np.linspace(0, 10, 400)
    y1 = np.sin(t)
    y2 = np.cos(t)
    
    # seaborn heatmap
    corr = np.corrcoef(np.vstack([y1, y2]))
    sns.heatmap(
    corr,
        annot=True,
        cmap='coolwarm',  
        fmt=".3f",
        vmin=0,
        vmax=1.0
    )
    

    plt.title("Correlation Matrix (Adjusted Scale)")
    plt.xlabel("Variable X")
    plt.ylabel("Variable Y")
    
    script_paste = Path(__file__).parent
    
    
    final_path = script_paste / 'correlation_matrix.png'
    plt.savefig(final_path, dpi=300, bbox_inches='tight')
    plt.close()   
    print("Imagem gravada")
    

if __name__ == "__main__":
    main()
    

