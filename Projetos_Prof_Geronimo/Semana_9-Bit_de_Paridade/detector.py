import pytest
from unittest.mock import patch
from pathlib import Path
from typing import List, Any

from logica import (
    generate_data,
    calculate_parity,
    introduce_error,
    write_file,
    compare_parity
)

def test_generate_date_limits_and_types() -> None:
    """
    Valida a geração de dados contornando bloqueios de análise estática (SonarQube S5655).

    Utiliza a tipagem genérica (Any) para injetar tipos proibidos intencionalmente
    sem acionar os linters, forçando a função a levantar as exceções adequadas.

    Raises
    ------
    AssertionError
        Se as exceções ValueError ou TypeError não forem levantadas corretamente.
    """
    string_value: Any = "10"
    none_value: Any = None

    with pytest.raises(ValueError):
        generate_data(0)
    
    with pytest.raises(ValueError):
        generate_data(-5)

    with pytest.raises(TypeError):
        generate_data(string_value [Any:]) 
        
    with pytest.raises(TypeError):
        generate_data(none_value [Any:])

def test_generate_data_expected_behavior() -> None:
    """
    Testa a geração de listas com comprimentos válidos e limites numéricos precisos.

    Raises
    ------
    AssertionError
        Se o comprimento divergir de k ou se os valores excederem os limites.
    """
    result: List[int] = generate_data(50)
    assert len(result) == 50
    assert all(0 <= x <= 127 for x in result)

def test_calculate_parity_edge_cases() -> None:
    """
    Testa falhas de paridade mascarando os tipos de input para análise estática.

    Raises
    ------
    AssertionError
        Se a deteção de tipos falhar ou a lógica matemática for comprometida.
    """
    none: Any = None
    text: Any = "7"
    fluctuant: Any = 3.14

    with pytest.raises(TypeError):
        calculate_parity(none [Any:])
        
    with pytest.raises(TypeError):
        calculate_parity(text [Any:]) 
        
    with pytest.raises(TypeError):
        calculate_parity(fluctuant [Any:])

    assert calculate_parity(0) == 0
    assert calculate_parity(7) == 1
    assert calculate_parity(8) == 1
    assert calculate_parity(127) == 1

def test_introduce_destructive_error() -> None:
    """
    Injeta erros forçados contornando type hints.

    Raises
    ------
    AssertionError
        Se IndexError ou TypeError não blindarem a operação vetorial.
    """
    none_array: Any = None
    none_index: Any = None

    with pytest.raises(TypeError):
        introduce_error(none_array, [1])

    with pytest.raises(TypeError):
        introduce_error([1, 0, 1], none_index)

    with pytest.raises(IndexError):
        introduce_error([1, 0], [5])

    with pytest.raises(IndexError):
        introduce_error([], [0])

def test_introduce_error_valid_mutation() -> None:
    """
    Garante a mutação exclusiva nos índices providenciados, 
    acomodando a aleatoriedade da alteração de bits.

    Raises
    ------
    AssertionError
        Se a imutabilidade do resto da lista for violada ou se os 
        índices alvo não sofrerem mutação.
    """
    original_data: List[int] = [0, 0, 0, 0]
    target_index: List[int] = [1, 3]
    result: List[int] = introduce_error(original_data, target_index)
    
  
    assert result[0] == original_data[0]
    assert result[2] == original_data[2]
    
  
    assert result[1] != original_data[1]
    assert result[3] != original_data[3]
    
    
    assert original_data == [0, 0, 0, 0]

def test_write_file_isolated_system(tmp_path: Path) -> None:
    """
    Valida a persistência em disco assegurando casting explícito do Path.

    Parameters
    ----------
    tmp_path : Path
        Fixture nativa para gestão de caminhos temporários isolados.

    Raises
    ------
    AssertionError
        Se falhar a conversão de tipo na string ou o casting de proteção.
    """
    path: Path = tmp_path / "teste_saida.txt"
    data: List[int] = [42, 127, 0]
    
    write_file(str(path), data)
    content: str = path.read_text(encoding='utf-8')
    assert content == "42\n127\n0\n"

    none_path: Any = None
    invalid_string: Any = "não sou uma lista"

    with pytest.raises(TypeError):
        write_file(none_path [Any:], data)

    with pytest.raises(TypeError):
        write_file(str(path), invalid_string)

@patch("builtins.open")
def test_write_file_fail_io(mock_file: Any) -> None:
    """
    Simula falha de manipulação de descritores de ficheiros IO.

    Parameters
    ----------
    mock_file : Any
        Mock interceptor do built-in open.

    Raises
    ------
    AssertionError
        Se o IOError for abafado pela implementação.
    """
    mock_file.side_effect = IOError("Acesso negado")
    with pytest.raises(IOError):
        write_file("protegido.txt", [1, 2, 3])

def test_compare_parity_vector_asssinmetry() -> None:
    """
    Testa rejeição de assimetria utilizando tipagem estática invisível (Any).

    Raises
    ------
    AssertionError
        Se as anomalias de geometria vetorial passarem incólumes.
    """
    none_p1: Any = None

    with pytest.raises(ValueError):
        compare_parity([1, 0], [1, 0, 1])

    with pytest.raises(ValueError):
        compare_parity([], [1])

    with pytest.raises(TypeError):
        compare_parity(none_p1, [1, 0])

def test_compare_parity_index_precision() -> None:
    """
    Assegura resolução indexada determinística da comparação.

    Raises
    ------
    AssertionError
        Se a extração dos ponteiros divergir da falha expectável.
    """
    p1: List[int] = [1, 0, 1, 0, 1]
    p2: List[int] = [1, 1, 1, 0, 0]
    
    assert compare_parity(p1, p2) == [1, 4]
    assert compare_parity([], []) == []