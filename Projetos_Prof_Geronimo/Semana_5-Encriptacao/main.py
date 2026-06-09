import sys
from logic import (
    read_database, create_users, encrypt_users, export_encrypted_users,
    read_json_database, decrypt_users, export_decrypted_users
)

def main() -> None:
    """Main function that coordinates the data generation and protection flow."""
    print("=== STARTING SECURITY SYSTEM ===")
    
    try:
        # Load and clean the names 
        raw_names_text = "".join(read_database("inputs/database.txt"))
             
        names_content = raw_names_text.split('[')[1].split(']')[0]
        names = [name.strip(' "\'\n') for name in names_content.split(',')]
        
        if not names or names == [""]:
            raise ValueError("The name database is empty or invalid.")
        
        # Load and clean the secret keys
        raw_keys_text = "".join(read_database("inputs/secret_keys.txt"))
            
        keys_content = raw_keys_text.split('[')[1].split(']')[0]
        keys = [int(num.strip()) for num in keys_content.split(',')]
            
        if not keys:
            raise ValueError("No secret keys found in the file.")
            
        # Generate (max 20), Encrypt, and Export
        users = create_users(names[:20])
        encrypted_result = encrypt_users(users, keys)
        export_encrypted_users(encrypted_result, "outputs/encrypted_database.json")
        print("20 users generated, encrypted, and exported.")

        # Import, Decrypt, and Export
        imported_users = read_json_database("outputs/encrypted_database.json")
        decrypted_result = decrypt_users(imported_users, keys)
        export_decrypted_users(decrypted_result, "outputs/decrypted_database.json")
        print("Data recovered, decrypted, and exported.")
        
        print("=== PROCESS COMPLETED ===")

    # System Error Handling
    except FileNotFoundError as e:
        print(f"\n[SYSTEM ERROR] A required file is missing: {e.filename}")
        sys.exit(1)
    except IndexError:
        # If no brackets in the file, the .split() will trigger this error
        print("\n[FORMAT ERROR] The text files must contain data inside brackets: [...]")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[DATA ERROR] {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[UNEXPECTED CRITICAL ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()