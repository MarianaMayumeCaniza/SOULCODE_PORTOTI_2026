def repor_estoque(estoque, salvar_arquivo):

    id_produto = int(input("Digite o [ID] do livro para repor o estoque: "))
    if id_produto < 0 or id_produto >= len(estoque):
        print("ERRO: ID inválido.")
    else:
        quantidade_repor = int(input(f"Digite a quantidade a ser adicionada ao estoque de '{estoque[id_produto]['nome']}': "))
        if quantidade_repor <= 0:
            print("ERRO: A quantidade a repor deve ser maior que zero.")
        else:
            estoque[id_produto]['quantidade'] += quantidade_repor
            salvar_arquivo("estoque.json", estoque)
            print(f"Estoque de '{estoque[id_produto]['nome']}' atualizado. Quantidade atual: {estoque[id_produto]['quantidade']} unidades.")