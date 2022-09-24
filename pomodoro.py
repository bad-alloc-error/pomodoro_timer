from PyQt5.QtWidgets import (QWidget, QTabWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
QGroupBox, QLCDNumber, QLabel)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

#Variaves globais para cada timer
POMODORO_TIME    = 1500000 #25 minutos
SHORT_BREAK_TIME = 300000  #5 minutos
LONG_BREAK_TIME  = 900000  #15 minutos

class Pomodoro(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.load_ui()
       
       

    def load_ui(self):
        """
            Inicializa a janela e carrega os widgets
            :param None
        """

        self.pomodoro_limit    = POMODORO_TIME
        self.short_break_limit = SHORT_BREAK_TIME
        self.long_break_limit  = LONG_BREAK_TIME

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

        self.set_pomodoro_tab()
        self.set_short_break_tab()
        self.set_long_break_tab()

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

    def set_pomodoro_tab(self):
        """
            Configura a aba Pomodoro
        """

        # converte o tempo inicial para ser exibido no timer
        start_time = self.calculate_display_time(self.pomodoro_limit)

        self.pomodoro_lcd = QLCDNumber()
        self.pomodoro_lcd.setObjectName("PomodoroLCD")
        self.pomodoro_lcd.setSegmentStyle(QLCDNumber.Filled)
        self.pomodoro_lcd.display(start_time)

        self.pomodoro_start_button = QPushButton("Iniciar")
        self.pomodoro_start_button.clicked.connect(self.start_count_down)

        self.pomodoro_stop_button = QPushButton("Parar")
        self.pomodoro_stop_button.clicked.connect(self.stop_count_down)

        self.pomodoro_reset_button = QPushButton("Reiniciar")
        self.pomodoro_reset_button.clicked.connect(self.reset_count_down)

        button_h_box = QHBoxLayout()
        button_h_box.addWidget(self.pomodoro_start_button)
        button_h_box.addWidget(self.pomodoro_stop_button)
        button_h_box.addWidget(self.pomodoro_reset_button)

        v_box = QVBoxLayout()
        v_box.addWidget(self.pomodoro_lcd)
        v_box.addLayout(button_h_box)
        self.pomodoro_tab.setLayout(v_box)

    def set_short_break_tab(self):
        """
            Configura Short Break Tab
        """

        start_time = self.calculate_display_time(self.short_break_limit)
        self.short_break_lcd = QLCDNumber()
        self.short_break_lcd.setObjectName("ShortLCD")
        self.short_break_lcd.setSegmentStyle(QLCDNumber.Filled)
        self.short_break_lcd.display(start_time)

        self.short_start_button = QPushButton("Iniciar")
        self.short_start_button.clicked.connect(self.start_count_down)

        self.short_stop_button = QPushButton("Parar")
        self.short_stop_button.clicked.connect(self.stop_count_down)

        self.short_reset_button = QPushButton("Reiniciar")
        self.short_reset_button.clicked.connect(self.reset_count_down)

        button_h_box = QHBoxLayout()
        button_h_box.addWidget(self.short_start_button)
        button_h_box.addWidget(self.short_stop_button)
        button_h_box.addWidget(self.short_reset_button)

        v_box = QVBoxLayout()
        v_box.addWidget(self.short_break_lcd)
        v_box.addLayout(button_h_box)
        self.short_break_tab.setLayout(v_box)

    def set_long_break_tab(self):
        """
            Configura Long Break Tab
        """

        start_time = self.calculate_display_time(self.long_break_limit)
        self.long_break_lcd = QLCDNumber()
        self.long_break_lcd.setObjectName("LongLCD")
        self.long_break_lcd.setSegmentStyle(QLCDNumber.Filled)
        self.long_break_lcd.display(start_time)

        self.long_start_button = QPushButton("Iniciar")
        self.long_start_button.clicked.connect(self.start_count_down)

        self.long_stop_button = QPushButton("Parar")
        self.long_stop_button.clicked.connect(self.stop_count_down)

        self.long_reset_button = QPushButton("Reiniciar")
        self.long_reset_button.clicked.connect(self.reset_count_down)

        button_h_box = QHBoxLayout()
        button_h_box.addWidget(self.long_start_button)
        button_h_box.addWidget(self.long_stop_button)
        button_h_box.addWidget(self.long_reset_button)

        v_box = QVBoxLayout()
        v_box.addWidget(self.long_break_lcd)
        v_box.addLayout(button_h_box)
        self.long_break_tab.setLayout(v_box)

    def start_count_down(self):
        """
        Inicia o timer, se o timer na aba atual for 00:00, reinicia o time caso o usuário aperte o botão de iniciar
        """

        self.current_start_button.setEnabled(False)

        # reinicia a contagem se o usuário tiver completado 4 ciclos de pomodoro
        if self.task_is_set == True and self.task_complete_counter == 0:
            self.counter_label.setText("{}/4".format(self.task_complete_counter))
        
        remaining_time = self.calculate_display_time(self.current_time_limit)
        
        if remaining_time == "00:00":
            self.reset_count_down()
            self.timer.start(1000)
        else:
            self.timer.start(1000)

    def stop_count_down(self):
        """
            Se o timer estivendo sendo executado, pare.
        """
        if self.timer.isActive() != False:
            self.timer.stop()

        self.current_start_button.setEnabled(True)

    def reset_count_down(self):
        """
            Reinicia o timer para a aba corrente se o botão Reiniciar for clicado.
        """
        self.stop_count_down()
        
        if self.current_tab_selected == 0:
            self.pomodoro_limit = POMODORO_TIME
            self.current_time_limit = self.pomodoro_limit
            reset_time = self.calculate_display_time(self.current_time_limit)

        elif self.current_tab_selected == 1: 
            self.short_break_limit = SHORT_BREAK_TIME
            self.current_time_limit = self.short_break_limit
            reset_time = self.calculate_display_time(self.current_time_limit)

        elif self.current_tab_selected == 2: 
            self.long_break_limit = LONG_BREAK_TIME
            self.current_time_limit = self.long_break_limit
            reset_time = self.calculate_display_time(self.current_time_limit)

        self.current_lcd.display(reset_time)

    def update_timer(self):
        """
            Atualiza o timer e o widget LCD, se tiver uma tarefa sendo executada 
            também atualiza o contador.
        """
       
        remaining_time = self.calculate_display_time(self.current_time_limit)
        if remaining_time == "00:00":
            self.stop_count_down()
            self.current_lcd.display(remaining_time)

        if self.current_tab_selected == 0 and self.task_is_set == True:
            self.task_complete_counter += 1
            if self.task_complete_counter == 4:
                self.counter_label.setText("Tempo pra uma longa pausa. {}/4".format(self.task_complete_counter))
                self.task_complete_counter = 0
            
            elif self.task_complete_counter < 4:
                self.counter_label.setText("{}/4".format(self.task_complete_counter))
        else:
            # atualiza o timer decrementando (por um segundo) o timer atual
            self.current_time_limit -= 1000
            self.current_lcd.display(remaining_time)

    def tabs_switched(self, index):
        """As views precisam ser atualizadas de acordo com a qual o usuário está interagindo, essa função
        atualiza essas infos da view corrente.
        """
        
        self.current_tab_selected = index
        self.stop_count_down()

        # reseta as variáveis, timer e os widgets dependendo da aba que está setada em current_tab_selected
        if self.current_tab_selected  == 0: #pomodoro
            self.current_start_button = self.pomodoro_start_button
            self.current_stop_button  = self.pomodoro_stop_button
            self.current_reset_button = self.pomodoro_reset_button
            self.pomodoro_limit       = POMODORO_TIME
            self.current_time_limit   = self.pomodoro_limit

            reset_time = self.calculate_display_time(self.current_time_limit)
            self.current_lcd          = self.pomodoro_lcd
            self.current_lcd.display(reset_time)
        
        elif self.current_tab_selected == 1: # short
            self.current_start_button  = self.short_start_button
            self.current_stop_button   = self.short_stop_button
            self.current_reset_button  = self.short_reset_button
            self.short_break_limit     = SHORT_BREAK_TIME
            self.current_time_limit    = self.short_break_limit
            reset_time                 = self.calculate_display_time(self.current_time_limit)
            self.current_lcd           = self.short_break_lcd
            self.current_lcd.display(reset_time)

        elif self.current_tab_selected == 2: # long
            self.current_start_button  = self.long_start_button
            self.current_stop_button   = self.long_stop_button
            self.current_reset_button  = self.long_reset_button
            self.long_break_limit      = LONG_BREAK_TIME
            self.current_time_limit    = self.long_break_limit
            reset_time                 = self.calculate_display_time(self.current_time_limit)
            self.current_lcd           = self.long_break_lcd
            self.current_lcd.display(reset_time)
        
    def add_task_to_task_bar(self):
        """
            Quando o usuário clicar no botão pra add, os widgets para a nova tarefa
            serão adicionados na task bar, apenas uma tarefa por vez é permitida.
        """
        text                            = self.enter_task_lineedit.text()
        self.enter_task_lineedit.clear()

        # altera a qtd de tarefas
        if text != "" and self.number_of_tasks != 1:
            self.enter_task_lineedit.setReadOnly(True)
            self.task_is_set = True
            self.new_task = QLabel(text)

            self.counter_label = QLabel("{}/4".format(self.task_complete_counter))
            self.counter_label.setAlignment(Qt.AlignmentFlag.AlignRight)
            self.cancel_task_button = QPushButton(QIcon("images/icons/menos.png"), None)
            self.cancel_task_button.setMaximumWidth(24)
            self.cancel_task_button.clicked.connect(self.clear_current_task)

            self.new_task_h_box = QHBoxLayout()
            self.new_task_h_box.addWidget(self.new_task)
            self.new_task_h_box.addWidget(self.counter_label)
            self.new_task_h_box.addWidget(self.cancel_task_button)
            self.tasks_v_box.addLayout(self.new_task_h_box)
            self.number_of_tasks += 1
    
    def clear_current_task(self):
        """
            Deleta as tarefas e reseta as variaveis
        """
        
        # remove os itens do parent widget colocando o setParent pra None
        self.new_task.setParent(None)
        self.counter_label.setParent(None)
        self.cancel_task_button.setParent(None)
        self.number_of_tasks -= 1
        self.task_is_set = False
        self.task_complete_counter = 0
        self.enter_task_lineedit.setReadOnly(False)
    
    def convert_total_time(self, time_in_milli):
        """
            Conversão dos milisegundos
        """
        minutes = (time_in_milli / (1000 * 60)) % 60
        seconds = (time_in_milli / 1000) % 60
        return int(minutes), int(seconds)

    def calculate_display_time(self, time):
        """
            Calcula o tempo que deve ser mostrado no lcd
        """
        minutes, seconds = self.convert_total_time(time)
        amount_of_time = "{:02d}:{:02d}".format(minutes, seconds)
        return amount_of_time