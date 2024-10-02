import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# Vakiot
CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        
        self.start_game()
        self.score = 0

    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # Päivitetään suunta vain jos se ei ole vastakkainen valitulle suunnalle
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            new_head = (head_x - 1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x + 1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y - 1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y + 1)

        # Game over text
        if (new_head in self.snake or new_head[0] >= GRID_WIDTH or new_head[0] <= -1 or new_head[1] >= GRID_HEIGHT or new_head[1] <= -1):
            self.dead = True

        # Tarkistetaan, syökö mato pallon
        if new_head == self.food:
            self.score += 1
            self.snake.insert(0, new_head)
            self.place_food()  # Aseta uusi pallo
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        self.print_game()

    def print_game(self):
        self.scene().clear()
        

        if (self.dead):
            self.die()
            self.timer.stop()
       

        # Piirrä mato
        for segment in self.snake:
            x, y = segment
            self.scene().addRect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.black))
        
        # Piirrä pallo
        food_x, food_y = self.food
        self.scene().addEllipse(food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.red), QBrush(Qt.red))
        self.scene().addText(f"Score: {self.score}", QFont("Arial", 12)).setPos(10, 10)

    def die(self):
        self.scene().clear()
        game_over_text = self.scene().addText("Game Over", QFont("Arial", 24))
        text_width = game_over_text.boundingRect().width()
        text_x = (self.width() - text_width) / 2
        game_over_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)
        self.timer.stop()

    def place_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.food = (x, y)
            if self.food not in self.snake:  # Varmista, että pallo ei tule maton päälle
                break

    def start_game(self):
        self.dead = False
        self.direction = Qt.Key_Right
        self.snake = [(5, 5), (5, 6), (5, 7)]
        self.place_food()  # Aseta ensimmäinen pallo
        self.timer.start(300)

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
