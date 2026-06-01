import sys

FILE_PATH = "texto.txt"

def read_file(file_path: str) -> str:
    """
    Lê o conteúdo de um ficheiro de texto.
    Cumpre o objetivo de manipulação de ficheiros.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Erro: O ficheiro '{file_path}' não foi encontrado.")
        sys.exit(1)

def compute_folding_hash(text: str, hash_length: int = 5, pad_char: str = '5', verbose: bool = False) -> str:
    """
    Requisito 1: Implementar o método de hashing por folding.
    -------------------------------------------------------
    1. Preenche o texto com o pad_char até ser múltiplo do hash_length.
    2. Divide em blocos e soma verticalmente (folding).
    3. Aplica o módulo 256 e converte para hexadecimal.
    """
    # 1. Padding (Preenchimento) para garantir múltiplos do comprimento
    padded_text = text
    while len(padded_text) % hash_length != 0:
        padded_text += pad_char
        
    ascii_values = [ord(char) for char in padded_text]
    col_sums = [0] * hash_length
    
    # 2. Soma Vertical
    for i, val in enumerate(ascii_values):
        col_index = i % hash_length
        col_sums[col_index] += val
        
    # 3. Módulo 256 e Conversão Hexadecimal
    mod_sums = [s % 256 for s in col_sums]
    hex_vals = [f"{s:02X}" for s in mod_sums]  # Formata para Hexadecimal de 2 dígitos
    
    # --- Secção Visual para "Verificar a correção dos resultados" (Objetivo 3) ---
    if verbose:
        print("\n--- MATRIZ DE FOLDING ---")
        for i in range(0, len(ascii_values), hash_length):
            linha = ascii_values[i:i+hash_length]
            print(" ".join(f"{num:3}" for num in linha))
        print("-" * 19)
        print(" ".join(f"{num:3}" for num in col_sums) + "  (adição)")
        print(" ".join(f"{num:3}" for num in mod_sums) + "  (resto da divisão por 256)")
        print(" ".join(f"{h:>3}" for h in hex_vals) + "  (caracteres hexadecimais)")
        print("-" * 19)

    return "".join(hex_vals)

def compute_keyed_hash(text: str, secret_key: str, hash_length: int = 5) -> str:
    """
    Requisito 3: Implementar o método de "keyed hash" com hashing por folding.
    --------------------------------------------------------------------------
    O texto original é concatenado com uma chave secreta antes de aplicar 
    o algoritmo de folding hash.
    """
    # Junta a chave ao texto (pode ser no fim ou no início, vamos pôr no fim)
    authenticated_text = text + secret_key
    
    # Reutilizamos a nossa máquina de folding principal
    return compute_folding_hash(authenticated_text, hash_length, verbose=False)

def main() -> None:
    """
    Função principal que orquestra os Requisitos 2 e 4.
    """
    print("Início da Análise Criptográfica")
    
    # Lê o ficheiro
    conteudo = read_file(FILE_PATH)
    print(f"📄 Conteúdo Original: '{conteudo}'")
    
    # REQUISITO 2: Calcular o hashing por folding para verificar integridade
    print("\n[Executando Requisito 2: Hash Simples / Integridade]")
    # Ativamos o verbose=True para veres a matriz igual à da professora!
    hash_simples = compute_folding_hash(conteudo, hash_length=5, pad_char='5', verbose=True)
    print(f" HASH DE INTEGRIDADE: {hash_simples}")
    
    # REQUISITO 4: Calcular o "keyed hash" para verificar AUTENTICIDADE
    print("\n[Executando Requisito 4: Keyed Hash / Autenticidade]")
    chave_secreta = "qwert1234"
    keyed_hash = compute_keyed_hash(conteudo, secret_key=chave_secreta, hash_length=5)
    print(f" Chave utilizada: '{chave_secreta}'")
    print(f" KEYED HASH FINAL:    {keyed_hash}")

if __name__ == "__main__":
    main()