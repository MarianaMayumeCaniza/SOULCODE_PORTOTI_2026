import sqlite3


def repor_estoque():
    try:
        id_produto = int(input("Digite o [ID] do livro para repor o estoque: "))
    except ValueError:
        print("ERRO: O ID deve ser um número.")
        return
    

    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, quantidade FROM livros WHERE id = ?", (id_produto,)) 
        livro = cursor.fetchone()   


        if not livro: 
            print("ERRO: ID INVALIDO")
            return
        
        try: 
            qtd_reposicao = int(input(f" Quantas unidades de '{livro[0]}' você deseja repor?"))

        except ValueError: 
            print("Quantidade deve ser um numero inteiro")
            return
        
        if qtd_reposicao <= 0:
            print("ERRO: QUANTIDADE INVALIDA")
        else: 
            with sqlite3.connect("livraria.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("UPDATE livros SET quantidade = quantidade + ? WHERE id = ?", (qtd_reposicao, id_produto))
                conexao.commit()
            print("ESTOQUE ATUALIZADO COM SUCESSO!!!! :)")

    