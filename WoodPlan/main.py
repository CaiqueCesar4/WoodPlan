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
from ui import OrcamentoApp

if __name__ == "__main__":
    OrcamentoApp().run()
