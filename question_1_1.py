import numpy as np
import pandas as pd
from sko.GA import GA
import random

data_route = []

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
    route_ls = ['D0']
    current_x, current_y = 0, 0
    t_ls = []
    # sum_w0 = sum(data_nd[i] for i in boat)

    while sum(data_nd[i] for i in boat) > 0:  # 使用索引直接获取需要的部分
        # 求当前船的坐标与各岛屿之间的距离
        d_ls = []
        for j in boat:
            d_temp = distance(current_x, current_y, data_x[j], data_y[j])
            if d_temp > 0 and data_nd[j] > 0:
                d_ls.append([j, d_temp])    # 二元矩阵，第一个元素为岛屿编号，第二个元素为距离

        if not d_ls:
            break
        # 取离当前船最近的岛屿
        d = min(d_ls)

        t_ls.append(travel_time(d[1], w, 26, 0.12))

        w -= data_nd[d[0]]
        route_ls.append(data_name[d[0]])
        if w >= 0:
            # 将已经访问过的岛屿的需求量置为0
            data_nd[d[0]] = 0
            current_x, current_y = data_x[d[0]], data_y[d[0]]
        else:
            # 如果装载需求量超过了船的容量，重新回到原点
            t_ls.append(travel_time(np.sqrt(data_x[d[0]] ** 2 + data_y[d[0]] ** 2), 0, 26, 0.12))
            data_nd[d[0]] = abs(w)
            if sum(data_nd[i] for i in boat) <= 50:
                w = sum(data_nd[i] for i in boat)
            else:
                w = w0
            current_x, current_y = 0, 0
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

    data_route.append([max(t_A, t_B, t_C), f'A:{route_A}, B:{route_B}, C:{route_C}'])
    # 计算总的航行时间
    return max(t_A, t_B, t_C)

if __name__ == '__main__':
    ga = GA(func=func, n_dim=3, size_pop=50, max_iter=100, prob_mut=0.001, lb=[0, 0, 0], ub=[50, 50, 50], precision=1e-7)
    best_x, best_y = ga.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)
    for index in data_route:
        for i in range(len(index)):
            if i == 0:
                if index[0] == best_y:
                    print(index[1])