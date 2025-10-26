from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from telas.tela_inicial import TelaInicial
from telas.gerenciamento_modulos import TelaGerenciamentoModulos
from telas.gerenciamento_mao_de_obra import TelaGerenciamentoMaoDeObra
from telas.orcamento_modulo import TelaOrcamentoModulo
from telas.orcamento_mao_de_obra import TelaOrcamentoMaoDeObra
from telas.historico_orcamento import TelaHistoricoOrcamentos
from data import OrcamentoData

Window.size = (1200, 800)  # largura, altura

class WoodPlanApp(App):
    def build(self):
        sm = ScreenManager()

        # Cria e armazena a instância do banco
        sm.data = OrcamentoData()

        sm.add_widget(TelaInicial(sm.data, name="tela_inicial"))
        sm.add_widget(TelaGerenciamentoModulos(sm.data, name="gerenciamento_modulos"))
        sm.add_widget(TelaGerenciamentoMaoDeObra(sm.data, name="gerenciamento_mao_de_obra"))
        sm.add_widget(TelaOrcamentoModulo(sm.data, name="orcamento_modulo"))
        sm.add_widget(TelaOrcamentoMaoDeObra(sm.data, name="orcamento_mao_de_obra"))
        sm.add_widget(TelaHistoricoOrcamentos(sm.data, name="historico_orcamentos"))

        return sm

if __name__ == "__main__":
    WoodPlanApp().run()