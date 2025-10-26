# telas/orcamento_modulo.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class TelaOrcamentoModulo(Screen):
    def __init__(self, data, orcamento_id=None, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.orcamento_id = orcamento_id
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Título
        root.add_widget(Label(
            text="Orçamento - Módulos",
            font_size=28,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50
        ))

        # Campo nome do orçamento
        self.nome_orcamento_input = TextInput(
            hint_text="Nome do Orçamento",
            size_hint=(1, None),
            height=45,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        # Campo descrição do orçamento
        self.descricao_input = TextInput(
            hint_text="Descrição (opcional)",
            size_hint=(1, None),
            height=80,
            multiline=True,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        # Spinner de módulos
        self.spinner_modulos = Spinner(
            text="Selecione um módulo",
            values=[],
            size_hint=(1, None),
            height=50,
            background_color=(0.35, 0.35, 0.35, 1),
            color=(1, 1, 1, 1)
        )

        # Entradas para largura e altura
        self.largura_input = TextInput(
            hint_text="Largura (m)",
            input_filter="float",
            size_hint=(1, None),
            height=45,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        self.altura_input = TextInput(
            hint_text="Altura (m)",
            input_filter="float",
            size_hint=(1, None),
            height=45,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        # Quantidade
        self.qtd_input = TextInput(
            hint_text="Quantidade",
            input_filter="int",
            size_hint=(1, None),
            height=45,
            foreground_color=(1, 1, 1, 1),
            background_color=(0.3, 0.3, 0.3, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.7, 0.7, 0.7, 1),
            padding=[10, 10],
        )

        # Botão adicionar módulo
        add_btn = Button(
            text="Adicionar Módulo",
            size_hint=(1, None),
            height=50,
            background_color=(0.45, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        add_btn.bind(on_release=self.adicionar_modulo)

        # Lista de módulos adicionados
        self.scroll = ScrollView(size_hint=(1, 1))
        self.lista_layout = GridLayout(cols=1, spacing=8, size_hint_y=None)
        self.lista_layout.bind(minimum_height=self.lista_layout.setter("height"))
        self.scroll.add_widget(self.lista_layout)

        # Botão para ir para mão de obra
        proximo_btn = Button(
            text="Próximo: Mão de Obra",
            size_hint=(1, None),
            height=50,
            background_color=(0.45, 0.25, 0.15, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        
        def ir_para_mao_de_obra(instance):
            if self.orcamento_id:
                tela_mao = self.manager.get_screen("orcamento_mao_de_obra")
                tela_mao.orcamento_id = self.orcamento_id
                self.manager.current = "orcamento_mao_de_obra"

        proximo_btn.bind(on_release=ir_para_mao_de_obra)

        # Botão voltar
        voltar_btn = Button(
            text="Voltar",
            size_hint=(1, None),
            height=45,
            background_color=(0.35, 0.35, 0.35, 1),
            color=(1, 1, 1, 1)
        )
        voltar_btn.bind(on_release=lambda x: setattr(self.manager, "current", "tela_inicial"))

        # Adiciona widgets ao layout principal
        root.add_widget(self.nome_orcamento_input)
        root.add_widget(self.descricao_input)
        root.add_widget(self.spinner_modulos)
        root.add_widget(self.largura_input)
        root.add_widget(self.altura_input)
        root.add_widget(self.qtd_input)
        root.add_widget(add_btn)
        root.add_widget(self.scroll)
        root.add_widget(proximo_btn)
        root.add_widget(voltar_btn)

        self.add_widget(root)

    def on_pre_enter(self):
        """Carrega módulos disponíveis"""
        modulos = [m["nome_modulo"] for m in self.data.listar_modulos()]
        self.spinner_modulos.values = modulos
        if modulos:
            self.spinner_modulos.text = modulos[0]
        self.atualizar_lista()

    def adicionar_modulo(self, instance):
        nome = self.spinner_modulos.text
        try:
            largura = float(self.largura_input.text)
            altura = float(self.altura_input.text)
            qtd = int(self.qtd_input.text)
        except ValueError:
            return
    
        # Se ainda não existe orçamento, cria um novo com nome e descrição
        if not self.orcamento_id:
            nome_orcamento = getattr(self, "nome_orcamento_input", None)
            descricao_orcamento = getattr(self, "descricao_orcamento_input", None)
    
            nome = nome_orcamento.text if nome_orcamento and nome_orcamento.text.strip() else "Orçamento sem nome"
            descricao = descricao_orcamento.text if descricao_orcamento else ""
    
            self.orcamento_id = self.data.criar_orcamento(nome, descricao)
            self.manager.current_orcamento_info = {"nome": nome, "descricao": descricao}
    
        modulo = next((m for m in self.data.listar_modulos() if m["nome_modulo"] == self.spinner_modulos.text), None)
        if not modulo:
            return
    
        area = largura * altura
        valor_total = area * modulo["valor_base"] * qtd
    
        self.data.adicionar_modulo_ao_orcamento(self.orcamento_id, modulo["id"], qtd, valor_total)
    
        self.largura_input.text = ""
        self.altura_input.text = ""
        self.qtd_input.text = ""
    
        self.atualizar_lista()

    def atualizar_lista(self):
        self.lista_layout.clear_widgets()
        if not self.orcamento_id:
            return
        for row in self.data.listar_modulos_do_orcamento(self.orcamento_id):
            linha = BoxLayout(size_hint_y=None, height=40)
            lbl = Label(
                text=f"{row['nome_modulo']} - {row['quantidade']}x - R$ {row['valor_total_modulo']:.2f}",
                color=(1, 1, 1, 1)
            )
            linha.add_widget(lbl)
            self.lista_layout.add_widget(linha)