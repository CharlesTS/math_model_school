import numpy as np
import pandas as pd

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def main():
    data = pd.read_excel('附件1.xlsx')
    data_x = data['x坐标'].tolist()
    data_y = data['y坐标'].tolist()
    d = []
    for i in range(len(data_x)):
        d.append(distance(data_x[i], data_y[i], 0, 0))

    d1 = sorted(d)
    average = sum(d) / (len(d) - 1)
    print(d)
    print(d1)
    print(d1[len(d1) // 2])
    print(average)

if __name__ == '__main__':
    main()