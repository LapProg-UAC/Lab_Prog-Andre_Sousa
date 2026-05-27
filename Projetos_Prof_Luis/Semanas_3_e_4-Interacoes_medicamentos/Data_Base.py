from typing import Dict, List



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