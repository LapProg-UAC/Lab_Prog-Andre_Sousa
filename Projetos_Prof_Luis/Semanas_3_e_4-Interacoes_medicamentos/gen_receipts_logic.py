import csv
import json 
import random
from typing import Dict, List, Tuple, Any, Optional, Set
from Data_Base import NAMES_POOL, INTERACTION_MAP


def parse_interaction_row(row_drug: str, row_data: List[str], headers: List[str]) -> Dict[Tuple[str, str], int]:
    """
    Analyzes an individual row of the CSV and extracts the mapped interaction pairs.

    Parameters
    ---------
    row_drug : str
        The name of the base drug corresponding to the current row.

    row_data : List[str]
        The list containing the raw values ​​extracted from the row.

    headers : List[str]
        The list of headers containing the names of the target drugs.

    Returns
    -------
    Dict[Tuple[str, str], int]
        A partial dictionary containing the numerical crosses detected in this row.
    """
    row_interactions: Dict[Tuple[str, str], int] = {}
    col_index: int
    col_name: str
    
    for col_index, col_name in enumerate(headers[1:], start=1):
        if col_index < len(row_data):
            col_drug: str = col_name.strip().lower()
            interaction_level_raw: str = row_data[col_index].strip()
            
            if interaction_level_raw.isdigit():
                sorted_pair: List[str] = sorted([row_drug, col_drug])
                normalized_tuple: Tuple[str, str] = (sorted_pair[0], sorted_pair[1])
                row_interactions[normalized_tuple] = int(interaction_level_raw)
                
    return row_interactions

def read_csv_matrix(file_path: str) -> Tuple[List[str], Dict[Tuple[str, str], int]]:
    """
    Processes the CSV file and extracts the list of medications and the numerically mapped matrix.

    Parameters
    ---------
    file_path : str
        The absolute or relative path to the CSV file containing the interaction matrix.

    Returns
    -------
    Tuple[List[str], Dict[Tuple[str, str], int]]
        A tuple containing the list of valid medications and the dictionary of quantitative crosses.

    Raises
    ------
    TypeError
        Raised if the file path is not strictly a string.
    FileNotFoundError
        Raised if the specified file is not found on the system.
    ValueError
        Raised in case of read failures or critical structural anomalies.
    """
    if not isinstance(file_path, str):
        raise TypeError("Erro: O caminho do ficheiro CSV deve ser obrigatoriamente uma string.")

    try:
        medications_list: List[str] = []
        interaction_matrix: Dict[Tuple[str, str], int] = {}
        
        with open(file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader: Any = csv.reader(csv_file)
            headers: List[str] = next(csv_reader)
            
            if not headers or len(headers) < 2:
                raise ValueError("Erro: O ficheiro CSV de interações encontra-se vazio ou desprovido de cabeçalhos.")
            
            medications_list = [med.strip().lower() for med in headers[1:] if med.strip()]
            
            row: List[str]
            for row in csv_reader:
                if not row:
                    continue
                
                row_drug: str = row[0].strip().lower()
                interaction_matrix.update(parse_interaction_row(row_drug, row, headers))
                            
        return medications_list, interaction_matrix

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Erro Crítico de I/O: Ficheiro não localizado no sistema. Detalhe: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Erro inesperado durante a extração de dados do CSV: {exc}") from exc

def generate_unique_id(registered_ids: Set[int]) -> int:
    """
    Generates a unique user identifier with exactly nine digits.

    Parameters
    ---------
    registered_ids : Set[int]
        The set of identifiers previously generated to guarantee uniqueness in O(1) time.

    Returns
    -------
    int
        The unique numeric identifier generated stochastically.
    """
    
    patient_id: int = random.randint(100000000, 999999999)
    if patient_id not in registered_ids:
        registered_ids.add(patient_id)
        return patient_id

def evaluate_prescription_interactions(selected_medications: List[str], interaction_matrix: Dict[Tuple[str, str], int]) -> List[str]:
    """
   Evaluates the exact combination of three medications against the matrix mapping the index (1+2, 1+3, 2+3).

    Parameters
    ---------
    selected_medications : List[str]
        The restricted list of medications uniquely selected for the current prescription.

    interaction_matrix : Dict[Tuple[str, str], int]
        The global quick-search dictionary containing the interactions.

    Returns
    -------
    List[str]
        List with the textual strings of each detected interaction, properly enumerated.
    """
    detected_interactions: List[str] = []
    
    index_combinations: List[Tuple[int, int]] = [(0, 1), (0, 2), (1, 2)]
    
    pair: Tuple[int, int]
    for pair in index_combinations:
        idx_a: int = pair[0]
        idx_b: int = pair[1]
        
        drug_a: str = selected_medications[idx_a].lower()
        drug_b: str = selected_medications[idx_b].lower()
        
        sorted_drugs: List[str] = sorted([drug_a, drug_b])
        search_target: Tuple[str, str] = (sorted_drugs[0], sorted_drugs[1])
        
        interaction_level: Optional[int] = interaction_matrix.get(search_target)
        if interaction_level is not None:
            translation: Optional[str] = INTERACTION_MAP.get(interaction_level)
            if translation:
                detected_interactions.append(f"Efeito de {idx_a + 1}+{idx_b + 1}: [{translation}]")
                
    return detected_interactions

def create_single_prescription(meds_list: List[str], interaction_matrix: Dict[Tuple[str, str], int], registered_ids: Set[int]) -> Dict[str, Any]:
    """
    Constructs a standalone record of a single prescription by applying numerical formatting to the drugs.

    Parameters
    ---------
    meds_list : List[str]
        The complete catalog of eligible medications present in the source file.
    interaction_matrix : Dict[Tuple[str, str], int]
        The matrix of numerical interactions in dictionary format.
    registered_ids : Set[int]
        The global and shared record of identifiers.

    Returns
    -------
    Dict[str, Any]
    The formatted dictionary containing the anthropomorphic data and interactions.
    """
    patient_id: int = generate_unique_id(registered_ids)
    first_name: str = random.choice(NAMES_POOL["first_names"])
    last_name: str = random.choice(NAMES_POOL["last_names"])
    
    selected_medications: List[str] = random.sample(meds_list, 3)
    
    detected_interactions: List[str] = evaluate_prescription_interactions(selected_medications, interaction_matrix)
    
    formatted_medications: List[str] = []
    med_index: int
    med_name: str
    for med_index, med_name in enumerate(selected_medications):
        formatted_medications.append(f"{med_index + 1}. {med_name}")
    
    return {
        "id": patient_id,
        "nome": f"{first_name} {last_name}",
        "medicamentos": formatted_medications,
        "interacoes": detected_interactions
    }

def generate_synthetic_prescriptions(num_records: int, meds_list: List[str], interaction_matrix: Dict[Tuple[str, str], int]) -> List[Dict[str, Any]]:
    """
    Combines the generation of synthetic recipe batches, mitigating any cognitive complexity.

    Parameters
    ---------
    num_records : int
        The total and strict quantity of synthetic records requested.

    meds_list : List[str]
        The clean and structured base drug catalog.

    interaction_matrix : Dict[Tuple[str, str], int]
        The hash table mapping containing the cross-risk quantification.

    Returns
    -------
    List[Dict[str, Any]]
        The aggregated structure containing the final records ready for export.

    Raises
    ------
    ValueError
        Raised due to unforeseen algorithmic failures in the loop orchestration.

    TypeError
        Raised due to type violations at runtime.
    """
    if not isinstance(num_records, int) or num_records <= 0:
        raise ValueError("Erro: A quantidade de registos a gerar deve ser um número inteiro estritamente positivo.")
    if not isinstance(meds_list, list) or len(meds_list) < 3:
        raise ValueError("Erro: A lista de medicamentos base deve conter no mínimo 3 opções válidas.")
    if not isinstance(interaction_matrix, dict):
        raise TypeError("Erro: A matriz de interações fornecida não obedece ao tipo dicionário esperado.")

    generated_data: List[Dict[str, Any]] = []
    registered_ids: Set[int] = set()

    try:
       
        for _ in range(num_records):
            prescription_record: Dict[str, Any] = create_single_prescription(meds_list, interaction_matrix, registered_ids)
            generated_data.append(prescription_record)

        return generated_data

    except Exception as exc:
        raise ValueError(f"Erro algorítmico crítico durante a síntese de registos: {exc}") from exc

def export_to_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Saves structured dictionaries in strict JSON format, ensuring global compatibility.

    Parameters
    ---------
    data : List[Dict[str, Any]]
        The volatile in-memory structure targeted for export.

    file_path : str
        The absolute or relative target path.

    Returns
    -------
    None
        Acts strictly, generating I/O side effects.

    Raises
    ------
    TypeError
        Raised in case of data structure discrepancies.

    IOError
        Raised due to operating system constraints during writing.
    """
    if not isinstance(data, list):
        raise TypeError("Erro: A estrutura de dados para exportação exige o formato de lista.")
    if not isinstance(file_path, str):
        raise TypeError("Erro: O caminho de exportação especificado deve ser uma string.")

    try:
        with open(file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as exc:
        raise IOError(f"Falha de sistema crítica ao escrever o ficheiro JSON: {exc}") from exc