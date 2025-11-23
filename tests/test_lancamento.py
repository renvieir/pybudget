import unittest
from modelos import Lancamento


class TestLancamento(unittest.TestCase):
    """Testes para a classe Lancamento"""

    def test_criar_lancamento_receita(self):
        """Testa criação de um lançamento de receita"""
        lancamento = Lancamento("Salário", 3000, "R")
        self.assertEqual(lancamento.descricao, "Salário")
        self.assertEqual(lancamento.valor, 3000.0)
        self.assertEqual(lancamento.tipo, "R")

    def test_criar_lancamento_despesa(self):
        """Testa criação de um lançamento de despesa"""
        lancamento = Lancamento("Aluguel", 1500, "D")
        self.assertEqual(lancamento.descricao, "Aluguel")
        self.assertEqual(lancamento.valor, 1500.0)
        self.assertEqual(lancamento.tipo, "D")

    def test_tipo_maiusculo(self):
        """Testa se o tipo é convertido para maiúsculo"""
        lancamento = Lancamento("Teste", 100, "r")
        self.assertEqual(lancamento.tipo, "R")

    def test_valor_float(self):
        """Testa conversão de valor para float"""
        lancamento = Lancamento("Teste", "250.50", "R")
        self.assertEqual(lancamento.valor, 250.50)
        self.assertIsInstance(lancamento.valor, float)

    def test_str_receita(self):
        """Testa representação em string de receita"""
        lancamento = Lancamento("Venda", 500, "R")
        resultado = str(lancamento)
        self.assertIn("+", resultado)
        self.assertIn("500.00", resultado)
        self.assertIn("Venda", resultado)

    def test_str_despesa(self):
        """Testa representação em string de despesa"""
        lancamento = Lancamento("Compra", 200, "D")
        resultado = str(lancamento)
        self.assertIn("-", resultado)
        self.assertIn("200.00", resultado)
        self.assertIn("Compra", resultado)

    def test_comparacao_valores(self):
        """Testa comparação entre lançamentos"""
        lancamento1 = Lancamento("A", 100, "R")
        lancamento2 = Lancamento("B", 200, "R")
        self.assertLess(lancamento1, lancamento2)
        self.assertGreater(lancamento2, lancamento1)


if __name__ == "__main__":
    unittest.main()
