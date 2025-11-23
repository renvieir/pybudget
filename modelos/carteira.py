from modelos import Lancamento


class Carteira:
    def __init__(self):
        self.lancamentos: list[Lancamento] = []

    def adicionar(self, lancamento):
        self.lancamentos.append(lancamento)

    def saldo_atual(self):
        return sum(
            lanc.valor if lanc.tipo == "R" else -lanc.valor for lanc in self.lancamentos
        )

    def __len__(self):
        return len(self.lancamentos)
