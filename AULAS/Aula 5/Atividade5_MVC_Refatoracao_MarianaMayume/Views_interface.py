

#  FUNÇÃO: EXIBIR O CARDAPIO
def exibir_cardapio(estoque):
    print("\nCARDÁPIO DISPONÍVEL:")
    for id, produto in enumerate(estoque):
        print(f"  [{id}] {produto['nome']:<20} | R$ {produto['preco_venda']:.2f} | Estoque: {produto['quantidade']}")



def exibir_menu (caixa, estoque):
        print(f"""
        ===========================================================
        CAFETERIA SOUL 
        Caixa Acumulado: R$ {caixa:.2f}
        ============================================================""")
        
        exibir_cardapio(estoque)

        print("""
        ===========================================================
        '1' = Caixa Registrar Venda
        '2' = Cadastrar Produto
        '3' = Ver Fornecedores
        '4' = Alterar Preço
        '5' = Repor Estoque
        '6' = Pesquisar por Nome/Marca
        '7' = Promoções
        '8' = Nota Fiscal (Vendas da Sessão)
        '9' = Painel de Estatísticas e Balanço
        '10' = PAINEL DE BUSSINES INTELIGENCE
        '0' = Sair
        ===========================================================
        """)