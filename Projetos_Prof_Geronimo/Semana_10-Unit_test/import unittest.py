import unittest
from funcao_semana_10 import generate_sequence

class TestSequenceGeneration(unittest.TestCase):
    """
    Testes implacáveis e estritos, baseados única e exclusivamente 
    na especificação original do contrato.
    """

    def test_invalid_inputs(self):
        """
        Objetivo: Garantir que a função rejeita números que não cumprem o requisito 
        "número inteiro não negativo".
        """
        negative_input_one = -1
        negative_input_five = -5
        
        with self.assertRaises(ValueError):
            generate_sequence(negative_input_one)
            
        with self.assertRaises(ValueError):
            generate_sequence(negative_input_five)

    def test_base_cases(self):
        """
        Objetivo: Verificar se a função devolve as listas corretas apenas com as regras 
        iniciais, sem precisar de acionar a fórmula matemática (f(0) e f(1)).
        """
        zero_index = 0
        one_index = 1
        
        self.assertEqual(generate_sequence(zero_index), [0])
        self.assertEqual(generate_sequence(one_index), [0, 1])

    def test_normal_cases(self):
        """
        Objetivo: Confirmar que a função aplica corretamente a fórmula 
        f(i) = 2 * f(i-2) + f(i-1) para índices i >= 2.
        """
        two_index = 2
        four_index = 4
        
        self.assertEqual(generate_sequence(two_index), [0, 1, 1])
        self.assertEqual(generate_sequence(four_index), [0, 1, 1, 3, 5])

if __name__ == '__main__':
    unittest.main()