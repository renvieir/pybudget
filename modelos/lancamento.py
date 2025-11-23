from datetime import datetime


class Lancamento:
    def __init__(self, descricao, valor, tipo):
        self.descricao = descricao
        self.valor = float(valor)
        self.tipo = tipo.upper()
        self.data = datetime.now().strftime("%d/%m/%Y")

    def __str__(self):
        simbolo = "+" if self.tipo == "R" else "-"
        return f"[{self.data}] {self.descricao:.<20} {simbolo} R$ {self.valor:.2f}"

    def __lt__(self, other):
        return self.valor < other.valor
