import os

from modelos import Lancamento

NOME_ARQUIVO = "dados_financeiros.txt"


def salvar_dados(carteira):
    try:
        with open(NOME_ARQUIVO, "w", encoding="utf-8") as arquivo:
            for item in carteira.lancamentos:
                linha = f"{item.descricao};{item.valor};{item.tipo};{item.data}\n"
                arquivo.write(linha)
        print("✅ Dados salvos com sucesso!")
    except IOError as e:
        print(f"❌ Erro ao salvar arquivo: {e}")


def carregar_dados(carteira):
    if not os.path.exists(NOME_ARQUIVO):
        return

    try:
        with open(NOME_ARQUIVO, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")
                if len(dados) >= 3:
                    desc, val, tipo, _ = dados
                    novo_lancamento = Lancamento(desc, val, tipo)
                    novo_lancamento.data = dados[3]
                    carteira.adicionar(novo_lancamento)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
