import tkinter as tk
from interface import PyBudgetGUI


class Aplicacao:
    def __init__(self):
        self.root = tk.Tk()
        self.gui = PyBudgetGUI(self.root)

    def executar(self):
        self.root.mainloop()
