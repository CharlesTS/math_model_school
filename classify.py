import random
import numpy as np
import pandas as pd

data = pd.read_excel('附件1.xlsx')
data = data.dropna()

data_num = data['海岛编号']
data_x = data['x坐标']
data_y = data['y坐标']
data_need = data['补给需求量']

def random_Q(data_Q):
    Q_ls = []    # 初始化一个需求量分配的列表
    m, n, p = 0, 0, 0
    for i in range(len(data_Q)):
        if i == 6 or i == 7 or i == 9 or i == 10:
            m = round(random.uniform(0, i), 1)
            if m < i:
                n = round(random.uniform(0, i - m), 1)
                if n < i - m:
                    p = i - m - n
        else:
            temp = random.randint(1, 3)
            if temp == 1:
                m = data_Q[i]
            if temp == 2:
                n = data_Q[i]
            if temp == 3:
                p = data_Q[i]
        Q_ls.append([m, n, p])
        m, n, p = 0, 0, 0
    return np.array(Q_ls)

print(random_Q(data_need))