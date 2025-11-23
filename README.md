# PyBudget

Um gerenciador financeiro desktop desenvolvido em Python com interface gráfica intuitiva.

## Descrição

PyBudget é uma aplicação para gestão de finanças pessoais que permite controlar receitas e despesas de forma simples e visual.

## Recursos

- ✨ Interface gráfica moderna com Tkinter
- 💰 Registro de receitas e despesas
- 📊 Cálculo automático de saldo
- 💾 Persistência de dados em arquivo
- 🎯 Visualização clara de transações em tabela

## Tecnologias

- **Linguagem:** Python
- **Interface:** Tkinter (GUI)
- **Estrutura:** Arquitetura em camadas (modelos, interface, dados)

## Estrutura do Projeto

```
pybudget/
├── main.py                 # Ponto de entrada da aplicação
├── applicacao/
│   ├── __init__.py
│   └── app.py             # Classe principal da aplicação
├── modelos/
│   ├── __init__.py
│   ├── carteira.py        # Modelo de carteira (gerencia transações)
│   └── lancamento.py      # Modelo de lançamento (receita/despesa)
├── interface/
│   ├── __init__.py
│   └── gui.py             # Interface gráfica do usuário
├── dados/
│   ├── __init__.py
│   ├── gerenciador.py     # Gerenciador de persistência de dados
│   └── dados.txt          # Arquivo de armazenamento
└── README.md
```

## Como Executar

```bash
python main.py
```


## Como rodar testes

```bash
python -m unittest
```

## Funcionamento

1. **Novo Lançamento:** Preencha a descrição, valor e selecione o tipo (Receita ou Despesa)
2. **Adicionar:** Clique no botão para registrar a transação
3. **Histórico:** Visualize todas as transações na tabela
4. **Saldo:** O saldo atual é calculado automaticamente

# Disclaimer

Feito com ajuda do gemini