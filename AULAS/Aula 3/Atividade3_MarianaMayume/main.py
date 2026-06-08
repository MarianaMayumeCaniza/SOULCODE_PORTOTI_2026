###############################################################
# SOULCODE PORTO TI 2026
# MARIANA MAYUME
# ATIVIDADE 3 - SISTEMA DE GERENCIAMENTO DE CAFETERIA
###############################################################


import datetime
import json
import os 

pasta = os.path.dirname(os.path.abspath(__file__))

# ============================================================
#  CARREGAR ESTOQUE
# ============================================================
try:
    with open(os.path.join(pasta, 'estoque.json'), 'r', encoding='utf-8') as arquivo_estoque:
        estoque = json.load(arquivo_estoque)
except FileNotFoundError:
    print("Arquivo estoque.json não encontrado. Usando lista reserva.")
    estoque = [
        {"nome": "Cafe",             "preco_venda": 4.50,  "quantidade": 80},
        {"nome": "Chocolate Quente", "preco_venda": 8.00,  "quantidade": 60},
        {"nome": "Cappuccino",       "preco_venda": 9.50,  "quantidade": 50},
    ]

# ============================================================
#  CARREGAR VENDAS
# ============================================================
try:
    with open(os.path.join(pasta, 'vendas.json'), 'r', encoding='utf-8') as arquivo_vendas:
        historico_vendas = json.load(arquivo_vendas)
except FileNotFoundError:
    print("Arquivo vendas.json não encontrado. Iniciando histórico vazio.")
    historico_vendas = []

# ============================================================
#  CARREGAR FORNECEDORES
# ============================================================
try:
    with open(os.path.join(pasta, 'fornecedores.json'), 'r', encoding='utf-8') as arquivo_fornecedores:
        fornecedores = json.load(arquivo_fornecedores)
except FileNotFoundError:
    print("Arquivo fornecedores.json não encontrado.")
    fornecedores = []


#INICIALIZAÇÃO DO CAIXA COM O TOTAL DAS VENDAS REGISTRADAS NO HISTÓRICO
caixa = sum(venda['valor'] for venda in historico_vendas)

# ============================================================
#  FUNÇOES DO MENU - GERENCIAMENTO DE CAFETERIA
# ============================================================

#  FUNÇÃO: CALCULAR LUCRO
def calcular_lucro(preco_venda, custo, quantidade_vendida):
    lucro_bruto   = preco_venda * quantidade_vendida
    custo_vendido = custo * quantidade_vendida
    lucro_liquido = lucro_bruto - custo_vendido
    lucro_por_uni = preco_venda - custo
    return lucro_liquido, lucro_por_uni

#  FUNÇÃO: SALVAR ARQUIVOS
def salvar_estoque():
    with open(os.path.join(pasta, 'estoque.json'), 'w', encoding='utf-8') as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)

def salvar_vendas():
    with open(os.path.join(pasta, 'vendas.json'), 'w', encoding='utf-8') as f:
        json.dump(historico_vendas, f, indent=4, ensure_ascii=False)

def salvar_fornecedores():
    with open(os.path.join(pasta, 'fornecedores.json'), 'w', encoding='utf-8') as f:
        json.dump(fornecedores, f, indent=4, ensure_ascii=False)


#  FUNÇÃO: BUSCAR CUSTO DO PRODUTO NO FORNECEDOR
#Já que eu fiz o custo no arquivo de fornecedores, preciso de uma função para buscar o custo do produto para a função de calcular lucro funcionar.
#Minha arquitura de banco de dados ficou assim, intencionalmente

def buscar_custo(nome_produto):
    for fornecedor in fornecedores:
        for item in fornecedor['produtos_fornecidos']:
            if item['nome'] == nome_produto:
                return item['custo']
    return None  # Se não encontrar fornecedor

#  FUNÇÃO: EXIBIR O CARDAPIO
def exibir_cardapio():
    print("\nCARDÁPIO DISPONÍVEL:")
    for id, produto in enumerate(estoque):
        print(f"  [{id}] {produto['nome']:<20} | R$ {produto['preco_venda']:.2f} | Estoque: {produto['quantidade']}")



while True:
    print(f"""
===========================================================
CAFETERIA SOUL 
Caixa Acumulado: R$ {caixa:.2f}
============================================================""")
    
    exibir_cardapio()

    print("""
===========================================================
'1' = Registrar Venda
'2' = Cadastrar Produto
'3' = Ver Fornecedores
'4' = Alterar Preço
'5' = Repor Estoque
'6' = Pesquisar por Nome/Marca
'7' = Promoções
'8' = Nota Fiscal (Vendas da Sessão)
'9' = Painel de Estatísticas e Balanço
'0' = Sair
===========================================================
""")

    comando = int(input("Digite o número da bebida que deseja comprar ou 0 para sair do sistema: "))

    # ----------------------------------------------------------
    #  0 - SAIR
    # ----------------------------------------------------------
    if comando == "0":
        print(f"\nEncerrando o sistema. Total em caixa: R$ {caixa:.2f}")
        break
    
    # ----------------------------------------------------------

    # ----------------------------------------------------------
    #  1 - REGISTRAR VENDA
    # ----------------------------------------------------------
    elif comando == 1:
        print("\n========== REGISTRAR VENDA ==========")
        try:
            id_venda = int(input("Digite o [ID] da bebida: "))
            if id_venda < 0 or id_venda >= len(estoque):
                print("ERRO: ID inválido. Por favor, digite um ID existente no cardápio.")
                exibir_cardapio()
            else:
                produto = estoque[id_venda]
                qtd = int(input(f"Quantas unidades de '{produto['nome']}'? "))
                if qtd <= 0:
                    print("ERRO: quantidade inválida. Digite uma quantidade maior que zero.")
                elif qtd > produto['quantidade']:
                    print(f"ERRO: estoque insuficiente. Restam apenas {produto['quantidade']} unidades.")
                else:
                    produto['quantidade'] -= qtd
                    valor_total = qtd * produto['preco_venda']
                    caixa += valor_total

                    historico_vendas.append({
                        "horario": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "item": produto['nome'],
                        "qtd": qtd,
                        "valor": valor_total
                    })

                    salvar_estoque() #atualiza a quandiade do estoque
                    salvar_vendas() #autaliza o historico de vendas em vendas
                    print(f"Venda registrada: {qtd} x '{produto['nome']}' por R$ {valor_total:.2f}. Obrigado!")
        except ValueError:
            print("ERRO: entrada inválida.")
                # %d/%m/%y = dia/mes/ano
                # %H/%M/%S = hota/minuto/segundo

    # ----------------------------------------------------------
    #  2 - CADASTRAR PRODUTO
    # ----------------------------------------------------------
    elif comando == 2:
        print("\n========== CADASTRAR PRODUTO ==========")
        try:
            novo_nome       = input("Nome do produto: ").strip()
            novo_preco      = float(input(f"Preço de venda de '{novo_nome}': R$ "))
            nova_quantidade = int(input(f"Quantidade inicial em estoque: "))

            novo_produto = {
                "nome": novo_nome,
                "preco_venda": novo_preco,
                "quantidade": nova_quantidade
            }
            estoque.append(novo_produto)
            salvar_estoque()
            print(f"Produto '{novo_nome}' cadastrado com sucesso!")
        except ValueError:
            print("ERRO: entrada inválida.")

    # ----------------------------------------------------------
    #  3 - VER FORNECEDORES
    # ----------------------------------------------------------
    elif comando == 3:
        print("\n========== FORNECEDORES ==========")
        for f in fornecedores:
            print(f"\n[{f['id']}] {f['nome']}")
            print(f"     Contato:  {f['contato']}")
            print(f"     Telefone: {f['telefone']}")
            print(f"     Produtos que fornece:")
            for item in f['produtos_fornecidos']:
                print(f"       - {item['nome']:<20} | Custo: R$ {item['custo']:.2f}")

    # ----------------------------------------------------------
    #  4 - ALTERAR PREÇO
    # ----------------------------------------------------------
    elif comando == 4:
        print("\n========== ALTERAR PREÇO ==========")
        # na vdd aqui nao precisava de try ja que ta convertendo a entrada para int, mas coloquei para evitar que o sistema quebre caso o usuario digite algo errado
        try:
            id_produto = int(input("Digite o [ID] do produto: "))
            if id_produto < 0 or id_produto >= len(estoque):
                print("ERRO: ID inválido.")
            else:
                produto = estoque[id_produto]
                custo   = buscar_custo(produto['nome'])
                novo_preco = float(input(f"Preço atual de '{produto['nome']}': R$ {produto['preco_venda']:.2f}. Novo preço: R$ "))

                if custo and novo_preco < custo:
                    print(f"ATENÇÃO: novo preço (R$ {novo_preco:.2f}) está abaixo do custo do fornecedor (R$ {custo:.2f})!")
                else:
                    produto['preco_venda'] = novo_preco
                    salvar_estoque()
                    print(f"Preço atualizado para R$ {novo_preco:.2f}.")
        except ValueError:
            print("ERRO: entrada inválida.")

    # ----------------------------------------------------------
    #  5 - REPOR ESTOQUE
    # ----------------------------------------------------------
    elif comando == 5:
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
                else:
                    print("Nenhum fornecedor cadastrado para este produto.")

                qtd = int(input(f"\nQuantas unidades deseja adicionar ao estoque de '{produto['nome']}'? "))
                if qtd <= 0:
                    print("ERRO: quantidade inválida.")
                else:
                    produto['quantidade'] += qtd
                    salvar_estoque()
                    print(f"Estoque reposto! '{produto['nome']}' agora tem {produto['quantidade']} unidades.")
        except ValueError:
            print("ERRO: entrada inválida.")

    # ----------------------------------------------------------
    #  6 - PESQUISAR POR NOME/MARCA
    # ----------------------------------------------------------
    elif comando == 6:
        print("\n========== PESQUISAR PRODUTO ==========")
        termo = input("Digite o nome ou parte do nome para pesquisar: ").strip().lower()
        encontrou = False

        for idx, produto in enumerate(estoque):
            if termo in produto['nome'].lower():
                custo = buscar_custo(produto['nome'])
                custo_str = f"R$ {custo:.2f}" if custo else "sem fornecedor"
                print(f"  [{idx}] {produto['nome']:<20} | R$ {produto['preco_venda']:.2f} | Estoque: {produto['quantidade']} | Custo: {custo_str}")
                encontrou = True

        if not encontrou:
            print("Nenhum produto encontrado com esse termo.")

    # ----------------------------------------------------------
    #  7 - PROMOÇÕES
    # ----------------------------------------------------------
    elif comando == 7:
        print("\n========== PROMOÇÕES ==========")
        print("  1 - Desconto em 1 produto específico")
        print("  2 - Desconto em todo o cardápio")

        try:
            tipo_promocao = int(input("\nEscolha o tipo de promoção: "))
            desconto      = float(input("Porcentagem de desconto (%): "))
            fator         = (100 - desconto) / 100

            if tipo_promocao == 1:
                exibir_cardapio()
                id_produto = int(input("Digite o [ID] do produto: "))
                if id_produto < 0 or id_produto >= len(estoque):
                    print("ERRO: ID inválido.")
                else:
                    produto = estoque[id_produto]
                    produto['preco_venda'] = round(produto['preco_venda'] * fator, 2)
                    salvar_estoque()
                    print(f"Desconto aplicado! Novo preço de '{produto['nome']}': R$ {produto['preco_venda']:.2f}")

            elif tipo_promocao == 2:
                for produto in estoque:
                    produto['preco_venda'] = round(produto['preco_venda'] * fator, 2)
                salvar_estoque()
                print(f"Desconto de {desconto}% aplicado em todo o cardápio!")
            else:
                print("ERRO: opção inválida.")
        except ValueError:
            print("ERRO: entrada inválida.")

    # ----------------------------------------------------------
    #  8 - NOTA FISCAL (VENDAS DA SESSÃO)
    # ----------------------------------------------------------
    elif comando == 8:
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

    # ----------------------------------------------------------
    #  9 - PAINEL DE ESTATÍSTICAS E BALANÇO
    # ----------------------------------------------------------
    elif comando == 9:
        print("\n========== PAINEL DE ESTATÍSTICAS E BALANÇO ==========")

        lucro_total    = 0
        produto_mais_vendido = None
        maior_qtd      = 0
        vendas_por_produto = {}

        for venda in historico_vendas:
            nome  = venda['item']
            custo = buscar_custo(nome)

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

    else:
        print("Comando inválido. Digite um número do menu.")
        exibir_cardapio