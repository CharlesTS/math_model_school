import numpy as np
import pandas as pd
from scipy import spatial

# def distance(x1, y1, x2, y2):
#     return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
#
# def main():
#     data = pd.read_excel('附件1.xlsx')
#     data_x = data['x坐标'].tolist()
#     data_y = data['y坐标'].tolist()
#
#     A = [0, 20, 3, 8, 0, 8, 6]
#     A_ls = [20, 3, 8, 0, 8, 6, 0]
#     B = [0, 13, 18, 17, 14, 0, 14, 15, 16]
#     C = [0, 11, 12, 2, 1, 0, 1, 4, 7, 19, 0, 5, 19, 9, 10]
#
#     # A的距离计算
#     A_distances = []
#
#     for i, j in A, A_ls:
#         d = distance(data_x[i], data_y[i], data_x[i+1], data_y[i+1])
#
# if __name__ == '__main__':
#     main()

# data = pd.read_excel('附件1.xlsx').dropna()
# data_x = data['x坐标'].tolist()
# data_y = data['y坐标'].tolist()
#
# points_coordinate = np.array([[data_x[i], data_y[i]] for i in range(len(data_x))])
# distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')
#
# print(distance_matrix)


import pandas as pd

# 二维数组
data = [
    [0.0, 60.01741414, 56.09821744, 47.95049531, 121.85671914, 106.55388308, 130.02342097, 144.18741277, 67.82103287, 152.23577109, 169.07016295, 38.10118108, 44.20180992, 42.63859754, 70.3463574, 71.09043536, 112.47421927, 71.50111887, 91.76300998, 116.10069294, 16.09627286],
    [60.01741414, 0.0, 5.41294744, 104.26706095, 66.30754105, 159.25388535, 75.6826268, 86.54859906, 88.54717669, 148.0595826, 157.9176051, 36.80991714, 36.30771268, 30.32754524, 130.1962365, 128.95952854, 136.29526771, 69.15272952, 39.40076141, 89.00522962, 68.18357573],
    [56.09821744, 5.41294744, 0.0, 99.53833432, 68.13934253, 157.0162412, 77.23470722, 89.15110768, 88.87458861, 143.99340263, 154.37230969, 31.41480543, 30.92199864, 24.91465432, 126.42278276, 124.32513825, 131.0176324, 71.06335202, 39.9459635, 86.32105711, 63.52086271],
    [47.95049531, 104.26706095, 99.53833432, 0.0, 158.78277614, 97.31361672, 165.47737005, 182.34088954, 102.10206903, 147.40318857, 168.07120515, 72.24326958, 76.74848533, 78.99430359, 42.4004717, 25.05394181, 89.37661887, 114.88376735, 128.70508925, 133.66449379, 36.11121709],
    [121.85671914, 66.30754105, 68.13934253, 158.78277614, 0.0, 225.13740249, 10.03045363, 23.87236896, 152.70573827, 136.53325602, 136.48919371, 87.01563078, 82.09616313, 80.7232928, 191.48913807, 183.71731002, 156.69055492, 128.76789196, 30.32111476, 67.46125481, 125.11071097],
    [106.55388308, 159.25388535, 157.0162412, 97.31361672, 225.13740249, 0.0, 234.05969324, 245.77261849, 89.88761038, 244.39508997, 264.53024402, 144.65410468, 150.74577938, 148.95811492, 57.30078533, 89.57521979, 185.40776683, 119.46254643, 196.03249731, 221.14632916, 110.88733021],
    [130.02342097, 75.6826268, 77.23470722, 165.47737005, 10.03045363, 234.05969324, 0.0, 20.66494616, 162.55495225, 133.64168511, 132.01685498, 94.32608335, 89.1298491, 88.28827782, 199.21305178, 190.28299977, 158.33439298, 138.77751979, 38.2800209, 65.45747398, 132.49098083],
    [144.18741277, 86.54859906, 89.15110768, 182.34088954, 23.87236896, 245.77261849, 20.66494616, 0.0, 169.55799155, 153.16298508, 150.20589203, 110.3288267, 105.59493359, 103.86924473, 214.21951358, 207.32009068, 178.9188084, 143.60891337, 53.63953766, 85.71278143, 148.2722496],
    [67.82103287, 88.54717669, 88.87458861, 102.10206903, 152.70573827, 89.88761038, 162.55495225, 169.55799155, 0.0, 217.76001125, 232.85212582, 94.35339157, 99.72628791, 94.57220786, 94.87577404, 116.11116441, 179.94549869, 30.04650562, 127.89422387, 171.68894956, 83.00543657],
    [152.23577109, 148.0595826, 143.99340263, 147.40318857, 136.53325602, 244.39508997, 133.64168511, 153.16298508, 217.76001125, 0.0, 22.84228535, 124.72597965, 120.27389575, 126.48936714, 189.42993428, 161.79851668, 69.79656152, 210.45688395, 127.17586249, 69.26051473, 140.1850206],
    [169.07016295, 157.9176051, 154.37230969, 168.07120515, 136.48919371, 264.53024402, 132.01685498, 150.20589203, 232.85212582, 22.84228535, 0.0, 138.69801729, 133.69353014, 139.50200715, 210.33784728, 183.49880109, 92.63050254, 223.18828374, 132.1723496, 72.19206951, 158.09671091],
    [38.10118108, 36.80991714, 31.41480543, 72.24326958, 87.01563078, 144.65410468, 94.32608335, 110.3288267, 94.35339157, 124.72597965, 138.69801729, 0.0, 6.14003257, 7.00071425, 105.04023039, 97.29342218, 101.63488574, 85.98540574, 56.73878744, 79.41451316, 38.16503636],
    [44.20180992, 36.30771268, 30.92199864, 76.74848533, 82.09616313, 150.74577938, 89.1298491, 105.59493359, 99.72628791, 120.27389575, 133.69353014, 6.14003257, 0.0, 6.66108099, 110.56079775, 101.74757982, 100.38550692, 90.18852477, 51.95700145, 73.42042563, 43.52528001],
    [42.63859754, 30.32754524, 24.91465432, 78.99430359, 80.7232928, 148.95811492, 88.28827782, 103.86924473, 94.57220786, 126.48936714, 139.50200715, 7.00071425, 6.66108099, 0.0, 110.92529017, 104.04806582, 106.86589727, 83.9948808, 50.4033729, 77.59983827, 44.41125983],
    [70.3463574, 130.1962365, 126.42278276, 42.4004717, 191.48913807, 57.30078533, 199.21305178, 214.21951358, 94.87577404, 189.42993428, 210.33784728, 105.04023039, 110.56079775, 110.92529017, 0.0, 32.63770825, 128.34461422, 117.21057973, 161.19801488, 174.23702505, 67.07503261],
    [71.09043536, 128.95952854, 124.32513825, 25.05394181, 183.71731002, 89.57521979, 190.28299977, 207.32009068, 116.11116441, 161.79851668, 183.49880109, 97.29342218, 101.74757982, 104.04806582, 32.63770825, 0.0, 97.59877048, 133.17334568, 153.6948275, 155.70675933, 60.80427617],
    [112.47421927, 136.29526771, 131.0176324, 89.37661887, 156.69055492, 185.40776683, 158.33439298, 178.9188084, 179.94549869, 69.79656152, 92.63050254, 101.63488574, 100.38550692, 106.86589727, 128.34461422, 97.59877048, 0.0, 181.97367942, 134.66023912, 98.46216989, 96.94637693],
    [71.50111887, 69.15272952, 71.06335202, 114.88376735, 128.76789196, 119.46254643, 138.77751979, 143.60891337, 30.04650562, 210.45688395, 223.18828374, 85.98540574, 90.18852477, 83.9948808, 117.21057973, 133.17334568, 181.97367942, 0.0, 106.95830964, 157.20783982, 87.57682342],
    [91.76300998, 39.40076141, 39.9459635, 128.70508925, 30.32111476, 196.03249731, 38.2800209, 53.63953766, 127.89422387, 127.17586249, 132.1723496, 56.73878744, 51.95700145, 50.4033729, 161.19801488, 153.6948275, 134.66023912, 106.95830964, 0.0, 60.00564057, 94.79883966],
    [116.10069294, 89.00522962, 86.32105711, 133.66449379, 67.46125481, 221.14632916, 65.45747398, 85.71278143, 171.68894956, 69.26051473, 72.19206951, 79.41451316, 73.42042563, 77.59983827, 174.23702505, 155.70675933, 98.46216989, 157.20783982, 60.00564057, 0.0, 110.30870727],
    [16.09627286, 68.18357573, 63.52086271, 36.11121709, 125.11071097, 110.88733021, 132.49098083, 148.2722496, 83.00543657, 140.1850206, 158.09671091, 38.16503636, 43.52528001, 44.41125983, 67.07503261, 60.80427617, 96.94637693, 87.57682342, 94.79883966, 110.30870727, 0.0]
]

# 将数组转换成 pandas 的 DataFrame
df = pd.DataFrame(data)
df.to_excel("output.xlsx", index=False)
# 输出表格
print(df)
