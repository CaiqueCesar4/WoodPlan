from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


class OrcamentoApp(App):
    def build(self):
        self.precos_m2 = {
            "cozinha": 500.0,
            "guarda-roupa": 400.0,
            "painel": 300.0,
            "escrivaninha": 350.0,
        }

        self.total = 0.0

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Seleção de móvel
        self.spinner = Spinner(
            text="Escolha o móvel",
            values=list(self.precos_m2.keys()),
            size_hint=(1, None),
            height=44,
        )

        self.largura_input = TextInput(hint_text="Largura (m)", input_filter="float")
        self.altura_input = TextInput(hint_text="Altura (m)", input_filter="float")

        add_btn = Button(text="Adicionar", size_hint=(1, None), height=44)
        add_btn.bind(on_release=self.adicionar_item)

        finalize_btn = Button(text="Finalizar Orçamento", size_hint=(1, None), height=44)
        finalize_btn.bind(on_release=self.finalizar_orcamento)

        # Área para mostrar lista de itens
        self.scroll = ScrollView(size_hint=(1, 1))
        self.itens_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.itens_layout.bind(minimum_height=self.itens_layout.setter("height"))
        self.scroll.add_widget(self.itens_layout)

        # Total
        self.total_label = Label(text="Total: R$ 0.00", size_hint=(1, None), height=40)

        root.add_widget(self.spinner)
        root.add_widget(self.largura_input)
        root.add_widget(self.altura_input)
        root.add_widget(add_btn)
        root.add_widget(finalize_btn)
        root.add_widget(self.scroll)
        root.add_widget(self.total_label)

        return root

    def adicionar_item(self, instance):
        tipo = self.spinner.text
        if tipo not in self.precos_m2:
            return

        try:
            largura = float(self.largura_input.text)
            altura = float(self.altura_input.text)
        except ValueError:
            return

        area = largura * altura
        valor_item = area * self.precos_m2[tipo]
        self.total += valor_item

        item_label = Label(
            text=f"{tipo} - {area:.2f} m² - R$ {valor_item:.2f}",
            size_hint_y=None,
            height=30,
        )
        self.itens_layout.add_widget(item_label)

        self.total_label.text = f"Total: R$ {self.total:.2f}"

        self.largura_input.text = ""
        self.altura_input.text = ""

    def finalizar_orcamento(self, instance):
        final_label = Label(
            text=f"===== ORÇAMENTO FINAL =====\nTOTAL: R$ {self.total:.2f}",
            size_hint_y=None,
            height=50,
        )
        self.itens_layout.add_widget(final_label)


if __name__ == "__main__":
    OrcamentoApp().run()
