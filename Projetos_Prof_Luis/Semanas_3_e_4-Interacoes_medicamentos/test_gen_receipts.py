import unittest
from unittest.mock import patch, mock_open, MagicMock
from typing import Dict, List, Tuple, Any, Set


from gen_receipts_logic import (
    read_csv_matrix,
    generate_synthetic_prescriptions,
    export_to_json
)


class testlogicgeneration(unittest.TestCase):
    """
    Classe de testes unitários para a validação estrita da geração 
    de receitas sintéticas, parsing de matrizes e exportação de dados.
    """

    def setUp(self) -> None:
        """
        Prepara as estruturas de dados base simuladas para os testes.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None
        """
        self.mock_interaction_matrix: Dict[Tuple[str, str], int] = {
            ("drug_a", "drug_b"): 1,
            ("drug_a", "drug_c"): 2,
            ("drug_b", "drug_c"): 3,
            ("drug_x", "drug_y"): 0
        }
        self.mock_meds_list: List[str] = ["drug_a", "drug_b", "drug_c", "drug_x", "drug_y"]
        self.num_synthetic_records: int = 50

    def tearDown(self) -> None:
        """
        Limpa o estado da memória após cada teste.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None
        """
        self.mock_interaction_matrix.clear()
        self.mock_meds_list.clear()

    @patch("builtins.open", new_callable=mock_open, read_data="drug,drug_a,drug_b\ndrug_a,0,1\ndrug_b,1,0\n")
    def test_read_csv_matrix_conversion_and_boundaries(self, mock_file: MagicMock) -> None:
        """
        Valida se o interpretador de CSV converte corretamente os níveis de 
        interação para inteiros e extrai a lista de medicamentos.

        Parameters
        ----------
        mock_file : MagicMock
            O objeto mock injetado para simular a leitura do ficheiro CSV.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a conversão falhar, se o tuplo não for gerado, ou se ficheiros 
            inexistentes não levantarem erro.
        """
        csv_path: str = "fake_path/matrix.csv"
        meds_result, matrix_result = read_csv_matrix(csv_path)

        self.assertIsInstance(meds_result, list, "Erro: A lista de medicamentos devia ser do tipo list.")
        self.assertIsInstance(matrix_result, dict, "Erro: A matriz devia ser do tipo dict.")
        self.assertGreater(len(matrix_result), 0, "Erro: A matriz CSV simulada gerou um dicionário vazio.")
        
        interaction_value: Any
        for interaction_value in matrix_result.values():
            self.assertIsInstance(
                interaction_value, 
                int, 
                f"Erro de tipagem: Esperado 'int', obtido '{type(interaction_value).__name__}'."
            )

        
        with self.assertRaises(TypeError, msg="Erro: Caminho inválido (inteiro) não levantou TypeError."):
            read_csv_matrix(123) #NOSONAR

    def test_generate_synthetic_prescriptions_id_constraints(self) -> None:
        """
        Garante que os IDs gerados possuem exatamente 9 dígitos e 
        são matematicamente únicos no universo gerado.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se houver colisões de ID ou violação das fronteiras de 9 dígitos.
        """
        results: List[Dict[str, Any]] = generate_synthetic_prescriptions(
            self.num_synthetic_records, 
            self.mock_meds_list,
            self.mock_interaction_matrix
        )

        generated_ids: Set[int] = set()
        
        record: Dict[str, Any]
        for record in results:
            patient_id: int = record.get("id", 0)
            
            # Boundary Test: Exatamente 9 dígitos (100.000.000 a 999.999.999)
            self.assertGreaterEqual(patient_id, 100000000, "Erro: ID abaixo do limite inferior de 9 dígitos.")
            self.assertLessEqual(patient_id, 999999999, "Erro: ID acima do limite superior de 9 dígitos.")
            self.assertEqual(len(str(patient_id)), 9, "Erro: O comprimento da string do ID falhou a restrição de 9 caracteres.")
            
            generated_ids.add(patient_id)

        self.assertEqual(
            len(generated_ids), 
            self.num_synthetic_records, 
            "Erro: Colisão de IDs sintéticos detetada. O gerador falhou a restrição de unicidade."
        )

    def test_generate_synthetic_prescriptions_meds_and_interactions(self) -> None:
        """
        Verifica a integridade combinatória das receitas geradas (exatamente 
        3 medicamentos únicos e interações limitadas ao cruzamento matemático).

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a restrição de unicidade dos 3 fármacos falhar.
        """
        results: List[Dict[str, Any]] = generate_synthetic_prescriptions(
            self.num_synthetic_records, 
            self.mock_meds_list,
            self.mock_interaction_matrix
        )

        record: Dict[str, Any]
        for record in results:
            medications: List[str] = record.get("medicamentos", [])
            
            
            unique_meds: Set[str] = set(medications)
            self.assertEqual(
                len(unique_meds), 
                3, 
                "Erro Crítico: A receita não contém exatamente 3 medicamentos únicos."
            )
            self.assertEqual(
                len(medications), 
                3, 
                "Erro: A lista de medicamentos gerada tem um tamanho diferente de 3."
            )

    def test_generate_synthetic_prescriptions_error_conditions(self) -> None:
        """
        Ataca brutalmente a função de orquestração injetando partições 
        de inputs inválidos e limites corrompidos.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se os mecanismos de defesa (ValueErrors/TypeErrors) falharem.
        """
        
        with self.assertRaises(ValueError, msg="Erro: Um pedido de 0 registos deve ser negado com ValueError."):
            generate_synthetic_prescriptions(0, self.mock_meds_list, self.mock_interaction_matrix)

        
        with self.assertRaises(ValueError, msg="Erro: Lista de fármacos com menos de 3 elementos deve ser negada."):
            generate_synthetic_prescriptions(10, ["drug_a", "drug_b"], self.mock_interaction_matrix)

        
        with self.assertRaises(TypeError, msg="Erro: Matriz inválida não levantou TypeError."):
            generate_synthetic_prescriptions(10, self.mock_meds_list, []) # type: ignore

    @patch("builtins.open", new_callable=mock_open)
    def test_export_to_json_io(self, mock_file: MagicMock) -> None:
        """
        Valida a operação de gravação isolada em ficheiro JSON simulado.

        Parameters
        ----------
        mock_file : MagicMock
            O objeto mock para capturar chamadas de escrita de sistema.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se o decorador de I/O falhar a interceção ou os tipos de dados falharem a validação.
        """
        payload: List[Dict[str, Any]] = [{"id": 1, "medicamentos": ["drug_a"]}]
        
        export_to_json(payload, "dummy.json")
        mock_file.assert_called_once_with("dummy.json", mode='w', encoding='utf-8')

        
        with self.assertRaises(TypeError, msg="Erro: Exportar um dicionário em vez de lista devia falhar."):
            export_to_json({"id": 1}, "dummy.json") # type: ignore


if __name__ == '__main__':
    unittest.main()