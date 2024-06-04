import numpy as np
import pandas as pd
from sko.GA import GA
import random

# 消除随机分配岛屿时，三艘船可能会重复的岛屿
def no_repeat_random(down, up, k, n, rm):
    """

    :param down: 下限
    :param up: 上限
    :param k: 抽取的个数
    :param n: 目标个数
    :param rm: 移除的元素
    :return:
    """

    random_list = random.sample(range(down, up), k)
    for i in rm:
        for j in random_list:
            if i == j:
                random_list.remove(j)
    while len(random_list) > n:
        random_list.remove(random_list[0])
    return random_list

# 将20个岛屿随机分给3条船
def random_island():
    boat_A = random.sample(range(1, 21), 6)
    boat_B = no_repeat_random(1, 21, 12, 7, boat_A)
    boat_C = no_repeat_random(1, 21, 20, 7, boat_A + boat_B)

    # for i in range(boat_A):
    #     boat_A[i] = 'D' + str(boat_A[i])
    # for i in range(boat_B):
    #     boat_B[i] = 'D' + str(boat_B[i])
    #     boat_C[i] = 'D' + str(boat_C[i])

    return boat_A, boat_B, boat_C

# 计算两点之间的距离
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 计算航行时间
def travel_time(distance, load, empty_speed, speed_loss_per_ton):
    speed = empty_speed - speed_loss_per_ton * load
    return distance / speed

def total_time(w0, total_travel_time):
    return 5 * w0 / 12 + total_travel_time

# 计算每艘船的航行时间
def boat_time(w0, boat, data_x, data_y, data_nd, data_name):
    w = w0
    current_x, current_y = 0, 0
    data_nd_temp = []
    for i in boat:
        data_nd_temp.append(data_nd[i])
    # 初始化时间的列表
    t_ls = []

    # d0 = []
    # for i in boat:
    #     d0.append(distance(data_x[i], data_y[i], 0, 0))

    while sum(data_nd_temp) > 0:
        # 求当前船的坐标与各岛屿之间的距离
        d_ls = []
        route_ls = ['D0']
        for j in boat:
            d_temp = distance(current_x, current_y, data_x[j], data_y[j])
            if d_temp > 0 and data_nd[j] > 0:
                d_ls.append([j, d_temp])    # 二元矩阵，第一个元素为岛屿编号，第二个元素为距离

        if not d_ls:
            print(data_nd_temp)
            break
        # 取离当前船最近的岛屿
        d = min(d_ls)

        t_ls.append(travel_time(d[1], w, 26, 0.12))

        w -= data_nd[d[0]]
        route_ls.append(data_name[d[0]])
        if w >= 0:
            # for i in range(len(data_nd_temp)):
            #     for j in range(len(data_nd)):
            #         if data_nd_temp[i] == data_nd[j]:
            #             data_nd_temp[i] = 0
            data_nd[d[0]] = 0
            # 添加这一行更新 data_nd_temp
            data_nd_temp = [data_nd[i] for i in boat if data_nd[i] >= 0]
            current_x, current_y = data_x[d[0]], data_y[d[0]]
        if w < 0:
            t_ls.append(travel_time(np.sqrt(data_x[d[0]] ** 2 + data_y[d[0]] ** 2), 0, 26, 0.12))
            # for i in range(len(data_nd_temp)):
            #     for j in range(len(data_nd)):
            #         if data_nd_temp[i] == data_nd[j]:
            #             data_nd_temp[i] = abs(w)
            data_nd[d[0]] = abs(w)
            # 添加这一行更新 data_nd_temp
            data_nd_temp = [data_nd[i] for i in boat if data_nd[i] >= 0]
            # print(1)
            current_x, current_y = 0, 0
            w = w0
            route_ls.append('D0')

    return sum(t_ls) + 5 * w0 / 12, route_ls


def func(x):
    w0_A, w0_B, w0_C = x

    dataFrame = pd.read_excel('附件1.xlsx').dropna()
    data_name = dataFrame['海岛编号'].tolist()
    data_x = dataFrame['x坐标'].tolist()
    data_y = dataFrame['y坐标'].tolist()
    data_nd = dataFrame['补给需求量'].tolist()

    boat_A, boat_B, boat_C = random_island()

    # 计算A船的航行时间
    t_A, route_A = boat_time(w0_A, boat_A, data_x, data_y, data_nd, data_name)

    # 计算B船的航行时间
    t_B, route_B = boat_time(w0_B, boat_B, data_x, data_y, data_nd, data_name)

    # 计算C船的航行时间
    t_C, route_C = boat_time(w0_C, boat_C, data_x, data_y, data_nd, data_name)

    print(f'A:{route_A}, B:{route_B}, C:{route_C}')
    # 计算总的航行时间
    return max(t_A, t_B, t_C)

if __name__ == '__main__':
    best_x_ls, best_y_ls = [], []
    # for _ in range(10):
    ga = GA(func=func, n_dim=3, size_pop=50, max_iter=100, prob_mut=0.001, lb=[0, 0, 0], ub=[50, 50, 50], precision=1e-7)
    best_x, best_y = ga.run()
    best_x_ls.append(list(best_x))
    best_y_ls.append(list(best_y))
    best_x = min(best_x_ls)
    best_y = min(best_y_ls)
    print('best_x:', best_x, '\n', 'best_y:', best_y)
