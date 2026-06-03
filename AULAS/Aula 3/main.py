import datetime
import json

try: 
    with open('estoque.js' , 'r', encoding = 'uft-8') as arquivo_estoque:
        arquivo_estoque = json.load(arquivo_estoque)
    
except FileNotFoundError:
    print("Arquivo estoque.js nao encontrado. executando lista reserva")