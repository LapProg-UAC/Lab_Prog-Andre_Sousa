from typing import List, Dict, Tuple, Any
from gen_matrix_logic import read_meds, gen_matrix, export_excel, convert_xlsx_to_csv
from gen_receipts_logic import read_csv_matrix, generate_synthetic_prescriptions, export_to_json

def main() -> None:
    """
    Main function that combines the execution of the interaction modules and synthetic prescriptions.
    This function coordinates the reading of medications, generation of the matrix, export to Excel and CSV files,
    reading of the converted matrix, and finally, 
    the generation and export of synthetic medical prescriptions in JSON format.

    Raises
    ------
    Exception
        Any unforeseen error during the input and output execution chain.
    """
    try:
        input_txt_file: str = "medicamentos.txt"
        output_excel_file: str = "interacoes_meds.xlsx"
        output_csv_file: str = "interacoes_meds.csv"
        output_json_file: str = "receitas_sinteticas.json"
        total_prescriptions: int = 100

        print("A iniciar o sistema de orquestração do Maquinista...")
        
        print("A extrair medicamentos do ficheiro de texto base...")
        base_medications: List[str] = read_meds(input_txt_file)
        
        print("A gerar a matriz algorítmica de interações medicamentosas...")
        generated_matrix: Dict[Tuple[str, str], int] = gen_matrix(base_medications)
        
        print("A exportar os dados estruturados para a folha de cálculo Excel...")
        export_excel(generated_matrix, base_medications, output_excel_file)
        
        print("A converter o artefacto Excel para a estrutura estrita CSV...")
        convert_xlsx_to_csv(output_excel_file, output_csv_file)
        
        print("A carregar as definições atualizadas a partir do ficheiro CSV...")
        csv_meds: List[str]
        csv_matrix: Dict[Tuple[str, str], int]
        csv_meds, csv_matrix = read_csv_matrix(output_csv_file)
        
        print("A orquestrar a síntese controlada dos registos de receitas médicas...")
        synthetic_records: List[Dict[str, Any]] = generate_synthetic_prescriptions(
            total_prescriptions, 
            csv_meds, 
            csv_matrix
        )
        
        print("A consolidar a exportação definitiva do lote no formato universal JSON...")
        export_to_json(synthetic_records, output_json_file)
        
        print("Orquestração concluída com sucesso. Todos os módulos completaram as suas rotinas.")

    except FileNotFoundError as exc:
        print(f"Erro Crítico de Leitura: Ficheiro essencial não localizado na diretoria. Detalhe técnico: {exc}")
    except TypeError as exc:
        print(f"Falha Estrutural de Tipos: As estruturas de dados não coincidem com o protocolo esperado. Detalhe técnico: {exc}")
    except ValueError as exc:
        print(f"Anomalia de Valores: Ocorreu uma quebra na lógica matemática ou estrutural. Detalhe técnico: {exc}")
    except Exception as exc:
        print(f"Colapso Sistémico Iminente: Ocorreu uma exceção não catalogada no fluxo de execução. Detalhe técnico: {exc}")

if __name__ == "__main__":
    main()