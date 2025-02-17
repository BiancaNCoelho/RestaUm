import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.selecionada = None

        self.setWindowTitle("RESTA UM")
        self.setGeometry(100, 100, 500, 500)
        self.setStyleSheet("background-color: #fff4e6;")

        self.layout = QGridLayout()

        self.label = QLabel("RESTA UM", self)
        self.label.setStyleSheet("font-size: 40px; color: #3c2f2f;")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label, 0, 0, 1, 3)

        self.play_button = QPushButton("Play", self)
        self.play_button.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.play_button.clicked.connect(self.jogar)
        self.layout.addWidget(self.play_button, 1, 0)

        self.rules_button = QPushButton("Rules", self)
        self.rules_button.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.rules_button.clicked.connect(self.regras)
        self.layout.addWidget(self.rules_button, 1, 1)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.setStyleSheet("background-color: #be9b7b;color: #3c2f2f;")
        self.quit_button.clicked.connect(self.sair)
        self.layout.addWidget(self.quit_button, 1, 2) 

        self.setRules = QWidget()
        self.setRules .setLayout(QGridLayout())
        self.setRules .setVisible(False) 
        self.layout.addWidget(self.setRules, 2, 0, 1, 3)

        self.create_board()
        self.board_widget = QWidget()
        self.board_widget.setLayout(self.board)
        self.board_widget.setVisible(False) 
        self.layout.addWidget(self.board_widget, 2, 0, 1, 3)

        self.setLayout(self.layout)

    def create_board(self):
        self.board = QGridLayout()
        self.state = [[1] * 7 for _ in range(7)]

        for row in range(7):
            for col in range(7):
                button = QPushButton("", self)
                button.setFixedSize(50, 50)
                button.row, button.col = row, col

                if (row < 2 or row > 4) and (col < 2 or col > 4):
                    button.setEnabled(False)
                    button.setStyleSheet("background-color: gray;")
                    self.state[row][col] = -1
                else:
                    button.setStyleSheet("background-color: blue;")
                    button.clicked.connect(self.click_cell)
                if (row == 3 and col == 3):
                    button.setStyleSheet("background-color: white;")
                    self.state[row][col] = 0

                self.board.addWidget(button, row, col)
    
    def click_cell(self):
        button = self.sender()
        row, col = button.row, button.col 

        if row < 0 or col < 0 or row >= len(self.state) or col >= len(self.state[0]):
            return

        if self.selecionada is None:
            if self.state[row][col] == 1:
                self.selecionada = (row, col)
                button.setStyleSheet("background-color: green;")
        else:
            row_piece, col_piece = self.selecionada
            if self.check_move(row_piece, col_piece, row, col):
                self.move_piece(row_piece, col_piece, row, col)
            else:
                button.setStyleSheet("background-color: red;")
            
            self.selecionada = None
            self.update()

    def check_move(self, row_piece, col_piece, row, col):
        if abs(row - row_piece) == 2 and col == col_piece:
            move_x, move_y = (row + row_piece) // 2, col
        elif abs(col - col_piece) == 2 and row == row_piece:
            move_x, move_y = row, (col + col_piece) // 2
        else:  
            return False

        return self.state[row][col] == 0 and self.state[move_x][move_y] == 1
        
    def move_piece(self, row_piece, col_piece, row, col):
        move_x, move_y = (row + row_piece) // 2, (col + col_piece) // 2

        self.state[row_piece][col_piece] = 0
        self.state[move_x][move_y] = 0
        self.state[row][col] = 1
        self.update()

    def update(self):
        for i in range(7):
            for j in range(7):
                button = self.board.itemAtPosition(i, j).widget()
                if self.state[i][j] == 1:
                    button.setStyleSheet("background-color: blue;")
                elif self.state[i][j] == 0:
                    button.setStyleSheet("background-color: white;")

    def regras(self):
        self.label.setText("How to Play")

        text = """
        1. Choose a piece.
        2. Jump the chosen piece over another piece, either horizontally or vertically, until it reaches an empty space.
        3. Repeat the moves until only one piece remains. 
        4. The game ends when no more moves are possible or when only one piece is left.
        """

        dir = os.path.dirname(__file__)
        path = os.path.join(dir, 'assets/game_images/solitaire.jpg')
        picture = QPixmap(path)

        if self.setRules.layout().count() == 0:
            picture = picture.scaled(200, 200)
            image = QLabel(self)
            image.setPixmap(picture)
            image.setAlignment(Qt.AlignCenter)
            s = QLabel(text, self)
            s.setWordWrap(True)    
            self.setRules.layout().addWidget(image)
            self.setRules.layout().addWidget(s)
        
        self.setRules.setVisible(True)
        self.board_widget.setVisible(False)

    def jogar(self):
        self.label.setText("Start!")
        self.board_widget.setVisible(True)
        self.setRules .setVisible(False) 

    def sair(self):
        self.close()

app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())