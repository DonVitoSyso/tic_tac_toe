import random

class BoardException(Exception):
    ...

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    ...

# класс написан полностью, точки
class Dot:
    def __init__(self, x=None, y=None, val='.'):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return True if self.x == other.x and self.y == other.y else False

    def get_Dot(self):
        return f'Dot - x:{self.x} y:{self.y}'

# класс написан полностью, карабль
class Ship():
    def __init__(self, ship_bow, length=None, orientation=''):
        self.length = length
        # нос коробля калсса Dot(x, y)
        self.ship_bow = ship_bow
        self.orientation = orientation
        self.lives = length

    def get_Ship(self):
        return f'Ship have length: {self.length} and his position ({self.ship.dot[0]}, {self.ship.dot[1]})'

    @property
    def dots(self):
        dots_ = []
        if self.orientation == "H":
            for h in range(self.length):
                dots_.append(Dot(self.ship_bow.x, self.ship_bow.y + h, '+'))
            # dots_.append(list(Dot(self.ship.x + h, self.ship.y, '+')) for h in range(0, self.length))
        elif self.orientation == "V":
            for v in range(self.length):
                dots_.append(Dot(self.ship_bow.x + v, self.ship_bow.y, '+'))
            # dots_ = Dot((self.ship.dot[0], self.ship.dot[1] + v, '+') for v in range(0, self.length))
        return dots_
    # проверка поподания выстрела в точки коробля
    def shooten(self, shot):
        return shot in self.dots

# класс написан полностью
class Board():
    def __init__(self, hid=False, size=6):
        self.board_ = [["o" for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.hid = hid
        self.size = size
        # колличество параженных короблей
        self.count = 0
        # количество занятых точек
        self.busy = []
    # начало игры обнуляем список busy
    def begin(self):
        self.busy = []

    def out(self, dot):
        return False if 0 <= dot.x < self.size and 0 <= dot.y < self.size else True
    # сделан полностью, и контур тоже
    def add_ship(self, ship):
        # # генераторы случайных расположений
        # ornt = random.choice("HV")
        # dot = Dot()
        # dot.x = random.randint(0, 5) if ornt == 'H' else random.randint(0, 5 - length)
        # dot.y = random.randint(0, 5 - length) if ornt == 'H' else random.randint(0, 5)
        # # генераторы случайных расположений
        # сохраняеv корабль на доску
        for i in ship.dots:
            if self.out(i) or i in self.busy:
                raise BoardWrongShipException()
        for i in ship.dots:
            self.board_[i.x][i.y] = "■"
            self.busy.append(i)
        self.ships.append(ship)
        self.contour(ship)
    # полностью скопирован из вэб + разобрался
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.board_[cur.x][cur.y] = "."
                    self.busy.append(cur)
    # мой метод
    def show(self):
        res = ""
        res += "    1  2  3  4  5  6"

        for i, j in enumerate(self.board_):
            res += f"\n {i+1}  " + "  ".join(j)
        # Разобраться надо!!!
        if self.hid:
            res = res.replace("■", "o")
        return res
    # скопирован из кода - всё понятно
    def shot(self, dot):

        if self.out(dot):
            raise BoardOutException()

        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if ship.shooten(dot):
                ship.lives -= 1
                self.board_[dot.x][dot.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.board_[dot.x][dot.y] = "."
        print("Мимо!")
        return False

class Player:
    def __init__(self, board_player1, board_player2):
        self.board_player1 = board_player1
        self.board_player2 = board_player2

    def ask(self):
        raise NotImplementedError()
    # скопирован из ВЭБинара - разобран
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.board_player2.shot(target)
                return repeat
            except BoardException as e:
                print(e)
# класс пользователь закончен - вводимые значения
class User(Player):
    def ask(self):
        while True:
            dot = input("Введите координаты: ").split()
            if len(dot) < 2:
                print("Введите 2 координаты")
                continue

            if not(dot[0].isdigit() and dot[1].isdigit()):
                print("Введите числа")
                continue

            return Dot(int(dot[0]) - 1, int(dot[1]) - 1)
# класс компьютера закончен - рандомные координаты
class AI(Player):
    def ask(self):
        d = Dot(random.randint(0, 5), random.randint(0, 5))
        print(f'Ход AI:({d.x + 1}, {d.y + 1})')
        return d
# класс Game закончен + скопирован + разобран
class Game:
    def random_board(self):
        ship_list = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        cont, i = 0, 0
        while True:
            cont += 1
            if i == len(ship_list):
                break
            if cont > 2000:
                # Переинициализация всего. Проблема зависания
                # переменно board при генерации свыше N-ой операции
                i, cont = 0, 0
                del board
                board = Board(size=self.size)
            # генератор случайных расположений
            ship = Ship(Dot(random.randint(0, self.size), random.randint(0, self.size)), ship_list[i],
                        random.choice("HV"))
            try:
                board.add_ship(ship)
                i += 1
                continue
            except BoardWrongShipException:
                pass
        board.begin()
        return board
    # скопирован из вэбинара + разобрался
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)
    # скопирован из вэбинара + разобрался
    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    # скопирован из вэбинара + разобрался
    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board_player1.show())
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board_player1.show())
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board_player1.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board_player1.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1
   # скопирован из вэбинара + разобрался
    def start(self):
        self.greet()
        self.loop()


# сама игра начинатся здесь
game = Game()
game.start()