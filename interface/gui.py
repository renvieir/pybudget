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
        """Cria a tabela com botões de ação"""
        frame_lista = ttk.Frame(self.root, padding=10)
        frame_lista.pack(fill="both", expand=True)

        # Frame para cabeçalhos
        frame_cabecalho = ttk.Frame(frame_lista)
        frame_cabecalho.pack(fill="x", pady=(0, 5))

        ttk.Label(frame_cabecalho, text="Data", width=10).pack(side="left")
        ttk.Label(frame_cabecalho, text="Descrição", width=20).pack(side="left")
        ttk.Label(frame_cabecalho, text="Valor (R$)", width=12).pack(side="left")
        ttk.Label(frame_cabecalho, text="Tipo", width=8).pack(side="left")
        ttk.Label(frame_cabecalho, text="Ações", width=20).pack(side="left")

        # Frame com scrollbar para os dados
        frame_scroll = ttk.Frame(frame_lista)
        frame_scroll.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.frame_dados = ttk.Frame(frame_scroll)
        self.frame_dados.pack(side="left", fill="both", expand=True)

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
        # Limpa os dados anteriores
        for widget in self.frame_dados.winfo_children():
            widget.destroy()

        # Ordena os lançamentos
        self.carteira.lancamentos.sort(reverse=True)

        # Cria as linhas da tabela
        for idx, lanc in enumerate(self.carteira.lancamentos):
            frame_linha = ttk.Frame(self.frame_dados)
            frame_linha.pack(fill="x", pady=2)

            # Cor baseada no tipo
            cor = "green" if lanc.tipo == "R" else "red"

            ttk.Label(frame_linha, text=lanc.data, width=10).pack(side="left")
            ttk.Label(frame_linha, text=lanc.descricao, width=20).pack(side="left")
            ttk.Label(
                frame_linha,
                text=f"R$ {lanc.valor:.2f}",
                width=12,
                foreground=cor,
            ).pack(side="left")
            ttk.Label(frame_linha, text=lanc.tipo, width=8).pack(side="left")

            # Botões de ação
            ttk.Button(
                frame_linha,
                text="Editar",
                command=lambda i=idx: self._editar_lancamento(i),
            ).pack(side="left", padx=2)

            ttk.Button(
                frame_linha,
                text="Excluir",
                command=lambda i=idx: self._remover_lancamento(i),
            ).pack(side="left", padx=2)

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

    def _editar_lancamento(self, idx):
        """Abre janela para editar um lançamento"""
        lanc = self.carteira.lancamentos[idx]

        # Cria janela de diálogo
        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Lançamento")
        janela_edicao.geometry("400x300")
        janela_edicao.transient(self.root)
        janela_edicao.grab_set()

        # Campo de descrição
        ttk.Label(janela_edicao, text="Descrição:").pack(pady=5)
        ent_desc = ttk.Entry(janela_edicao, width=30)
        ent_desc.insert(0, lanc.descricao)
        ent_desc.pack(pady=5)

        # Campo de valor
        ttk.Label(janela_edicao, text="Valor (R$):").pack(pady=5)
        ent_valor = ttk.Entry(janela_edicao, width=30)
        ent_valor.insert(0, str(lanc.valor))
        ent_valor.pack(pady=5)

        # Radio buttons para tipo
        var_tipo = tk.StringVar(value=lanc.tipo)
        ttk.Radiobutton(
            janela_edicao, text="Receita", variable=var_tipo, value="R"
        ).pack()
        ttk.Radiobutton(
            janela_edicao, text="Despesa", variable=var_tipo, value="D"
        ).pack()

        def salvar_edicao():
            try:
                nova_desc = ent_desc.get()
                novo_valor = float(ent_valor.get().replace(",", "."))
                novo_tipo = var_tipo.get()

                if not nova_desc or novo_valor <= 0:
                    messagebox.showwarning(
                        "Aviso",
                        "Descrição e valor válido são necessários!",
                    )
                    return

                lanc.descricao = nova_desc
                lanc.valor = novo_valor
                lanc.tipo = novo_tipo

                self.atualizar_tabela()
                janela_edicao.destroy()
            except ValueError:
                msg = "Valor inválido. Digite apenas números."
                messagebox.showerror("Erro", msg)

        # Frame para os botões
        frame_botoes = ttk.Frame(janela_edicao)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Salvar", command=salvar_edicao).pack(
            side="left", padx=5
        )

        ttk.Button(frame_botoes, text="Cancelar", command=janela_edicao.destroy).pack(
            side="left", padx=5
        )

    def _remover_lancamento(self, idx):
        """Remove um lançamento da carteira"""
        msg = "Deseja remover este lançamento?"
        if messagebox.askyesno("Confirmação", msg):
            del self.carteira.lancamentos[idx]
            self.atualizar_tabela()

    def salvar_e_sair(self):
        gerenciador.salvar_dados(self.carteira)
        self.root.destroy()
