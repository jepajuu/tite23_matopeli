"# tite23_matopeli" 

Madon pituuden kasvatus pisteiden lisääntyessä

-------------------------------------------------------------------------------------------------------------------------------------

Lisää peliin aloitusruutu
	"Lisää koodiin metodi:
def init_screen(self):
        start_text = self.scene().addText(""Press any key to start"", QFont(""Arial"", 18))
        text_width = start_text.boundingRect().width()
        text_x = (self.width() - text_width) / 5
        start_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)

Poista konstruktorista def init(self): rivi:
        #self.start_game()
 ja lisää tilalle rivit:
# starting game by button
self.game_started = False
        self.init_screen()
Lisää metodiin def keyPressEvent(self, event) seuraavat rivit:
# starting game by button
        if not self.game_started:
            if key == event.key():
                self.game_started = True
                self.scene().clear()
                self.start_game()"

--------------------------------------------------------------------------------------------------------------------------------------
Lisää uuden pelin aloitus	
"Lisää uuden pelin aloitus painikkeella, kun on päädytty Game Over -tilanteeseen.
Teksti näytöllä seuraava:
Game Over
Press any key to start new game
Tässä voi olla tarpeen huomioida, että näppäimeksi ei huomioida nuolinäppäimiä."


--------------------------------------------------------------------------------------------------------------------------------------
Lisää pistelaskenta	
"Lisätään pistelasku matopeliin:

Metodiin start_game() lisätään:
# for score calculation
        self.score = 0

Rivin if new_head == self.food: alle lisätään rivi:
        self.score += 1

Metodin print_game():  loppuun lisätään pisteiden piirto:
self.scene().addText(f""Score: {self.score}"", QFont(""Arial"", 12))"


--------------------------------------------------------------------------------------------------------------------------------------
Lisää Game Over -teksti
	"Lisää teksti Game Over tilanteeseen, jossa mato törmää itseensä tai pelia-alueen reunaan:

# Game over text
game_over_text = self.scene().addText(""Game Over"", QFont(""Arial"", 24))
text_width = game_over_text.boundingRect().width()
text_x = (self.width() - text_width) / 2
game_over_text.setPos(text_x, GRID_HEIGHT * CELL_SIZE / 2)"


--------------------------------------------------------------------------------------------------------------------------------------
Lisää mato	Madon lisäys pelialueelle, kun valittu start game


--------------------------------------------------------------------------------------------------------------------------------------
Lisää eri vaikeustasot matopeliin

"Lisää/muokkaa def start_game(self): metodiin seuraavat rivit:

# for levels
        self.level_limit = 5
        self.timer_delay = 300
        self.timer.start(self.timer_delay)

Lisää pisteiden kasvatuksen jälkeen saman if-lauseen sisälle seuraavat rivit:
# for levels
if self.score == self.level_limit:
self.level_limit += 5
self.timer_delay -= 50
self.timer.setInterval(self.timer_delay)"


--------------------------------------------------------------------------------------------------------------------------------------
Syötävien pallojen lisäys	"Uusi metodi:
 # add food
    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

Metodiin print_game piirron lisäys:
# print food
        fx, fy = self.food
        self.scene().addRect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.red))"


--------------------------------------------------------------------------------------------------------------------------------------
Ruuan syönti	"self.snake.pop() tilalle tarkistus ja uuden ruuan teko:

if new_head == self.food:
            self.food = self.spawn_food()
else:
            self.snake.pop()"


--------------------------------------------------------------------------------------------------------------------------------------
Pelialueen rajat	"update_game metodiin suuntien tarkistuksen jälkeen
# board limits
if new_head in self.snake or not (0 <= new_head[0] < GRID_WIDTH) or not (0 <= new_head[1] < GRID_HEIGHT):
     self.timer.stop()
     return"


--------------------------------------------------------------------------------------------------------------------------------------
