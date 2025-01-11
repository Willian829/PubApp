import tkinter as tk
from tkinter import messagebox, simpledialog

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
    
class Estoque:
    def __init__(self):
        self.produtos = {}

    def registrar_produto(self, produto, quantidade):
        if produto.nome in self.produtos:
            self.produtos[produto.nome]['quantidade'] += quantidade
        else:
            self.produtos[produto.nome] = {'produto': produto, 'quantidade': quantidade}

    def remover_produto(self, produto_nome, quantidade):
        if produto_nome in self.produtos and self.produtos[produto_nome]['quantidade'] >= quantidade:
            self.produtos[produto_nome]['quantidade'] -= quantidade
            if self.produtos[produto_nome]['quantidade'] == 0:
                del self.produtos[produto_nome]
            return True
        return False
    
    def listar_produtos(self):
        return [(info['produto'].nome, info['produto'].preco, info['quantidade']) for info in self.produtos.values()]
    
class Pedido:
    def __init__(self):
        self.itens = []

    def add_item(self, produto, quantidade):
        self.itens.append((produto, quantidade))

    def calc_total(self):
        total = sum(produto.preco * quantidade for produto, quantidade in self.itens)
        return total
    
    def listar_pedido(self):
        return [(produto.nome, quantidade, produto.preco * quantidade) for produto, quantidade in self.itens]
    
class Pagamento:
    def __init__(self, total):
        self.total = total

    def calc_troco(self, valor_pago):
        if valor_pago >= self.total:
            return valor_pago - self.total
        else:
            return None
        
    def realizar_pagamento(self, metodo_pagamento, valor_pago = 0):
        if metodo_pagamento == 'Dinheiro':
            troco = self.calc_troco(valor_pago)
            if troco is not None:
                return f"Pagemento realizado com sucesso! Troco: R${troco:.2f}"
            else:
                return "Valor insuficiente para pagamento"
        else:
            return f"Pagemento realizado com sucesso via {metodo_pagamento}!"
        
class PubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Richter's Pub")

        self.estoque = Estoque()
        self.pedido = Pedido()

        # Produtos Iniciais ao Estoque
        self.estoque.registrar_produto(Produto("Cerveja", 5.00), 50)
        self.estoque.registrar_produto(Produto("Refrigerante", 3.00), 30)
        self.estoque.registrar_produto(Produto("Água", 2.00), 20)
        self.estoque.registrar_produto(Produto("Porção de Batata Frita", 10.00), 15)
        self.estoque.registrar_produto(Produto("Porção de Coxinha de Frango", 15.00), 10)
        self.estoque.registrar_produto(Produto("Picadão: Queijo, Ovo de Codorna, Batata Frita, Pepino, Azeitona, Picanha, Linguiça", 60.00), 60)

        # Interface
        self.create_widgets()

    def create_widgets(self):
        self.frame_produtos = tk.Frame(self.root)
        self.frame_produtos.pack(pady = 10)

        self.label_produtos = tk.Label(self.frame_produtos, text = "Produtos Disponíveis")
        self.label_produtos.pack()

        self.lista_produtos = tk.Listbox(self.frame_produtos, width = 50)
        self.lista_produtos.pack()
        self.atualizar_lista_produtos()

        self.frame_pedido = tk.Frame(self.root)
        self.frame_pedido.pack(pady = 10)

        self.label_pedido = tk.Label(self.frame_pedido, text = "Pedido Atual")
        self.label_pedido.pack()

        self.lista_pedido = tk.Listbox(self.frame_pedido, width = 50)
        self.lista_pedido.pack()

        self.frame_acoes = tk.Frame(self.root)
        self.frame_acoes.pack(pady = 10)

        self.label_quantidade = tk.Label(self.frame_acoes, text = "Quantidade")
        self.label_quantidade.pack()

        self.entry_quantidade = tk.Entry(self.frame_acoes)
        self.entry_quantidade.pack()

        self.button_add = tk.Button(self.frame_acoes, text = "Adicionar ao Pedido", command = self.add_ao_pedido)
        self.button_add.pack()

        self.button_finalizar = tk.Button(self.frame_acoes, text = "Finalizar Pedido", command = self.finalizar_pedido)
        self.button_finalizar.pack()

        self.button_add_produto = tk.Button(self.frame_acoes, text = "Adicionar Produto ao Estoque", command = self.add_produto)
        self.button_add_produto.pack()

    def atualizar_lista_produtos(self):
        self.lista_produtos.delete(0, tk.END)
        for nome, preco, quantidade in self.estoque.listar_produtos():
            self.lista_produtos.insert(tk.END, f"{nome} - Preço: R${preco:.2f} - Qtd: {quantidade}")

    def add_ao_pedido(self):
        try:
            selection = self.lista_produtos.curselection()
            if not selection:
                messagebox.showwarning("Seleção inválida", "Selecione um produto da lista.")
                return
            
            produto_nome = self.lista_produtos.get(selection[0]).split(" - ")[0]
            quantidade = int(self.entry_quantidade.get())
            produto_info = self.estoque.produtos[produto_nome]
            produto = produto_info['produto']

            if not self.estoque.remover_produto(produto_nome, quantidade):
                messagebox.showwarning("Estoque insuficiente", "Quantidade insuficiente em estoque.")
                return
            
            self.pedido.add_item(produto, quantidade)
            self.lista_pedido.insert(tk.END, f"{produto.nome} - Qtd: {quantidade} - Subtotal: R${produto.preco * quantidade:.2f}")
            self.entry_quantidade.delete(0, tk.END)
            self.atualizar_lista_produtos()

        except ValueError:
            messagebox.showwarning("Entrada inválida", "Por favor, insira uma quantidade válida.")
    
    def finalizar_pedido(self):
        total = self.pedido.calc_total()
        metodo_pagamento = tk.simpledialog.askstring("Método de Pagamento", "Digite o método de pagamento (Pix, Cartão de Crédito, Cartão de Débito, Dinheiro):")
        if metodo_pagamento.lower() == 'dinheiro':
            valor_pago = float(tk.simpledialog.askstring("Valor Pago", "Digite o valor pago:"))
            pagamento = Pagamento(total)
            resultado = pagamento.realizar_pagamento("Dinheiro", valor_pago)
        else:
            pagamento = Pagamento(total)
            resultado = pagamento.realizar_pagamento(metodo_pagamento)

        messagebox.showinfo("Resultado do Pagamento", resultado)
        self.pedido = Pedido()
        self.lista_pedido.delete(0, tk.END)

    def add_produto(self):
        nome = simpledialog.askstring("Nome do Produto", "Digite o nome do novo produto:")
        if nome is None:
            return
        try:
            preco = float(simpledialog.askstring("Preço do Produto", "Digite o preço do novo produto:"))
            quantidade = int(simpledialog.askstring("Quantidade do Produto", "Digite a quantidade do novo produto:"))
        except (ValueError, TypeError):
            messagebox.showwarning("Entrada inválida", "Por favor, insira vaores válidos para preço e quantidade.")
            return
        
        novo_produto = Produto(nome, preco)
        self.estoque.registrar_produto(novo_produto, quantidade)
        self.atualizar_lista_produtos()
        messagebox.showinfo("Produto Adicionado", f"Produto {nome} adicionado com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PubApp(root)
    root.mainloop()
