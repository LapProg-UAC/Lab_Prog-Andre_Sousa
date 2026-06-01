from typing import Optional

class NooArvGenAsc:
    """
    Represents a node in an ascending genealogical tree.

    Parameters
    ----------
    name : str
        The name of the person.
    maternal_node : Optional['NooArvGenAsc']
        The node representing the mother.
    paternal_node : Optional['NooArvGenAsc']
        The node representing the father.
    """

    def __init__(self, name: str, maternal_node: Optional['NooArvGenAsc'] = None, paternal_node: Optional['NooArvGenAsc'] = None) -> None:
        self._name: str = name
        self._maternal_node: Optional['NooArvGenAsc'] = maternal_node
        self._paternal_node: Optional['NooArvGenAsc'] = paternal_node

    def get_nome(self) -> str:
        """
        Retrieves the person's name.

        Returns
        -------
        str
            The name of the person.
        """
        return self._name

    def set_nome(self, name: str) -> None:
        """
        Updates the person's name.

        Parameters
        ----------
        name : str
            The new name to be set.
        """
        self._name = name

    def get_mae(self) -> Optional['NooArvGenAsc']:
        """
        Retrieves the maternal node.

        Returns
        -------
        Optional[NooArvGenAsc]
            The node representing the mother, or None if not set.
        """
        return self._maternal_node

    def set_mae(self, node: Optional['NooArvGenAsc']) -> None:
        """
        Updates the maternal node.

        Parameters
        ----------
        node : Optional[NooArvGenAsc]
            The new maternal node to be set.
        """
        self._maternal_node = node

    def get_pai(self) -> Optional['NooArvGenAsc']:
        """
        Retrieves the paternal node.

        Returns
        -------
        Optional[NooArvGenAsc]
            The node representing the father, or None if not set.
        """
        return self._paternal_node

    def set_pai(self, node: Optional['NooArvGenAsc']) -> None:
        """
        Updates the paternal node.

        Parameters
        ----------
        node : Optional[NooArvGenAsc]
            The new paternal node to be set.
        """
        self._paternal_node = node