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




#  FUNÇÃO: BUSCAR CUSTO DO PRODUTO NO FORNECEDOR
#Já que eu fiz o custo no arquivo de fornecedores, preciso de uma função para buscar o custo do produto para a função de calcular lucro funcionar.
#Minha arquitura de banco de dados ficou assim, intencionalmente

def buscar_custo(nome_produto, fornecedores):
    for fornecedor in fornecedores:
        for item in fornecedor['produtos_fornecidos']:
            if item['nome'] == nome_produto:
                return item['custo']
    return None  # Se não encontrar fornecedor

