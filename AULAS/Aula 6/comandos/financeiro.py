from banco_dados  import salvar_arquivo

def alterar_preco (estoque, salvar_arquivo):
    id_produto = int(input("Digite o [ID] do livro para alterar o preço: "))
    if id_produto < 0 or id_produto >= len(estoque):
        print("ERRO: ID inválido.")
    else:
        novo_preco = float(input(f"Digite o novo preço para '{estoque[id_produto]['nome']}': "))
        if novo_preco <= 0:
            print("ERRO: O preço deve ser maior que zero.")
        else:
            estoque[id_produto]['preco'] = novo_preco
            salvar_arquivo("estoque.json", estoque)
            print(f"Preço de '{estoque[id_produto]['nome']}' atualizado para R$ {novo_preco:.2f} com sucesso!")


def aplicar_promocao (estoque):
    print("\n========== PROMOÇÕES ==========")
    print("  1 - Desconto em 1 produto específico")
    print("  2 - Desconto em todo o cardápio")

    tipo_promocao = int(input("Digite o número do tipo de promoção desejada: "))

    porcentagem_desconto = float(input("Digite a porcentagem de desconto (ex: 10 para 10%): "))

    fator_desconto = 1 - (porcentagem_desconto / 100)

    if tipo_promocao == 1:
        id_produto = int(input("Digite o [ID] do livro para aplicar o desconto: "))
        if id_produto < 0 or id_produto >= len(estoque):
            print("ERRO: ID inválido.")
        else:
            estoque[id_produto]['preco'] = round(estoque[id_produto]['preco'] * fator_desconto, 2)
            salvar_arquivo("estoque.json", estoque)
            print(f"Desconto aplicado! Novo preço de '{estoque[id_produto]['nome']}': R$ {estoque[id_produto]['preco']:.2f}")

    elif tipo_promocao == 2:
        for livro in estoque:
            livro['preco'] = round(livro['preco'] * fator_desconto, 2)
        salvar_arquivo("estoque.json", estoque)
        print(f"Desconto de {porcentagem_desconto:.2f}% aplicado a todos os livros! Confira os novos preços no menu principal.")
    
    else:
        print("ERRO: Tipo de promoção inválido.")


def nota_fiscal (historico_vendas):
    print("\n========== NOTA FISCAL ==========")
    if not historico_vendas:
        print("Nenhuma venda registrada ainda.")
    else:
        for i, venda in enumerate(historico_vendas):
            print(f"[{i}] Data/Hora: {venda['horarios']} - {venda['quantidade']} x {venda['item']} | Total venda:  R$ {venda['valor']:.2f} ")


def exibir_painel_bi (historico_vendas):
    print("\n========== PAINEL DE BUSSINES INTELIGENCE ==========")
        
    if len(historico_vendas) == 0:
        print("Nenhuma venda registrada ainda.")
        return

    faturamento_total = sum(venda['valor'] for venda in historico_vendas)
    print("Faturamento total: R$ {:.2f}".format(faturamento_total))

    ticket_medio = faturamento_total / len(historico_vendas)
    print("Ticket médio: R$ {:.2f}".format(ticket_medio))

    #livro_mais_vendido = max(set(venda['item'] for venda in historico_vendas), key=lambda item: sum(venda['quantidade'] for venda in historico_vendas if venda['item'] == item))
    #print("Livro mais vendido: {}".format(livro_mais_vendido))
    #O prfesor fez uma funçã para isso

    historico_vendas_por_livro = {}
    for venda in historico_vendas:
        if venda['item'] in historico_vendas_por_livro:
            historico_vendas_por_livro[venda['item']] += venda['quantidade']
            # Se existe o item no historico eu somo a quantidade vendida
        else:
            historico_vendas_por_livro[venda['item']] = venda['quantidade']
            # Se não existe o item no historico eu crio a chave e já atribuo a quantidade vendida. Nao entendi muito bem a logica 
            # a menos que o comando 9 for chamado varias vezes então ok.... vai armazenar
            #o professor fez ao contrario... mas ok
        #if venda['item'] not in historico_vendas_por_livro:
            #historico_vendas_por_livro[venda['item']] = 0
        #historico_vendas_por_livro[venda['item']] += venda['quantidade']

    produto_campeao = ""
    maior_qtd_vendida = 0
    for produto_nome, total_qtd in historico_vendas_por_livro.items():
        if total_qtd > maior_qtd_vendida:
            maior_qtd_vendida = total_qtd
            produto_campeao = produto_nome
    print("Livro mais vendido: {} ({} unidades)".format(produto_campeao, maior_qtd_vendida))