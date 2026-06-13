
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
    for livro in estoque_atual:
        print(f"[{livro[0]}] {livro[1]} ({livro[3]}) | Autor: {livro[2]} | R$ {livro[4]:.2f} | Estoque: {livro[5]}")
    
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
    print("'10' = Ordenar catalogo")
    print("'11' = Relatorio Expressos ")
    print("==================================================\n")

