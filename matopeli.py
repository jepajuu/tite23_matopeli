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
        
        self.game_started = False
        self.init_screen()
        self.score = 0

    def keyPressEvent(self, event):
        key = event.key()

        # Aloita peli, jos se ei ole vielä alkanut
        if not self.game_started:
            if key not in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                self.game_started = True
                self.scene().clear()
                self.start_game()
            return

        # Jos peli on ohi, aloita uusi peli
        if self.dead:
            if key not in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                self.restart_game()
            return

        # Päivitetään suunta
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
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
        if (new_head in self.snake or new_head[0] >= GRID_WIDTH or new_head[0] < 0 or new_head[1] >= GRID_HEIGHT or new_head[1] < 0):
            self.dead = True

        # Tarkistetaan, syökö mato pallon
        if new_head == self.food:
            self.score += 1
            self.snake.insert(0, new_head)
            self.place_food()
            if self.score == self.level_limit:  # Jos pisteet kasvaneet 5p nopeus kasvaa
                self.level_limit += 5
                self.timer_delay -= 50
                self.timer.setInterval(self.timer_delay)
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

        self.print_game()

    def print_game(self):
        self.scene().clear()

        if self.dead:
            self.die()
            return

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
        
        restart_text = self.scene().addText("Press any key to start new game", QFont("Arial", 18))
        restart_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2 + 30)

        self.timer.stop()

    def init_screen(self):
        start_text = self.scene().addText("Press any key to start", QFont("Arial", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

    def restart_game(self):
        self.game_started = True
        self.scene().clear()
        self.score = 0
        self.start_game()

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
        # for levels
        self.level_limit = 5  # määrä, joiden mukaan nopeus kasvaa
        self.timer_delay = 300  # aloitusnopeus
        self.timer.start(self.timer_delay)

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
