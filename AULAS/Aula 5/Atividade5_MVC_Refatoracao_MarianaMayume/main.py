###############################################################
# SOULCODE PORTO TI 2026
# MARIANA MAYUME
# ATIVIDADE 3 - SISTEMA DE GERENCIAMENTO DE CAFETERIA
###############################################################


import datetime
import os
from Models_banco_dados import carregar_bebidas, carregar_vendas, carregar_fornecedores, salvar_estoque, salvar_vendas, salvar_fornecedores
from Views_interface import exibir_cardapio, exibir_menu
from ControllerFunc import calcular_lucro, buscar_custo
from ControllerMenu import registrar_venda, cadastrar_produto, ver_fornecedores, alterar_preco, repor_estoque, pesquisar_produto, aplicar_promocao, exibir_business_intelligence, exibir_nota_fiscal, exibir_estatisticas

pasta = os.path.dirname(os.path.abspath(__file__)) 

estoque = [
            {"nome": "Cafe",                   "marca": "Nescafe",       "temperatura": "Quente", "tipo": "Cafeinado",     "preco_venda": 4.50,  "quantidade": 80},
            {"nome": "Cappuccino",             "marca": "Nescafe",       "temperatura": "Quente", "tipo": "Cafeinado",     "preco_venda": 9.50,  "quantidade": 50},
        ]

estoque = carregar_bebidas("estoque.json", estoque, pasta_atual=pasta)
historico_vendas = carregar_vendas("vendas.json", [], pasta_atual=pasta)
fornecedores = carregar_fornecedores("fornecedores.json", [], pasta_atual=pasta) # Aqui eu vou precisar pensar.... a lista de fornecedores nao pdoe ta vazia....

#INICIALIZAÇÃO DO CAIXA COM O TOTAL DAS VENDAS REGISTRADAS NO HISTÓRICO
caixa = sum(venda['valor'] for venda in historico_vendas)


while True:
    exibir_menu(caixa, estoque)

    comando = int(input("Digite o número da bebida que deseja comprar ou 0 para sair do sistema: "))

    # ----------------------------------------------------------
    #  0 - SAIR
    # ----------------------------------------------------------
    if comando == 0:
        print(f"\nEncerrando o sistema. Total em caixa: R$ {caixa:.2f}")
        break
    
    # ----------------------------------------------------------

    # ----------------------------------------------------------
    #  1 - REGISTRAR VENDA
    # ----------------------------------------------------------
    elif comando == 1:

        caixa = registrar_venda(estoque, historico_vendas, caixa)

    # ----------------------------------------------------------
    #  2 - CADASTRAR PRODUTO
    # ----------------------------------------------------------
    elif comando == 2:
        cadastrar_produto(estoque)

    # ----------------------------------------------------------
    #  3 - VER FORNECEDORES
    # ----------------------------------------------------------
    elif comando == 3:
        ver_fornecedores(fornecedores)
    # ----------------------------------------------------------
    #  4 - ALTERAR PREÇO
    # ----------------------------------------------------------
    elif comando == 4:
        alterar_preco(estoque, fornecedores)

    # ----------------------------------------------------------
    #  5 - REPOR ESTOQUE
    # ----------------------------------------------------------
    elif comando == 5:
        repor_estoque(estoque, fornecedores)

    # ----------------------------------------------------------
    #  6 - PESQUISAR POR NOME/MARCA
    # ----------------------------------------------------------
    elif comando == 6:
        pesquisar_produto(estoque, fornecedores)

    # ----------------------------------------------------------
    #  7 - PROMOÇÕES
    # ----------------------------------------------------------
    elif comando == 7:
        aplicar_promocao(estoque, fornecedores)

    # ----------------------------------------------------------
    #  8 - NOTA FISCAL (VENDAS DA SESSÃO)
    # ----------------------------------------------------------
    elif comando == 8:
        exibir_nota_fiscal(historico_vendas, caixa)

    # ----------------------------------------------------------
    #  9 - PAINEL DE ESTATÍSTICAS E BALANÇO
    # ----------------------------------------------------------
    elif comando == 9:
        exibir_estatisticas(historico_vendas, estoque, fornecedores, caixa)

    
    
    # ----------------------------------------------------------
    #  10 - PAINEL DE BUSSINES INTELIGENCE
    # ----------------------------------------------------------
    elif comando == 10:
        exibir_business_intelligence(historico_vendas)


    else:
        print("Comando inválido. Digite um número do menu.")
        exibir_cardapio(estoque)