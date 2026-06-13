import sqlite3
from Banco_Dados import inicializar_banco
from interface  import exibir_menu_e_estoque
from comandos.carrinho import realizar_venda
from comandos.financeiro import alterar_preco, aplicar_promocao, nota_fiscal, exibir_painel_bi
from comandos.cadastro import cadastrar_livro
from comandos.estoque import repor_estoque
from comandos.filtros import pesquisa_livro, catalogo_ordenado, relatorio_expresso
# No main eu nao vou ter arquiuvos para salvar, já que quem salva em si sao as funções
# Entao o salvar vai ficar dentro das subfuncoes

inicializar_banco()

while True:

    with sqlite3.connect("livraria.db") as conexao: 
        cursor = conexao.cursor()

        cursor.execute("SELECT SUM(valor_total) FROM vendas")
        resultado_caixa = cursor.fetchone()[0]
        caixa = resultado_caixa if resultado_caixa is not None else 0.0

        cursor.execute("SELECT * FROM livros")
        estoque = cursor.fetchall()


    exibir_menu_e_estoque(caixa, estoque)

    try: 
        comando = int(input("Digite o comando: "))
    except ValueError:
        print("ERRO: COMANDO DEVE SER UM NUMERO INTEIRO: ")
    
    if comando ==  3:
        print(f"Encerrando sistema. Total geral em caixa: R$  {caixa:.2f}")
    
    elif comando == 1:
        caixa = realizar_venda()
    elif comando ==2:
        alterar_preco()
    elif comando == 4:
        cadastrar_livro()
    elif comando ==5:
        repor_estoque()
    elif comando == 6:
        pesquisa_livro(estoque)
    elif comando == 7:
        aplicar_promocao()
    elif comando == 8: 
        nota_fiscal()
    elif comando == 9:
        exibir_painel_bi()
    elif comando == 10:
        catalogo_ordenado(estoque)
    elif comando == 11: 
        relatorio_expresso()

    # --- BLOCO DE PAUSA ---
    print("\n-----------------------------------------")
    print("[1] Fechar sistema")
    print("[2] Voltar ao menu principal")
    try:
        acao_pos_comando = int(input("O que deseja fazer agora? "))
        if acao_pos_comando == 1:
            print(f"Encerrando o sistema. Total geral em caixa: R$ {caixa:.2f}")
            break
    except ValueError:
        pass

    

    





