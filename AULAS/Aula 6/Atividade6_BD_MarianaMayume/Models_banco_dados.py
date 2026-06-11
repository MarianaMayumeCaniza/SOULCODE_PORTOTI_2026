import json
import os 

pasta = os.path.dirname(os.path.abspath(__file__))

# ============================================================
#  CARREGAR ESTOQUE
# ============================================================
def carregar_bebidas(nome_arquivo, valor_padrao, pasta_atual=pasta):
    """ 
    Tenta carregar um arquivo JSON. Se o arquivo não existir, retorna um valor padrão.

    """    
    try:
        with open(os.path.join(pasta, 'estoque.json'), 'r', encoding='utf-8') as arquivo_estoque:
            estoque = json.load(arquivo_estoque)
            return estoque
    except FileNotFoundError:
        print("Arquivo estoque.json não encontrado. Usando lista reserva.")
        return valor_padrao
        

# ============================================================
#  CARREGAR VENDAS
# ============================================================

def carregar_vendas(nome_arquivo, dados, pasta_atual=pasta):
    """ 
    Recebe um nome de arquivo e os dados e joga tudo para o HD
    
    """
    try:
        with open(os.path.join(pasta, 'vendas.json'), 'r', encoding='utf-8') as arquivo_vendas:
            return json.load(arquivo_vendas)

    except FileNotFoundError:
        print("Arquivo vendas.json não encontrado. Iniciando histórico vazio.")
        historico_vendas = []
        return historico_vendas

# ============================================================
#  CARREGAR FORNECEDORES
# ============================================================

def carregar_fornecedores(nome_arquivo, valor_padrao, pasta_atual=pasta):
    """ 
    Tenta carregar um arquivo JSON. Se o arquivo não existir, retorna um array vazio... Na verdade aqui vai dar problema....
    """
    try:
        with open(os.path.join(pasta, 'fornecedores.json'), 'r', encoding='utf-8') as arquivo_fornecedores:
            return json.load(arquivo_fornecedores)
    except FileNotFoundError:
        print("Arquivo fornecedores.json não encontrado.")
        fornecedores = []
        return fornecedores


#  FUNÇÃO: SALVAR ARQUIVOS
def salvar_estoque(estoque):
    with open(os.path.join(pasta, 'estoque.json'), 'w', encoding='utf-8') as f:
        json.dump(estoque, f, indent=4, ensure_ascii=False)

def salvar_vendas(historico_vendas):
    with open(os.path.join(pasta, 'vendas.json'), 'w', encoding='utf-8') as f:
        json.dump(historico_vendas, f, indent=4, ensure_ascii=False)

def salvar_fornecedores(fornecedores):
    with open(os.path.join(pasta, 'fornecedores.json'), 'w', encoding='utf-8') as f:
        json.dump(fornecedores, f, indent=4, ensure_ascii=False)