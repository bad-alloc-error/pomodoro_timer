from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

#Variaves globais para cada timer
POMODORO_TIME    = 1500000 #25 minutos
SHORT_BREAK_TIME = 300000  #5 minutos
LONG_BREAK_TIME  = 900000  #15 minutos

class Pomodoro(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pomodoro_limit = POMODORO_TIME
        self.short_break_limit = SHORT_BREAK_TIME
        self.long_break_limit = LONG_BREAK_TIME
        self.load_ui()

    def load_ui(self):
        """
            Inicializa a janela e carrega os widgets
            :param None
        """
        self.setMinimumSize(500, 400)
        self.setWindowTitle("0.1 Pomodoro Timer")
        self.setWindowIcon(QIcon('images/icons/tomate.jpg'))
        self.setup_tabs_and_widgets()

        # variáveis relativas a aba corrente e aos widgets que serão carregados dentro delas

        self.current_tab_selected = 0
        self.current_start_button = self.pomodoro_start_button
        self.current_stop_button  = self.pomodoro_stop_button
        self.current_reset_button = self.pomodoro_reset_button
        self.current_time_limit   = self.pomodoro_limit
        self.current_lcd          = self.pomodoro_lcd

        