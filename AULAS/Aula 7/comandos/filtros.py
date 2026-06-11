
def pesquisa_livro (estoque):
    print("\n========== PESQUISAR POR NOME/AUTOR ==========")

    termo_pesquisa = input("Digite o nome ou autor para pesquisar: ").strip().lower()
    resultado = False

    for livro in estoque:
        if termo_pesquisa in livro['nome'].lower() or termo_pesquisa in livro['autor'].lower() or termo_pesquisa in str(livro['ano']):
            print(f" - {livro['nome']} ({livro['ano']}) | Autor: {livro['autor']} - R$ {livro['preco']:.2f} | Estoque: {livro['quantidade']}")
            resultado = True
    if not resultado:
        print("Nenhum livro encontrado com esse termo de pesquisa.")


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
        print(f"- {livro['nome']} | R$ {livro['preco']:.2f}")
    

def relatorio_expresso(estoque):
    print("\n RELATORIOS EXPRESSOS")
    print("Livros em alerta de estoque (menos que 5)")

    estoque_baixo = [livro['nome'] for livro in estoque if livro['quantidade'] < 5]

    if len(estoque_baixo) == 0:
        print("Nenhum livro com estoque baixo")
    else:
        print(", ".join(estoque_baixo))
    
    print("\n Livros populares abaixo de R$ 40,00:")
    livros_baratos = [livro['nome'] for livro in estoque if livro['preco']<=40]

    print(", " .join(livros_baratos))