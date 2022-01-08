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
                result[0][i] == result[1][i] == result[2][i] != '-' or \
                result[0][2-i] == result[1][2-i] == result[2][2-i] != '-':
            print("Выиграл ", op)
            return True
    return False


def input_step(fld, str_, value):

    #запись хода в таблицу
    while True:
        if (str_[0].isdigit() and str_[1].isdigit()) and \
                0 <= int(str_[0]) <= 2 and 0 <= int(str_[1]) <= 2 \
                and fld[int(str_[0])][int(str_[1])] == '-':
            fld[int(str_[0])][int(str_[1])] = value
            return fld[int(str_[0])][int(str_[1])]
        else:
            str_ = input(f'Не верная координата. Повторите ход: ')


str_ = ''
field = [
    ['-', '-', '-'],
    ['-', '-', '-'],
    ['-', '-', '-'],
]

for i in range(9):
    print_res(field)
    if i%2:
        str_ = input("Ход противника 2 (o): ")
        input_step(field, str_, 'o')
        str_ = 'Противник 2 (o)!'
    else:
        str_ = input("Ход противника 1 (x): ")
        input_step(field, str_, 'x')
        str_ = 'Противник 1 (x)!'

    if check_step(field, str_):
        break

print("Игра окончена!")