import numpy as np
import pandas as pd
from scipy import spatial
from sko.GA import GA_TSP
import matplotlib.pyplot as plt

route_ls = []

# def no_repeat_island():
#
# # 将岛屿随机分配给三艘船
# def random_island():
#     # 初始化列表
#     boat_A, boat_B, boat_C = [], [], []
#     # 随机给A船的岛屿数量
#     n = np.random.randint(1,21)
#     boat_A = np.random.sample(range(1, 21), n)
#     if n < 20:
#         # 随机给B船的岛屿数量
#         m = np.random.randint(1, 21-n)
#         boat_B = np.random.sample(range(1, 21), 20-n)
#         if m < 20-n:
#             boat_C = np.random.sample(range(1, 21), 20-n-m)

data = pd.read_excel('附件1.xlsx').dropna()
data_x = data['x坐标'].tolist()
data_y = data['y坐标'].tolist()

num_points = 21
points_coordinate = np.array([[data_x[i], data_y[i]] for i in range(len(data_x))])
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])

ga_tsp = GA_TSP(func=cal_total_distance, n_dim=num_points, size_pop=50, max_iter=500, prob_mut=1)
best_points, best_distance = ga_tsp.run()

fig, ax = plt.subplots(1, 2)
best_points_ = np.concatenate([best_points, [best_points[0]]])
best_points_coordinate = points_coordinate[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
ax[1].plot(ga_tsp.generation_best_Y)
plt.show()

# for i in best_points:
#     if i == 0:

print(best_points)
