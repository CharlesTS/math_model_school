import pandas as pd

data = pd.read_excel('附件1.xlsx')
data = data.dropna()

data_num = data['海岛编号']
data_x = data['x坐标(海里)']
data_y = data['y坐标(海里)']
data_need = data['补给需求量（t）']

data_x_1, data_x_2, data_x_3, data_x_4 = [], [], [], []
data_y_1, data_y_2, data_y_3, data_y_4 = [], [], [], []

for i in range(1, len(data_num)):
    if data_x[i] > 0:
        if data_y[i] > 0:
            data_x_1.append(data_x[i])
            data_y_1.append(data_y[i])
        else:
            data_x_4.append(data_x[i])
            data_y_4.append(data_y[i])
    else:
        if data_y[i] > 0:
            data_x_2.append(data_x[i])
            data_y_2.append(data_y[i])
        else:
            data_x_3.append(data_x[i])
            data_y_3.append(data_y[i])

df