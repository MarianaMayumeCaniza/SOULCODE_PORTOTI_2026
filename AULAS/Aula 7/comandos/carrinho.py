import datetime
import sqlite3

def realizar_venda():
    print("\n ============== CARRINHO DE COMPRAS =============")
    carrinho = []

    while True: 
        try: 
            id_venda = int(input ("digite o [ID] do produto: (-1 para concluir compra )"))
        except ValueError:
            print("ERRO: ID DEVE SER UM NUMERO INTEIRO")
            continue
        
        if id_venda == -1:
            break
        elif id_venda == -2:
            print("COMPRA CANCELADA")
            carinho = []
            return
        
    
        with sqlite3.connect("livraria.db") as conexao:
            cursor = conexao.cursor()
        
        cursor.execute("SELECT nome, preco, quantidade FROM livro WHERE id = ?", (id_venda,))

        livro_encontrado = cursor.fetchone()

        if not livro_encontrado: 
            print("ERRO: ID INVALIDO. Esse livro não existe no sistema")
            continue
        
        nome_livro, preco_livro, estoque_real = livro_encontrado

        try: 
            qtd = int(input(f"Quantos exemplares do '{nome_livro}' você deseja adicionar? disponível no estoque {estoque_real}"))
        except ValueError:
            print("ERRO: quantidade invalida")
            continue

        qtd_ja_no_carrinho = sum(item['qtd'] for item in carrinho if item['id'] == id_venda)
        estoque_disponiel = estoque_real - qtd_ja_no_carrinho

        if qtd<=0: 
            print("ERRO: QUANTIDADE INVALIDA")
        elif qtd > estoque_disponiel:
            print(f" ESTOQUE INSUFICIENTE. Você já tem {qtd_ja_no_carrinho} no carrinho")
        else: 
            carrinho.append(
                {
                    "id": id_venda,
                    "nome": nome_livro,
                    "preco": preco_livro,
                    "qtd": qtd,
                    "subtotal" : qtd * preco_livro
                }
            ) 
            print(f" -> {qtd} x '{nome_livro}' adicionado ao carrinho. ")

    if len(carrinho) > 0:
        total_compra = sum(item['subtotal'] for item in carrinho)
        print(f"\n ========== FECHAMENTO DE CAIXA =============")
        print(f" Total a pagar: R$ {total_compra:.2f}")
        confirmar = input("Confirmar pagamento e registrar a venda? (s/n): ").strip()

        if confirmar == "s":
            with sqlite3.connect("livraria.db") as conexao: 
                cursor = conexao.cursor()

                for item in carrinho: 
                    cursor.execute("""
                        UPDATE livros
                        SET quantidade = quantidade - ?
                        WHERE id = ? 
                        """, (item['qtd'], item['id']))
                
                    cursor.execute("""
                        INSERT INTO vendas (horario, item_nome, quantidade, valor_total)
                        VALUE (?, ?, ?, ?)""", (
                            datetime.datetime.now().strftime("%d/%m/%y H:%M:S"),
                            item['nome'],
                            item['qtd'],
                            item['subtotal']
                        ))

                conexao.commit()
            # conexao leva tudo que foi executado para o banco
            print("VENDA CONCLUIDA COM SUCESSO!!!!    :)   ")
        else:
            print("VENDA N FINALIZADA") 




        
        