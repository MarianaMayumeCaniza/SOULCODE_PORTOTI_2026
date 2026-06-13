import sqlite3 

def pesquisa_livro (estoque):
    print("\n========== PESQUISAR POR NOME/AUTOR ==========")

    termo_pesquisa = input("Digite o nome ou autor para pesquisar: ").strip().lower()
    resultado = False

    for livro in estoque:
        if termo_pesquisa in (livro[1]).lower() or termo_pesquisa in livro[2].lower() or termo_pesquisa in str(livro[3]):
            print(f"[{livro[0]}] {livro[1]} ({livro[3]}) | Autor: {livro[2]} | R$ {livro[4]:.2f} | Estoque: {livro[5]}")
            encontrou = True
    if not resultado:
        print("Nenhum resultado encontrado pra sua pesquisa :(")


def catalogo_ordenado (estoque):
    print("\n ============= CATALOGO ORDENADO ================= ")
    print("1. Ordem alfabética")
    print("2. Mais baratos primeiro")
    print("3. Mais caros primeiro")

    ordem = input("Escolha a ordenação: ")

    if ordem == "1":
        estoque_ordenado = sorted(estoque, key=lambda livro: livro['nome'].lower())
    if ordem == "2":
        estoque_ordenado = sorted(estoque, key= lambda livro: livro['preco'])
    if ordem == "3":
        estoque_ordenado = sorted(estoque, key = lambda livro:livro['preco'], reverse= True)
    else:
        print("opção inválida")
        return

    for livro in estoque_ordenado:
        print(f"- {livro[1]:<20} | R$ {livro[4]:.2f} | Qtd: {livro[5]}")
    

def relatorio_expresso():
    print("\n RELATORIOS EXPRESSOS")
    print("Livros em alerta de estoque (menos que 5)")

    with sqlite3.connect("livraria.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT nome FROM livros WHERE quantidade < 5")  
        estoque_baixo = [linha[0] for linha in cursor.fetchall()]
        

        if len(estoque_baixo) == 0:
            print("Nenhum livro com estoque baixo")
        else:
            print(", ".join(estoque_baixo))
        
        print("Livros populares abaixo de R$ 40,00: ")
        cursor.execute("SELECT nome FROM livros WHERE preco <= 40.0")
        estoque_baratos = [linha[0] for linha in cursor.fetchall()]

        if len(estoque_baratos) == 0:
            print("Nenhum livro barato")
        else:
            print(", ".join(estoque_baratos))