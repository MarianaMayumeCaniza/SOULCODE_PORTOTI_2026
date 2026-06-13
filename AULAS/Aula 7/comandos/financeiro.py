import sqlite3


def alterar_preco():
    try: 
        id_produto = int(input("Digite o [ID] do livro para alterar o preço: "))
    except ValueError:
        print("ERRO: O ID deve ser um numero")
        return
    
    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, preco FROM livros WHERE id = ?", id_produto)
        livro = cursor.fetchone

        if not livro:
            print("ERRO: ID INVALIDO, LIVRO NAO ENCONTRADO")
            return
        
        try: 
            novo_preco = float(input(f"Digite o novo preço para o livro '{livro[0]}' (preço atual: R$ {livro[1]}) "))
        except ValueError:
            print("ERRO: O preço deve ser numerico")
            return
    
    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()
        cursor.execute("UPDATE livros SET preco = ? WHERE id = ? ", (novo_preco, id_produto))

        conexao.commit()
    
    print("Preco autalizado com sucesso!!!! :)    ")
        
    


def aplicar_promocao ():
    print("\n========== PROMOÇÕES ==========")
    print("  1 - Desconto em 1 produto específico")
    print("  2 - Desconto em todo o cardápio")

    try:
        tipo_promocao = int(input("Digite o número do tipo de promoção desejada: "))
    except ValueError: 
        print("ERRO: O tipo e promoção deve ser um número.")
        return

    if tipo_promocao == 1:
        try: 
            porcentagem = float(input("Qual a porcentagem (%) do desconto: "))
            id_produto = int(input("Digite o [ID] do livvro: "))
        except ValueError:
            print("ERRO: Porcentagem e ID devem ser numeros válidos")
            return
        
        fator_desconto = (100 - porcentagem) / 100

        with sqlite3.connect("livraria.db") as conexao: 
            cursor = conexao.cursor()
            cursor.execute("UPDATE livros SET preco = ROUND (preco * ?, 2) WHERE id = ?", (fator_desconto, id_produto ))
            conexao.commit()
            print("Desconto aplicado com sucesso!!!!")



    elif tipo_promocao == 2:
        try:
            porcentagem = float(input("Digite a pocentagem(%) que deseja aplicar no acervo: "))
        except ValueError:
            print("ERRO: procentagem(%) invalida")
            return

        fator_desconto = (100 - porcentagem) / 100

        with sqlite3.connect("livraria.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("UPDATE livros SET preco = ROUND(preco * ?, 2)", (fator_desconto,))
            conexao.commit()
            print("Desconto aplicado com sucesso!!!! :)")

    else:
        print("Comando invalido")
    


def nota_fiscal ():
    print("\n========== NOTA FISCAL ==========")
    with sqlite3.connect("livrria.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT  id, horario, item_nome, quantidade, valor_total FROM vendas")
        historico = cursor.fetchall()

        if len(historico) == 0:
            print("Não foi realizado nenhuma venda ainda")
        else:
            for venda in historico:
                print(f"[{venda[0]}] Data/Hora: {venda[1]} | {venda[2]} x{venda[3]} | Total venda R$ {venda[4]:.2f}")



def exibir_painel_bi ():
    print("\n========== PAINEL DE BUSSINES INTELIGENCE ==========")

    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT (*) FROM vendas")

        if cursor.fetchone()[0] == 0:
            print("Sem dados de vendas, nenhuma venda realizada ainda")
            return
        
        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        faturamento = cursor.fetchone()[0]
        print(f" Historico e faturamento Bruto: R$ {faturamento:.2f}")

        cursor.execute("SELECT AVG(valor_total) FROM vendas")
        ticket_medio = cursor.fetchone()[0]
        print(f"Ticket Médio por vena: R$ {ticket_medio:.2f} ===============")

        cursor.execute("""
            SELECT item_nome, SUM(quantidade)
            FROM venda
            GROUP BY item_nome
            ORER BY SUM (quantidade) DESC
            LIMIT 1
        """)

        produto_campeao, maior_qtd = cursor.fetchone()
        print(f" -> LIVRO MAIS VENDIDO: {produto_campeao} ({maior_qtd}) exemplares venda")

        
            
