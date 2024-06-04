import numpy as np
import random

# 参数设置
num_islands = 20
max_capacity = 50
empty_speed = 26
speed_loss_per_ton = 0.12
loading_time_per_ton = 10 / 60  # 小时
unloading_time_per_ton = 15 / 60  # 小时
num_ships = 3
population_size = 100
generations = 500
mutation_rate = 0.1

# 海岛坐标与补给需求量
islands = [
    (57.50, 17.20, 13.5), (52.60, 19.50, 5.2), (-46.60, 11.30, 13.3),
    (102.5, 65.90, 13.0), (-65.30, -84.20, 6.6), (106, 75.30, 15.8),
    (126, 70.10, 13.6), (22.30, -64.05, 29.7), (-3.300, 152.2, 7.4),
    (12.60, 168.6, 6.0), (23.10, 30.30, 13.9), (26.20, 35.60, 14.2),
    (30.10, 30.20, 5.3), (-65, -26.90, 18.3), (-70.90, 5.200, 15.6),
    (-50.30, 100.6, 24.4), (49.60, -51.50, 12.5), (75.40, 52.30, 7.1),
    (48.03, 105.7, 12.5), (-10.5, 12.2, 8.6)
]

# 计算两点之间的距离
def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# 计算航行时间
def travel_time(distance, load):
    speed = empty_speed - speed_loss_per_ton * load
    return distance / speed

# 计算个体的适应度（总时间）
def fitness(individual):
    total_time = 0
    for ship in individual:
        ship_time = 0
        load = 0
        prev_island = (0, 0)
        for island_idx in ship[1]:
            island = islands[island_idx]
            distance_to_island = distance(prev_island[0], prev_island[1], island[0], island[1])
            travel_time_to_island = travel_time(distance_to_island, load)
            ship_time += travel_time_to_island + island[2] * unloading_time_per_ton
            load += island[2]
            prev_island = island
        total_time += ship_time
    return total_time

# 生成初始种群
def generate_population():
    population = []
    for _ in range(population_size):
        individual = []
        remaining_islands = list(range(num_islands))
        for ship_id in range(num_ships):
            ship_load = []
            while remaining_islands and sum(islands[idx][2] for idx in ship_load) < max_capacity:
                if not remaining_islands:
                    break
                island_idx = remaining_islands.pop(random.randint(0, len(remaining_islands) - 1))
                ship_load.append(island_idx)
            individual.append((ship_id, ship_load))
        population.append(individual)
    return population

# 选择操作（锦标赛选择）
def selection(population):
    selected = random.choices(population, k=2)
    return min(selected, key=fitness)

# 交叉操作（部分映射交叉 PMX）
def crossover(parent1, parent2):
    child1, child2 = parent1.copy(), parent2.copy()
    for i in range(len(parent1)):
        ship1, ship2 = parent1[i], parent2[i]
        if len(ship1[1]) > 1 and len(ship2[1]) > 1:
            point1, point2 = sorted(random.sample(range(len(ship1[1])), 2))
            new_ship1 = ship1[1][:point1] + ship2[1][point1:point2] + ship1[1][point2:]
            new_ship2 = ship2[1][:point1] + ship1[1][point1:point2] + ship2[1][point2:]
            child1[i] = (ship1[0], new_ship1)
            child2[i] = (ship2[0], new_ship2)
    return child1, child2

# 变异操作
def mutation(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            ship_id = random.randint(0, num_ships - 1)
            if len(individual[ship_id][1]) > 1:
                idx1, idx2 = random.sample(range(len(individual[ship_id][1])), 2)
                individual[ship_id][1][idx1], individual[ship_id][1][idx2] = individual[ship_id][1][idx2], individual[ship_id][1][idx1]
    return individual

# 遗传算法主过程
def genetic_algorithm():
    population = generate_population()
    best_individual = min(population, key=fitness)
    best_fitness = fitness(best_individual)
    for _ in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = selection(population)
            parent2 = selection(population)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1)
            child2 = mutation(child2)
            new_population.extend([child1, child2])
        population = new_population
        current_best = min(population, key=fitness)
        current_fitness = fitness(current_best)
        if current_fitness < best_fitness:
            best_individual, best_fitness = current_best, current_fitness
    return best_individual, best_fitness

def print_best_solution(solution):
    for ship_id, route in solution:
        route_details = [(f"D{island_id}", islands[island_id][2]) for island_id in route]
        print(f"船只 {ship_id} 的运输路线: {route_details}")

best_solution, best_time = genetic_algorithm()
print(f"最短总时间: {best_time} 小时")
print("最优转运方案:")
print_best_solution(best_solution)
