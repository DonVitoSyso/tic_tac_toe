def print_res(result):
#выводим результат в консоль
    print("   0 1 2")
    for i in range(3):
        print(f"{i} ", *result[i])

def check_step(result, op):
#проверка хода на выигрыш
    for i in range(3):
        if result[i][0] == result[i][1] == result[i][2] != '-' or \
                result[0][i] == result[1][i] == result[2][i] != '-' or \
                result[0][0] == result[1][1] == result[2][2] != '-' or \
                result[0][2] == result[1][1] == result[2][0] != '-':
            print("Выиграл ", op)
            return True
    return False

def input_step(fld, str_, value):

    #запись хода в таблицу
    while True:
        if 0 <= int(str_[0]) <= 2 or 0 <= int(str_[1]) <= 2 \
                and fld[int(str_[0])][int(str_[1])] == '-':
            fld[int(str_[0])][int(str_[1])] = value
            return fld[int(str_[0])][int(str_[1])]




opponent = True
x, y = 0, 0
str_ = ''
field = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-'],
]

while True:
    print_res(field)
    if opponent:
        str_ = input("Ход противника 1 (х): ")
        input_step(field, str_, 'x')
        #field[int(str_[0])][int(str_[1])] = 'x'
        str_ = 'Противник 1 (х)!'
    else:
        str_ = input("Ход противника 2 (o): ")
        field[int(str_[0])][int(str_[1])] = 'o'
        str_ = 'Противник 2 (o)!'

    if check_step(field, str_):
        break

    #чередуем ходы противников
    opponent = False if opponent else True
