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

for column_index in range(len(a) - 1):

    max_index = max(range(len(a)), key=lambda i: a[i][column_index])

    if column_index != max_index:
        a[column_index], a[max_index] = a[max_index], a[column_index]
        f[column_index], f[max_index] = f[max_index], f[column_index]

    for row in range(column_index+1, len(a)):
        k = - (a[row][column_index] / a[column_index][column_index])
        a[row] = list(map(lambda cur, prv: cur + prv*k, a[row], a[column_index]))
        f[row] = list(map(lambda cur, prv: cur + prv*k, f[row], f[column_index]))

u = [0] * len(a)

for i in range(len(a) - 1, -1, -1):
    s = sum(a[i][j] * u[j] for j in range(i + 1, len(a)))
    u[i] = (f[i][0] - s) / a[i][i]

for i in range(len(u)):
    print(f"x{i} = {u[i]}")