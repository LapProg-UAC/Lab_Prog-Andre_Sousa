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
        # 1. Escolhe a chave a usar nesta ronda (anda em círculo se necessário)
        actual_key = keys[i % len(keys)]
        
        # 2. Transforma a letra no seu número da tabela ASCII
        original_number = ord(char)              
        
        # 3. Soma a chave para dar o "salto"
        altered_number = original_number + actual_key               
        
        # 4. Garante que não passa do limite máximo da tabela (255)
        secret_number = altered_number % 256
        
        # 5. Transforma o novo número de volta no símbolo/letra encriptada
        new_letter = chr(secret_number)
        
        # 6. Adiciona ao resultado final
        encripted_text += new_letter

    return encripted_text



original_text = "O modelo está funcional"
secret_keys = [3, 1, 4] 
codified_text = encript(original_text, secret_keys)


def decript(text: str, keys: list) -> str:
    decripted_text = ""
    for i, char in enumerate(text):
        actual_key = keys[i % len(keys)]
        encripted_number = ord(char)
        altered_number = encripted_number - actual_key
        secret_number = altered_number % 256
        original_letter = chr(secret_number)
        decripted_text += original_letter
    return decripted_text
# --- ZONA DE TESTE COMPLETA ---

original_text = "O modelo está funcional"
secret_keys = [3, 1, 4] 

# 1. Encriptar
codified_text = encript(original_text, secret_keys)

# 2. Desencriptar (passando o texto que acabou de ser codificado!)
recovered_text = decript(codified_text, secret_keys)

print("=== RELATÓRIO DE CRIPTOGRAFIA ===")
print(f"Texto original:      {original_text}")
print(f"Texto encriptado:    {codified_text}")
print(f"Texto desencriptado: {recovered_text}")

# O teste de ouro: O texto recuperado é exatamente igual ao original?
if original_text == recovered_text:
    print("A encriptação e desencriptação funcionam a 100%!")
else:
    print(" O texto sofreu mutações pelo caminho.")