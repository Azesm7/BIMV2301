a = [
    [4.503, 0.219, 0.527, 0.396],
    [0.259, 5.121, 0.423, 0.206],
    [0.413, 0.531, 4.317, 0.264],
    [0.327, 0.412, 0.203, 4.851]
]

f = [
    [0.533],
    [0.358],
    [0.565],
    [0.436]
]

e = 0.01

u = [
    [0],
    [0],
    [0],
    [0]
]

def is_convergent(): 

    for i in range(len(a)):
        sum_a = sum(list(map(lambda x: abs(x[1]), filter(lambda x: x[0] != i, enumerate(a[i])))))
        if sum_a > a[i][i]:
            return False
    return True

def replace_lines():

    for column_index in range(len(a) - 1):

        max_index = max(range(len(a)), key=lambda i: a[i][column_index])

        if column_index != max_index:
            a[column_index], a[max_index] = a[max_index], a[column_index]
            f[column_index], f[max_index] = f[max_index], f[column_index]

def solve():

    for iteration in range(1000): 

        for i in range(len(u)):
            cleared_a = list(map(lambda x: x[1], filter(lambda x: x[0] != i, enumerate(a[i]))))
            cleared_u = list(map(lambda x: x[1], filter(lambda x: x[0] != i, enumerate(map(lambda x: x[iteration], u)))))
            sum_axu = sum(list(map(lambda x, y: x * y, cleared_a, cleared_u)))
            x = (f[i][0] - sum_axu) / a[i][i]
            u[i].append(x)

        current_u = list(map(lambda x: x[iteration + 1], u))
        past_u = list(map(lambda x: x[iteration], u))
        max_delta = max(list(map(lambda x, y: abs(x - y), past_u, current_u)))

        if max_delta <= e:
            print("Приближенное решение найдено:\n")
            for i in range(len(current_u)):
                print(f"x{i} = {current_u[i]}")
            print(f"\nТочность = {max_delta} < e={e}, количество итераций: {iteration+1}")
            return True
        
if is_convergent():
    if solve() == None:
        print("Количество итераций иcчерпано, пробую переставить строки...")
        replace_lines()
        if solve() == None:
            print("Количество итераций иcчерпано, решение не найдено.")
else:
    print("Матрица не удовлетворяет условию сходимости")
