import datetime
from Views_interface import exibir_cardapio, exibir_menu
from Models_banco_dados import carregar_bebidas, carregar_vendas, carregar_fornecedores, salvar_estoque, salvar_vendas, salvar_fornecedores
from ControllerFunc import calcular_lucro, buscar_custo

def registrar_venda(estoque, historico_vendas, caixa):
    """
    Registra uma venda no caixa.
    Retorna o valor atualizado do caixa.
    """
    carrinho_compras = []

    print("\n========== CAIXA REGISTRAR VENDA ==========")

    while True:
        try:
            id_venda = int(input(
                "\nDigite o [ID] da Bebida:\n"
                "[-1] Concluir compra\n"
                "[-2] Cancelar a compra\n"
                "> "
            ))
        except ValueError:
            print("ERRO: ID inválido. Por favor, digite um número.")
            exibir_cardapio(estoque)
            continue

        if id_venda == -1:
            print("Compra finalizada!")
            break

        elif id_venda == -2:
            print("Compra cancelada. Carrinho esvaziado.")
            carrinho_compras = []
            break

        elif id_venda < 0:
            print("ERRO: Comando inválido.")
            continue

        if id_venda >= len(estoque):
            print("ERRO: ID inválido. Por favor, digite um ID existente no cardápio.")
            exibir_cardapio(estoque)
            continue

        try:
            quantidade_bebidas = int(input(
                f"Quantas unidades de '{estoque[id_venda]['nome']}' deseja comprar? "
            ))
        except ValueError:
            print("ERRO: Digite um número válido.")
            continue

        qtd_ja_no_carrinho = sum(item['qtd'] for item in carrinho_compras if item['id'] == id_venda)
        estoque_disponivel = estoque[id_venda]['quantidade'] - qtd_ja_no_carrinho

        if quantidade_bebidas <= 0:
            print("ERRO: Quantidade inválida. Digite um valor maior que zero.")
        elif quantidade_bebidas > estoque_disponivel:
            print(
                f"ESTOQUE INSUFICIENTE. Já há {qtd_ja_no_carrinho} no carrinho "
                f"e o estoque disponível é {estoque_disponivel} unidades."
            )
        else:
            carrinho_compras.append({
                "id":       id_venda,
                "nome":     estoque[id_venda]['nome'],
                "preco":    estoque[id_venda]['preco_venda'],
                "qtd":      quantidade_bebidas,
                "subtotal": quantidade_bebidas * estoque[id_venda]['preco_venda']
            })
            print(f" -> {quantidade_bebidas} x '{estoque[id_venda]['nome']}' adicionado ao carrinho.")

    # ── Fechamento ──────────────────────────────────────────────
    if not carrinho_compras:
        print("Nenhum item no carrinho. Venda não realizada.")
        return caixa  # retorna caixa sem alteração

    total_compra = sum(item['subtotal'] for item in carrinho_compras)

    print("\n========== FECHAMENTO DO CAIXA ==========")
    for item in carrinho_compras:
        print(f"  {item['qtd']} x {item['nome']:<20} R$ {item['subtotal']:.2f}")
    print(f"  {'TOTAL':<24} R$ {total_compra:.2f}")

    confirmar = input("\nConfirmar pagamento e registrar a venda? (s/n) ").strip().lower()

    if confirmar == "s":
        for item in carrinho_compras:
            estoque[item['id']]['quantidade'] -= item['qtd']
            historico_vendas.append({
                "horario": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "item":    item['nome'],
                "qtd":     item['qtd'],
                "valor":   item['subtotal']
            })

        caixa += total_compra
        salvar_estoque(estoque)
        salvar_vendas(historico_vendas)
        print(f"\nVENDA EFETUADA! Total recebido: R$ {total_compra:.2f}. Obrigado! :)")
    else:
        print("Venda não finalizada. Carrinho descartado.")

    return caixa  # sempre retorna o caixa (atualizado ou não)


def cadastrar_produto(estoque):
    """Cadastra um novo produto no estoque."""
    print("\n========== CADASTRAR PRODUTO ==========")
    try:
        novo_nome        = input("Nome do produto: ").strip()
        novo_preco       = float(input(f"Preço de venda de '{novo_nome}': R$ "))
        nova_quantidade  = int(input("Quantidade inicial em estoque: "))
        nova_marca       = input("Marca do produto: ").strip()
        nova_temperatura = input("Temperatura (Quente/Frio): ").strip()
        nova_tipo        = input("Tipo (Cafeinado/Descafeinado): ").strip()

        novo_produto = {
            "nome":        novo_nome,
            "preco_venda": novo_preco,
            "quantidade":  nova_quantidade,
            "marca":       nova_marca,
            "temperatura": nova_temperatura,
            "tipo":        nova_tipo
        }

        estoque.append(novo_produto)
        salvar_estoque(estoque)
        print(f"Produto '{novo_nome}' cadastrado com sucesso!")

    except ValueError:
        print("ERRO: entrada inválida. Produto não cadastrado.")


def ver_fornecedores(fornecedores):
    """Exibe a lista de fornecedores e seus produtos."""
    print("\n========== FORNECEDORES ==========")
    for f in fornecedores:
        print(f"\n[{f['id']}] {f['nome']}")
        print(f"     Contato:  {f['contato']}")
        print(f"     Telefone: {f['telefone']}")
        print(f"     Produtos que fornece:")
        for item in f['produtos_fornecidos']:
            print(f"       - {item['nome']:<20} | Custo: R$ {item['custo']:.2f}")

def alterar_preco(estoque, fornecedores):
    """Altera o preço de venda de um produto do estoque."""
    print("\n========== ALTERAR PREÇO ==========")
    try:
        id_produto = int(input("Digite o [ID] do produto: "))

        if id_produto < 0 or id_produto >= len(estoque):
            print("ERRO: ID inválido.")
            return

        produto    = estoque[id_produto]
        custo      = buscar_custo(produto['nome'], fornecedores)
        preco_atual = produto['preco_venda']

        novo_preco = float(input(
            f"Preço atual de '{produto['nome']}': R$ {preco_atual:.2f}\n"
            f"Novo preço: R$ "
        ))

        # validação extra: mesmo preço
        if novo_preco == preco_atual:
            print("ATENÇÃO: o novo preço é igual ao atual. Nenhuma alteração feita.")
            return

        if novo_preco <= 0:
            print("ERRO: o preço deve ser maior que zero.")
            return

        if custo and novo_preco < custo:
            print(f"ATENÇÃO: novo preço (R$ {novo_preco:.2f}) está abaixo do custo do fornecedor (R$ {custo:.2f})!")
            return

        produto['preco_venda'] = novo_preco
        salvar_estoque(estoque)
        print(f"Preço de '{produto['nome']}' atualizado: R$ {preco_atual:.2f} → R$ {novo_preco:.2f}")

    except ValueError:
        print("ERRO: entrada inválida.")


def repor_estoque(estoque, fornecedores):
    print("\n========== REPOR ESTOQUE ==========")
    try:
        id_produto = int(input("Digite o [ID] do produto: "))
        if id_produto < 0 or id_produto >= len(estoque):
            print("ERRO: ID inválido.")
        else:
            produto = estoque[id_produto]

            fornecedor_encontrado = None
            for f in fornecedores:
                for item in f['produtos_fornecidos']:
                    if item['nome'] == produto['nome']:
                        fornecedor_encontrado = f
                        break

            if fornecedor_encontrado:
                print(f"\nFornecedor: {fornecedor_encontrado['nome']}")
                print(f"Contato:    {fornecedor_encontrado['contato']}")
                print(f"Telefone:   {fornecedor_encontrado['telefone']}")
                #aqui coloca o custo tambéM! 
            else:
                print("Nenhum fornecedor cadastrado para este produto.")# arrumar essa parte heinnnn

            qtd = int(input(f"\nQuantas unidades deseja adicionar ao estoque de '{produto['nome']}'? "))
            if qtd <= 0:
                print("ERRO: quantidade inválida.")
            else:
                produto['quantidade'] += qtd
                salvar_estoque(estoque)
                print(f"Estoque reposto! '{produto['nome']}' agora tem {produto['quantidade']} unidades.")
    except ValueError:
        print("ERRO: entrada inválida.")

def pesquisar_produto(estoque, fornecedores):
    print("\n========== PESQUISAR PRODUTO ==========")
    print("  1 - Por Nome")
    print("  2 - Por Marca")
    print("  3 - Por Temperatura  (Quente / Frio / Gelado)")
    print("  4 - Por Tipo         (Cafeinado / Achocolatado / Lacteo / Sem Cafeina)")
    #Depois colocar aqui na view
    termo = input("Digite o nome ou parte do nome para pesquisar: ").strip().lower()
    encontrou = False

    for idx, produto in enumerate(estoque):
        if (termo in produto['nome'].lower() or termo in produto['marca'].lower() or termo in produto['temperatura'].lower() or termo in produto['tipo'].lower()):
            custo = buscar_custo(produto['nome'], fornecedores)
            custo_str = f"R$ {custo:.2f}" if custo else "sem fornecedor"
            print(f"  [{idx}] {produto['nome']:<20} | R$ {produto['preco_venda']:.2f} | Estoque: {produto['quantidade']} | Custo: {custo_str}")
            encontrou = True

    if not encontrou:
        print("Nenhum produto encontrado com esse termo.")

def aplicar_promocao(estoque, fornecedores):
    print("\n========== PROMOÇÕES ==========")
    print("  1 - Desconto em 1 produto específico")
    print("  2 - Desconto em todo o cardápio")

    try:
        tipo_promocao = int(input("\nEscolha o tipo de promoção: "))
        desconto      = float(input("Porcentagem de desconto (%): "))
        fator         = (100 - desconto) / 100

        if tipo_promocao == 1:
            exibir_cardapio(estoque)
            id_produto = int(input("Digite o [ID] do produto: "))
            if id_produto < 0 or id_produto >= len(estoque):
                print("ERRO: ID inválido.")
            else:
                produto = estoque[id_produto]
                produto['preco_venda'] = round(produto['preco_venda'] * fator, 2)
                salvar_estoque(estoque)
                print(f"Desconto aplicado! Novo preço de '{produto['nome']}': R$ {produto['preco_venda']:.2f}")

        elif tipo_promocao == 2:
            for produto in estoque:
                produto['preco_venda'] = round(produto['preco_venda'] * fator, 2)
            salvar_estoque(estoque)
            print(f"Desconto de {desconto}% aplicado em todo o cardápio!")
        else:
            print("ERRO: opção inválida.")
    except ValueError:
        print("ERRO: entrada inválida.")


def exibir_nota_fiscal(historico_vendas, caixa):
    print("\n========== NOTA FISCAL ==========")
    if not historico_vendas:
        print("Nenhuma venda registrada ainda.")
    else:
        print(f"{'#':<4} {'Horário':<22} {'Produto':<22} {'Qtd':>4} {'Valor':>10}")
        print("-" * 65)
        for i, venda in enumerate(historico_vendas):
            print(f"[{i}]  {venda['horario']:<22} {venda['item']:<22} {venda['qtd']:>4}x  R$ {venda['valor']:>7.2f}")
        print("-" * 65)
        print(f"{'TOTAL EM CAIXA':>52} R$ {caixa:>7.2f}")

def exibir_estatisticas(historico_vendas, estoque, fornecedores, caixa):
    print("\n========== PAINEL DE ESTATÍSTICAS E BALANÇO ==========")

    lucro_total    = 0
    produto_mais_vendido = None
    maior_qtd      = 0
    vendas_por_produto = {}

    for venda in historico_vendas:
        nome  = venda['item']
        custo = buscar_custo(nome, fornecedores)

        if nome not in vendas_por_produto:
            vendas_por_produto[nome] = {"qtd": 0, "receita": 0.0, "lucro": 0.0}

        vendas_por_produto[nome]["qtd"]     += venda['qtd']
        vendas_por_produto[nome]["receita"] += venda['valor']

        if custo:
            preco = next((p['preco_venda'] for p in estoque if p['nome'] == nome), 0)
            lucro_venda, _ = calcular_lucro(preco, custo, venda['qtd'])
            vendas_por_produto[nome]["lucro"] += lucro_venda
            lucro_total += lucro_venda

    print(f"\n{'Produto':<22} {'Qtd Vendida':>12} {'Receita':>12} {'Lucro':>12}")
    print("-" * 60)
    for nome, dados in vendas_por_produto.items():
        print(f"{nome:<22} {dados['qtd']:>12} R$ {dados['receita']:>9.2f} R$ {dados['lucro']:>9.2f}")
        if dados['qtd'] > maior_qtd:
            maior_qtd = dados['qtd']
            produto_mais_vendido = nome

    print("-" * 60)
    print(f"\n  Caixa total:           R$ {caixa:.2f}")
    print(f"  Lucro total:           R$ {lucro_total:.2f}")
    if produto_mais_vendido:
        print(f"  Produto mais vendido:  {produto_mais_vendido} ({maior_qtd} unidades)")


def exibir_business_intelligence(historico_vendas):
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

    vendas_por_produto = {}
    for venda in historico_vendas:
        if venda['item'] in vendas_por_produto:
            vendas_por_produto[venda['item']] += venda['qtd']
        else:
            vendas_por_produto[venda['item']] = venda['qtd']

            # Se não existe o item no historico eu crio a chave e já atribuo a quantidade vendida. Nao entendi muito bem a logica 
            # a menos que o comando 9 for chamado varias vezes então ok.... vai armazenar
            #o professor fez ao contrario... mas ok
        #if venda['item'] not in historico_vendas_por_livro:
            #historico_vendas_por_livro[venda['item']] = 0
        #historico_vendas_por_livro[venda['item']] += venda['quantidade']
    
    produto_campeao = ""
    maior_qtd_vendida = 0
    for produto_nome, total_qtd in vendas_por_produto.items():
        if total_qtd > maior_qtd_vendida:
            maior_qtd_vendida = total_qtd
            produto_campeao = produto_nome
    print("Bebida mais vendido: {} ({} unidades)".format(produto_campeao, maior_qtd_vendida))