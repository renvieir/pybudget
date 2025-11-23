import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Carteira, Lancamento
from dados import gerenciador


class PyBudgetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyBudget - Gestão Financeira")
        self.root.geometry("900x450")

        # Inicializa a lógica de negócios
        self.carteira = Carteira()
        gerenciador.carregar_dados(self.carteira)

        # Configura o evento de fechamento da janela
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar_janela)

        # Configuração de Estilos (Cores)
        style = ttk.Style()
        style.configure("Treeview", rowheight=25)

        # --- MONTAGEM DA TELA ---
        self._criar_area_insercao()
        self._criar_area_lista()
        self._criar_area_resumo()

        # Carrega dados na tabela
        self.atualizar_tabela()

    def _criar_area_insercao(self):
        """Cria os campos de input e botão adicionar"""
        frame_input = ttk.LabelFrame(self.root, text="Novo Lançamento", padding=10)
        frame_input.pack(fill="x", padx=10, pady=5)

        # Descrição
        ttk.Label(frame_input, text="Descrição:").grid(row=0, column=0, padx=5)
        self.ent_desc = ttk.Entry(frame_input, width=25)
        self.ent_desc.grid(row=0, column=1, padx=5)

        # Valor
        ttk.Label(frame_input, text="Valor (R$):").grid(row=0, column=2, padx=5)
        self.ent_valor = ttk.Entry(frame_input, width=10)
        self.ent_valor.grid(row=0, column=3, padx=5)

        # Tipo (Radio Buttons)
        self.var_tipo = tk.StringVar(value="D")  # D para Despesa por padrão
        rb_rec = ttk.Radiobutton(
            frame_input, text="Receita", variable=self.var_tipo, value="R"
        )
        rb_des = ttk.Radiobutton(
            frame_input, text="Despesa", variable=self.var_tipo, value="D"
        )
        rb_rec.grid(row=0, column=4)
        rb_des.grid(row=0, column=5)

        # Botão Adicionar
        btn_add = ttk.Button(
            frame_input, text="Adicionar", command=self.adicionar_lancamento
        )
        btn_add.grid(row=0, column=6, padx=10)

    def _criar_area_lista(self):
        """Cria a tabela (Treeview) para exibir os dados"""
        frame_lista = ttk.Frame(self.root, padding=10)
        frame_lista.pack(fill="both", expand=True)

        colunas = ("data", "desc", "valor", "tipo")
        self.tree = ttk.Treeview(frame_lista, columns=colunas, show="headings")

        # Cabeçalhos
        self.tree.heading("data", text="Data")
        self.tree.heading("desc", text="Descrição")
        self.tree.heading("valor", text="Valor (R$)")
        self.tree.heading("tipo", text="Tipo")

        # Tamanho das colunas
        self.tree.column("data", width=80, anchor="center")
        self.tree.column("desc", width=200)
        self.tree.column("valor", width=100, anchor="e")  # 'e' = east (direita)
        self.tree.column("tipo", width=50, anchor="center")

        # Barra de rolagem
        scrollbar = ttk.Scrollbar(
            frame_lista, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Tags de cor para as linhas
        self.tree.tag_configure("receita", foreground="green")
        self.tree.tag_configure("despesa", foreground="red")

    def _criar_area_resumo(self):
        """Mostra o Saldo e Botão Salvar"""
        frame_resumo = ttk.Frame(self.root, padding=10)
        frame_resumo.pack(fill="x")

        self.lbl_saldo = ttk.Label(
            frame_resumo, text="Saldo: R$ 0.00", font=("Arial", 12, "bold")
        )
        self.lbl_saldo.pack(side="left")

        btn_salvar = ttk.Button(
            frame_resumo, text="Salvar e Sair", command=self.salvar_e_sair
        )
        btn_salvar.pack(side="right")

    def adicionar_lancamento(self):
        desc = self.ent_desc.get()
        valor_str = self.ent_valor.get()
        tipo = self.var_tipo.get()

        if not desc or not valor_str:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            valor = float(valor_str.replace(",", "."))  # Aceita virgula ou ponto
            novo = Lancamento(desc, valor, tipo)
            self.carteira.adicionar(novo)

            # Atualiza a interface
            self.atualizar_tabela()

            # Limpa campos
            self.ent_desc.delete(0, tk.END)
            self.ent_valor.delete(0, tk.END)
            self.ent_desc.focus()

        except ValueError:
            messagebox.showerror("Erro", "Valor inválido. Digite apenas números.")

    def atualizar_tabela(self):
        # Limpa a tabela atual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reinsere os dados da carteira
        # Ordenamos para mostrar os mais caros/importantes primeiro
        self.carteira.lancamentos.sort(reverse=True)

        for lanc in self.carteira.lancamentos:
            # Define a cor baseada no tipo
            tag = "receita" if lanc.tipo == "R" else "despesa"

            self.tree.insert(
                "",
                "end",
                values=(lanc.data, lanc.descricao, f"R$ {lanc.valor:.2f}", lanc.tipo),
                tags=(tag,),
            )

        # Atualiza o Saldo
        saldo = self.carteira.saldo_atual()
        self.lbl_saldo.config(
            text=f"Saldo Total: R$ {saldo:.2f}",
            foreground="#55FF11" if saldo >= 0 else "#FF5511",
        )

    def ao_fechar_janela(self):
        """Chamado quando o usuário clica no botão X"""
        resposta = messagebox.askyesnocancel(
            "Confirmação", "Deseja salvar as alterações antes de sair?"
        )
        if resposta is True:  # Sim - salva e fecha
            gerenciador.salvar_dados(self.carteira)
            self.root.destroy()
        elif resposta is False:  # Não - fecha sem salvar
            self.root.destroy()
        # None significa cancelar - não faz nada

    def salvar_e_sair(self):
        gerenciador.salvar_dados(self.carteira)
        self.root.destroy()
