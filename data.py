import sqlite3
from pathlib import Path
from datetime import datetime

class OrcamentoData:
    """Gerencia a conexão e as operações CRUD para o banco de dados de Orçamentos."""

    def __init__(self, db_path: str = "orcamento.db"):
        self.db_path = Path(db_path)
        # Conexão: Cria o arquivo se não existir
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        # Habilita o controle de chaves estrangeiras
        self.conn.execute("PRAGMA foreign_keys = ON;")
        
        self._criar_tabelas()
        self._popular_dados_iniciais()
        
    def _criar_tabelas(self):
        """Cria todas as tabelas conforme o diagrama ERD."""
        cur = self.conn.cursor()

        # Tabela principal: Orçamentos
        # Equivalente ao seu TB_ORCAMENTOS original
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_orcamento TEXT NOT NULL,
                data_criacao TEXT NOT NULL, 
                descricao TEXT,
                valor_total REAL DEFAULT 0.0
            )
        """)

        # Tabela de apoio: Módulos (Produtos/Subprodutos)
        # Equivalente ao seu TB_MODULOS original (e seu 'subprodutos')
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_MODULOS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_modulo TEXT UNIQUE NOT NULL,
                valor_base REAL NOT NULL -- Preço por m²
            )
        """)

        # Tabela de apoio: Mão de Obra
        # Equivalente ao seu TB_MAO_DE_OBRA original (e seu 'mao_obra')
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_MAO_DE_OBRA (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_servico TEXT UNIQUE NOT NULL,
                custo_dia REAL NOT NULL -- Custo por dia de serviço
            )
        """)
        
        # Tabela de Junção: Módulos no Orçamento (N:N)
        # Equivalente ao seu TB_ORCAMENTO_MODULO original
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTO_MODULO (
                orcamento_id INTEGER NOT NULL,
                modulo_id INTEGER NOT NULL,
                quantidade INTEGER NOT NULL, -- Largura * Altura (m²)
                valor_total_modulo REAL NOT NULL,
                PRIMARY KEY (orcamento_id, modulo_id),
                FOREIGN KEY (orcamento_id) REFERENCES TB_ORCAMENTOS(id) ON DELETE CASCADE,
                FOREIGN KEY (modulo_id) REFERENCES TB_MODULOS(id) ON DELETE RESTRICT
            )
        """)

        # Tabela de Junção: Mão de Obra no Orçamento (N:N)
        # Equivalente ao seu TB_ORCAMENTO_MAO_DE_OBRA original
        cur.execute("""
            CREATE TABLE IF NOT EXISTS TB_ORCAMENTO_MAO_DE_OBRA (
                orcamento_id INTEGER NOT NULL,
                servico_id INTEGER NOT NULL,
                dias_utilizados INTEGER NOT NULL,
                valor_total_servico REAL NOT NULL,
                PRIMARY KEY (orcamento_id, servico_id),
                FOREIGN KEY (orcamento_id) REFERENCES TB_ORCAMENTOS(id) ON DELETE CASCADE,
                FOREIGN KEY (servico_id) REFERENCES TB_MAO_DE_OBRA(id) ON DELETE RESTRICT
            )
        """)
        
        self.conn.commit()

    def _popular_dados_iniciais(self):
        """Popula TB_MODULOS e TB_MAO_DE_OBRA se estiverem vazias."""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM TB_MODULOS")
        if cur.fetchone()[0] > 0:
            return

        # Dados de Módulos (Produtos) - Equivalente ao seu antigo 'subprodutos'
        modulos = {
            "Gabinete de Cozinha": 500.0,
            "Armário Superior": 480.0,
            "Guarda-Roupa Cabides/Gavetas": 420.0,
            "Guarda-Roupa Prateleiras": 400.0,
        }
        for nome, preco in modulos.items():
            try:
                cur.execute(
                    "INSERT INTO TB_MODULOS (nome_modulo, valor_base) VALUES (?, ?)",
                    (nome, preco)
                )
            except sqlite3.IntegrityError:
                pass # Ignora se já existir

        # Dados de Mão de Obra
        mao_de_obra = {
            "Montagem Padrão (Dia)": 350.0,
            "Instalação Elétrica (Dia)": 400.0,
            "Pintura Detalhada (Dia)": 300.0,
        }
        for nome, custo in mao_de_obra.items():
            try:
                cur.execute(
                    "INSERT INTO TB_MAO_DE_OBRA (nome_servico, custo_dia) VALUES (?, ?)",
                    (nome, custo)
                )
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()

    # ------------------ Métodos CRUD MÓDULOS (Produtos) ------------------

    def get_modulos(self):
        """Lista todos os módulos (produtos) disponíveis."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome_modulo, valor_base FROM TB_MODULOS ORDER BY nome_modulo")
        return cur.fetchall()

    def adicionar_modulo(self, nome: str, preco_m2: float):
        """Adiciona um novo módulo/produto."""
        cur = self.conn.cursor()
        try:
            cur.execute(
                "INSERT INTO TB_MODULOS (nome_modulo, valor_base) VALUES (?, ?)",
                (nome, preco_m2)
            )
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            print("Erro: Módulo com este nome já existe.")
            return None

    def atualizar_modulo(self, modulo_id: int, novo_nome: str, novo_preco: float):
        """Atualiza o nome e o preço base de um módulo."""
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE TB_MODULOS 
            SET nome_modulo = ?, valor_base = ?
            WHERE id = ?
        """, (novo_nome, novo_preco, modulo_id))
        self.conn.commit()

    def remover_modulo(self, modulo_id: int):
        """Remove um módulo/produto."""
        cur = self.conn.cursor()
        cur.execute("DELETE FROM TB_MODULOS WHERE id = ?", (modulo_id,))
        self.conn.commit()
        
    # ------------------ Métodos CRUD MÃO DE OBRA ------------------

    def listar_mao_obra(self):
        """Lista todos os serviços de mão de obra disponíveis."""
        cur = self.conn.cursor()
        cur.execute("SELECT id, nome_servico, custo_dia FROM TB_MAO_DE_OBRA ORDER BY nome_servico")
        return cur.fetchall()
    
    # ... (Os métodos adicionar_mao_obra, atualizar_mao_obra e remover_mao_obra são mantidos com novos nomes de coluna)

    def adicionar_mao_obra(self, nome: str, valor: float):
        cur = self.conn.cursor()
        try:
            cur.execute("INSERT INTO TB_MAO_DE_OBRA (nome_servico, custo_dia) VALUES (?, ?)", (nome, valor))
            self.conn.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            print("Erro: Serviço com este nome já existe.")
            return None

    def atualizar_mao_obra(self, servico_id: int, novo_nome: str, novo_valor: float):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE TB_MAO_DE_OBRA
            SET nome_servico = ?, custo_dia = ?
            WHERE id = ?
        """, (novo_nome, novo_valor, servico_id))
        self.conn.commit()

    def remover_mao_obra(self, servico_id: int):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM TB_MAO_DE_OBRA WHERE id = ?", (servico_id,))
        self.conn.commit()

    # ------------------ Métodos de ORÇAMENTO ------------------

    def iniciar_novo_orcamento(self, nome: str, descricao: str) -> int:
        """Cria um novo registro em TB_ORCAMENTOS e retorna o ID."""
        cur = self.conn.cursor()
        data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """
            INSERT INTO TB_ORCAMENTOS (nome_orcamento, data_criacao, descricao)
            VALUES (?, ?, ?)
            """,
            (nome, data_criacao, descricao)
        )
        self.conn.commit()
        return cur.lastrowid

    def incluir_modulo_orcamento(self, orcamento_id: int, modulo_id: int, largura: float, altura: float):
        """Adiciona um Módulo/Produto a um Orçamento (TB_ORCAMENTO_MODULO)."""
        cur = self.conn.cursor()
        
        # 1. Obter o valor_base do módulo
        cur.execute("SELECT valor_base FROM TB_MODULOS WHERE id = ?", (modulo_id,))
        row = cur.fetchone()
        if not row:
            print(f"Erro: Módulo ID {modulo_id} não encontrado.")
            return

        preco_m2 = row["valor_base"]
        area = largura * altura
        quantidade = area # A 'quantidade' é a área em m²
        valor_total_modulo = round(area * preco_m2, 2)
        
        # 2. Inserir na tabela de junção
        cur.execute(
            """
            INSERT INTO TB_ORCAMENTO_MODULO (orcamento_id, modulo_id, quantidade, valor_total_modulo)
            VALUES (?, ?, ?, ?)
            """,
            (orcamento_id, modulo_id, quantidade, valor_total_modulo)
        )
        self.conn.commit()

        # 3. Atualizar o valor total do Orçamento
        self._atualizar_total_orcamento(orcamento_id)


    def incluir_mao_obra_orcamento(self, orcamento_id: int, servico_id: int, dias: int):
        """Adiciona Mão de Obra a um Orçamento (TB_ORCAMENTO_MAO_DE_OBRA)."""
        cur = self.conn.cursor()

        # 1. Obter o custo_dia
        cur.execute("SELECT custo_dia FROM TB_MAO_DE_OBRA WHERE id = ?", (servico_id,))
        row = cur.fetchone()
        if not row:
            print(f"Erro: Serviço ID {servico_id} não encontrado.")
            return

        custo_dia = row["custo_dia"]
        valor_total_servico = round(custo_dia * dias, 2)
        
        # 2. Inserir na tabela de junção
        cur.execute(
            """
            INSERT INTO TB_ORCAMENTO_MAO_DE_OBRA (orcamento_id, servico_id, dias_utilizados, valor_total_servico)
            VALUES (?, ?, ?, ?)
            """,
            (orcamento_id, servico_id, dias, valor_total_servico)
        )
        self.conn.commit()

        # 3. Atualizar o valor total do Orçamento
        self._atualizar_total_orcamento(orcamento_id)


    def _atualizar_total_orcamento(self, orcamento_id: int):
        """Recalcula e atualiza o valor total em TB_ORCAMENTOS."""
        cur = self.conn.cursor()
        
        # Soma dos Módulos
        cur.execute(
            "SELECT SUM(valor_total_modulo) FROM TB_ORCAMENTO_MODULO WHERE orcamento_id = ?", 
            (orcamento_id,)
        )
        total_modulos = cur.fetchone()[0] or 0.0

        # Soma da Mão de Obra
        cur.execute(
            "SELECT SUM(valor_total_servico) FROM TB_ORCAMENTO_MAO_DE_OBRA WHERE orcamento_id = ?", 
            (orcamento_id,)
        )
        total_mao_obra = cur.fetchone()[0] or 0.0

        valor_final = round(total_modulos + total_mao_obra, 2)
        
        # Atualiza a tabela principal
        cur.execute(
            "UPDATE TB_ORCAMENTOS SET valor_total = ? WHERE id = ?",
            (valor_final, orcamento_id)
        )
        self.conn.commit()
        
    def get_orcamento_detalhes(self, orcamento_id: int):
        """Retorna os detalhes completos de um orçamento."""
        cur = self.conn.cursor()
        
        # Detalhes do Orçamento
        cur.execute("SELECT * FROM TB_ORCAMENTOS WHERE id = ?", (orcamento_id,))
        orcamento = cur.fetchone()

        if not orcamento:
            return None

        # Itens de Módulos
        cur.execute("""
            SELECT m.nome_modulo, t.quantidade, t.valor_total_modulo
            FROM TB_ORCAMENTO_MODULO t
            JOIN TB_MODULOS m ON m.id = t.modulo_id
            WHERE t.orcamento_id = ?
        """, (orcamento_id,))
        modulos = cur.fetchall()

        # Itens de Mão de Obra
        cur.execute("""
            SELECT o.nome_servico, t.dias_utilizados, t.valor_total_servico
            FROM TB_ORCAMENTO_MAO_DE_OBRA t
            JOIN TB_MAO_DE_OBRA o ON o.id = t.servico_id
            WHERE t.orcamento_id = ?
        """, (orcamento_id,))
        mao_obra = cur.fetchall()

        return {
            "orcamento": dict(orcamento),
            "modulos": [dict(m) for m in modulos],
            "mao_obra": [dict(m) for m in mao_obra]
        }


    def close(self):
        """Fecha a conexão com o banco de dados."""
        self.conn.close()