# data.py
import sqlite3
from pathlib import Path


class OrcamentoData:
    def __init__(self, db_path: str = "orcamento.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()
        self._popular_dados_iniciais()
        self.total = 0.0

    def _criar_tabelas(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS subprodutos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                preco_m2 REAL NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        """)
        self.conn.commit()

    def _popular_dados_iniciais(self):
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM categorias")
        if cur.fetchone()[0] > 0:
            return

        dados = {
            "cozinha": {
                "gabinete": 500.0,
                "armário superior": 480.0,
            },
            "guarda-roupa": {
                "com cabides e gavetas": 420.0,
                "com prateleiras": 400.0,
                "com gavetas e prateleiras": 450.0,
                "com cabide": 410.0,
            },
        }

        for categoria, subprodutos in dados.items():
            self.adicionar_categoria(categoria)
            for nome, preco in subprodutos.items():
                self.adicionar_subproduto(categoria, nome, preco)

    def get_categorias(self):
        cur = self.conn.cursor()
        cur.execute("SELECT nome FROM categorias ORDER BY nome")
        return [row["nome"] for row in cur.fetchall()]

    def get_subprodutos(self, categoria: str):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT s.nome, s.preco_m2 
            FROM subprodutos s
            JOIN categorias c ON c.id = s.categoria_id
            WHERE c.nome = ?
            ORDER BY s.nome
        """, (categoria,))
        return {row["nome"]: row["preco_m2"] for row in cur.fetchall()}

    def adicionar_categoria(self, nome: str):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass

    def adicionar_subproduto(self, categoria: str, nome: str, preco_m2: float):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
        row = cur.fetchone()
        if not row:
            self.adicionar_categoria(categoria)
            cur.execute("SELECT id FROM categorias WHERE nome = ?", (categoria,))
            row = cur.fetchone()
        categoria_id = row["id"]

        cur.execute(
            "INSERT INTO subprodutos (categoria_id, nome, preco_m2) VALUES (?, ?, ?)",
            (categoria_id, nome, preco_m2),
        )
        self.conn.commit()

    def listar_todos_subprodutos(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT s.id, c.nome as categoria, s.nome, s.preco_m2
            FROM subprodutos s
            JOIN categorias c ON c.id = s.categoria_id
            ORDER BY c.nome, s.nome
        """)
        return cur.fetchall()

    def atualizar_subproduto(self, subproduto_id: int, novo_nome: str, novo_preco: float):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE subprodutos 
            SET nome = ?, preco_m2 = ?
            WHERE id = ?
        """, (novo_nome, novo_preco, subproduto_id))
        self.conn.commit()

    def remover_subproduto(self, subproduto_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM subprodutos WHERE id = ?", (subproduto_id,))
        self.conn.commit()

    def calcular_valor(self, categoria: str, subproduto: str, largura: float, altura: float) -> float:
        subprodutos = self.get_subprodutos(categoria)
        if subproduto not in subprodutos:
            return 0.0
        area = largura * altura
        preco_m2 = subprodutos[subproduto]
        valor_item = area * preco_m2
        self.total += valor_item
        return valor_item

    def get_total(self) -> float:
        return self.total

    def close(self):
        self.conn.close()
