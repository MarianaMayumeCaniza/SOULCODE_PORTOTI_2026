

def cadastrar_livro(estoque, salvar_arquivo):
    print("\n========== CADASTRAR NOVO LIVRO ==========")
    novo_nome = input("Qual o nome do livro? ").strip()
    novo_autor = input("Quem é o autor do livro? ").strip()
    novo_ano = int(input("Qual o ano de lançamento do livro? ").strip())    
    novo_preco = float(input("Qual o preço de venda do livro? ").strip())    
    nova_quantidade = int(input("Qual a quantidade em estoque? ").strip())

    estoque.append({
        "nome": novo_nome,
        "autor": novo_autor,
        "ano": novo_ano,
        "preco": novo_preco,
        "quantidade": nova_quantidade
    })

    salvar_arquivo("estoque.json", estoque)
    print(f"Livro '{novo_nome}' cadastrado com sucesso!")
