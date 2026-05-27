import unittest
from unittest.mock import patch, mock_open, MagicMock


from gen_matrix_logic import read_meds, gen_matrix, export_excel, convert_xlsx_to_csv


class TestMedicalProcessor(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="Aspirin \n\n  Ibuprofen\nParacetamol  \n \n")
    def test_read_meds_valid_and_blank_lines(self, mock_file: MagicMock) -> None:
        """
        Testa a leitura de medicamentos lidando com linhas em branco e espaços residuais.

        Parameters
        ----------
        mock_file : MagicMock
            Mock de ficheiro de texto aberto em memória.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a limpeza de espaços e remoção de linhas em branco falhar.
        """
        result = read_meds("dummy_data.txt")
        expected_meds = ["Aspirin", "Ibuprofen", "Paracetamol"]
        self.assertEqual(result, expected_meds, "Erro: A lista extraída não ignorou espaços ou linhas vazias.")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_meds_empty_file(self, mock_file: MagicMock) -> None:
        """
        Testa o comportamento ao processar um ficheiro totalmente vazio.

        Parameters
        ----------
        mock_file : MagicMock
            Mock de ficheiro vazio em memória.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a função não retornar uma lista perfeitamente vazia.
        """
        result = read_meds("empty.txt")
        self.assertEqual(result, [], "Erro: Ficheiro vazio não gerou uma lista vazia de medicamentos.")

    @patch("builtins.open", side_effect=FileNotFoundError("Ficheiro não encontrado."))
    def test_read_meds_missing_file(self, mock_file: MagicMock) -> None:
        """
        Testa a condição de erro grave quando o ficheiro requisitado não existe.

        Parameters
        ----------
        mock_file : MagicMock
            Mock configurado para rebentar com FileNotFoundError.

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            Exceção estritamente esperada quando a leitura aponta para o vácuo.
        """
        with self.assertRaises(FileNotFoundError, msg="Erro Crítico: FileNotFoundError não foi levantado para ficheiro fantasma."):
            read_meds("missing_file.txt")

    def test_gen_matrix_standard_n_by_n(self) -> None:
        """
        Testa a geração de matriz cruzada para uma lista de múltiplos medicamentos (NxN).

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se as regras restritas de interação falharem (0 na diagonal, 1-6 no resto).
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
        Testa a geração de matriz no limite inferior extremo para apenas um medicamento (1x1).

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a matriz 1x1 não for exclusivamente composta pelo valor 0.
        """
        meds_list = ["DrugA"]
        matrix = gen_matrix(meds_list)
        expected_matrix = {("DrugA", "DrugA"): 0}
        self.assertEqual(matrix, expected_matrix, "Erro: A matriz isolada 1x1 falhou estruturalmente.")

    def test_gen_matrix_empty_list(self) -> None:
        """
        Testa a estabilidade da geração de matriz ao receber uma lista vazia.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se o retorno não for um dicionário inofensivo e vazio.
        """
        matrix = gen_matrix([])
        self.assertEqual(matrix, {}, "Erro: Matriz instanciada através de lista vazia não retornou um dicionário vazio.")

    def test_gen_matrix_invalid_type(self) -> None:
        """
        Força a rutura do sistema ao injetar tipos de dados inválidos.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Exceção mandatória ao injetar um valor None onde era esperada uma lista.
        """
        with self.assertRaises(TypeError, msg="Erro Crítico: TypeError ausente. A função engoliu um input inválido em vez de falhar."):
            gen_matrix(None)  # type: ignore

    @patch("openpyxl.Workbook")
    def test_export_excel_success(self, mock_workbook: MagicMock) -> None:
        """
        Valida a operação de exportação XLSX sem comprometer o disco físico.

        Parameters
        ----------
        mock_workbook : MagicMock
            Simulador de instância do Workbook do openpyxl.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se a função não invocar o método de guardar o ficheiro corretamente.
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
        Testa a reação destrutiva do exportador de Excel ao receber matriz nula.

        Parameters
        ----------
        Nenhum

        Returns
        -------
        None

        Raises
        ------
        TypeError
            Espera que a injeção de `None` faça a função implodir imediatamente com erro de tipo.
        """
        with self.assertRaises(TypeError, msg="Erro Crítico: TypeError não disparou ao tentar exportar uma matriz nula para Excel."):
            export_excel(None, ["DrugA"], "crash.xlsx")  # type: ignore


class TestFileConversion(unittest.TestCase):

    @patch("openpyxl.load_workbook")
    @patch("builtins.open", new_callable=mock_open)
    def test_convert_valid_partition(self, mock_file: MagicMock, mock_load_wb: MagicMock) -> None:
        """
        Testa o fluxo limpo de conversão de XLSX para CSV (Input Space Partitioning - Caso Válido).

        Parameters
        ----------
        mock_file : MagicMock
            Mock injetado para a função builtins.open (escrita do CSV).
        mock_load_wb : MagicMock
            Mock injetado para simular o motor de leitura do openpyxl.

        Returns
        -------
        None

        Raises
        ------
        AssertionError
            Se os métodos vitais de I/O não forem ativados no processo.
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
        Força a condição limite de um ficheiro fonte inexistente.

        Parameters
        ----------
        mock_load_wb : MagicMock
            Mock do openpyxl configurado para detonar um FileNotFoundError.

        Returns
        -------
        None

        Raises
        ------
        FileNotFoundError
            Garantia de que a função não mascare a ausência de ficheiro fonte.
        """
        mock_load_wb.side_effect = FileNotFoundError("Ficheiro XLSX origem não existe.")

        with self.assertRaises(FileNotFoundError, msg="Falha na Defesa: A função abafou um FileNotFoundError originado pela leitura do Excel."):
            convert_xlsx_to_csv("ghost_input.xlsx", "output.csv")

    @patch("openpyxl.load_workbook")
    @patch("builtins.open", side_effect=PermissionError("Sem autorização de escrita."))
    def test_convert_io_exception(self, mock_file: MagicMock, mock_load_wb: MagicMock) -> None:
        """
        Garante a correta propagação de erros de I/O na escrita do destino.

        Parameters
        ----------
        mock_file : MagicMock
            Mock do builtins.open configurado para bloquear a escrita (PermissionError).
        mock_load_wb : MagicMock
            Mock passivo do openpyxl, permitindo que a leitura passe sem erros.

        Returns
        -------
        None

        Raises
        ------
        PermissionError
            Assegura que a violação de permissões I/O no SO é lançada de volta.
        """
        mock_wb_instance = MagicMock()
        mock_load_wb.return_value = mock_wb_instance

        with self.assertRaises(PermissionError, msg="Falha na Defesa: A conversão não bloqueou adequadamente perante uma violação de permissão de sistema (PermissionError)."):
            convert_xlsx_to_csv("source.xlsx", "protected_output.csv")


if __name__ == '__main__':
    unittest.main()