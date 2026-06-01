import random
from typing import List, Any

def generate_data(k: int) -> List[int]:
    """
    Gera uma lista de inteiros aleatórios entre 0 e 127.

    Parameters
    ----------
    k : int
        O número de elementos numéricos a gerar.

    Returns
    -------
    List[int]
        Uma lista contendo 'k' números inteiros aleatórios.

    Raises
    ------
    ValueError
        Se 'k' for menor ou igual a zero.
    TypeError
        Se 'k' não for do tipo inteiro.
    """
    if not isinstance(k, int):
        raise TypeError("Parameter 'k' must be an integer.")
    if k <= 0:
        raise ValueError("Parameter 'k' must be strictly positive.")

    generated_data: List[int] = [random.randint(0, 127) for _ in range(k)]
    return generated_data

def calculate_parity(number: int) -> int:
    """
    Calcula o bit de paridade par para um número inteiro.

    Parameters
    ----------
    number : int
        O valor numérico cujo bit de paridade será avaliado.

    Returns
    -------
    int
        O bit de paridade calculado (0 ou 1).

    Raises
    ------
    TypeError
        Se o argumento passado não for um número inteiro.
    """
    if not isinstance(number, int):
        raise TypeError("The argument must be an integer.")

    binary_representation: str = bin(number)
    set_bits_count: int = binary_representation.count('1')
    parity_bit: int = set_bits_count % 2
    return parity_bit

def introduce_error(data: List[int], indices: List[int]) -> List[int]:
    """
    Altera um bit dos elementos da lista nos índices indicados usando a operação XOR.

    Parameters
    ----------
    data : List[int]
        A lista de números originais a ser processada.
    indices : List[int]
        A lista de índices sinalizando onde a corrupção de dados ocorrerá.

    Returns
    -------
    List[int]
        Uma nova lista de dados contendo os erros introduzidos.

    Raises
    ------
    IndexError
        Se qualquer um dos índices fornecidos estiver fora dos limites da lista.
    TypeError
        Se as estruturas de dados passadas não forem listas.
    """
    if not isinstance(data, list) or not isinstance(indices, list):
        raise TypeError("Parameters 'data' and 'indices' must be lists.")

    corrupted_data: List[int] = data.copy()
    target_index: int

    
    for target_index in indices:
        bit_position = random.randint (0,6)
        mascara = 1 <<bit_position
        corrupted_data[target_index] = corrupted_data[target_index] ^ mascara
    return corrupted_data

def write_file(filename: str, data: List[Any]) -> None:
    """
    Persiste a lista de dados num ficheiro de texto, escrevendo linha a linha.

    Parameters
    ----------
    filename : str
        O caminho ou identificador do ficheiro de destino.
    data : List[Any]
        A estrutura de informação que será convertida em texto e guardada.

    Raises
    ------
    IOError
        Se o sistema operativo rejeitar a abertura ou escrita do ficheiro.
    TypeError
        Se os parâmetros não corresponderem aos tipos esperados.
    """
    if not isinstance(filename, str):
        raise TypeError("The filename must be a string.")
    if not isinstance(data, list):
        raise TypeError("The data must be provided as a list.")

    current_item: Any

    try:
        with open(filename, 'w', encoding='utf-8') as file_handler:
            for current_item in data:
                file_handler.write(f"{current_item}\n")
    except IOError as io_error:
        raise IOError("Critical failure during file system write operation.") from io_error

def compare_parity(p1: List[int], p2: List[int]) -> List[int]:
    """
    Avalia duas listas de bits de paridade e localiza as divergências.

    Parameters
    ----------
    p1 : List[int]
        A estrutura primária de bits de paridade.
    p2 : List[int]
        A estrutura secundária de bits de paridade para análise comparativa.

    Returns
    -------
    List[int]
        Uma lista com os índices precisos onde as paridades não coincidem.

    Raises
    ------
    ValueError
        Se as listas a analisar tiverem comprimentos discrepantes.
    TypeError
        Se os parâmetros não forem listas de inteiros.
    """
    if not isinstance(p1, list) or not isinstance(p2, list):
        raise TypeError("Both comparison parameters must be lists.")
    if len(p1) != len(p2):
        raise ValueError("Parity lists must have the exact same length.")

    mismatched_indices: List[int] = [
        current_index for current_index, (first_bit, second_bit) in enumerate(zip(p1, p2)) if first_bit != second_bit
    ]
    return mismatched_indices