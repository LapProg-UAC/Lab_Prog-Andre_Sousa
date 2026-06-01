import unittest
from typing import Any
from lp_noo_arv_gen_asc import NooArvGenAsc
from lp_arv_gen_asc import ArvGenAsc


class TestAscendantGenealogicalTree(unittest.TestCase):
    """
    Test suite for the Ascendant Genealogical Tree.
    
    Validates the tree structure integrity while strictly respecting 
    encapsulation principles.
    """

    def test_right_grandfather_retrieval(self) -> None:
        """
        Validates tree instantiation and right grandfather retrieval.

        Evaluates if the right grandfather (degree 2 ascendant) is reachable 
        via proper getter methods instead of direct attribute access.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the retrieved node name does not match the expected grandfather name.
        """
        right_grandfather: NooArvGenAsc = NooArvGenAsc("Right Grandfather")
        
        right_parent: NooArvGenAsc = NooArvGenAsc("Right Parent")
        right_parent.set_pai(right_grandfather)
        
        root_node: NooArvGenAsc = NooArvGenAsc("Root")
        root_node.set_pai(right_parent)
        
        tree: ArvGenAsc = ArvGenAsc(root_node)
        
        target_node: NooArvGenAsc = tree.get_root().get_pai().get_pai()
        
        self.assertEqual(target_node.get_nome(), "Right Grandfather")

    def test_invalid_ascendant_path(self) -> None:
        """
        Tests the input space partition for an invalid lineage boundary.

        Verifies that an AttributeError is properly raised when requesting a
        lineage path that does not exist in the tree structure using getters.

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        AttributeError
            If the requested ascendant node does not exist.
        """
        root_node: NooArvGenAsc = NooArvGenAsc("Root")
        tree: ArvGenAsc = ArvGenAsc(root_node)
        
        with self.assertRaises(AttributeError):
            
         tree.get_root().get_pai().get_pai()


if __name__ == '__main__':
    unittest.main()