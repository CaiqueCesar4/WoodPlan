import sqlite3
from pathlib import Path


class OrcamentoData:
    def __init__(self, db_path: str = "orcamento.db"):
        self.db_path = Path(db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        cur = self.conn.cursor()

        # Orçamentos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_orcamento TEXT NOT NULL,
                data_criacao DATE DEFAULT CURRENT_DATE,
                descricao TEXT
            )
        """)

        # Módulos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_MODULOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_modulo TEXT NOT NULL,
                valor_base REAL NOT NULL
            )
        """)

        # Mão de obra
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_MAO_DE_OBRA (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_trabalhador TEXT NOT NULL,
                custo_dia REAL NOT NULL
            )
        """)

        # Orçamento ↔ Módulos
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTO_MODULO (
                orcamento_id INTEGER NOT NULL,
                modulo_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                valor_total_modulo REAL NOT NULL,
                PRIMARY KEY (orcamento_id, modulo_id),
                FOREIGN KEY (orcamento_id) REFERENCES TB_ORCAMENTOS(id) ON DELETE CASCADE,
                FOREIGN KEY (modulo_id) REFERENCES TB_MODULOS(id) ON DELETE CASCADE
            )
        """)

        # Orçamento ↔ Mão de obra
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTO_MAO_DE_OBRA (
                orcamento_id INTEGER NOT NULL,
                servico_id INTEGER NOT NULL,
                dias_utilizados INTEGER NOT NULL,
                valor_total_servico REAL NOT NULL,
                PRIMARY KEY (orcamento_id, servico_id),
                FOREIGN KEY (orcamento_id) REFERENCES TB_ORCAMENTOS(id) ON DELETE CASCADE,
                FOREIGN KEY (servico_id) REFERENCES TB_MAO_DE_OBRA(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    # ---------------------------
    # ORÇAMENTOS
    # ---------------------------
    def criar_orcamento(self, nome: str, descricao: str = "") -> int:
        cur = self.conn.cursor()
        cur.execute("""
        INSERT INTO TB_ORCAMENTOS (nome_orcamento, data_criacao, descricao)
        VALUES (?, DATE('now'), ?)
    """, (nome, descricao))
        self.conn.commit()
        return cur.lastrowid


    def listar_orcamentos(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM TB_ORCAMENTOS ORDER BY data_criacao DESC")
        return cur.fetchall()
    
    def obter_orcamento(self, orcamento_id: int):
        """Retorna as informações básicas de um orçamento pelo ID."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, nome_orcamento, descricao, data_criacao
            FROM TB_ORCAMENTOS
            WHERE id = ?
        """, (orcamento_id,))
        row = cur.fetchone()
        if row:
            return {
                "id": row["id"],
                "nome_orcamento": row["nome_orcamento"],
                "descricao": row["descricao"],
                "data_criacao": row["data_criacao"],
            }
        return None

    # ---------------------------
    # MÓDULOS
    # ---------------------------
    def adicionar_modulo(self, nome: str, valor_base: float):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO TB_MODULOS (nome_modulo, valor_base)
            VALUES (?, ?)
        """, (nome, valor_base))
        self.conn.commit()

    def listar_modulos(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM TB_MODULOS ORDER BY nome_modulo")
        return cur.fetchall()

    def atualizar_modulo(self, modulo_id: int, nome: str, valor_base: float):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE TB_MODULOS SET nome_modulo = ?, valor_base = ?
            WHERE id = ?
        """, (nome, valor_base, modulo_id))
        self.conn.commit()

    def remover_modulo(self, modulo_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM TB_MODULOS WHERE id = ?", (modulo_id,))
        self.conn.commit()

    def adicionar_modulo_ao_orcamento(self, orcamento_id: int, modulo_id: int, quantidade: int, valor_total: float):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO TB_ORCAMENTO_MODULO (orcamento_id, modulo_id, quantidade, valor_total_modulo)
            VALUES (?, ?, ?, ?)
        """, (orcamento_id, modulo_id, quantidade, valor_total))
        self.conn.commit()

    def listar_modulos_do_orcamento(self, orcamento_id: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT m.nome_modulo, om.quantidade, om.valor_total_modulo
            FROM TB_ORCAMENTO_MODULO om
            JOIN TB_MODULOS m ON m.id = om.modulo_id
            WHERE om.orcamento_id = ?
        """, (orcamento_id,))
        return cur.fetchall()

    # ---------------------------
    # MÃO DE OBRA
    # ---------------------------
    def listar_trabalhador(self):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT id, nome_trabalhador, custo_dia
        FROM TB_MAO_DE_OBRA
        ORDER BY nome_trabalhador
    """)
        return cur.fetchall()
    
    def adicionar_mao_de_obra(self, nome_trabalhador: str, custo_dia: float):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO TB_MAO_DE_OBRA (nome_trabalhador, custo_dia)
            VALUES (?, ?)
        """, (nome_trabalhador, custo_dia))
        self.conn.commit()

    def listar_mao_de_obra(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM TB_MAO_DE_OBRA ORDER BY nome_trabalhador")
        return cur.fetchall()

    def atualizar_mao_de_obra(self, servico_id: int, nome: str, custo_dia: float):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE TB_MAO_DE_OBRA SET nome_trabalhador = ?, custo_dia = ?
            WHERE id = ?
        """, (nome, custo_dia, servico_id))
        self.conn.commit()

    def remover_mao_de_obra(self, servico_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM TB_MAO_DE_OBRA WHERE id = ?", (servico_id,))
        self.conn.commit()

    def adicionar_mao_de_obra_ao_orcamento(self, orcamento_id: int, servico_id: int, dias: int, valor_total: float):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO TB_ORCAMENTO_MAO_DE_OBRA (orcamento_id, servico_id, dias_utilizados, valor_total_servico)
            VALUES (?, ?, ?, ?)
        """, (orcamento_id, servico_id, dias, valor_total))
        self.conn.commit()

    def listar_mao_de_obra_do_orcamento(self, orcamento_id: int):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT s.nome_trabalhador, o.dias_utilizados, o.valor_total_servico
            FROM TB_ORCAMENTO_MAO_DE_OBRA o
            JOIN TB_MAO_DE_OBRA s ON s.id = o.servico_id
            WHERE o.orcamento_id = ?
        """, (orcamento_id,))
        return cur.fetchall()

    # ---------------------------
    # UTIL
    # ---------------------------
    
    def calcular_total_orcamento(self, orcamento_id: int) -> float:
        cur = self.conn.cursor()
        cur.execute("SELECT SUM(valor_total_modulo) FROM TB_ORCAMENTO_MODULO WHERE orcamento_id = ?", (orcamento_id,))
        total_modulos = cur.fetchone()[0] or 0.0

        cur.execute("SELECT SUM(valor_total_servico) FROM TB_ORCAMENTO_MAO_DE_OBRA WHERE orcamento_id = ?", (orcamento_id,))
        total_servicos = cur.fetchone()[0] or 0.0

        return total_modulos + total_servicos

    def close(self):
        self.conn.close()
