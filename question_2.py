import numpy as np
from sko.GA import GA
import matplotlib.pyplot as plt
import pandas as pd
import random

data_route = []  # 初始化一个航程的列表

# 随机分配岛屿的需求量给三艘船
def random_Q(data_Q):
    Q_ls = []    # 初始化一个需求量分配的列表
    m, n, p, z = 0, 0, 0, 0
    for i in range(len(data_Q)):
        temp = random.randint(1, 4)
        if temp == 1:
            m = data_Q[i]
        elif temp == 2:
            n = data_Q[i]
        elif temp == 3:
            p = data_Q[i]
        else:
            z = data_Q[i]
        Q_ls.append([m, n, p, z])
        m, n, p, z = 0, 0, 0, 0
    return np.array(Q_ls)

# 计算两点之间的距离
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 计算航行时间
def travel_time(d, w, empty_speed, speed_loss_per_ton):
    speed = empty_speed - speed_loss_per_ton * w
    return d / speed

def boat_time(w0, Q_ls, data_x, data_y, data_name, empty_speed, speed_loss_per_ton, max_ton):
    w = w0  # 初始化初始载货量
    current_x, current_y = 0, 0     # 初始化当前的位置
    t_ls = []
    sum_Q = sum(Q_ls)
    route_ls = ['D0']

    while sum(Q_ls) > 0:
        t_list = []  # 初始化航程列表
        for i in range(len(Q_ls)):
            if Q_ls[i] > 0:
                d = distance(current_x, current_y, data_x[i], data_y[i])
                t = travel_time(d, w, empty_speed, speed_loss_per_ton)
                t_list.append([data_name[i], t, i])

        if not t_list:
            break

        min_time = min(t_list, key=lambda x: x[1])
        t_ls.append(min_time[1])
        num_temp = min_time[2]
        route_ls.append(min_time[0])
        Q = Q_ls[num_temp]

        w -= Q  # 更新当前载货量
        if w >= 0:
            Q_ls[num_temp] = 0  # 将已经访问过的岛屿的需求量置零
            current_x, current_y = data_x[num_temp], data_y[num_temp]  # 更新当前坐标
        else:
            Q_ls[num_temp] = abs(w)
            t_ls.append(travel_time(distance(current_x, current_y, 0, 0), 0, empty_speed, speed_loss_per_ton))
            current_x, current_y = 0, 0

            if sum(Q_ls) > max_ton:
                w = max_ton
            else:
                w = sum(Q_ls)
            route_ls.append('D0')

    return sum(t_ls) + 5 * sum_Q / 12, route_ls

def func():
    w0_A, w0_B, w0_C, w0_D = 50, 50, 50, 80

    dataFrame = pd.read_excel('附件1.xlsx').dropna()
    data_name = dataFrame['海岛编号'].tolist()
    data_x = dataFrame['x坐标'].tolist()
    data_y = dataFrame['y坐标'].tolist()
    data_Q = dataFrame['补给需求量'].tolist()

    Q_ls = random_Q(data_Q)

    Q_A = list(np.concatenate(Q_ls[:, 0:1]))
    Q_B = list(np.concatenate(Q_ls[:, 1:2]))
    Q_C = list(np.concatenate(Q_ls[:, 2:3]))
    Q_D = list(np.concatenate(Q_ls[:, 3:4]))

    for i in Q_A:
        num = 0
        if i > 0:
           num += 1
        if num <= 4:
            Q_ls = random_Q(data_Q)

            Q_A = list(np.concatenate(Q_ls[:, 0:1]))
            Q_B = list(np.concatenate(Q_ls[:, 1:2]))
            Q_C = list(np.concatenate(Q_ls[:, 2:3]))
            Q_D = list(np.concatenate(Q_ls[:, 3:4]))

    for i in Q_B:
        num = 0
        if i > 0:
           num += 1
        if num <= 4:
            Q_ls = random_Q(data_Q)

            Q_A = list(np.concatenate(Q_ls[:, 0:1]))
            Q_B = list(np.concatenate(Q_ls[:, 1:2]))
            Q_C = list(np.concatenate(Q_ls[:, 2:3]))
            Q_D = list(np.concatenate(Q_ls[:, 3:4]))

    for i in Q_C:
        num = 0
        if i > 0:
           num += 1
        if num <= 4:
            Q_ls = random_Q(data_Q)

            Q_A = list(np.concatenate(Q_ls[:, 0:1]))
            Q_B = list(np.concatenate(Q_ls[:, 1:2]))
            Q_C = list(np.concatenate(Q_ls[:, 2:3]))
            Q_D = list(np.concatenate(Q_ls[:, 3:4]))

    for i in Q_D:
        num = 0
        if i > 0:
           num += 1
        if num <= 4:
            Q_ls = random_Q(data_Q)

            Q_A = list(np.concatenate(Q_ls[:, 0:1]))
            Q_B = list(np.concatenate(Q_ls[:, 1:2]))
            Q_C = list(np.concatenate(Q_ls[:, 2:3]))
            Q_D = list(np.concatenate(Q_ls[:, 3:4]))

    t_A, route_A = boat_time(w0_A, Q_A, data_x, data_y, data_name, 26, 0.12, 50)
    t_B, route_B = boat_time(w0_B, Q_B, data_x, data_y, data_name, 26, 0.12, 50)
    t_C, route_C = boat_time(w0_C, Q_C, data_x, data_y, data_name, 26, 0.12, 50)
    t_D, route_D = boat_time(w0_D, Q_D, data_x, data_y, data_name, 30, 0.1, 80)

    data_route.append([max(t_A, t_B, t_C, t_D), f'A:{route_A}, B:{route_B}, C:{route_C}, D:{route_D}'])

    return max(t_A, t_B, t_C, t_D)

def main():
    t = []
    for _ in range(1000000):
        t.append(func())

    best_y = min(t)
    print(best_y)
    for index in data_route:
        if index[0] == best_y:
            print(index[1])

if __name__ == '__main__':
    main()