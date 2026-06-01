def generate_sequence(n: int) -> list[int]:
    """
    Gera uma lista com os valores da sequência matemática até ao índice n.

    A sequência é construída de forma que cada elemento no índice i seja
    igual ao valor definido pela expressão f[i] = 2 * f(i-2) + f(i-1),
    para i >= 2, tendo como casos base f(0) = 0 e f(1) = 1.

    Parameters
    ----------
    n : int
        O número inteiro não negativo que define o limite superior do índice da lista.

    Returns
    -------
    list[int]
        Uma lista de números inteiros correspondentes aos elementos calculados da função.

    Raises
    ------
    TypeError
        Se o argumento n não for uma instância do tipo int.
    ValueError
        Se o argumento n for um número negativo.
    """
    if not isinstance(n, int):
        raise TypeError("Erro: O argumento fornecido deve ser um número inteiro!")

    if n < 0:
        raise ValueError("Erro: O número deve ser não negativo (>= 0)!")

    if n == 0:
        return [0]

    sequence: list[int] = [0, 1]

    for i in range(2, n + 1):
        next_value: int = (2 * sequence[i - 2]) + sequence[i - 1]
        sequence.append(next_value)

    return sequence
if __name__ == "__main__":
    try:
        
        resultado: list[int] = generate_sequence(4)
        print(f"Sequência gerada: {resultado}")
    except (ValueError, TypeError) as erro:
        print(f"Falha na execução: {erro}")