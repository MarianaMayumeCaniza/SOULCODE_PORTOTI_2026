import datetime
from banco_dados import carregar_arquivo, salvar_arquivo
from interface import exibir_menu_e_estoque


    
#Anotações para o futuro: O estoque pode existir e estar vazio
#Criar uma validação para avisar o usuário que o estoque está vazio e perguntar se quer prosseguir com isso mesmo



estoque_padrão = [
    {"nome": "O Alquimista", "autor": "Paulo Coelho", "ano": 1988, "preco": 45.00, "quantidade": 15},
    {"nome": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "preco": 35.00, "quantidade": 20},
]

estoque = carregar_arquivo("estoque.json", estoque_padrão)
historico_vendas = carregar_arquivo("historico_vendas.json", [])

caixa = sum(venda['preco'] for venda in historico_vendas)

while True:
    exibir_menu_e_estoque(caixa, estoque)

    comando = int(input("Digite o número do comando desejado: "))

    if comando == 3: 
        print("Encerrando o sistema. Total geral em caixa: R$ {:.2f}".format(caixa))
        break

    elif comando == 1:
        id_venda = int(input("Digite o ID do livro vendido: ").strip())
        if 0 <= id_venda < len(estoque):
            print(("ERRO: ID INVALIDO"))
        else:
            qtd = int(input(f"Quantos exemplares de {estoque[id_venda]['nome']} foram vendidos? ").strip())
            if qtd <=0:
                print("ERRO: Quantidade deve ser maior que zero.")
            elif qtd > estoque[id_venda]['quantidade']:
                print(f"ERRO: Estoque insuficiente. Apenas {estoque[id_venda]['quantidade']} disponíveis.")
            else:
                estoque[id_venda]['quantidade'] -= qtd
                valor_total = qtd * estoque[id_venda]['preco'] 

                caixa += valor_total

                # %d%,%m/%Y 
                # %H:%M:%S

                historico_vendas.append({
                    "item": estoque[id_venda]['nome'],
                    "autor": estoque[id_venda]['autor'],
                    "valor": valor_total,
                    "quantidade": qtd,
                    "horarios": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })

    elif comando == 2:
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

    
    elif comando == 4:
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
        
    elif comando == 5:
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

    
    elif comando == 6:
        print("\n========== PESQUISAR POR NOME/AUTOR ==========")

        termo_pesquisa = input("Digite o nome ou autor para pesquisar: ").strip().lower()
        resultado = False

        for livro in estoque:
            if termo_pesquisa in livro['nome'].lower() or termo_pesquisa in livro['autor'].lower() or termo_pesquisa in str(livro['ano']):
                print(f" - {livro['nome']} ({livro['ano']}) | Autor: {livro['autor']} - R$ {livro['preco']:.2f} | Estoque: {livro['quantidade']}")
                resultado = True
        if not resultado:
            print("Nenhum livro encontrado com esse termo de pesquisa.")

    elif comando == 7:
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
        
    elif comando == 8:
        print("\n========== NOTA FISCAL ==========")
        if not historico_vendas:
            print("Nenhuma venda registrada ainda.")
        else:
            for i, venda in enumerate(historico_vendas):
                print(f"[{i}] Data/Hora: {venda['horarios']} - {venda['quantidade']} x {venda['item']} | Total venda:  R$ {venda['valor']:.2f} ")
    
    elif comando == 9:
        print("\n========== PAINEL DE BUSSINES INTELIGENCE ==========")
        
        if len(historico_vendas) == 0:
            print("Nenhuma venda registrada ainda.")
            continue

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
        





            

        