import unittest
import os
import tempfile
from modelos import Carteira, Lancamento
from dados import gerenciador


class TestGerenciador(unittest.TestCase):
    """Testes para o gerenciador de dados"""

    def setUp(self):
        """Configura um arquivo temporário para testes"""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        )
        self.temp_file.close()
        self.original_arquivo = gerenciador.NOME_ARQUIVO
        gerenciador.NOME_ARQUIVO = self.temp_file.name

    def tearDown(self):
        """Limpa o arquivo temporário após os testes"""
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
        gerenciador.NOME_ARQUIVO = self.original_arquivo

    def test_salvar_e_carregar_dados(self):
        """Testa salvamento e carregamento de dados"""
        # Cria e salva carteira
        carteira_salva = Carteira()
        carteira_salva.adicionar(Lancamento("Salário", 5000, "R"))
        carteira_salva.adicionar(Lancamento("Aluguel", 1500, "D"))
        gerenciador.salvar_dados(carteira_salva)

        # Carrega dados em nova carteira
        carteira_carregada = Carteira()
        gerenciador.carregar_dados(carteira_carregada)

        # Verifica se os dados foram restaurados
        self.assertEqual(len(carteira_carregada), 2)
        self.assertEqual(carteira_carregada.saldo_atual(), 5000 - 1500)

    def test_carregar_arquivo_inexistente(self):
        """Testa carregamento quando arquivo não existe"""
        carteira = Carteira()
        os.remove(self.temp_file.name)
        # Não deve lançar exceção
        gerenciador.carregar_dados(carteira)
        self.assertEqual(len(carteira), 0)

    def test_salvar_carteira_vazia(self):
        """Testa salvamento de carteira vazia"""
        carteira = Carteira()
        gerenciador.salvar_dados(carteira)

        # Verifica se o arquivo foi criado vazio
        self.assertTrue(os.path.exists(self.temp_file.name))
        with open(self.temp_file.name, "r") as f:
            conteudo = f.read()
            self.assertEqual(conteudo, "")

    def test_persistencia_multiplos_lancamentos(self):
        """Testa persistência de múltiplos lançamentos"""
        carteira_salva = Carteira()
        lancamentos = [
            Lancamento("Receita 1", 1000, "R"),
            Lancamento("Despesa 1", 500, "D"),
            Lancamento("Receita 2", 2000, "R"),
            Lancamento("Despesa 2", 300, "D"),
        ]
        for lancamento in lancamentos:
            carteira_salva.adicionar(lancamento)

        gerenciador.salvar_dados(carteira_salva)

        carteira_carregada = Carteira()
        gerenciador.carregar_dados(carteira_carregada)

        self.assertEqual(len(carteira_carregada), 4)
        self.assertEqual(carteira_carregada.saldo_atual(), carteira_salva.saldo_atual())


if __name__ == "__main__":
    unittest.main()
