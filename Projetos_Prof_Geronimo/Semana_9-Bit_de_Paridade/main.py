import random
import sys
from datetime import datetime
from typing import List

from logica import (
    generate_data, 
    calculate_parity, 
    introduce_error, 
    write_file, 
    compare_parity
)

def main() -> None:
    """
    Orchestrates the data pipeline: generation, parity calculation, 
    error injection, and detection through file comparison.
    """
    random.seed(datetime.now().timestamp())
    print("System initialized. Random seed set.")

    k_elements: int = random.randint(51, 64)
    print(f"Generating sequence of {k_elements} elements...")

    try:
        original_data: List[int] = generate_data(k_elements)
        write_file("originais.txt", original_data)

        original_parity: List[int] = [calculate_parity(num) for num in original_data]
        write_file("paridade_original.txt", original_parity)

        indices_to_corrupt: List[int] = random.sample(range(k_elements), 3)
        corrupted_data: List[int] = introduce_error(original_data, indices_to_corrupt)
        write_file("corrompidos.txt", corrupted_data)

        corrupted_parity: List[int] = [calculate_parity(num) for num in corrupted_data]
        write_file("paridade_corrompida.txt", corrupted_parity)

        print("Data generation and corruption phase complete.")

        print("\n--- Starting Detection Analysis ---")
        
        with open("paridade_original.txt", 'r', encoding='utf-8') as f1, \
             open("paridade_corrompida.txt", 'r', encoding='utf-8') as f2:
            
            p1_loaded: List[int] = [int(line.strip()) for line in f1]
            p2_loaded: List[int] = [int(line.strip()) for line in f2]

        mismatched: List[int] = compare_parity(p1_loaded, p2_loaded)

        if not mismatched:
            print("Status: No errors detected in the dataset.")
        else:
            print(f"Status: {len(mismatched)} errors detected.")
            for error_idx in mismatched:
                print(f"  [!] DISCREPANCY FOUND AT INDEX: {error_idx}")

    except FileNotFoundError as fnf:
        print(f"Critical Error: A required file is missing. {fnf}")
        sys.exit(1)
    except (ValueError, TypeError, IOError) as err:
        print(f"Critical Error: Pipeline failure. {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()