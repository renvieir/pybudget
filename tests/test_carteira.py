import unittest
from modelos import Carteira, Lancamento


class TestCarteira(unittest.TestCase):
    """Testes para a classe Carteira"""

    def setUp(self):
        """Configura uma carteira vazia antes de cada teste"""
        self.carteira = Carteira()

    def test_carteira_vazia(self):
        """Testa criação de uma carteira vazia"""
        self.assertEqual(len(self.carteira), 0)
        self.assertEqual(self.carteira.saldo_atual(), 0)

    def test_adicionar_lancamento(self):
        """Testa adição de um lançamento"""
        lancamento = Lancamento("Teste", 100, "R")
        self.carteira.adicionar(lancamento)
        self.assertEqual(len(self.carteira), 1)

    def test_saldo_com_receita(self):
        """Testa cálculo de saldo com receita"""
        lancamento = Lancamento("Salário", 5000, "R")
        self.carteira.adicionar(lancamento)
        self.assertEqual(self.carteira.saldo_atual(), 5000)

    def test_saldo_com_despesa(self):
        """Testa cálculo de saldo com despesa"""
        lancamento = Lancamento("Aluguel", 1000, "D")
        self.carteira.adicionar(lancamento)
        self.assertEqual(self.carteira.saldo_atual(), -1000)

    def test_saldo_misto(self):
        """Testa cálculo de saldo com receitas e despesas"""
        self.carteira.adicionar(Lancamento("Salário", 5000, "R"))
        self.carteira.adicionar(Lancamento("Aluguel", 1500, "D"))
        self.carteira.adicionar(Lancamento("Alimentação", 800, "D"))
        self.carteira.adicionar(Lancamento("Bônus", 1000, "R"))

        saldo_esperado = 5000 - 1500 - 800 + 1000
        self.assertEqual(self.carteira.saldo_atual(), saldo_esperado)

    def test_multiplos_lancamentos(self):
        """Testa adição de múltiplos lançamentos"""
        for i in range(5):
            self.carteira.adicionar(Lancamento(f"Item {i}", 100, "R"))
        self.assertEqual(len(self.carteira), 5)

    def test_len_carteira(self):
        """Testa método __len__"""
        self.assertEqual(len(self.carteira), 0)
        self.carteira.adicionar(Lancamento("A", 100, "R"))
        self.assertEqual(len(self.carteira), 1)
        self.carteira.adicionar(Lancamento("B", 200, "R"))
        self.assertEqual(len(self.carteira), 2)


if __name__ == "__main__":
    unittest.main()
