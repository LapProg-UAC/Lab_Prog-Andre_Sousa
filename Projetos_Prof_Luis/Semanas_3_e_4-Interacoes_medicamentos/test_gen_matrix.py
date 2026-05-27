import unittest
from unittest.mock import patch, mock_open, MagicMock


from gen_matrix_logic import read_meds, gen_matrix, export_excel, convert_xlsx_to_csv


class test_medical_processor(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="Aspirin \n\n  Ibuprofen\nParacetamol  \n \n")
    def test_read_meds_valid_and_blank_lines(self, mock_file: MagicMock) -> None:
        """
        Tests the reading of medications by handling blank lines and residual spaces.

        Parameters

        ---------
        mock_file : MagicMock
            Mock of a text file opened in memory.

        Returns

        -------
        None

        Raises

        ------
        AssertionError
            If cleaning spaces and removing blank lines fails.
        """
        result = read_meds("dummy_data.txt")
        expected_meds = ["Aspirin", "Ibuprofen", "Paracetamol"]
        self.assertEqual(result, expected_meds, "Erro: A lista extraída não ignorou espaços ou linhas vazias.")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_meds_empty_file(self, mock_file: MagicMock) -> None:
        """
        Tests the behavior when processing a completely empty file.

        Parameters
        ---------
        mock_file : MagicMock 
            Mock of an empty file in memory.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the function does not return a perfectly empty list.
        """
        result = read_meds("empty.txt")
        self.assertEqual(result, [], "Erro: Ficheiro vazio não gerou uma lista vazia de medicamentos.")

    @patch("builtins.open", side_effect=FileNotFoundError("Ficheiro não encontrado."))
    def test_read_meds_missing_file(self, mock_file: MagicMock) -> None:
        """
        Tests for a critical error condition when the requested file does not exist.

        Parameters
        ---------
        mock_file : MagicMock
            Mock configured to trigger a FileNotFoundError.

        Returns
        -------
        None

        Raises
        ------ 
        FileNotFoundError
            Strictly expected exception when the read point to a blank file.
        """
        with self.assertRaises(FileNotFoundError, msg="Erro Crítico: FileNotFoundError não foi levantado para ficheiro fantasma."):
            read_meds("missing_file.txt")

    def test_gen_matrix_standard_n_by_n(self) -> None:
        """
        Tests the generation of a cross-matrix for a list of multiple medications (NxN).

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------    
        AssertionError
            If the restricted interaction rules fail (0 on the diagonal, 1-6 on the rest).
        """
        meds_list = ["DrugA", "DrugB", "DrugC"]
        matrix = gen_matrix(meds_list)

        if matrix is None:
            self.fail("Erro: A matriz gerada é None.")

        
        for med in meds_list:
            self.assertEqual(matrix.get((med, med)), 0, f"Erro: A diagonal principal para {med} não é zero absoluto.")

        
        interaction_value = matrix.get(("DrugA", "DrugB"), 1)
        self.assertTrue(1 <= interaction_value <= 6, "Erro: Valor de interação gerado violou o limite estabelecido de 1 a 6.")

    def test_gen_matrix_one_by_one(self) -> None:
        """
        Tests matrix generation at the extreme lower bound for only one drug (1x1).

        Parameters
        ----------
        None

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the 1x1 matrix is ​​not exclusively composed of the value 0.
        """
        meds_list = ["DrugA"]
        matrix = gen_matrix(meds_list)
        expected_matrix = {("DrugA", "DrugA"): 0}
        self.assertEqual(matrix, expected_matrix, "Erro: A matriz isolada 1x1 falhou estruturalmente.")

    def test_gen_matrix_empty_list(self) -> None:
        """
        Tests the stability of matrix generation when receiving an empty list.

        Parameters
        ---------
        None

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the return is not a harmless, empty dictionary.
        """
        matrix = gen_matrix([])
        self.assertEqual(matrix, {}, "Erro: Matriz instanciada através de lista vazia não retornou um dicionário vazio.")

    def test_gen_matrix_invalid_type(self) -> None:
        """
        Forces system crash by injecting invalid data types.

        Parameters
        ---------
        None

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Mandatory exception when injecting a None value where a list was expected.
        """
        with self.assertRaises(TypeError, msg="Erro Crítico: TypeError ausente. A função engoliu um input inválido em vez de falhar."):
            gen_matrix(None)  # type: ignore

    @patch("openpyxl.Workbook")
    def test_export_excel_success(self, mock_workbook: MagicMock) -> None:
        """
        Validates the XLSX export operation without compromising the physical disk.

        Parameters
        ---------
        mock_workbook : MagicMock
            Openpyxl Workbook instance simulator.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If the function does not invoke the method to save the file correctly.
        """
        mock_wb_instance = MagicMock()
        mock_workbook.return_value = mock_wb_instance

        meds_list = ["DrugA", "DrugB"]
        matrix = {("DrugA", "DrugA"): 0, ("DrugA", "DrugB"): 4, ("DrugB", "DrugA"): 1, ("DrugB", "DrugB"): 0}
        target_filename = "output_matrix.xlsx"

        export_excel(matrix, meds_list, target_filename)

        mock_wb_instance.save.assert_called_once_with(target_filename)
        self.assertTrue(mock_wb_instance.save.called, "Erro: A operação de gravação no disco simulado foi abortada ou esquecida.")

    def test_export_excel_invalid_matrix(self) -> None:
        """
        Tests the destructive reaction of the Excel exporter when receiving a null array.

        Parameters
        ---------
        None

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Expects the injection of `None` to cause the function to implode immediately with a type error.
        """
        with self.assertRaises(TypeError, msg="Erro Crítico: TypeError não disparou ao tentar exportar uma matriz nula para Excel."):
            export_excel(None, ["DrugA"], "crash.xlsx")  # type: ignore


class TestFileConversion(unittest.TestCase):

    @patch("openpyxl.load_workbook")
    @patch("builtins.open", new_callable=mock_open)
    def test_convert_valid_partition(self, mock_file: MagicMock, mock_load_wb: MagicMock) -> None:
        """
        Tests the clean flow of XLSX to CSV conversion (Input Space Partitioning - Valid Case).

        Parameters
        ----------
        mock_file : MagicMock
            Mock injected for the builtins.open function (CSV writing).

        mock_load_wb : MagicMock
            Mock injected to simulate the openpyxl read engine.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            If vital I/O methods are not activated in the process.
        """
        mock_wb_instance = MagicMock()
        mock_sheet = MagicMock()
        mock_sheet.iter_rows.return_value = [("Medicine", "Interaction"), ("Aspirin", "1")]
        mock_wb_instance.active = mock_sheet
        mock_load_wb.return_value = mock_wb_instance

        convert_xlsx_to_csv("valid_input.xlsx", "valid_output.csv")

        mock_load_wb.assert_called_once_with("valid_input.xlsx")
        self.assertTrue(mock_file.called, "Erro Crítico: A operação de gravação do ficheiro CSV nunca foi instigada.")

    @patch("openpyxl.load_workbook")
    def test_convert_boundary_exception(self, mock_load_wb: MagicMock) -> None:
        """
        Forces the limit condition of a non-existent source file.

        Parameters
        ---------
        mock_load_wb : MagicMock
            Openpyxl mock configured to trigger a FileNotFoundError.

        Returns
        -------
        None

        Raises
        ------ 
        FileNotFoundError
            Ensures that the function does not mask the absence of a source file.
        """
        mock_load_wb.side_effect = FileNotFoundError("Ficheiro XLSX origem não existe.")

        with self.assertRaises(FileNotFoundError, msg="Falha na Defesa: A função abafou um FileNotFoundError originado pela leitura do Excel."):
            convert_xlsx_to_csv("ghost_input.xlsx", "output.csv")

    @patch("openpyxl.load_workbook")
    @patch("builtins.open", side_effect=PermissionError("Sem autorização de escrita."))
    def test_convert_to_exception(self, mock_file: MagicMock, mock_load_wb: MagicMock) -> None:
        """
        Ensures the correct propagation of I/O errors when writing to the destination.

        Parameters
        ---------
        mock_file : MagicMock 
            Mock of builtins.open configured to block writing (PermissionError).

        mock_load_wb : MagicMock 
            Passive mock of openpyxl, allowing reading to pass without errors.

        Returns
        -------
        None

        Raises
        ------
        PermissionError
            Ensures that I/O permission violations in the OS are thrown back.
        """
        mock_wb_instance = MagicMock()
        mock_load_wb.return_value = mock_wb_instance

        with self.assertRaises(PermissionError, msg="Falha na Defesa: A conversão não bloqueou adequadamente perante uma violação de permissão de sistema (PermissionError)."):
            convert_xlsx_to_csv("source.xlsx", "protected_output.csv")


if __name__ == '__main__':
    unittest.main()