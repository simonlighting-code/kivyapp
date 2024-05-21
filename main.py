from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class KirakoJatekApp(App):  # Az alkalmazás fő osztálya, amely örökli az App osztályt
    def build(self):  # Az alkalmazás felépítéséért felelős metódus
        game_board = GridLayout(cols=4, rows=4)  # Létrehoz egy 4x4-es GridLayoutot a játéktáblának
        self.buttons = []  # Lista a gombok tárolására
        self.shuffle_board()  # A játéktábla keverését végző metódus hívása
        self.draw_board(game_board)  # A játéktábla kirajzolását végző metódus hívása
        return game_board  # Visszaadja a GridLayoutot, hogy megjelenjen az alkalmazásban

    def shuffle_board(self):  # A játéktábla keveréséért felelős metódus
        numbers = list(range(1, 16)) + [""]  # Létrehoz egy listát az 1-től 15-ig terjedő számokkal és egy üres hellyel
        
        for i in range(len(numbers) - 1, 0, -1):  # Fisher-Yates keverési algoritmus
            j = i % (i + 1)
            numbers[i], numbers[j] = numbers[j], numbers[i]

        self.board = [numbers[i:i + 4] for i in range(0, 16, 4)]  # A kevert listát 4x4-es táblába rendezi

        for row in range(4):  # Az üres hely pozíciójának meghatározása
            for col in range(4):
                if self.board[row][col] == "":
                    self.empty_pos = (row, col)  # Az üres hely pozícióját tárolja
                    return

    def draw_board(self, game_board):  # A játéktábla kirajzolását végző metódus
        for row in range(4):
            for col in range(4):
                if (row, col) == self.empty_pos:
                    btn = Button(text="", on_press=self.move)  # Létrehoz egy gombot az üres hely számára
                else:
                    btn = Button(text=str(self.board[row][col]), on_press=self.move)  # Létrehoz egy gombot a megfelelő számmal
                game_board.add_widget(btn)  # Hozzáadja a gombot a játéktáblához
                self.buttons.append(btn)  # A gombot hozzáadja a gombok listájához

    def move(self, button):  # A gomb megnyomására végrehajtandó metódus
        index = self.buttons.index(button)  # Meghatározza a megnyomott gomb indexét
        row, col = index // 4, index % 4  # Meghatározza a gomb sor- és oszlopszámát
        if (row, col) in self.get_neighbors(self.empty_pos):  # Ellenőrzi, hogy a gomb az üres hely szomszédja-e
            self.swap(row, col)  # Ha igen, cseréli a gomb és az üres hely pozícióját
            self.update_buttons()  # Frissíti a gombok szövegét

    def get_neighbors(self, position):  # Visszaadja az adott pozíció szomszédait
        row, col = position
        neighbors = []
        for r, c in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:  # Az adott pozíció lehetséges szomszédai
            if 0 <= r < 4 and 0 <= c < 4:  # Csak a játéktáblán belüli pozíciókat veszi figyelembe
                neighbors.append((r, c))
        return neighbors

    def swap(self, row, col):  # A gomb és az üres hely cseréjét végző metódus
        current_value = self.board[row][col]  # A gomb jelenlegi értéke
        self.board[self.empty_pos[0]][self.empty_pos[1]] = current_value  # Az üres hely értékének beállítása a gomb értékére
        self.board[row][col] = ""  # A gomb helyére üres értéket tesz
        self.empty_pos = (row, col)  # Az üres hely új pozíciójának beállítása

    def update_buttons(self):  # A gombok szövegének frissítését végző metódus
        for row in range(4):
            for col in range(4):
                index = row * 4 + col  # Az index kiszámítása
                if (row, col) == self.empty_pos:
                    self.buttons[index].text = ""  # Ha az üres hely, akkor a szöveg üres
                else:
                    self.buttons[index].text = str(self.board[row][col])  # Egyébként a gomb szövege a tábla értéke

KirakoJatekApp().run()  # Az alkalmazás futtatása