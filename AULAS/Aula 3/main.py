import datetime
import json
import os 

pasta = os.path.dirname(os.path.abspath(__file__))

try: 
    with open('estoque.js' , 'r') as arquivo_estoque:
        estoque = json.load(arquivo_estoque)
    
except FileNotFoundError:
    print("Usando lista reserva.")
    estoque = [
        {"nome": "O extraordinário", "autor": "R. J. Palacio", "ano": 2012, "preco": 29.90, "quantidade": 15},
        {"nome": "O iluminado", "autor": "Stephen King", "ano": 1977, "preco": 39.90, "quantidade": 15},
    ]

print(estoque)

try: 
    with open('vendas.js' , 'r') as arquivo_vendas:
        Historico_vendas = json.load(arquivo_vendas)
except FileNotFoundError:
    print("Arquivo vendas.js nao encontrado. executando lista reserva")
    Historico_vendas = []

caixa = sum(venda['valor'] for venda in Historico_vendas)

while True:
    print(f"""
===========================================================
                   LIVRARIA SOUL 
          Caixa Acumulado: R$ {caixa:.2f}
============================================================""")
    
    print("ACERVO DISPONÍVEL:")
    for id_livro, livro in enumerate(estoque):
        print(f"[{id_livro}] - {livro['nome']}, | R$ {livro['preco']:.2f} | {livro['autor']} | {livro['ano']} | Estoque: {livro['quantidade']}")

    print("============MENU DE COMANDOS======================")
    print("--------------------------------------------------")
    print("'1' = Registrar Venda de Livro")
    print("'2' = Cadastrar Novo Livro")
    print("'3' = Sair do Sistema")
    print("'4' = Alterar Preço")
    print("'5' = Repor Estoque")
    print("'6' = Pesquisar por Nome/Autor")
    print("'7' = PROMOÇÕES")
    print("'8' = Nota Fiscal (Vendas da Sessão)")
    print("'9' = PAINEL DE ESTATÍSTICAS E BALANÇO")
    print("==================================================\n")

    comando = int(input("Digite o número do livro que deseja comprar ou 0 para sair: "))

    if comando == 0:
        print("Obrigado por visitar a Livraria Soul! Volte sempre!")
        break
        
    if comando == 3:
        print(f"Encerrando o sistema. Total geral em caixa: R$ {caixa:.2f}")
        break

    elif comando == 1:

        id_venda = int(input("Digite o [ID] do livro: "))
        if id_venda < 0 or id_venda >= len(estoque):
            print("ERRO: COMANDO INVALIDO")  
        else:
            qtd = int(input(f"Quantos exemplares de '{estoque[id_venda]['nome']}'?  "))
            if qtd <= 0:
                print("ERRP: QUANTIDADE INVALIDA.")
            elif qtd > estoque [id_venda]['quantidade']:
                print(f"ESTOQUE INSUFICIENTE PRA DEMANDA EXIGIDA. Restam apenas {estoque[id_venda]['quantidade']}")
            else:
                estoque[id_venda]['quantidade'] -= qtd
                valor_total = qtd * estoque[id_venda]['preco']
                caixa += valor_total

                # %d/%m/%y = dia/mes/ano
                # %H/%M/%S = hota/minuto/segundo

                Historico_vendas.append({
                    "horarios": datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S"),
                    "item": estoque[id_venda]['nome'],
                    "qtd": qtd,
                    "valor": valor_total
                })

                # Pega a pasta onde o main.py está
                pasta = os.path.dirname(os.path.abspath(__file__))
                with open(os.path.join(pasta, 'estoque.js'), 'w', encoding='utf-8') as arquivo_estoque_vendas:
                    #Dum de arquivos. As variaveis que estao em diversos arquivos serao convertidas, jogar de uma vez para o arquivo. 
                    # O indent é a formatação do arquivo, o ensure_ascii é para manter os caracteres acentuados
                    #Pega tudo que estao nas variaves e joga para o arquivo, convertendo para o formato json
                    json.dump(estoque, arquivo_estoque_vendas, indent=4, ensure_ascii=False)

                with open(os.path.join(pasta, 'vendas.js'), 'w', encoding='utf-8') as arquivo_estoque_vendas:
                    json.dump(Historico_vendas, arquivo_estoque_vendas, indent=4, ensure_ascii=False)

                print(f"Venda registrada: {qtd}x '{estoque[id_venda]['nome']}' por R$ {valor_total:.2f}. Obrigado pela preferência!")
    elif comando == 2:

        print("\n ===================== CADASTRO DE NOVO LIVRO ====================")

        
        novo_nome = input("Digite o nome do livro: ").strip()
        novo_autor = input("Digite o nome do autor: ").strip()
        novo_ano = int(input("Digite o ano de publicação: "))
        novo_preco = float(input("Digite o preço do livro R$: "))
        nova_quantidade = int(input("Digite a quantidade em estoque: "))
        
        novo_livro = {
            "nome": novo_nome,
            "autor": novo_autor,
            "ano": novo_ano,
            "preco": novo_preco,
            "quantidade": nova_quantidade
        }

        estoque.append(novo_livro)

        with open(os.path.join(pasta, 'estoque.js'), 'w', encoding='utf-8') as arquivo_novo_livro:
            json.dump(estoque, arquivo_novo_livro, indent=4, ensure_ascii=False)
        
        print(f"Livro '{novo_nome}' cadastrado com sucesso!")
    elif comando == 4:

        print("\n ===================== ALTERAÇÃO DE PREÇO ====================")


        id_produto = int(input("Digite o [ID] do livro para alterar o preço: "))
        if id_produto < 0 or id_produto >= len(estoque):
            print("ERRO: COMANDO INVALIDO")
        else:
            novo_preco = float(input(f"Digite o novo preço para '{estoque[id_produto]['nome']}': R$ "))
            estoque[id_produto]['preco'] = novo_preco

            with open(os.path.join(pasta, 'estoque.js'), 'w', encoding='utf-8') as arquivo_estoque_preco:
                json.dump(estoque, arquivo_estoque_preco, indent=4, ensure_ascii=False)
            
            print(f"Preço de '{estoque[id_produto]['nome']}' atualizado para R$ {novo_preco:.2f} com sucesso!")
    
    elif comando == 5:
        print("\n ===================== REPOR ESTOQUE ====================")
        id_produto = int(input("Digite o [ID] do livro para repor o estoque: "))
        if id_produto < 0 or id_produto >= len(estoque):
            print("ERRO: COMANDO INVALIDO")
        else:
            qtd_reposicao = int(input(f"Digite a quantidade a ser adicionada ao estoque de '{estoque[id_produto]['nome']}': "))
            if qtd_reposicao <= 0:
                print("ERRO: QUANTIDADE INVALIDA.")
            else:
                estoque[id_produto]['quantidade'] += qtd_reposicao

                with open(os.path.join(pasta, 'estoque.js'), 'w', encoding='utf-8') as arquivo_estoque_reposicao:
                    json.dump(estoque, arquivo_estoque_reposicao, indent=4, ensure_ascii=False)
                
                print(f"Estoque de '{estoque[id_produto]['nome']}' atualizado. Quantidade atual: {estoque[id_produto]['quantidade']} unidades.")

    elif comando == 6:
        print("\n ===================== PESQUISA DE LIVRO POR NOME OU AUTOR  ====================")
        termo_pesquisa = input("Digite o nome ou autor do livro para pesquisar: ").strip().lower()
        encontrou = False
        
        for livro in estoque:
            if termo_pesquisa in livro['nome'].lower() or termo_pesquisa in livro['autor'].lower():
                print(f"Livro encontrado: '{livro['nome']}' por {livro['autor']} - R$ {livro['preco']:.2f} - Estoque: {livro['quantidade']} unidades.")
                encontrou = True


        if not encontrou:
            print("Nenhum livro encontrado com esse termo de pesquisa.")
    
    elif comando == 7:
        print("\n ===================== PROMOÇÕES ====================")

        print("""
            1 - Desconto em 1 livro específico
            2 - Desconto em todo o acervo
            
            """)

        tipo_promocao = int(input("Digite o número da promoção que deseja aplicar: "))
        porcentagem_desconto = float(input("Digite a porcentagem de desconto: "))

        fator_desconto = (100 - porcentagem_desconto) / 100

        if tipo_promocao == 1:
            id_produto = int(input("Digite o [ID] do livro para aplicar o desconto em %: "))
            if id_produto < 0 or id_produto >= len(estoque):
                print("ERRO: NAO EXISTE O ID DO LIVRO PARA APLICAÇÃO DE DESCONTO.")
            else:
                estoque[id_produto]['preco'] = round(livro['preco'] * fator_desconto, 2)
        
        elif tipo_promocao == 2:
            for livro in estoque:
                livro['preco'] = round(livro['preco'] * fator_desconto, 2)

        with open(os.path.join(pasta, 'estoque.js'), 'w', encoding='utf-8') as arquivo_estoque_desconto:
            json.dump(estoque, arquivo_estoque_desconto, indent=4, ensure_ascii=False)
        
        print(f"Desconto aplicado em '{estoque[id_produto]['nome']}'. Novo preço: R$ {estoque[id_produto]['preco']:.2f}")
    
    elif comando == 8:
        print("\n ===================== NOTA FISCAL (VENDAS DA SESSÃO) ====================")
        if not Historico_vendas:
            print("Nenhuma venda registrada nesta sessão.")
        else:
            print("NOTA FISCAL - VENDAS DA SESSÃO")
            print("=================================")
            for i, venda in enumerate(Historico_vendas):
                print(f"[{i}] Horário: {venda['horarios']} - {venda['qtd']}x '{venda['item']}' - R$ {venda['valor']:.2f} ")
            print("=================================")
            print(f"Total em caixa nesta sessão: R$ {caixa:.2f}")
            
#poderia ter desconto progessivo por compra de muitas unidades
        

