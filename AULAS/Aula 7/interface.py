
def exibir_menu_e_estoque (caixa_atual, estoque_atual):
    '''
    Função dedidada a exibir o menu e o estoque tela.

    '''

    print(f"""
===========================================================
                   LIVRARIA SOUL 
          Caixa Acumulado: R$ {caixa_atual:.2f}
============================================================""")
    
    print("ACERVO DISPONÍVEL: ")
    for id_livro, livro in enumerate(estoque_atual):
        print(f" [{id_livro}] - {livro['nome']} ({livro['ano']}) | Autor: {livro['autor']} - R$ {livro['preco']:.2f} | Estoque: {livro['quantidade']}")
    
    print("============MENU DE COMANDOS======================")
    print("--------------------------------------------------")
    print("'1' = Carrinho de Compras")
    print("'2' = Cadastrar Novo Livro")
    print("'3' = Sair do Sistema")
    print("'4' = Alterar Preço")
    print("'5' = Repor Estoque")
    print("'6' = Pesquisar por Nome/Autor")
    print("'7' = PROMOÇÕES")
    print("'8' = Nota Fiscal (Vendas da Sessão)")
    print("'9' = PAINEL DE ESTATÍSTICAS E BALANÇO")
    print("==================================================\n")

