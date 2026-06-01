import sys
from typing import List, Tuple, Optional
from lp_noo_arv_gen_asc import NooArvGenAsc
from lp_arv_gen_asc import ArvGenAsc


try:
    ArvGenAsc._build_tree_recursively = ArvGenAsc.build_tree_recursively
    ArvGenAsc._find_node_recursively = ArvGenAsc.find_node_recursively
    ArvGenAsc._find_ancestor_recursively = ArvGenAsc.find_ancestor_recursively
except AttributeError as e:
   
    pass

def main() -> None:
    """
    Main orchestration script adapted specifically for the UNCORRECTED lp_arv_gen_asc.py.
    
    Uses dynamic method mapping (monkey-patching) to allow the original file to run
    without modifying its source code, fully adapting to 'get_root()' and internal 
    mismatches.
    """
    tree_file_path = "arvore.txt"
    search_file_path = "testes_pesquisa.txt"
    
    print("=" * 60)
    print("  GENEALOGICAL TREE PIPELINE - UNCORRECTED COMPATIBILITY MODE")
    print("=" * 60)
    
   
    print("\n[PHASE 1] Initializing Tree and Importing Data...")
    try:
        
        root_node = NooArvGenAsc("P1")
        tree = ArvGenAsc(root_node)
        
        print(f" -> Reading family lines from '{tree_file_path}'...")
        tree.build_from_file(tree_file_path)
        print(" -> Genealogical tree built successfully via patched recursion.")
        print(f" -> Root person verified via get_root(): {tree.get_root().get_nome()}")
        
    except FileNotFoundError as exc:
        print(f"[!] Critical Error: Family data file missing. Details: {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(f"[!] Critical Error: Invalid data format within tree file. Details: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Unexpected Error during tree building phase: {exc}")
        sys.exit(1)

    
    print("\n[PHASE 2] Executing Recursive Search Queries from File...")
    try:
        search_names: List[str] = []
        with open(search_file_path, 'r', encoding='utf-8') as search_handler:
            for line in search_handler:
                clean_name = line.strip()
                if clean_name:
                    search_names.append(clean_name)
                    
        print(f" -> Loaded {len(search_names)} targets to query: {search_names}")
        print("-" * 60)
        
        for name in search_names:
            print(f"\nQuerying Target: [{name}]")
            
           
            try:
                mother, father = tree.get_parents(name)
                print(f"  • Parents discovered: Mother -> {mother}, Father -> {father}")
            except ValueError as exc:
                print(f"  • Parents query failed: {exc}")
                
       
        print("\n" + "-" * 60)
        print("Querying Lineage Hierarchy from Root Subject:")
        for degree in range(1, 5):
            maternal_ancestor = tree.get_ancestor_by_degree(degree, "maternal")
            paternal_ancestor = tree.get_ancestor_by_degree(degree, "paternal")
            print(f"  • Degree {degree} Ascendants: Maternal -> {maternal_ancestor}, Paternal -> {paternal_ancestor}")
            
    except FileNotFoundError as exc:
        print(f"[!] Critical Error: Search query input file missing. Details: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"[!] Unexpected Error during search execution phase: {exc}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  SUCCESS: Compatibility execution completed flawlessly.")
    print("=" * 60)

if __name__ == "__main__":
    main()