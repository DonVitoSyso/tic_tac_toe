def print_res(result):
#выводим результат в консоль
    print("   0 1 2")
    print("0 ", *result[0])
    print("1 ", *result[1])
    print("2 ", *result[2])

def check_step(result, op):
#проверка хода на выигрыш
    for i in range(3):
        if result[i][0] == result[i][1] == result[i][2] != '-' or \
                result[0][0] == result[1][1] == result[2][2] != '-' or \
                result[0][2] == result[1][1] == result[2][0] != '-':
            print("Выиграл ", op)
            return True
    return False


opponent = True
x, y = 0, 0
str_ = ''
field = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-'],
]

for i in range(10):
    if opponent:
        str_ = input("Ход противника 1 (х): ")
        field[int(str_[0])][int(str_[1])] = 'x'
        str_ = 'Противник 1 (х)!'
    else:
        str_ = input("Ход противника 2 (o): ")
        field[int(str_[0])][int(str_[1])] = 'o'
        str_ = 'Противник 2 (0)!'

    print_res(field)
    if check_step(field, str):
        break

    #чередуем ходы противников
    opponent = False if opponent else True
