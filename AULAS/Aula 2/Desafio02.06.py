#Lista Sorveteria Picole?

estoque = [
    {"nome": "Abacaxi" , "preco": 4.00,"quantidade": 100 }, #1
    {"nome": "Coco" , "preco": 4.00,"quantidade": 100 }, #2
    {"nome": "Chocolate" , "preco": 5.0,"quantidade": 200 }, #3
    {"nome": "Baunilha" , "preco": 5.00,"quantidade": 200 }, #4
    {"nome": "Morango" , "preco": 5.00,"quantidade": 200 }, #5
    {"nome": "Napolitano" , "preco": 6.00,"quantidade": 150 }, #6
    {"nome": "BlueBerry" , "preco": 6.00,"quantidade": 200 }, #7
    {"nome": "TuttiFrutti" , "preco": 6.00,"quantidade": 150 }, #8
    {"nome": "Kitkat" , "preco": 8.00,"quantidade": 250 }, #9
    {"nome": "Nutella" , "preco": 8.00,"quantidade": 250 } #10
    

]


caixa = 0.0

while True:


    print(f"""
    ===================================
    BEM VINDO A SORVETERIA!

    
    Caixa atual: R# {caixa}
    --------------------------


    """)


    print("MENU DE PICOLETES")
    print("      Nome         |        Preco         |    Quantidade    ")

    for id_sorvete, sorvete in enumerate(estoque):
        print(f"[{id_sorvete}] {sorvete['nome']} | R$ {sorvete['preco']} | Estoque: {sorvete['quantidade']} ")
    

    print("""
    ===================================
    
    Escolha uma opção do menu abaixo:
    1 - Adicionar Vendas
    2 - Cadastrar um novo Produto
    3 - Alterar o preço de um Produto existente
    4 - Adicionar Produtos ao Estoque
    
    ------------------------------------
    Digite 0 para sair do sistema

    
    """)
    
    opcao = int(input("Escolha uma opçao do menu: "))

    if opcao == 1:
        print("Adicionar a venda de um picole: ")

        id_venda = int(input("Digite o codigo do picole vendido: "))

        #print((estoque[0]['quantidade']))
        if id_venda < 0 or id_venda>=len(estoque):
            print("CODIGO DO PRODUTO INVALIDO! Veja a lista de codigos abaixo:")
            for id_sorvete, sorvete in enumerate(estoque):
                print([{id_sorvete}] , {sorvete['nome']})
        
        else:
            qtd = int(input(f"Quantos sorvetes de {estoque[id_venda]['nome']} foram vendidos ? "))
            if qtd <= 0:
                print("ERRO: Você nao pode vender um numero menor que 0")
            elif qtd > estoque[id_venda]['quantidade']:
                print(f" ESTOQUE INSUFICIENTE: Restam apenas {estoque[id_venda]['quantidade']} sorvetes de {estoque[id_venda]['nome']}")
            else:
                estoque[id_venda]['quantidade'] = estoque[id_venda]['quantidade'] - qtd
                valor_total = qtd * estoque[id_venda]['preco']
                caixa += valor_total

                print(f"Venda registrada com sucesso! Entrou no caixa R$ {valor_total}")
                print(f"Agora seu estoque é de: {estoque[id_venda]['quantidade']}")

                if estoque[id_venda]['quantidade'] == 0:
                    print("Seu estoque acabou! Melhor repor o seu estoque")
        
    #2 - Cadastrar um novo Produto
    elif opcao == 2:
        print("""------------- Cadastrar novo picole ----------------- """)

        novo_nome = input("Qual o nome do novo sabor de picole? ")
        novo_preco = float(input("Qual o preço de venda? R$"))
        nova_qtd = int(input("Qual o valor inicial de estoque do picole? "))

            # Adicionando o novo produto a lista
        novo_picole = {
            "nome": novo_nome,
            "preco": novo_preco,
            "quantidade": nova_qtd
        }

        #Adicionando ao estoque
        estoque.append(novo_picole)
        print(f"Produto {novo_nome} adicionado ao sistema")
            
    #3 - Alterar o preço de um Produto existente
    elif opcao == 3:
        print("""---------------------- Alterar preço do produto ---------------------""")

        id_sorvete = int(input(f" Digite o codigo do sorvete: "))

        if id_sorvete < 0 or id_sorvete >= len(estoque):
                print("ERRO: codigo de sorvete inexistente")
            
        else:
            novo_preco = float (input(f""" Digite o novo preço do sorvete de {estoque[id_sorvete]['nome']}
            o preço atual é R$ {estoque[id_sorvete]['preco']} """))

            if novo_preco < 0:
                print(f" VOCE NAO PODE VENDER POR ESSE VALOR!")
            else:
                estoque[id_sorvete]['preco'] = novo_preco
                print(f"""O preço do sorvete de {estoque[id_sorvete]['nome']} foi alterado para:{estoque[id_sorvete]['preco']}""")


    #4 - Adicionar Produtos ao Estoque
    elif opcao == 4:
        id_sorvete = int(input("Digite codigo do sorvete para repor o estoque: "))

        if id_sorvete  <0 or id_sorvete  >= len(estoque):
            print("ERRO: Codigo de sorvete inexistente")
        else:
            qtd_reposicao = int(input(f"Quantas unidade de {estoque[id_sorvete ]['nome']} deseja repor? "))

            if qtd_reposicao <= 0:
                print("ERRO: QUANTIDADE INVALIDA")
            else:
                estoque[id_sorvete ]['quantidade'] += qtd_reposicao
                print(f" SUCESSO! Agora existem {estoque[id_sorvete]['quantidade']} unidades de {estoque[id_sorvete]['nome']} no estoque.")
    
    elif opcao == 0:
        print("Saindo......")
        break

    else:
        print("Opção invalida, digite uma opcao do menu")









    
    


