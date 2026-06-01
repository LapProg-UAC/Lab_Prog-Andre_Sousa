# Caminho para o ficheiro de texto — altera este valor conforme necessário
FILE_PATH = "texto.txt"


def read_file(file_path: str) -> str:
    """
    Leitura do ficheiro.
    ------
    Lê e retorna o conteúdo de um ficheiro de texto.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def text_to_ascii(text: str) -> list:
    """
    Conversão para ASCII.
    ------
    Converte cada caractere do texto para o seu valor ASCII decimal.
    """
    return [ord(char) for char in text]


def compute_folding_hash(ascii_values: list) -> int:
    """
    Cálculo do hash por folding.
    ------
    Calcula o hash por folding somando todos os valores ASCII.
    """
    return sum(ascii_values)


def main() -> None:
    """
    Função principal.
    ------
    Lê um ficheiro, converte para ASCII e calcula o hash por folding.
    """
    try:
        content = read_file(FILE_PATH)
    except FileNotFoundError:
        print(f"Erro: O ficheiro '{FILE_PATH}' não foi encontrado.")
        return
    except OSError as error:
        print(f"Erro ao ler o ficheiro: {error}")
        return

    ascii_values = text_to_ascii(content)
    hash_value = compute_folding_hash(ascii_values)

    print(f"Conteúdo   : {repr(content)}")
    print(f"ASCII      : {ascii_values}")
    print(f"Hash (dec) : {hash_value}")
    print(f"Hash (hex) : {hex(hash_value)}")


if __name__ == "__main__":
    main()