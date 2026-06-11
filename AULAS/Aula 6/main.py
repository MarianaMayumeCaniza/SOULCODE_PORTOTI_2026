from banco_dados import carregar_arquivo
from interface  import exibir_menu_e_estoque
from comandos.carrinho import realizar_venda
from comandos.financeiro import alterar_preco, aplicar_promocao, nota_fiscal, exibir_painel_bi
from comandos.cadastro import cadastrar_livro
from comandos.estoque import repor_estoque
from comandos.filtros import pesquisa_livro, catalogo_ordenado, relatorio_expresso
# No main eu nao vou ter arquiuvos para salvar, já que quem salva em si sao as funções
# Entao o salvar vai ficar dentro das subfuncoes

estoque_padrão = [
    {"nome": "O Alquimista", "autor": "Paulo Coelho", "ano": 1988, "preco": 45.00, "quantidade": 15},
    {"nome": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "preco": 35.00, "quantidade": 20},
]

estoque = carregar_arquivo("estoque.json", estoque_padrão)
historico_vendas = carregar_arquivo("historico_vendas.json", [])

caixa = sum(venda['preco'] for venda in historico_vendas)

while True:
    exibir_menu_e_estoque(caixa, estoque)

    try: 
        comando = int(input("Digite o comando: "))
    except ValueError:
        print("ERRO: COMANDO DEVE SER UM NUMERO INTEIRO: ")
    
    if comando ==  3:
        print(f"Encerrando sistema. Total geral em caixa: R$  {caixa:.2f}")
    
    elif comando == 1:
        caixa = realizar_venda(caixa, estoque, historico_vendas)
    elif comando ==2:
        alterar_preco(estoque)
    elif comando == 4:
        cadastrar_livro(estoque)
    elif comando ==5:
        repor_estoque(estoque)
    elif comando == 6:
        pesquisa_livro(estoque)
    elif comando == 7:
        aplicar_promocao(estoque)
    elif comando == 8: 
        nota_fiscal(estoque)
    elif comando == 9:
        exibir_painel_bi(estoque)
    elif comando == 10:
        catalogo_ordenado(estoque)
    elif comando == 11: 
        relatorio_expresso(estoque)


    

    





