import sqlite3

def cadastrar_livro(estoque):
    print("\n========== CADASTRAR NOVO LIVRO ==========")
    novo_nome = input("Qual o nome do livro? ").strip()
    novo_autor = input("Quem é o autor do livro? ").strip()

    try: 
        novo_ano = int(input("Qual o ano de lançamento do livro? ").strip())    
        novo_preco = float(input("Qual o preço de venda do livro? ").strip())    
        nova_quantidade = int(input("Qual a quantidade em estoque? ").strip())
    except ValueError:
        print("EERRO: Ano, preco e quantidade devem ser valores numericos")
        return
    
    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()
    ## chama a conexao com o metodo cursor
        cursor.execute ("""
            INSERT INTO livros (nome, autor, ano, preco, quantidade)
            VALUES (? , ?, ?, ?)
                
        """, (novo_nome, novo_autor, novo_ano, novo_preco, nova_quantidade))

        conexao.commit()
    print(f"Livro '{novo_nome}' cadastrado com sucesso!")
