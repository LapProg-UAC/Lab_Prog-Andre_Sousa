import json
import sys
import random

# ==========================================
# 1. A MÁQUINA DE CIFRA (SUBSTITUIÇÃO)
# ==========================================

def encript(text: str, keys: list) -> str:
    """Encriptação
    ------
    Encripta um texto utilizando o método de substituição (Cifra).

    Esta função percorre cada carácter do texto original, converte-o para o seu
    valor numérico na tabela ASCII, e soma o valor da chave correspondente.
    Se a lista de chaves for menor que o texto, as chaves são aplicadas de 
    forma cíclica. O resultado é mantido dentro do limite de 256 (ASCII estendido).

    Parâmetros:
    ----------
    text : str
        O texto original que se pretende encriptar.
    keys : list
        Uma lista de inteiros contendo as chaves de deslocamento. 
        

    Retorna:
    -------
    str
        Uma nova string contendo o texto encriptado.
    """     
    encripted_text = ""
    for i, char in enumerate(text):
        # Seleção cíclica da chave (Requisito 1) [cite: 17]
        actual_key = keys[i % len(keys)]
        
        # Transformação ASCII (Objetivo 1) [cite: 9]
        original_number = ord(char)              
        altered_number = (original_number + actual_key) % 256
        encripted_text += chr(altered_number)
        
    return encripted_text


def main() -> None:
    """
    Função principal que coordena o fluxo de geração e proteção de dados.
    ------
    Esta função realiza as seguintes etapas:
    1. Define as chaves de encriptação por substituição[cite: 7, 10].
    2. Gera uma base de dados fictícia com 20 registos, contendo nomes e 
       números de utente (IDs) de 9 dígitos[cite: 16, 17].
    3. Aplica o método de encriptação ao campo sensível (ID) para garantir 
       a confidencialidade dos dados[cite: 2, 8].
    4. Exporta o dicionário resultante para um ficheiro JSON estruturado.
    
    Objetivos cumpridos: Manipulação de ficheiros, operações com ASCII e 
    análise da qualidade do código através de documentação adequada.
    """
    secret_keys = [3, 1, 4]
    
    nomes_base = ["Roberto", "Maria", "Ana", "Pedro", "Joana", "Rui", "Sofia", "Carlos", "Luis", "Marta"]
    
    
    todos_utentes = []
    for _ in range(20):
        
        nome_escolhido = random.choice(nomes_base)
        id_original = str(random.randint(100000000, 999999999))
        
        # Criamos o registo apenas com Nome e ID 
        utente_registo = {
            "nome": nome_escolhido,
            "numero_utente": id_original
        }
        todos_utentes.append(utente_registo)

    print(f"--- Foram gerados {len(todos_utentes)} registos na memória ---")

    # PASSO B: Encriptação dos IDs para garantir a confidencialidade [cite: 2]
    for utente in todos_utentes:
        # Encriptamos apenas o campo delimitado (Requisito 3) 
        utente["numero_utente"] = encript(utente["numero_utente"], secret_keys)

    # PASSO C: Exportação para o ficheiro JSON final [cite: 3]
    filename = "registos_secretos.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # O indent=4 deixa o bloco de texto bonito e legível no ficheiro
            json.dump(todos_utentes, f, indent=4, ensure_ascii=False)
        
        print(f"O ficheiro '{filename}' foi criado.")
        
    except Exception as e:
        print(f" Erro ao guardar o ficheiro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
