from PyQt5.QtWidgets import (QWidget, QTabWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
QGroupBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer

#Variaves globais para cada timer
POMODORO_TIME    = 1500000 #25 minutos
SHORT_BREAK_TIME = 300000  #5 minutos
LONG_BREAK_TIME  = 900000  #15 minutos

class Pomodoro(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pomodoro_limit    = POMODORO_TIME
        self.short_break_limit = SHORT_BREAK_TIME
        self.long_break_limit  = LONG_BREAK_TIME
        self.load_ui()

    def load_ui(self):
        """
            Inicializa a janela e carrega os widgets
            :param None
        """

        self.setMinimumSize(500, 400)
        self.setWindowTitle('0.1 Pomodoro Timer')
        self.setWindowIcon(QIcon('images/icons/tomate.jpg'))
        self.setup_tabs_and_widgets()

        # variáveis relativas a aba corrente e aos widgets que serão carregados dentro delas
        self.current_tab_selected = 0
        self.current_start_button = self.pomodoro_start_button
        self.current_stop_button  = self.pomodoro_stop_button
        self.current_reset_button = self.pomodoro_reset_button
        self.current_time_limit   = self.pomodoro_limit
        self.current_lcd          = self.pomodoro_lcd

        # variáveis relativas a tarefa atual do usuário
        self.task_is_set           = False
        self.number_of_tasks       = 0
        self.task_complete_counter = 0

        # cria o objeto timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        # mostra a janela
        self.show()
    
    def setup_tabs_and_widgets(self):
        """
            Configura as abas para os direntes "perfis"
            :param None
        """

        # cria a barra de abas e os containers de widget para cada aba
        self.tab_bar      = QTabWidget(self)

        # cria a aba do perfil Pomodoro (25 min)
        self.pomodoro_tab = QWidget()
        self.pomodoro_tab.setObjectName("Pomodoro")
        
        # cria a aba de pausa curta (5 min)
        self.short_break_tab = QWidget()
        self.short_break_tab.setObjectName("ShortBreak")

        # cria aba de pausa longa (15 min)
        self.long_break_tab = QWidget()
        self.long_break_tab.setObjectName("LongBreak")

        self.tab_bar.addTab(self.pomodoro_tab, "Pomodoro")
        self.tab_bar.addTab(self.short_break_tab, "Short Break")
        self.tab_bar.addTab(self.long_break_tab, "Long Break")

        # sinal
        self.tab_bar.currentChanged.connect(self.tabs_switched)

        # cria os widgets button e lineedit e a barra de tarefas para o perfil Pomodoro
        self.enter_task_lineedit = QLineEdit()
        self.enter_task_lineedit.setClearButtonEnabled(True)
        self.enter_task_lineedit.setPlaceholderText("Digite sua tarefa atual")

        confirm_task_button = QPushButton(QIcon("images/icons/icons8-mais.gif"), None)
        confirm_task_button.setObjectName("ConfirmButton")
        confirm_task_button.clicked.connect(self.add_task_to_task_bar)

        task_entry_h_box = QHBoxLayout()
        task_entry_h_box.addWidget(self.enter_task_lineedit)
        task_entry_h_box.addWidget(confirm_task_button)

        self.tasks_v_box = QVBoxLayout()
        
        task_v_box = QVBoxLayout()
        task_v_box.addLayout(task_entry_h_box)
        task_v_box.addLayout(self.tasks_v_box)

        # container p/ barra de tarefas
        task_bar_gb = QGroupBox("Tarefas")
        task_bar_gb.setLayout(task_v_box)

        # cria e configura o layout da view principal
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(self.tab_bar)
        main_v_box.addWidget(task_bar_gb)
        self.setLayout(main_v_box)