
import datetime
import json
import os 

#Definir a pasta de trabalho para o diretório do script
# Pega o diretório de trabalho atual
pasta = os.getcwd()
print(pasta)

def carregar_arquivo(nome_arquivo, valor_padrao, pasta_atual=pasta):
    """ 
    Tenta carregar um arquivo JSON. Se o arquivo não existir, retorna um valor padrão.

    """    
    caminho_completo = os.path.join(pasta_atual, nome_arquivo)
    try:
        with open(caminho_completo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return valor_padrao
    

def salvar_arquivo(nome_arquivo, dados):
    """ 
    Recebe um nome de arquivo e os dados e joga tudo para o HD
    
    """
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4)