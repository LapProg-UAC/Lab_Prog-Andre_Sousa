import numpy as np
from logica import generate_signals, calculate_correlation
from artist import generate_formatted_heatmap

def main() -> None:
    """
    Ponto de entrada principal que junta a geração de dados e a sua visualização.

    Esta função coordena a lógica matemática para gerar sinais trigonométricos,
    calcula a correlação correspondente, e aciona o módulo artístico para 
    gerar e exportar o respetivo mapa de calor.

    Returns
    -------
    None
    """
    print("A iniciar o processamento de dados...")
    
    time_vector: np.ndarray
    signal_sin: np.ndarray
    signal_cos: np.ndarray
    
    time_vector, signal_sin, signal_cos = generate_signals(0.0, 10.0, 400)
    print("Sinais trigonométricos gerados com sucesso.")
    
    correlation_matrix: np.ndarray = calculate_correlation(signal_sin, signal_cos)
    print("Correlação calculada com sucesso. Matriz resultante:")
    print(correlation_matrix)
    
    print("A iniciar o módulo de renderização gráfica...")
    generate_formatted_heatmap()
    print("Arte de dados processada: Mapa de calor (heatmap_ajustado.png) guardado no diretório atual.")

if __name__ == "__main__":
    main()