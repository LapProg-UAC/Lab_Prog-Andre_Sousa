from typing import Optional, Tuple, Dict, List
from lp_noo_arv_gen_asc import NooArvGenAsc

class ArvGenAsc:
    """
    Represents an ascending genealogical tree.

    Parameters
    ----------
    root_node : NooArvGenAsc
        The pre-instantiated root node that will serve as the base of the tree.
    """

    def __init__(self, root_node: NooArvGenAsc) -> None:
        self._root: NooArvGenAsc = root_node

    def get_root(self) -> NooArvGenAsc:
        """
        Retrieves the root node of the tree.

        Returns
        -------
        NooArvGenAsc
            The root node.
        """
        return self._root

    def build_from_file(self, file_path: str) -> None:
        """
        Builds the tree by reading relations from a text file.

        Parameters
        ----------
        file_path : str
            The path to the text file.

        Raises
        ------
        FileNotFoundError
            If the file is not found.
        ValueError
            If the file format is invalid.
        """
        relations: Dict[str, Tuple[str, str]] = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file_handler:
                for line in file_handler:
                    clean_line: str = line.strip()
                    if not clean_line:
                        continue
                    parts: List[str] = clean_line.split(',')
                    if len(parts) != 3:
                        raise ValueError("Invalid file format. Expected: person,mother,father.")
                    relations[parts[0].strip()] = (parts[1].strip(), parts[2].strip())
        except FileNotFoundError as error:
            raise FileNotFoundError(f"File not found: {file_path}") from error
            
        self._build_tree_recursively(self._root, relations)

    def build_tree_recursively(self, current_node: NooArvGenAsc, relations: Dict[str, Tuple[str, str]]) -> None:
        """
        Recursively builds the tree nodes based on the relations.

        Parameters
        ----------
        current_node : NooArvGenAsc
            The current node to be processed.
        relations : Dict[str, Tuple[str, str]]
            The dictionary containing relation mappings.
        """
        current_name: str = current_node.get_nome()
        if current_name in relations:
            mother_name, father_name = relations[current_name]
            
            if mother_name and mother_name.lower() != "none":
                maternal_node: NooArvGenAsc = NooArvGenAsc(mother_name)
                current_node.set_mae(maternal_node)
                self._build_tree_recursively(maternal_node, relations)
                
            if father_name and father_name.lower() != "none":
                paternal_node: NooArvGenAsc = NooArvGenAsc(father_name)
                current_node.set_pai(paternal_node)
                self._build_tree_recursively(paternal_node, relations)

    def get_parents(self, target_name: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Recursively searches for a person and returns their parents' names.

        Parameters
        ----------
        target_name : str
            The name of the target person to search for.

        Returns
        -------
        Tuple[Optional[str], Optional[str]]
            The names of the mother and father.

        Raises
        ------
        ValueError
            If the person is not found in the tree.
        """
        target_node: Optional[NooArvGenAsc] = self._find_node_recursively(self._root, target_name)
        if target_node is None:
            raise ValueError(f"Person not found in the tree: {target_name}")
        
        maternal_node: Optional[NooArvGenAsc] = target_node.get_mae()
        paternal_node: Optional[NooArvGenAsc] = target_node.get_pai()
        
        return (
            maternal_node.get_nome() if maternal_node else None,
            paternal_node.get_nome() if paternal_node else None
        )

    def find_node_recursively(self, current_node: Optional[NooArvGenAsc], target_name: str) -> Optional[NooArvGenAsc]:
        """
        Recursively searches for a node by name.

        Parameters
        ----------
        current_node : Optional[NooArvGenAsc]
            The node currently being inspected.
        target_name : str
            The name to search for.

        Returns
        -------
        Optional[NooArvGenAsc]
            The found node or None.
        """
        if current_node is None or current_node.get_nome() == target_name:
            return current_node
        
        return self._find_node_recursively(current_node.get_mae(), target_name) or \
               self._find_node_recursively(current_node.get_pai(), target_name)

    def get_ancestor_by_degree(self, degree: int, lineage: str) -> Optional[str]:
        """
        Recursively searches for an ancestor by degree and lineage.

        Parameters
        ----------
        degree : int
            The degree of ancestry (between 1 and 4).
        lineage : str
            The lineage path ('maternal' or 'paternal').

        Returns
        -------
        Optional[str]
            The name of the ancestor.

        Raises
        ------
        ValueError
            If the degree or lineage are invalid.
        """
        if not 1 <= degree <= 4:
            raise ValueError("The degree must be between 1 and 4.")
        if lineage.lower() not in ["maternal", "paternal"]:
            raise ValueError("The lineage must be 'maternal' or 'paternal'.")
            
        ancestor_node: Optional[NooArvGenAsc] = self._find_ancestor_recursively(self._root, degree, lineage.lower(), 1)
        return ancestor_node.get_nome() if ancestor_node else None

    def find_ancestor_recursively(self, current_node: Optional[NooArvGenAsc], target_degree: int, lineage: str, current_degree: int) -> Optional[NooArvGenAsc]:
        """
        Recursively traverses the lineage to find an ancestor.

        Parameters
        ----------
        current_node : Optional[NooArvGenAsc]
            The current node.
        target_degree : int
            The target degree of ancestry.
        lineage : str
            The lineage path ('maternal' or 'paternal').
        current_degree : int
            The current depth.

        Returns
        -------
        Optional[NooArvGenAsc]
            The found ancestor node or None.
        """
        if current_node is None:
            return None
        
        next_node: Optional[NooArvGenAsc] = current_node.get_mae() if lineage == "maternal" else current_node.get_pai()
        
        if next_node is None:
            return None
        if current_degree == target_degree:
            return next_node
            
        return self._find_ancestor_recursively(next_node, target_degree, lineage, current_degree + 1)