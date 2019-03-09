import numpy as np
import matplotlib.pyplot as plt

# 参数设置
KP = 5.0  # 终点的吸引
ETA = 100.0  # 障碍物的排斥
AREA_WIDTH = 12  # 宽度
AREA_HIGHT = 9   #高度

DEBUG = True


def calculate_potential(goal_x, goal_y, obstacle_x, obstacle_y, resolution, robot_radius):
    minx = -AREA_WIDTH/2
    maxx = AREA_WIDTH/2
    miny = -AREA_HIGHT/2
    maxy = AREA_HIGHT/2

    grid_x = int((maxx-minx)/resolution)  # 地图宽度/格子数
    grid_y = int((maxy-miny)/resolution)  # 地图高度/格子数
    if DEBUG is True:
        print("Grid map size: ", grid_x, " x ", grid_y)
    # 生成地图的数据结构（数组）
    potential_map = [[0.0 for i in range(grid_y)] for i in range(grid_x)]

    for ix in range(grid_x):
        x = ix*resolution+minx
        for iy in range(grid_y):
            y = iy*resolution+miny

            attractive = 0.5*KP*np.hypot(x - goal_x, y-goal_y)
            repulsive = calculate_repulsive(
                x, y, obstacle_x, obstacle_y, robot_radius)
            potential = attractive+repulsive
            potential_map[ix][iy] = potential
    return potential_map, minx, miny


def calculate_repulsive(x, y, obstacle_x, obstacle_y, robot_radius):
    minid = -1
    dmin = float("inf")
    for i, ox in enumerate(obstacle_x):
        d = np.hypot(x-obstacle_x[i], y-obstacle_y[i])
        if dmin >= d:
            dmin = d
            minid = i

    distance = np.hypot(x-obstacle_x[minid], y-obstacle_y[minid])
    if DEBUG is True:
        if distance is 0:
            print("???")
    if distance <= robot_radius:
        if distance <= 0.1:
            dq = 0.1

        return 0.5*ETA*(1.0/distance-1.0/robot_radius)**2
    else:
        return 0.0


def plan_potential_path(start_x, start_y, goal_x, goal_y, obstacle_x, obstacle_y, resolution, robot_radius):
    potential_map, minx, miny = calculate_potential(
        goal_x, goal_y, obstacle_x, obstacle_y, resolution, robot_radius)


if __name__ == '__main__':

    goal_x = 5.5  #目标位置
    goal_y = -4.0  # 目标位置
    resolution = 0.1  # 分辨率
    robot_radius = 0.1  # 小车半径

    obstacle_x = [-1.0, 1.0, 1.0, 2.0]  # 障碍物x坐标
    obstacle_y = [2.0, -1.5, 2.5, 3]  # 障碍物y坐标

    potential_map, minx, miny = calculate_potential(
        goal_x, goal_y, obstacle_x, obstacle_y, resolution, robot_radius)
    data = np.array(potential_map).T
    plt.grid=True
    plt.pcolor(data, vmax=100, cmap=plt.cm.hot_r)
    plt.show()
