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
                dots_.append(Dot(self.ship_bow.x + h, self.ship_bow.y, '+'))
            # dots_.append(list(Dot(self.ship.x + h, self.ship.y, '+')) for h in range(0, self.length))
        elif self.orientation == "V":
            for v in range(self.length):
                dots_.append(Dot(self.ship_bow.x, self.ship_bow.y + v, '+'))
            # dots_ = Dot((self.ship.dot[0], self.ship.dot[1] + v, '+') for v in range(0, self.length))
        return dots_
    # проверка поподания выстрела в точки коробля
    def shooten(self, shot):
        return shot in self.dots

# класс написан полностью, БЕЗ ОПИСАНИЯ ВЫСТРЕЛОВ
class Board():
    def __init__(self, hid=False, size=6):
        self.board_ = [["o" for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.hid = hid
        self.size = size
        self.count = 0
        # этот тип непонятен
        self.busy = []

    def begin(self):
        self.busy = []

    def out(self, dot):
        return False if 0 <= dot.x < 6 and 0 <= dot.y < 6 else True
    # зделан полностью, и контур тоже
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
    # полностью скопирован из вэб
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

    def show(self):
        # print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
        # print("---+---+---+---+---+---+---+")
        # for i in range(0, 6):
        #     print(f' {i+1} ', end='|')
        #     for j in range(0, 6):
        #         print(f' {self.board_[j].dot[0]} ', end='|')
        #     print('\n---+---+---+---+---+---+---+')
        print("    1  2  3  4  5  6 ")
        for i in range(0, 6):
            print(f' {i + 1} ', end='')
            for j in range(0, 6):
                print(f' {self.board_[i][j].val} ', end='')
            print()

    def shot(self):
        ...

class Player(Board):
    def __init__(self, board_player1, board_player2):
        self.board_player1 = board_player1
        self.board_player2 = board_player2

    def ask(self):
        raise NotImplementedError()

    def move(self):
        ...
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
        print(f'Ход AI:({d.x}, {d.y})')
        return d

# класс Game осталось завести loop
class Game(Player):
    def random_board(self):
        ship_list = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        cont, i = 0, 0
        while True:
            cont += 1
            if i == len(ship_list):
                break
            if cont > 2000:
                i = 0
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


    def __init__(self, size=6):
        board1 = random_board()
        board2 = random_board()
        self.player1 = User(board1, board2)
        self.player2 = AI(board2, board1)
        # параметры для всех классов объявлены size, hid
        self.size = size
        self.hid = True

    # greet закончен подсказка на игру
    def greet():
        print("-------------------")
        print("  Приветсвуем вас  ")
        print(" формат ввода: x y ")

    def loop(self):
        ...
    # метод start описан
    def start(self):
        self.greet()
        self.loop()


board_test = [[] for _ in range(0, 6)]
print(board_test)
print(len(board_test))
dot_ = Dot(2, 3)
ship = Ship(3, dot_, "V")

#print(ship.get_Ship(), ship.get_Dot())
#print(*ship.dots())
board = Board(ship, True, 1)
print(board.ships.ship.get_Dot())
# print(board.board_)
# board.show()
board.show()
ship_list = [1, 2, 2, 1, 1, 1, 1]
for s in ship_list:
    print(board.add_ship(s))
board.show()

list_1 = [Dot(y, x) for x, y in zip(range(4), range(4))]
print(list_1)

list_2 = [Dot(0,0), Dot(1,1), Dot(1,2)]

# print(list(filter(lambda i: i in list_2, list_2)))
if all(x in list_1 for x in list_2):
    print("Проверка прошла!")
else:
    print(False)


# сама игра начинатся здесь
game = Game
game.greet()
