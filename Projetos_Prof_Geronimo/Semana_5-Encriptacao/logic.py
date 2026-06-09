import json
import random

def read_database(file_path : str) -> list[str]:
    """Return lines as a list.""" 
    with open (file_path, 'r', encoding="UTF-8") as file:
        return [line.strip() for line in file]
    

def create_users(database : list[str])->list[dict[str, str | int]]:
    """Goes through the database, return a list of random users with a random ID that does not repeat
     :parameter1: List in database with strings with different names
     :return: List with dicts of users containing name and id which can be a string and an integer, respectively
     :raises TypeError: If the database is None.
     :raises ValueError: If the database's list is empty.  
     """
   
    if database is None:
        raise TypeError("The database list cannot be None.")
    
    if not database:
         return[]
   
    users = []
    used_ids = set()
    for _ in database:
        new_name = random.choice(database)
        new_id = random.randint(100000000, 999999999)
        while new_id in used_ids:
                new_id = random.randint(100000000, 999999999)
                
        used_ids.add(new_id)    

        registered_id = {
            "name" : new_name ,
            "id" : new_id
        }
        users.append(registered_id)
    print(f"{len(users)} users id successfully created.")
    return users
   
    
def encrypt(text : str, keys :list[int]) -> str:
    """Encrypts a text using the substitution method (Cipher).
    
    :param text: The original text to be encrypted.
    :param keys: List of numerical keys to apply the shift.
    :return: The encrypted text as a string.
    :raises TypeError: If the keys list is None.
    :raises ValueError: If the keys list is empty.
    """
    if keys is None:
        raise TypeError("The key list cannot be None.")
    if len(keys) == 0:
        raise ValueError("The key list cannot be empty.")
    encrypted_text = ""
    for i, char in enumerate(text):
        # Determine the correct key for the current character
        actual_key = keys[i % len(keys)] 
        
        # Apply the mathematical transformation
        original_number = ord(char)
        altered_number = original_number + actual_key
        secret_number = altered_number % 256 
        
        # Append the new character to the result
        encrypted_text += chr(secret_number)
        
    return encrypted_text
   

def decrypt(text : str, keys : list[int]) -> str:
    """Decrypts a text reversing the substitution method (Cipher).
    
    :param text: The encrypted text to be encrypted.
    :param keys: List of numerical keys to apply the shift.
    :return: The decrypted text as a string.
    :raises TypeError: If the keys list is None.
    :raises ValueError: If the keys list is empty.
    """

    if keys is None:
        raise TypeError("The key list cannot be None.")
    if  len(keys) == 0:
        raise ValueError("The key list cannot be empty.")
    
    decrypted_text = ""
    for i,char in enumerate(text):
        actual_key = keys[i % len(keys)] 
        encrypted_number = ord(char)
        altered_number_2 = encrypted_number - actual_key
        decrypted_number = altered_number_2 % 256 
        decrypted_text += chr(decrypted_number)
        
    return decrypted_text


def encrypt_users(users : list[dict[str, str | int]], keys : list[int]) -> list[dict[str, str | int]]:
    """
    Goes through the user database and encrypts ONLY their IDs.
    
    :param users: List of dictionaries containing 'name' and 'id'.
    :param keys: List of numerical keys for the substitution cipher.
    :return: A new list of dictionaries with encrypted IDs.
    :raises TypeError: If the users list is None.
    """
    # Boundary condition to satisfy our error test
    if users is None:
        raise TypeError("The users list cannot be None.")
        
    encrypted_database = []
    
    for user in users:
        # 1. We extract the original data
        original_name = user["name"]
        original_id = user["id"]
        
        # 2. We convert the integer ID to a string, then encrypt it using our previous function
        string_id = str(original_id)
        secret_id = encrypt(string_id, keys)
        
        # 3. We build a new secure dictionary for this user
        secure_user = {
            "name": original_name,
            "id": secret_id
        }
        
        # 4. Add the secured user to our new list
        encrypted_database.append(secure_user)

    print("The users' ids were encrypted.")    
    return encrypted_database


def export_encrypted_users(encrypted_users : list[dict[str, str | int]], filename : str) -> None:
    """
    Exports the list of encrypted users to a JSON file.
    
    :param encrypted_users: List of dictionaries containing the users' data.
    :param filename: The name or path of the destination JSON file.
    :return: None
    :raises TypeError: If the encrypted_users list is None.
    """
    
    if encrypted_users is None:
        raise TypeError("The encrypted_users list cannot be None.")
    
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(encrypted_users, file, indent=4)


def read_json_database(filename : str) -> list[dict[str, str | int]]:
    """
    Reads a JSON file containing the user database.
    
    :param filename: The path to the JSON file.
    :return: A list of dictionaries representing the users.
    :raises TypeError: If the filename is None.
    """

    if filename is None:
        raise TypeError("The filename cannot be None.")
        
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
    

def decrypt_users(encrypted_users : list[dict[str, str | int]], keys:list[int]) -> list[dict[str, str | int]]:
    """
    Goes through the encrypted user database and decrypts ONLY their IDs.
    
    :param encrypted_users: List of dictionaries containing the encrypted data.
    :param keys: List of numerical keys used in the original substitution cipher.
    :return: A new list of dictionaries with the decrypted original IDs.
    :raises TypeError: If the ecrypted_users' list is None.
    """
    if encrypted_users is None:
        raise TypeError("The encrypted_users list cannot be None.")

    decrypted_database = []
    
    for user in encrypted_users:
        original_name = user["name"]
        
        # Enusres to pass ID as a string for the decrypting function
        secret_id_str = str(user["id"])
        
        # Reverts the cypher using the original function
        recovered_id_str = decrypt(secret_id_str, keys)
        
        recovered_user = {
            "name": original_name,
            "id": int(recovered_id_str)
        }
        decrypted_database.append(recovered_user)
        
    return decrypted_database


def export_decrypted_users(decrypted_users : list[dict[str, str | int]], filename : str) -> None:
    """
    Exports the list of decrypted users to a JSON file.
    
    :param decrypted_users: List of dictionaries containing the users' data.
    :param filename: The name or path of the destination JSON file.
    :return: None
    :raises TypeError: If the decrypted_users list is None.
    """
    
    if decrypted_users is None:
        raise TypeError("The decrypted_users list cannot be None.")
    
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(decrypted_users, file, indent=4)
