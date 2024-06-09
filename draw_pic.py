import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text

# 设置字体以支持负号
plt.rcParams['axes.unicode_minus'] = False
# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 海岛数据，包括坐标和需求量
island_data = {
    'D0': (0, 0, 0),
    'D1': (57.50, 17.20, 13.5),
    'D2': (52.60, 19.50, 5.2),
    'D3': (-46.60, 11.30, 13.3),
    'D4': (102.5, 65.90, 13.0),
    'D5': (-65.30, -84.20, 6.6),
    'D6': (106, 75.30, 15.8),
    'D7': (126, 70.10, 13.6),
    'D8': (22.30, -64.05, 29.7),
    'D9': (-3.30, 152.2, 7.4),
    'D10': (12.60, 168.6, 6.0),
    'D11': (23.10, 30.30, 13.9),
    'D12': (26.20, 35.60, 14.2),
    'D13': (30.10, 30.20, 5.3),
    'D14': (-65.0, -26.90, 18.3),
    'D15': (-70.90, 5.20, 15.6),
    'D16': (-50.30, 100.6, 24.4),
    'D17': (49.60, -51.50, 12.5),
    'D18': (75.40, 52.30, 7.1),
    'D19': (48.03, 105.7, 12.5),
    'D20': (-10.5, 12.2, 8.6)
}

# 提取海岛坐标和需求量
island_coords = np.array([[v[0], v[1]] for v in island_data.values()])
island_demands = np.array([v[2] for v in island_data.values()])
island_names = list(island_data.keys())


# 定义一个函数来绘制带箭头的线条
def draw_route_with_arrows(coords, color, label):
    for i in range(len(coords) - 1):
        start, end = coords[i], coords[i + 1]
        plt.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1],
                  head_width=3, head_length=3, fc=color, ec=color, label=label if i == 0 else "",
                  length_includes_head=True)

def draw_pic_island():
    # 绘制海岛坐标图
    plt.figure(figsize=(10, 8))
    texts = []
    for i, (x, y) in enumerate(island_coords):
        plt.scatter(x, y, color='blue' if i != 0 else 'red')  # 绘制海岛坐标点，D0为黄色
        texts.append(plt.text(x, y, f"{list(island_data.keys())[i]}\n{island_demands[i]:.1f}", fontsize=10, ha='right'))

    plt.title('海岛坐标图')  # 图表标题
    plt.xlabel('X 坐标 (海里)')  # X轴标签
    plt.ylabel('Y 坐标 (海里)')  # Y轴标签
    plt.grid(True)  # 显示网格线
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 调整文本位置以避免重叠
    adjust_text(texts)
    plt.savefig('海岛坐标图.png', dpi=300, bbox_inches='tight')
    plt.show()  # 显示图表

def draw_pic_first():
    # 定义船的运输路线
    routes = {
        'A': ['D0', 'D3', 'D16', 'D0', 'D0', 'D1', 'D18', 'D6', 'D7'],
        'B': ['D0', 'D20', 'D11', 'D12', 'D4', 'D0', 'D0', 'D8', 'D17'],
        'C': ['D0', 'D14', 'D15', 'D5', 'D0', 'D0', 'D13', 'D2', 'D19', 'D9', 'D10']
    }

    # 定义不同路线的颜色
    initial_route_colors = {
        'A': 'red',
        'B': 'green',
        'C': 'black'
    }
    secondary_route_colors = {
        'A': 'orange',
        'B': 'cyan',
        'C': 'purple'
    }

    # 绘制海岛坐标图
    plt.figure(figsize=(14, 10))
    texts = []
    for i, (x, y) in enumerate(island_coords):
        plt.scatter(x, y, color='blue' if i != 0 else 'yellow')  # 绘制海岛坐标点，D0为黄色
        texts.append(plt.text(x, y, f"{island_names[i]}\n{island_demands[i]:.1f}", fontsize=8, ha='right'))

    # 绘制船的运输路线
    for ship, route in routes.items():
        # 将初次路径和回到中转站后的路径分开处理
        initial_route_coords = []
        secondary_route_coords = []
        is_initial_route = True

        for stop in route:
            if stop == 'D0' and not is_initial_route:
                is_initial_route = False
            if is_initial_route:
                initial_route_coords.append(island_data[stop][:2])
            else:
                secondary_route_coords.append(island_data[stop][:2])

        # 绘制初次路径
        if initial_route_coords:
            draw_route_with_arrows(np.array(initial_route_coords), initial_route_colors[ship], f"{ship} 船路线 ")

        # 绘制回到中转站后的路径
        if secondary_route_coords:
            draw_route_with_arrows(np.array(secondary_route_coords), secondary_route_colors[ship], f"{ship} 船路线 ")

    # 添加图注
    plt.legend(loc='upper right')

    # 调整文本位置以避免重叠
    adjust_text(texts)

    plt.title('海岛坐标图及船的运输路线')  # 图表标题
    plt.xlabel('X 坐标 (海里)')  # X轴标签
    plt.ylabel('Y 坐标 (海里)')  # Y轴标签
    plt.grid(True)  # 显示网格线
    plt.savefig('第一题：货船运输图.png', dpi=300, bbox_inches='tight')
    plt.show()  # 显示图表

def draw_pic_second():
    # 定义船的运输路线
    routes = {
        'A':['D0', 'D20', 'D8', 'D17', 'D0', 'D17', 'D4'],
        'B':['D0', 'D12', 'D1', 'D18', 'D6', 'D0', 'D6', 'D7'],
        'C':['D0', 'D11', 'D13', 'D2', 'D3', 'D15', 'D0', 'D15', 'D5'],
        'D':['D0', 'D14', 'D16', 'D9', 'D10', 'D19']
    }

    # 定义不同路线的颜色
    initial_route_colors = {
        'A': 'red',
        'B': 'green',
        'C': 'black',
        'D': 'purple'
    }
    secondary_route_colors = {
        'A': 'orange',
        'B': 'cyan',
        'C': 'purple'
    }

    # 绘制海岛坐标图
    plt.figure(figsize=(14, 10))
    texts = []
    for i, (x, y) in enumerate(island_coords):
        plt.scatter(x, y, color='blue' if i != 0 else 'yellow')  # 绘制海岛坐标点，D0为黄色
        texts.append(plt.text(x, y, f"{island_names[i]}\n{island_demands[i]:.1f}", fontsize=8, ha='right'))

    # 绘制船的运输路线
    for ship, route in routes.items():
        # 将初次路径和回到中转站后的路径分开处理
        initial_route_coords = []
        secondary_route_coords = []
        is_initial_route = True

        for stop in route:
            if stop == 'D0' and not is_initial_route:
                is_initial_route = False
            if is_initial_route:
                initial_route_coords.append(island_data[stop][:2])
            else:
                secondary_route_coords.append(island_data[stop][:2])

        # 绘制初次路径
        if initial_route_coords:
            draw_route_with_arrows(np.array(initial_route_coords), initial_route_colors[ship], f"{ship} 船路线 ")

        # 绘制回到中转站后的路径
        if secondary_route_coords:
            draw_route_with_arrows(np.array(secondary_route_coords), secondary_route_colors[ship], f"{ship} 船路线 ")

    # 添加图注
    plt.legend(loc='upper right')

    # 调整文本位置以避免重叠
    adjust_text(texts)

    plt.title('海岛坐标图及船的运输路线')  # 图表标题
    plt.xlabel('X 坐标 (海里)')  # X轴标签
    plt.ylabel('Y 坐标 (海里)')  # Y轴标签
    plt.grid(True)  # 显示网格线
    plt.savefig('第二题：货船运输图.png', dpi=300, bbox_inches='tight')
    plt.show()  # 显示图表

if __name__ == '__main__':
    draw_pic_island()
    draw_pic_first()
    draw_pic_second()