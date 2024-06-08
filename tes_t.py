import numpy as np
from scipy import spatial
from sko.GA import GA_TSP
import matplotlib.pyplot as plt
import pandas as pd
import random

data_route = []  # 初始化一个航程的列表

dataFrame = pd.read_excel('附件1.xlsx').dropna()
data_name = dataFrame['海岛编号'].tolist()
data_x = dataFrame['x坐标'].tolist()
data_y = dataFrame['y坐标'].tolist()
data_Q = dataFrame['补给需求量'].tolist()

# 随机分配岛屿的需求量给三艘船
def random_Q(data_Q):
    Q_ls = []    # 初始化一个需求量分配的列表
    m, n, p = 0, 0, 0
    for i in range(len(data_Q)):
        temp = random.randint(1, 3)
        if temp == 1:
            m = data_Q[i]
        elif temp == 2:
            n = data_Q[i]
        else:
            p = data_Q[i]
        Q_ls.append([m, n, p])
        m, n, p = 0, 0, 0
    return np.array(Q_ls)

# 计算两点之间的距离
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 计算航行时间
def travel_time(d, w, empty_speed, speed_loss_per_ton):
    speed = empty_speed - speed_loss_per_ton * w
    return d / speed

# 计算航程中每个航程的坐标
def point_coord(data_x, data_y, Q_ls):
    points_coordinate = []
    num_points = 0
    for i in range(len(Q_ls)):
        if Q_ls[i] > 0:
            points_coordinate = np.array([[data_x[i], data_y[i]]])
            num_points += 1


    return points_coordinate, num_points

# 计算航程的总距离
def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    points_coordinate, num = point_coord(data_x, data_y, Q_A)
    distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

def best_route():
    points_coordinate, num_points = point_coord(data_x, data_y, Q_A)
    ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
    best_points, best_distance = ga_tsp.run()
    return best_points, best_distance, ga_tsp.generation_best_Y

# 计算总航程时间
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
    w0_A, w0_B, w0_C = 50, 50, 50

    # Q_ls = random_Q(data_Q)
    #
    # Q_A = list(np.concatenate(Q_ls[:, 0:1]))
    # Q_B = list(np.concatenate(Q_ls[:, 1:2]))
    # Q_C = list(np.concatenate(Q_ls[:, 2:3]))

    t_A, route_A = boat_time(w0_A, Q_A, data_x, data_y, data_name, 26, 0.12, 50)
    t_B, route_B = boat_time(w0_B, Q_B, data_x, data_y, data_name, 26, 0.12, 50)
    t_C, route_C = boat_time(w0_C, Q_C, data_x, data_y, data_name, 26, 0.12, 50)

    data_route.append([max(t_A, t_B, t_C), f'A:{route_A}, B:{route_B}, C:{route_C}'])

    return max(t_A, t_B, t_C)

Q_ls = random_Q(data_Q)

Q_A = list(np.concatenate(Q_ls[:, 0:1]))
Q_B = list(np.concatenate(Q_ls[:, 1:2]))
Q_C = list(np.concatenate(Q_ls[:, 2:3]))

def main():
    t = []
    for _ in range(10000):
        t.append(func())

    best_y = min(t)
    print(best_y)
    for index in data_route:
        if index[0] == best_y:
            print(index[1])

if __name__ == '__main__':
    main()

    # best_points, best_distance, generation_best_Y = best_route()
    # print(best_points)
    # print(best_distance)
