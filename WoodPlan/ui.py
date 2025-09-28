# # ui.py
# from kivy.uix.widget import Widget
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.textinput import TextInput
# from kivy.uix.spinner import Spinner
# from kivy.uix.button import Button
# from kivy.uix.scrollview import ScrollView
# from kivy.uix.gridlayout import GridLayout
# from kivy.uix.screenmanager import ScreenManager, Screen

# from data import OrcamentoData

# class TelaInicial(Screen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.build_ui()

#     def build_ui(self):
#         root = BoxLayout(orientation="vertical", padding=20, spacing=20)

#         novo_btn = Button(text="Novo Orçamento", size_hint=(1, None), height=60)
#         novo_btn.bind(on_release=lambda x: setattr(self.manager, "current", "principal"))

#         gerenciar_btn = Button(text="Gerenciar Módulos", size_hint=(1, None), height=60)
#         gerenciar_btn.bind(on_release=lambda x: setattr(self.manager, "current", "gerenciamento"))

#         mao_obra_btn = Button(text="Gerenciar Mão de Obra", size_hint=(1, None), height=60)
#         mao_obra_btn.bind(on_release=lambda x: setattr(self.manager, "current", "mao_obra"))

#         root.add_widget(Label(text="Bem-vindo ao Sistema de Orçamentos", size_hint=(1, None), height=60))
#         root.add_widget(novo_btn)
#         root.add_widget(gerenciar_btn)
#         root.add_widget(mao_obra_btn)

#         self.add_widget(root)

# class TelaMaoObra(Screen):
#     def __init__(self, data, **kwargs):
#         super().__init__(**kwargs)
#         self.data = data
#         self.build_ui()

#     def build_ui(self):
#         root = BoxLayout(orientation="vertical", padding=10, spacing=10)

#         add_btn = Button(text="Adicionar Mão de Obra", size_hint=(1, None), height=44)
#         add_btn.bind(on_release=self.form_adicionar_mao_obra)

#         self.scroll = ScrollView(size_hint=(1, 1))
#         self.mao_obra_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
#         self.mao_obra_layout.bind(minimum_height=self.mao_obra_layout.setter("height"))
#         self.scroll.add_widget(self.mao_obra_layout)

#         back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
#         back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

#         root.add_widget(Label(text="Gerenciamento de Mão de Obra"))
#         root.add_widget(add_btn)
#         root.add_widget(self.scroll)
#         root.add_widget(back_btn)

#         self.add_widget(root)

#     def form_adicionar_mao_obra(self, instance):
#         self.mao_obra_layout.clear_widgets()

#         linha = BoxLayout(size_hint_y=None, height=40)
#         nome_input = TextInput(hint_text="Nome")
#         valor_input = TextInput(hint_text="Valor (R$)", input_filter="float")
#         salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

#         def salvar(instance):
#             try:
#                 valor = float(valor_input.text)
#             except ValueError:
#                 return
#             self.data.adicionar_mao_obra(nome_input.text, valor)
#             self.on_enter()

#         salvar_btn.bind(on_release=salvar)

#         linha.add_widget(nome_input)
#         linha.add_widget(valor_input)
#         linha.add_widget(salvar_btn)

#         self.mao_obra_layout.add_widget(linha)

#     def on_enter(self):
#         self.mao_obra_layout.clear_widgets()
#         for row in self.data.listar_mao_obra():
#             linha = BoxLayout(size_hint_y=None, height=40)
#             lbl = Label(text=f"{row['nome']} - R$ {row['valor']:.2f}")

#             editar_btn = Button(text="Editar", size_hint=(None, 1), width=80)
#             remover_btn = Button(text="Remover", size_hint=(None, 1), width=80)

#             editar_btn.bind(on_release=lambda x, r=row: self.editar_mao_obra(r))
#             remover_btn.bind(on_release=lambda x, r=row: self.remover_mao_obra(r["id"]))

#             linha.add_widget(lbl)
#             linha.add_widget(editar_btn)
#             linha.add_widget(remover_btn)
#             self.mao_obra_layout.add_widget(linha)

#     def editar_mao_obra(self, row):
#         self.mao_obra_layout.clear_widgets()
#         linha = BoxLayout(size_hint_y=None, height=40)
#         nome_input = TextInput(text=row["nome"])
#         valor_input = TextInput(text=str(row["valor"]), input_filter="float")
#         salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

#         def salvar(instance):
#             try:
#                 novo_valor = float(valor_input.text)
#             except ValueError:
#                 return
#             self.data.atualizar_mao_obra(row["id"], nome_input.text, novo_valor)
#             self.on_enter()

#         salvar_btn.bind(on_release=salvar)

#         linha.add_widget(nome_input)
#         linha.add_widget(valor_input)
#         linha.add_widget(salvar_btn)
#         self.mao_obra_layout.add_widget(linha)

#     def remover_mao_obra(self, mao_obra_id):
#         self.data.remover_mao_obra(mao_obra_id)
#         self.on_enter()

# class TelaPrincipal(Screen):
#     def __init__(self, data, **kwargs):
#         super().__init__(**kwargs)
#         self.data = data
#         self.build_ui()

#     def build_ui(self):
#         root = BoxLayout(orientation="vertical", padding=10, spacing=10)

#         self.spinner_categoria = Spinner(
#             text="Escolha a categoria",
#             values=self.data.get_categorias(),
#             size_hint=(1, None),
#             height=44,
#         )
#         self.spinner_categoria.bind(text=self.atualizar_subprodutos)

#         self.spinner_subproduto = Spinner(
#             text="Escolha o subproduto",
#             values=[],
#             size_hint=(1, None),
#             height=44,
#         )

#         self.largura_input = TextInput(hint_text="Largura (m)", input_filter="float")
#         self.altura_input = TextInput(hint_text="Altura (m)", input_filter="float")

#         add_btn = Button(text="Adicionar", size_hint=(1, None), height=44)
#         add_btn.bind(on_release=self.adicionar_item)

#         finalize_btn = Button(text="Finalizar Orçamento", size_hint=(1, None), height=44)
#         finalize_btn.bind(on_release=self.finalizar_orcamento)

#         self.scroll = ScrollView(size_hint=(1, 1))
#         self.itens_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
#         self.itens_layout.bind(minimum_height=self.itens_layout.setter("height"))
#         self.scroll.add_widget(self.itens_layout)

#         self.total_label = Label(text="Total: R$ 0.00", size_hint=(1, None), height=40)

#         # Botão voltar para tela inicial
#         back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
#         back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

#         root.add_widget(self.spinner_categoria)
#         root.add_widget(self.spinner_subproduto)
#         root.add_widget(self.largura_input)
#         root.add_widget(self.altura_input)
#         root.add_widget(add_btn)
#         root.add_widget(finalize_btn)
#         root.add_widget(self.scroll)
#         root.add_widget(self.total_label)
#         root.add_widget(back_btn)

#         self.add_widget(root)

#     def atualizar_subprodutos(self, spinner, categoria):
#         subprodutos = list(self.data.get_subprodutos(categoria).keys())
#         if subprodutos:
#             self.spinner_subproduto.values = subprodutos
#             self.spinner_subproduto.text = subprodutos[0]
#         else:
#             self.spinner_subproduto.values = []
#             self.spinner_subproduto.text = "Escolha o subproduto"

#     def adicionar_item(self, instance):
#         categoria = self.spinner_categoria.text
#         subproduto = self.spinner_subproduto.text

#         try:
#             largura = float(self.largura_input.text)
#             altura = float(self.altura_input.text)
#         except ValueError:
#             return

#         valor_item = self.data.calcular_valor(categoria, subproduto, largura, altura)
#         if valor_item == 0:
#             return

#         area = largura * altura
#         item_label = Label(
#             text=f"{categoria} - {subproduto} - {area:.2f} m² - R$ {valor_item:.2f}",
#             size_hint_y=None,
#             height=30,
#         )
#         self.itens_layout.add_widget(item_label)

#         self.total_label.text = f"Total: R$ {self.data.get_total():.2f}"

#         self.largura_input.text = ""
#         self.altura_input.text = ""

#     def finalizar_orcamento(self, instance):
#         # ao invés de mostrar o label final, abre a tela de mão de obra
#         self.manager.current = "mao_obra"

# class TelaGerenciamento(Screen):
#     def __init__(self, data, **kwargs):
#         super().__init__(**kwargs)
#         self.data = data
#         self.build_ui()

#     def build_ui(self):
#         root = BoxLayout(orientation="vertical", padding=10, spacing=10)

#         add_btn = Button(text="Adicionar Módulo", size_hint=(1, None), height=44)
#         add_btn.bind(on_release=self.form_adicionar_modulo)

#         self.scroll = ScrollView(size_hint=(1, 1))
#         self.subprodutos_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
#         self.subprodutos_layout.bind(minimum_height=self.subprodutos_layout.setter("height"))
#         self.scroll.add_widget(self.subprodutos_layout)

#         back_btn = Button(text="Voltar", size_hint=(1, None), height=44)
#         back_btn.bind(on_release=lambda x: setattr(self.manager, "current", "inicial"))

#         root.add_widget(Label(text="Gerenciamento de módulos"))
#         root.add_widget(add_btn)
#         root.add_widget(self.scroll)
#         root.add_widget(back_btn)

#         self.add_widget(root)

#     def form_adicionar_modulo(self, instance):
#         self.subprodutos_layout.clear_widgets()

#         linha = BoxLayout(size_hint_y=None, height=40)
#         categoria_input = TextInput(hint_text="Categoria")
#         nome_input = TextInput(hint_text="Nome do módulo")
#         preco_input = TextInput(hint_text="Preço por m²", input_filter="float")
#         salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

#         def salvar(instance):
#             try:
#                 preco = float(preco_input.text)
#             except ValueError:
#                 return
#             self.data.adicionar_subproduto(
#                 categoria_input.text, nome_input.text, preco
#             )
#             self.on_enter()

#         salvar_btn.bind(on_release=salvar)

#         linha.add_widget(categoria_input)
#         linha.add_widget(nome_input)
#         linha.add_widget(preco_input)
#         linha.add_widget(salvar_btn)

#         self.subprodutos_layout.add_widget(linha)

#     def on_enter(self):
#         self.subprodutos_layout.clear_widgets()
#         for row in self.data.listar_todos_subprodutos():
#             linha = BoxLayout(size_hint_y=None, height=40)
#             lbl = Label(text=f"{row['categoria']} - {row['nome']} (R$ {row['preco_m2']:.2f}/m²)")

#             editar_btn = Button(text="Editar", size_hint=(None, 1), width=80)
#             remover_btn = Button(text="Remover", size_hint=(None, 1), width=80)

#             editar_btn.bind(on_release=lambda x, r=row: self.editar_subproduto(r))
#             remover_btn.bind(on_release=lambda x, r=row: self.remover_subproduto(r["id"]))

#             linha.add_widget(lbl)
#             linha.add_widget(editar_btn)
#             linha.add_widget(remover_btn)
#             self.subprodutos_layout.add_widget(linha)

#     def editar_subproduto(self, row):
#         self.subprodutos_layout.clear_widgets()
#         linha = BoxLayout(size_hint_y=None, height=40)
#         nome_input = TextInput(text=row["nome"])
#         preco_input = TextInput(text=str(row["preco_m2"]), input_filter="float")
#         salvar_btn = Button(text="Salvar", size_hint=(None, 1), width=80)

#         def salvar(instance):
#             try:
#                 novo_preco = float(preco_input.text)
#             except ValueError:
#                 return
#             self.data.atualizar_subproduto(row["id"], nome_input.text, novo_preco)
#             self.on_enter()

#         salvar_btn.bind(on_release=salvar)

#         linha.add_widget(Label(text=row["categoria"]))
#         linha.add_widget(nome_input)
#         linha.add_widget(preco_input)
#         linha.add_widget(salvar_btn)
#         self.subprodutos_layout.add_widget(linha)

#     def remover_subproduto(self, subproduto_id):
#         self.data.remover_subproduto(subproduto_id)
#         self.on_enter()

# class OrcamentoApp(App):
#     def build(self):
#         self.data = OrcamentoData()

#         sm = ScreenManager()
#         sm.add_widget(TelaInicial(name="inicial"))
#         sm.add_widget(TelaPrincipal(self.data, name="principal"))
#         sm.add_widget(TelaGerenciamento(self.data, name="gerenciamento"))
#         sm.add_widget(TelaGerenciarMaoObra(self.data, name="gerenciar_mao_obra"))  # já tinha
#         sm.add_widget(TelaMaoObra(self.data, name="mao_obra"))  # nova tela

#         return sm

# if __name__ == "__main__":
#     OrcamentoApp().run()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from data import OrcamentoData
from telas.inicial import tela_inicial
from telas.orcamento_modulo import tela_orcamento_modulo
from telas.gerenciar_modulos import tela_gerenciar_modulos
from telas.gerenciar_mao_de_obra import tela_gerenciar_mao_de_obra
from telas.orcamento_mao_de_obra import tela_orcamento_mao_de_obra


class OrcamentoApp(App):
    def build(self):
        self.data = OrcamentoData()

        sm = ScreenManager()
        sm.add_widget(tela_inicial(name="inicial"))
        sm.add_widget(tela_orcamento_modulo(self.data, name="orcamento modulos"))
        sm.add_widget(tela_gerenciar_modulos(self.data, name="gerenciamento de modulos"))
        sm.add_widget(tela_gerenciar_mao_de_obra(self.data, name="gerenciar mao de obra"))
        sm.add_widget(tela_orcamento_mao_de_obra(self.data, name="orcamento mao obra"))

        return sm