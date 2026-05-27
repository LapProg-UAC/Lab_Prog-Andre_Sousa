import csv
import json 
import random
from typing import Dict, List, Tuple, Any, Optional, Set

NAMES_POOL: Dict[str, List[str]] = {
    "first_names": ["Ana", "João", "Maria", "Rui", "Catarina", "Pedro", "Marta", "Tiago", "Sofia", "Nuno", "Inês", "Miguel", "Beatriz", "Diogo", "Joana", "Bruno", "Diana", "Hugo", "Leonor", "Carlos"],
    "last_names": ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira", "Costa", "Rodrigues", "Martins", "Jesus", "Sousa", "Fernandes", "Gomes", "Marques", "Almeida", "Ribeiro", "Pinto", "Carvalho", "Teixeira", "Moreira", "Correia"]
}

INTERACTION_MAP: Dict[int, str] = {
    1: "Sem significado clínico",
    2: "Potencialmente grave",
    3: "Potenciador do efeito terapêutico/tóxico dos medicamentos da coluna horizontal",
    4: "Potenciador do efeito terapêutico/tóxico dos medicamentos da coluna vertical",
    5: "Diminuidor do efeito terapêutico/tóxico dos medicamentos da coluna horizontal",
    6: "Diminuidor do efeito terapêutico/tóxico dos medicamentos da coluna vertical"
}

def _parse_interaction_row(row_drug: str, row_data: List[str], headers: List[str]) -> Dict[Tuple[str, str], int]:
    """
    Analisa uma linha individual do CSV e extrai os pares de interação mapeados.

    Parameters
    ----------
    row_drug : str
        O nome do medicamento base correspondente à linha atual.
    row_data : List[str]
        A lista contendo os valores em bruto extraídos da linha.
    headers : List[str]
        A lista de cabeçalhos contendo os nomes dos medicamentos alvos.

    Returns
    -------
    Dict[Tuple[str, str], int]
        Um dicionário parcial contendo os cruzamentos numéricos detetados nesta linha.
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
    Processa o ficheiro CSV e extrai a lista de medicamentos e a matriz numéricamente mapeada.

    Parameters
    ----------
    file_path : str
        O caminho absoluto ou relativo para o ficheiro CSV contendo a matriz de interações.

    Returns
    -------
    Tuple[List[str], Dict[Tuple[str, str], int]]
        Um tuplo contendo a lista de medicamentos válidos e o dicionário de cruzamentos quantitativos.

    Raises
    ------
    TypeError
        Levantado caso o caminho do ficheiro não seja estritamente uma string.
    FileNotFoundError
        Levantado caso o ficheiro especificado não seja encontrado no sistema.
    ValueError
        Levantado perante falhas na leitura ou anomalias estruturais críticas.
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
                interaction_matrix.update(_parse_interaction_row(row_drug, row, headers))
                            
        return medications_list, interaction_matrix

    except FileNotFoundError as exc:
        raise FileNotFoundError(f"Erro Crítico de I/O: Ficheiro não localizado no sistema. Detalhe: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Erro inesperado durante a extração de dados do CSV: {exc}") from exc

def _generate_unique_id(registered_ids: Set[int]) -> int:
    """
    Gera um identificador de utente único com exatamente nove dígitos.

    Parameters
    ----------
    registered_ids : Set[int]
        O conjunto de identificadores previamente gerados para garantir unicidade em tempo O(1).

    Returns
    -------
    int
        O identificador numérico único gerado de forma estocástica.
    """
    while True:
        patient_id: int = random.randint(100000000, 999999999)
        if patient_id not in registered_ids:
            registered_ids.add(patient_id)
            return patient_id

def _evaluate_prescription_interactions(selected_medications: List[str], interaction_matrix: Dict[Tuple[str, str], int]) -> List[str]:
    """
    Avalia a exata combinação de três medicamentos face à matriz mapeando o índice (1+2, 1+3, 2+3).

    Parameters
    ----------
    selected_medications : List[str]
        A lista restrita de medicamentos selecionados de forma única para a receita atual.
    interaction_matrix : Dict[Tuple[str, str], int]
        O dicionário global de pesquisa rápida contendo as interações.

    Returns
    -------
    List[str]
        Lista com as strings textuais de cada interação detetada devidamente enumeradas.
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

def _create_single_prescription(meds_list: List[str], interaction_matrix: Dict[Tuple[str, str], int], registered_ids: Set[int]) -> Dict[str, Any]:
    """
    Constrói o registo isolado de uma única receita médica aplicando formatação numérica aos fármacos.

    Parameters
    ----------
    meds_list : List[str]
        O catálogo completo de medicamentos elegíveis presentes no ficheiro de origem.
    interaction_matrix : Dict[Tuple[str, str], int]
        A matriz de interações numéricas em formato de dicionário.
    registered_ids : Set[int]
        O registo global e partilhado de identificadores.

    Returns
    -------
    Dict[str, Any]
        O dicionário formatado contendo os dados antropomórficos e as interações.
    """
    patient_id: int = _generate_unique_id(registered_ids)
    first_name: str = random.choice(NAMES_POOL["first_names"])
    last_name: str = random.choice(NAMES_POOL["last_names"])
    
    selected_medications: List[str] = random.sample(meds_list, 3)
    
    detected_interactions: List[str] = _evaluate_prescription_interactions(selected_medications, interaction_matrix)
    
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
    Orquestra a geração do lote de receitas sintéticas mitigando qualquer complexidade cognitiva.

    Parameters
    ----------
    num_records : int
        A quantidade total e estrita de registos sintéticos requisitados.
    meds_list : List[str]
        O catálogo de medicamentos base limpo e estruturado.
    interaction_matrix : Dict[Tuple[str, str], int]
        O mapeamento em tabela de dispersão contendo a quantificação do risco cruzado.

    Returns
    -------
    List[Dict[str, Any]]
        A estrutura agregada contendo os registos definitivos prontos a exportar.

    Raises
    ------
    ValueError
        Levantado perante falhas algorítmicas imprevistas na orquestração dos laços.
    TypeError
        Levantado face a violações de tipo em tempo de execução.
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
            prescription_record: Dict[str, Any] = _create_single_prescription(meds_list, interaction_matrix, registered_ids)
            generated_data.append(prescription_record)

        return generated_data

    except Exception as exc:
        raise ValueError(f"Erro algorítmico crítico durante a síntese de registos: {exc}") from exc

def export_to_json(data: List[Dict[str, Any]], file_path: str) -> None:
    """
    Grava os dicionários estruturados no formato estrito JSON assegurando compatibilidade global.

    Parameters
    ----------
    data : List[Dict[str, Any]]
        A estrutura volátil em memória alvo da exportação.
    file_path : str
        O caminho alvo absoluto ou relativo.

    Returns
    -------
    None
        Atua estritamente gerando efeitos colaterais de I/O.

    Raises
    ------
    TypeError
        Levantado em caso de discrepância de estruturas de dados.
    IOError
        Levantado perante constrangimentos do sistema operativo no momento da escrita.
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