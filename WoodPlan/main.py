# # def calcular_custo_locomocao(distancia_km, km_por_litro, preco_combustivel, tempo_trajeto_horas, pessoas, meias_horas_diaria=18):
    
# """
#     Calcula o custo total de locomoção (combustível + pessoas).
    
#     distancia_km: distância de ida (em km)
#     km_por_litro: rendimento do veículo (km/l)
#     preco_combustivel: preço do combustível por litro
#     tempo_trajeto_horas: tempo total de locomoção (ida + volta) em horas
#     pessoas: lista com valores de diária de cada pessoa [diaria1, diaria2, ...]
#     horas_diaria: quantidade de horas que corresponde a uma diária (padrão 9h)
#     """
    
#     # ida e volta
#     # distancia_total = distancia_km * 2
    
#     # # custo de combustível
#     # custo_combustivel = (distancia_total / km_por_litro) * preco_combustivel
    
#     # # custo de pessoas
#     # custo_pessoas = 0
#     # for diaria in pessoas:
#     #     valor_meia_hora = diaria / meias_horas_diaria
#     #     custo_pessoas += valor_meia_hora * tempo_trajeto_horas
    
#     # # custo total
#     # custo_total = custo_combustivel + custo_pessoas
#     # return custo_total, custo_combustivel, custo_pessoas

# def calcular_orcamento():
#     precos_m2 = {
#         "cozinha": 500.0,
#         "guarda-roupa": 400.0,
#         "painel": 300.0,
#         "escrivaninha": 350.0
#     }

#     total = 0.0

#     while True:
#         print("Tipos disponíveis:")
#         for tipo in precos_m2:
#             print(f" - {tipo} (R$ {precos_m2[tipo]:.2f}/m²)")

#         tipo = input("Escolha o tipo de móvel (ou 'sair' para finalizar): ").strip().lower()
#         if tipo == "sair":
#             break

#         if tipo not in precos_m2:
#             print("Tipo inválido! Tente novamente.\n")
#             continue

#         try:
#             largura = float(input("Digite a largura (em metros): "))
#             altura = float(input("Digite a altura (em metros): "))
#         except ValueError:
#             print("Entrada inválida! Digite apenas números.\n")
#             continue

#         area = largura * altura
#         valor_item = area * precos_m2[tipo]
#         total += valor_item

#         print(f"Área calculada: {area:.2f} m²")
#         print(f"Valor deste item: R$ {valor_item:.2f}")
#         print(f"Total parcial: R$ {total:.2f}\n")

#     print("\n===== ORÇAMENTO FINAL =====")
#     return total

# # Exemplo de uso
# distancia = 2  # km (ida)
# km_por_litro = 6
# preco_combustivel = 6.00
# tempo_trajeto_horas = 1  # ida + volta
# pessoas = [140, 300]  # valores de diária de cada pessoa

# custo_material = calcular_orcamento()

# # custo_total, custo_combustivel, custo_pessoas = calcular_custo_locomocao(
# #     distancia, km_por_litro, preco_combustivel, tempo_trajeto_horas, pessoas
# # )

# # print(f"Custo combustível: R${custo_combustivel:.2f}")
# print(f'Custo Material: R${custo_material:.2f}')
# # print(f"Custo pessoas: R${custo_pessoas:.2f}")
# # print(f"Custo total: R${custo_material + custo_total:.2f}")

# main.py


from screen_manager import WoodPlanApp


if __name__ == "__main__":
   WoodPlanApp().run()

# import sqlite3

# # Caminho do banco de dados (ajuste se necessário)
# DB_PATH = "orcamento.db"

# # Dados a serem inseridos
# trabalhadores = [
#     ("Trabalhador 1", 140.00),
#     ("Trabalhador 2", 130.00),
#     ("Trabalhador 3", 320.00),
# ]

# def popular_mao_de_obra():
#     conn = sqlite3.connect(DB_PATH)
#     cur = conn.cursor()

#     # Garante que a tabela existe
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS TB_MAO_DE_OBRA (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome_trabalhador TEXT NOT NULL,
#             custo_dia REAL NOT NULL
#         )
#     """)

#     # Insere os dados se ainda não existirem
#     for nome, custo in trabalhadores:
#         cur.execute("""
#             INSERT OR IGNORE INTO TB_MAO_DE_OBRA (nome_servico, custo_dia)
#             VALUES (?, ?)
#         """, (nome, custo))

#     conn.commit()
#     conn.close()
#     print("✅ Dados de trabalhadores adicionados com sucesso!")

# if __name__ == "__main__":
#     popular_mao_de_obra()