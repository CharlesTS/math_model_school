import numpy as np
import random
import pandas as pd
from sko.GA import GA

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

def boat_track(boat, d, w0, data_x, data_y):
    t = 0
    w = []
    w_boat = 0
    temp = 0
    for i in range(len(boat)):
        w_boat += w0[i][1] + temp
        if w_boat > 50:
            temp = w_boat - 50
            w.append(50)
            w_boat = 0
        if i == len(boat) - 1 and sum(w) < sum([x[1] for x in w0]):
            w.append(w_boat)

    n = 0
    for i in range(len(boat)):
        current_x = data_x[boat[i]]
        current_y = data_y[boat[i]]
        if i == 0:
            t += d[i][1] / 26 - 0.12 * w[n]
            w[n] -= w0[i][1]

        elif i == len(boat) - 1:
            if w[n - 1] < 0:
                t += d[i - 1][1] / 26 - 0.12 * w[n]
                w[n] -= w[n - 1]
            t += d[i][1] / 26
            w[n] -= w0[i][1]

        else:
            if w[n - 1] < 0:
                t += d[i - 1][1] / 26 - 0.12 * w[n]
                w[n] -= w[n - 1]
                current_x = data_x[boat[i - 1]]
                current_y = data_y[boat[i - 1]]
            t += np.sqrt((current_x - data_x[boat[i + 1]]) ** 2 + (current_y - data_y[boat[i + 1]]) ** 2)
            w[n] -= w0[i][1]

        if w[n] <= 0:
            n += 1
            t += d[i][1] / 26

    t += 5 * sum([x[1] for x in w0]) / 12
    return t


def main():
    data = pd.read_excel('附件1.xlsx').dropna()
    data_x = data['x坐标'].tolist()
    data_y = data['y坐标'].tolist()
    data_w0 = data['补给需求量'].tolist()

    # 初始化岛屿距离的集合
    d_ls = []

    t_max = []
    for i in range(1000):

        # 随机分配岛屿
        boat_A, boat_B, boat_C = random_island()

        d_A, d_B, d_C = {}, {}, {}
        w0_A, w0_B, w0_C = {}, {}, {}

        for a in boat_A:
            d_A[a] = (np.sqrt(data_x[a] ** 2 + data_y[a] ** 2))
            w0_A[a] = data_w0[a]

        for b in boat_B:
            d_B[b] = (np.sqrt(data_x[b] ** 2 + data_y[b] ** 2))
            w0_B[b] = data_w0[b]

        for c in boat_C:
            d_C[c] = (np.sqrt(data_x[c] ** 2 + data_y[c] ** 2))
            w0_C[c] = data_w0[c]

        # d_A = sorted(d_A.items(), key=lambda kv: (kv[1], kv[0]))
        # d_B = sorted(d_B.items(), key=lambda kv: (kv[1], kv[0]))
        # d_C = sorted(d_C.items(), key=lambda kv: (kv[1], kv[0]))
        d_A, d_B, d_C = d_A.items(), d_B.items(), d_C.items()
        w0_A, w0_B, w0_C = w0_A.items(), w0_B.items(), w0_C.items()

        # A船情况
        t_A = 0
        w = []
        w_A = 0
        temp = 0
        for i in range(len(boat_A)):
            w_A += w0_A[i][1] + temp
            if w > 50:
                temp = w_A - 50
                w.append(50)
                w_A = 0
            if i == len(boat_A) - 1 and sum(w) < sum(w0_A):
                w.append(w_A)

        n = 0
        for i in range(len(boat_A)):
            # 目前的x,y坐标
            current_x = data_x[boat_A[i]]
            current_y = data_y[boat_A[i]]
            if i == 0:
                t_A += d_A[i][1] / 26 - 0.12 * w[n]
                w[n] -= w0_A[i][1]

            elif i == len(boat_A) - 1:
                if w[n - 1] < 0:
                    t_A += d_A[i - 1][1] / 26 - 0.12 * w[n]
                    w[n] -= w[n - 1]
                    # current_x = data_x[boat_A[i - 1]]
                    # current_y = data_y[boat_A[i - 1]]
                t_A += d_A[i][1] / 26
                w[n] -= w0_A[i][1]

            else:
                if w[n - 1] < 0:
                    t_A += d_A[i - 1][1] / 26 - 0.12 * w[n]
                    w[n] -= w[n - 1]
                    current_x = data_x[boat_A[i - 1]]
                    current_y = data_y[boat_A[i - 1]]
                t_A += np.sqrt((current_x - data_x[boat_A[i + 1]]) ** 2 + (current_y - data_y[boat_A[i + 1]]) ** 2)
                w[n] -= w0_A[i][1]

            # 如果载货量变为负数了:
            if w[n] <= 0:
                n += 1
                t_A += d_A[i][1] / 26   # 返航补充货物

        t_A += 5 * sum(w0_A) / 12
        print(t_A)

def main_1():
    data = pd.read_excel('附件1.xlsx').dropna()
    data_x = data['x坐标'].tolist()
    data_y = data['y坐标'].tolist()
    data_w0 = data['补给需求量'].tolist()

    t_max = []

    for i in range(1000):
        # if i == 0:
        #     boat_A_set, boat_B_set, boat_C_set = set(), set(), set()
        boat_A, boat_B, boat_C = random_island()

        # if set(boat_A) == boat_A_set:
        #     boat_A = random_island()
        #
        # if set(boat_B) == boat_B_set:
        #     boat_B = random_island()
        #
        # if set(boat_C) == boat_C_set:
        #     boat_C = random_island()
        #
        # boat_A_set, boat_B_set, boat_C_set = set(boat_A), set(boat_B), set(boat_C)

        d_A, d_B, d_C = {}, {}, {}
        w0_A, w0_B, w0_C = {}, {}, {}

        for a in boat_A:
            d_A[a] = np.sqrt(data_x[a] ** 2 + data_y[a] ** 2)
            w0_A[a] = data_w0[a]

        for b in boat_B:
            d_B[b] = np.sqrt(data_x[b] ** 2 + data_y[b] ** 2)
            w0_B[b] = data_w0[b]

        for c in boat_C:
            d_C[c] = np.sqrt(data_x[c] ** 2 + data_y[c] ** 2)
            w0_C[c] = data_w0[c]

        d_A, w0_A = list(d_A.items()), list(w0_A.items())
        d_B, w0_B = list(d_B.items()), list(w0_B.items())
        d_C, w0_C = list(d_C.items()), list(w0_C.items())

        # A船情况
        t_A = boat_track(boat_A, d_A, w0_A, data_x, data_y)
        # B船情况
        t_B = (boat_track(boat_B, d_B, w0_B, data_x, data_y))
        # C船情况
        t_C = (boat_track(boat_C, d_C, w0_C, data_x, data_y))

        t_max.append(max(t_A, t_B, t_C))

    print(min(t_max))


def fun(x):
    data = pd.read_excel('附件1.xlsx').dropna()
    data_x = data['x坐标'].tolist()
    data_y = data['y坐标'].tolist()
    data_w0 = data['补给需求量'].tolist()

    t_A, t_B, t_C = x
    boat_A, boat_B, boat_C = random_island(), random_island(), random_island()

    d_A, d_B, d_C = {}, {}, {}
    w0_A, w0_B, w0_C = {}, {}, {}

    for a in boat_A:
        d_A[a] = np.sqrt(data_x[a] ** 2 + data_y[a] ** 2)
        w0_A[a] = data_w0[a]

    for b in boat_B:
        d_B[b] = np.sqrt(data_x[b] ** 2 + data_y[b] ** 2)
        w0_B[b] = data_w0[b]

    for c in boat_C:
        d_C[c] = np.sqrt(data_x[c] ** 2 + data_y[c] ** 2)
        w0_C[c] = data_w0[c]

    boat_A, boat_B, boat_C = random_island()
    # A船情况
    t_A = boat_track(boat_A, d_A, w0_A, data_x, data_y)
    # B船情况
    t_B = (boat_track(boat_B, d_B, w0_B, data_x, data_y))
    # C船情况
    t_C = (boat_track(boat_C, d_C, w0_C, data_x, data_y))

    return max(t_A, t_B, t_C)

if __name__ == '__main__':
    ga = GA(func=fun, n_dim=3, size_pop=50, max_iter=800, prob_mut=0.001, lb=[0, 0, 0], ub=[1000, 1000, 1000], precision=1e-7)
    best_x, best_y = ga.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)