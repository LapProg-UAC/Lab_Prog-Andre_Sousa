import numpy as np
from typing import Tuple

def generate_signals(start: float, stop: float, samples: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Gera um vetor de tempo e dois sinais trigonométricos (seno e cosseno).

    Parameters
    ----------
    start : float
        O valor inicial do intervalo de tempo.
    stop : float
        O valor final do intervalo de tempo.
    samples : int
        O número de amostras a gerar.

    Returns
    -------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Um tuplo contendo o vetor de tempo, o sinal seno e o sinal cosseno.
    """
    try:
        time_vector: np.ndarray = np.linspace(start, stop, samples)
        signal_sin: np.ndarray = np.sin(time_vector)
        signal_cos: np.ndarray = np.cos(time_vector)
        return time_vector, signal_sin, signal_cos
    except (ValueError, TypeError) as error:
        raise RuntimeError(f"Erro na geração de sinais: {error}")

def calculate_correlation(signal_a: np.ndarray, signal_b: np.ndarray) -> np.ndarray:
    """
    Calcula a matriz de correlação de Pearson entre dois sinais.

    Parameters
    ----------
    signal_a : np.ndarray
        O primeiro sinal para análise.
    signal_b : np.ndarray
        O segundo sinal para análise.

    Returns
    -------
    np.ndarray
        A matriz de correlação 2x2 resultante.
    """
    try:
        correlation_matrix: np.ndarray = np.corrcoef(signal_a, signal_b)
        return correlation_matrix
    except Exception as error:
        raise RuntimeError(f"Erro no cálculo da correlação: {error}")

def main() -> None:
    """
    Executa o fluxo principal de geração de dados e análise estatística.

    Returns
    -------
    None
    """
    time: np.ndarray
    y1: np.ndarray
    y2: np.ndarray
    
    time, y1, y2 = generate_signals(0.0, 10.0, 400)
    
    matrix: np.ndarray = calculate_correlation(y1, y2)
    
    print(f"Matriz de Correlação:\n{matrix}")

