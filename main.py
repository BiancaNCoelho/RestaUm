import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MinhaJanela(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RESTA UM")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #fff4e6;")

        self.layout = QGridLayout()

        self.label = QLabel("RESTA UM", self)
        self.label.setStyleSheet("font-size: 40px; color: #3c2f2f;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label, 0, 0, 1, 3)

        self.botao_jogar = QPushButton("Jogar", self)
        self.botao_jogar.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.botao_jogar.clicked.connect(self.jogar)
        self.layout.addWidget(self.botao_jogar, 1, 0)

        self.botao_jogar = QPushButton("Regras", self)
        self.botao_jogar.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.botao_jogar.clicked.connect(self.regras)
        self.layout.addWidget(self.botao_jogar, 1, 1)

        self.botao_sair = QPushButton("Sair", self)
        self.botao_sair.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.botao_sair.clicked.connect(self.sair)
        self.layout.addWidget(self.botao_sair, 1, 2) 

        self.setregras = QWidget()
        self.setregras .setLayout(QGridLayout())
        self.setregras .setVisible(False) 
        self.layout.addWidget(self.setregras, 2, 0, 1, 3)

        self.criar_tabuleiro()
        self.tabuleiro_widget = QWidget()
        self.tabuleiro_widget.setLayout(self.tabuleiro)
        self.tabuleiro_widget.setVisible(False) 
        self.layout.addWidget(self.tabuleiro_widget, 2, 0, 1, 3)

        self.setLayout(self.layout)

    def criar_tabuleiro(self):
        self.tabuleiro = QGridLayout()

        for linha in range(7):
            for coluna in range(7):
                botao = QPushButton("", self)
                botao.setFixedSize(50, 50)

                if (linha < 2 or linha > 4) and (coluna < 2 or coluna > 4):
                    botao.setEnabled(False)
                    botao.setStyleSheet("background-color: gray;")
                else:
                    botao.setStyleSheet("background-color: blue;")
                    botao.clicked.connect(self.clicar_celula)
                if (linha == 3 and coluna == 3):
                    botao.setStyleSheet("background-color: white;")

                self.tabuleiro.addWidget(botao, linha, coluna)

    def clicar_celula(self):
        botao = self.sender()
        print(f"Célula clicada: {botao.x()}, {botao.y()}")
        if botao.isEnabled() and botao.styleSheet() != "background-color: white;":
            botao.setStyleSheet("background-color: green;")

    def regras(self):
        self.label.setText("Regras")
        text = """

        Como jogar:
        1. Escolha uma peça para começar.
        2. Pula a peça escolhida sobre outra peça, na horizontal ou na vertical, até chegar a um espaço vazio.
        3. Repita os movimentos até restar apenas uma peça. 
        
        A partida terminaa quando não for possivel realizar um movimento ou quando restar apenas uma peça."""

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'assets/solitaire.jpg')
        picture = QPixmap(path)

        if self.setregras.layout().count() == 0:
            picture = picture.scaled(200, 200)
            image = QLabel(self)
            image.setPixmap(picture)
            image.setAlignment(Qt.AlignCenter)
            s = QLabel(text, self)
            s.setWordWrap(True)    
            self.setregras.layout().addWidget(image)
            self.setregras.layout().addWidget(s)
        
        self.setregras.setVisible(True)
        self.tabuleiro_widget.setVisible(False)

    def jogar(self):
        self.label.setText("Jogando...")
        self.tabuleiro_widget.setVisible(True)
        self.setregras .setVisible(False) 

    def sair(self):
        self.close()

app = QApplication(sys.argv)
janela = MinhaJanela()
janela.show()
sys.exit(app.exec_())