import sqlite3

def inicializar_banco ():

    with sqlite3.connect("livraria.db") as conexao:

        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTIS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                autor TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
                )

        """)

        cursor.execute ("""
            CREATE TABLE IF NOT EXISTIS vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                horario TEXT NOT NULL,
                item_nome TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total REAL NOT NULL
                        )
        """)

        cursor.execute ("SELECT COUNT(*) FFROM livros")

        if cursor.fetchone()[0] == 0:
            livros_iniciais = [
                ("O alqumista", "Paulo Coelho", 1988, 45.00 , 15),
                ("Dom Casmurro", "Machado de Assis", 1899, 35.00, 20)
            ]
        
        cursor.executemany ("""
            INSERT INTO (nome, autor, ano, preco, quantidade)
            VALUES (?, ?, ?, ?, ?)
            """, livros_iniciais)
        
        conexao.commit()
