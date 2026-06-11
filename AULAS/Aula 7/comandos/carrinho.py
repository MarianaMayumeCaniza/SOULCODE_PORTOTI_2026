import datetime   
from banco_dados import salvar_arquivo

def realizar_venda (estoque, historico_vendas, salvar_arquivo):

    print("\n =============== CARRINHO DE COMPRAS ====================")
            
    carrinho = []

    while True:
        try:
            id_venda = int(input("Digite o [ID] do Produto: "))
        except ValueError:
            print("ERRO [ID] Inválido")
            continue

        if id_venda == -1:
            break
        
        elif id_venda == -2:
            print("Compra cancelada")
            carrinho = []
            break

        if id_venda < 0 or id_venda >= len(estoque):
            print("ERRO: ID Invalido")
        
        try:
            qtd = int(input(f"Quantos exemplares do {estoque[id_venda]['nome']} você deseja comprar?"))
        except ValueError:
            print("Erro: digite um numero:")
            continue
        
        qtd_ja_no_carrinho = sum(item['qtd'] for item in carrinho if item['id'] == id_venda)
        estoque_disponivel = estoque[id_venda]['quantidade'] - qtd_ja_no_carrinho

        if qtd <= 0: 
            print("ERRO: Quantidade inválida")
        elif qtd > estoque_disponivel :
            print(f"ESTOQUE INSUFICIENTE. Você tem já tem {qtd_ja_no_carrinho} no carrinho e seu estoque real é {estoque[id_venda]['quantidade']} ")
        else: 
            # adiciona item no carrinho
            carrinho.append({
                "id" : id_venda,
                "nome": estoque[id_venda]['nome'],
                "preco": estoque[id_venda]['preco'],
                "qtd": qtd,
                "subtotal": qtd * estoque[id_venda]['preco']

            })

            print(f" -> {qtd} x '{estoque[id_venda]['nome']}' adicionado ao carrindo.")
    
    if len(carrinho) > 0: 
        total_compra = sum(item['subtotal'] for item in carrinho)
        print("\n ========= FECHAMENTO CAIXA ============")
        print(f" Total a pagar é {total_compra: .2f}")
        confirmar = input("Confimrar pagamento e registrar a venda? (s/n)").strip()
    
        if confirmar == "s":
            for item in carrinho: 
                estoque[item['id']]['quantidade'] -= item['qtd']

                historico_vendas.append(
                    {
                        "horários": datetime.datetime.now().strftime("%d/%m/%y %H/%M/%S"),
                        "item": item['nome'],
                        "qtd" : item['qtd'],
                        "valor": item['subtotal']
                    }
                )
            caixa+= total_compra
            salvar_arquivo("estoque.json", estoque)
            salvar_arquivo("vendas.json", historico_vendas)

            print("VENDA EFETIVADA !!!! :)")

        else: 
            print("Venda nao finalizada. Carrinho descartado")