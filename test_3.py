import numpy as np
from sko.GA import GA
import matplotlib.pyplot as plt
import pandas as pd
import random

data_route = []  # 初始化一个航程的列表

# 随机分配岛屿的需求量给三艘船
def random_Q(data_Q):
    Q_ls = []    # 初始化一个需求量分配的列表
    m, n, p = 0, 0, 0   # 初始化三个船的需求量
    
    for i in data_Q:
        m = round(random.uniform(0, i), 1)
        if m < i:
            n = round(random.uniform(0, i - m), 1)
            if n < i - m:
                p = i - m - n

        Q_ls.append([m, n, p])

    return np.array(Q_ls)

# 计算两点之间的距离
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 计算航行时间
def travel_time(d, w, empty_speed, speed_loss_per_ton):
    speed = empty_speed - speed_loss_per_ton * w
    return d / speed

def boat_time(w0, Q_ls, data_x, data_y, data_name, empty_speed, speed_loss_per_ton, max_ton):
    """

    :param w0: 自变量（初始载货量）
    :param Q_ls: 需求量列表
    :param data_x: x坐标列表
    :param data_y: y坐标列表
    :param data_name: 岛屿编号列表
    :param empty_speed: 船只空载速度
    :param speed_loss_per_ton: 每吨货物速度损耗
    :param max_ton: 船只最大载货量
    :return:
    """
    w = w0  # 初始化初始载货量
    sum_Q = sum(Q_ls)
    current_x, current_y = 0, 0     # 初始化当前的位置
    t_ls = []
    route_ls = ['D0']

    # 如果当前船需要送的岛屿的需求总量大于0的话
    # 进入循环体
    while sum(Q_ls) > 0:
        t = []  # 初始化航程列表
        Q = 0   # 初始化当前船需要送的岛屿的求总量
        num_temp = 0    # 初始化传递岛屿编号的变量
        for i in range(len(Q_ls)):
            # 计算当前船到各个岛屿的距离
            d = distance(current_x, current_y, data_x[i], data_y[i])
            # 计算当前船到各个岛屿的航行时间
            t = travel_time(d, w, empty_speed, speed_loss_per_ton)
            # 计算当前船到各个岛屿的航行时间
            t.append([data_name[i], t, i])

        # 找到时间最短的两个岛屿
        min_time = min(t, key=lambda x:x[1])
        t_ls.append(min_time)

        # 将当前船送到的岛屿的编号添加到航程列表中
        for i in range(len(t)):
            if t[i][1] == min_time:
                num_temp = t[i][2]
                route_ls.append(t[i][0])
                Q = Q_ls[num_temp]

        w -= Q  # 更新当前载货量

        # 如果当前载货量大于0
        if w >= 0:
            Q_ls[num_temp] = 0  # 将已经访问过的岛屿的需求量置零
            current_x, current_y = data_x[num_temp], data_y[num_temp]  # 更新当前坐标
        else:
            Q_ls[num_temp] = abs(w)
            # 如果当前载货量小于0
            # 将当前载货量置零，并将当前船的坐标重置为初始位置
            t_ls.append(travel_time(distance(current_x, current_y, 0, 0), 0, empty_speed, speed_loss_per_ton))
            current_x, current_y = 0, 0

            if sum(Q_ls) > max_ton:
                w = w0
            else:
                w = sum(Q_ls)
            route_ls.append('D0')

    return sum(t_ls) + 5 * sum_Q / 12, route_ls

def func(x):
    w0_A, w0_B, w0_C = x

    dataFrame = pd.read_excel('附件1.xlsx').dropna()
    data_name = dataFrame['海岛编号'].tolist()
    data_x = dataFrame['x坐标'].tolist()
    data_y = dataFrame['y坐标'].tolist()
    data_Q = dataFrame['补给需求量'].tolist()

    Q_ls = random_Q(data_Q)

    Q_A = list(np.concatenate(Q_ls[0:, 0:1]))
    Q_B = list(np.concatenate(Q_ls[0:, 1:2]))
    Q_C = list(np.concatenate(Q_ls[0:, 2:3]))

    t_A, route_A = boat_time(w0_A, Q_A, data_x, data_y, data_name, 26, 0.12, 50)
    t_B, route_B = boat_time(w0_B, Q_B, data_x, data_y, data_name, 26, 0.12, 50)
    t_C, route_C = boat_time(w0_C, Q_C, data_x, data_y, data_name, 26, 0.12, 50)

    data_route.append([max(t_A, t_B, t_C), f'A:{route_A}, B:{route_B}, C:{route_C}'])

    # 计算总的航行时间
    return max(t_A, t_B, t_C)

def main():
    ga = GA(func=func, n_dim=3, size_pop=50, max_iter=100, prob_mut=0.001, lb=[0, 0, 0], ub=[50, 50, 50],precision=1e-7)
    best_x, best_y = ga.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)
    for index in data_route:
        for i in range(len(index)):
            if i == 0:
                if index[0] == best_y:
                    print(index[1])

if __name__ == '__main__':
    main()