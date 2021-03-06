from math import inf, pow, sqrt
from queue import Queue


class DStar:
    STRAIGHT_DIST = 1
    DIAGONAL_DIST = sqrt(2)

    @classmethod
    def heuristic(cls, a, b):    ## 启发式因子
        x_diff, y_diff = abs(a.x - b.x), abs(a.y - b.y)
        return (cls.DIAGONAL_DIST - 1) * min(x_diff, y_diff) + max(x_diff, y_diff)

    @classmethod
    def key_hash_code(cls, u):   # 计算k值
        return u.k.first() + 1193 * u.k.second()

    @classmethod
    def true_dist(cls, a, b):   # 欧式距离
        return sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))

    @classmethod
    def close(cls, x, y):      # 判断是否相等
        if x == inf and y == inf:
            return True
        return abs(x - y) < 0.00001

    def get_path(self):      # 获取计算的路径 
        return self.path

    def cost(self, a, b):    # 获取相邻点的距离，DIAGONAL_DIST（斜线距离），STRAIGHT_DIST（直线距离）
        x_diff = abs(a.x - b.x)
        y_diff = abs(a.y - b.y)

        scale = self.DIAGONAL_DIST if x_diff + y_diff > 1 else self.STRAIGHT_DIST

        if a in self.cell_hash.keys():
            return scale * self.cell_hash[a].cost
        return scale

    def get_rhs(self, u):  # 后继节点的估计值
        if u == self.s_goal:
            return 0
        if u not in self.cell_hash:
            return self.heuristic(u, self.s_goal)
        return self.cell_hash[u].rhs

    def get_g(self, u):   # 前继点的估计值
        if u not in self.cell_hash.keys():
            return self.heuristic(u, self.s_goal)
        return self.cell_hash[u].g

    def calculate_key(self, u):   # 计算key值
        val = min(self.get_rhs(u), self.get_g(u))
        return State(u.x, u.y, Pair(val + self.heuristic(u, self.s_start) + self.k_m, val))

    def make_new_cell(self, u):   # 创建新的一个结点
        if u in self.cell_hash.keys():
            return
        dist = self.heuristic(u, self.s_goal)
        tmp = CellInfo(dist, dist, self.STRAIGHT_DIST)
        self.cell_hash[u] = tmp

    def clear_fields(self):   #清除存储的地图数据
        self.cell_hash = {}
        self.open_hash = {}
        self.open_list = Queue()
        self.k_m = 0

        self.make_new_cell(self.s_goal)
        self.make_new_cell(self.s_start)

        self.s_start = self.calculate_key(self.s_start)

        self.s_last = self.s_start

    def __init__(self, x_start, y_start, x_goal, y_goal):
        self.path = []

        self.s_start = State(x_start, y_start, Pair(0, 0))
        self.s_goal = State(x_goal, y_goal, Pair(0, 0))

        self.clear_fields()

    def set_g(self, u, g):  # 设置g
        self.make_new_cell(u)
        self.cell_hash[u].g = g

    def set_rhs(self, u, rhs):  # 设置rhs
        self.make_new_cell(u)
        self.cell_hash[u].rhs = rhs

    def is_valid(self, u):
        if u not in self.open_hash:
            return False
        if not self.close(self.key_hash_code(u), self.open_hash[u]):
            return False
        return True

    def occupied(self, u):   # 是否被不可行
        if u not in self.cell_hash:
            return False
        return self.cell_hash[u].cost < 0

    def get_predecessors(self, u):   # 前继节点遍历
        s = []

        tmp = State(u.x + 1, u.y, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x + 1, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y + 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x - 1, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)
        tmp = State(u.x + 1, u.y - 1, Pair(-1, -1))
        if not self.occupied(tmp):
            s.append(tmp)

        return s

    def get_successors(self, u):  # 后继节点遍历
        s = []
        
        if self.occupied(u):
            return s

        s.append(State(u.x + 1, u.y, Pair(-1, -1)))
        s.append(State(u.x + 1, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y + 1, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y, Pair(-1, -1)))
        s.append(State(u.x - 1, u.y - 1, Pair(-1, -1)))
        s.append(State(u.x, u.y - 1, Pair(-1, -1)))
        s.append(State(u.x + 1, u.y - 1, Pair(-1, -1)))

        return s


    def update_start(self, x, y): #更新起点
        self.s_start.x = x
        self.s_start.y = y
        self.k_m += self.heuristic(self.s_last, self.s_start)
        self.s_start = self.calculate_key(self.s_start)
        self.s_last = self.s_start

    def update_goal(self, x, y):  # 更新终点
        to_add = []
        for state in self.cell_hash:
            if not self.close(self.cell_hash[state], self.STRAIGHT_DIST):
                to_add.append(Pair(Point(state.x, state.y), self.cell_hash[state].cost))

        self.s_goal.x = x
        self.s_goal.y = y

        self.clear_fields()

        for p in to_add:
            self.update_cell(p.first().x, p.first().y, p.second())
 
    def insert(self, u):    #设置u点的各个值
        u = self.calculate_key(u)
        csum = self.key_hash_code(u)
        self.open_hash[u] = csum
        self.open_list.put(u)

    def update_vertex(self, u):   # 设置顶点（rhs，g的值）
        if u != self.s_goal:
            s = self.get_successors(u)
            tmp = inf

            for i in s:
                tmp = min(tmp, self.get_g(i) + self.cost(u, i))

            if not self.close(self.get_rhs(u), tmp):
                self.set_rhs(u, tmp)

        if not self.close(self.get_g(u), self.get_rhs(u)):
            self.insert(u)

    def update_cell(self, x, y, val): # 更新地图单元
        u = State(x, y, Pair(0, 0))

        if u == self.s_start or u == self.s_goal:
            return

        self.make_new_cell(u)
        self.cell_hash[u].cost = val
        self.update_vertex(u)

    def compute_shortest_path(self): # 反向传播计算地图估计值
        if self.open_list.empty():
            return 1

        self.s_start = self.calculate_key(self.s_start)
        while not self.open_list.empty() and self.open_list.queue[0] < self.s_start \
                or self.get_rhs(self.s_start) != self.get_g(self.s_start):

            test = self.get_rhs(self.s_start) != self.get_g(self.s_start)

            while True:
                if self.open_list.empty():
                    return 1
                u = self.open_list.get()
                if not self.is_valid(u):
                    continue
                if not u < self.s_start and not test:
                    return 2
                break

            self.open_hash.pop(u)
            k_old = State(u.x, u.y, u.k)

            if k_old < self.calculate_key(u):
                self.insert(u)
            elif self.get_g(u) > self.get_rhs(u):
                self.set_g(u, self.get_rhs(u))
                s = self.get_predecessors(u)
                for i in s:
                    self.update_vertex(i)
            else:
                self.set_g(u, inf)
                s = self.get_predecessors(u)
                for i in s:
                    self.update_vertex(i)
                self.update_vertex(u)

            self.s_start = self.calculate_key(self.s_start)
        return 0

    def replan(self):  # 路劲规划主函数
        self.path = []
        if self.compute_shortest_path() < 0: # 反向传播计算地图估计值
            print("no path") 
            return False

        cur = self.s_start
        if self.get_g(self.s_start) == inf: #是否存在可行路径
            print("g==inf")
            return False

        while cur != self.s_goal:  #逐步循环
            self.path.append(cur)
            n = self.get_successors(cur)
            self.update_cell(cur.x,cur.y,100) # 设置单次路径规划不允许走回头路

            if len(n) == 0:
                print("n=0")
                return False

            cmin = inf
            tmin = 0

            for i in n: # 对所用邻域的点，寻找最小估计值的点
                val = self.cost(cur, i)
                val2 = self.true_dist(i, self.s_goal) + self.true_dist(self.s_start, i)
                val += self.get_rhs(i)
                if  i in self.cell_hash and self.cell_hash[i].cost < 0:
                    continue

                if self.close(val, cmin) and tmin > val2 or val < cmin:
                    tmin = val2
                    cmin = val
                    smin = i

            cur = State(smin.x, smin.y, smin.k)
        self.path.append(self.s_goal) # 添加到路径
        for i in self.cell_hash.keys(): # 删除单次路径规划中的设置
            if self.cell_hash[i].cost==100:
                self.cell_hash[i].cost=1

        return True

    def set_obstract(self,x,y,r,val):
        x_max=int(x+r)+1
        x_min=int(x-r)
        y_max=int(y+r)+1
        y_min=int(y-r)
        for i in range(x_min,x_max):
            for j in range(y_min,y_max):
                if (i-x)**2+(j-y)**2<r**2:
                    self.update_cell(i,j,val)

    def initialize_map(self,x,y):
        for i in range(int(-x/2),int(x/2)):
            self.update_cell(i,int(y/2),-1)
            self.update_cell(i,int(-y/2),-1)
        for i in range(int(-y/2),int(y/2)):
            self.update_cell(int(-x/2),i,-1)
            self.update_cell(int(x/2),i,-1)
        return True 
    

    def shorter_the_path(self,e,step):
        self.path = self.path[::step]
        flag=True
        while flag:
            flag=False 
            n=len(self.path)    
            index=n-1
            while index>=2:
                d=abs(self.path[index].x+self.path[index-2].x-2*self.path[index-1].x)+\
                    abs(self.path[index].y+self.path[index-2].y-2*self.path[index-1].y)
                if d<=e:
                    del self.path[index-1]
                    flag=True
                index=index-2
        return True

    def shorter_the_path2(self,e,step):
        a=0
        #self.path = self.path[::step]
        while a+step<len(self.path): 
            for i in range(a,a+step-1):
                del self.path[a+1]
            dx=(self.path[a+1].x-self.path[a].x)/step
            dy=(self.path[a+1].y-self.path[a].y)/step
            index=1
            while abs(self.path[a+2].x-self.path[a+1].x-dx*index)+abs(self.path[a+2].x-self.path[a+1].x-dy*index)<e\
                | a+2<len(self.path)-1 :
                del self.path[a+2]
                index=index+1
            a=a+1
        



class State:
    def __init__(self, x, y, k):
        self.x = x
        self.y = y
        self.k = k

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __gt__(self, other):
        if self.k.first() - 0.00001 > other.k.first():
            return True
        elif self.k.first() < other.k.first() - 0.00001:
            return False
        return self.k.second() > other.k.second()

    def __le__(self, other):
        if self.k.first() < other.k.first():
            return True
        elif self.k.first() > other.k.first():
            return False
        return self.k.second() < other.k.second() + 0.00001

    def __lt__(self, other):
        if self.k.first() + 0.000001 < other.k.first():
            return True
        elif self.k.first() - 0.000001 > other.k.first():
            return False
        return self.k.second() < other.k.second()

    def __cmp__(self, other):
        if self.k.first() - 0.00001 > other.k.first():
            return 1
        elif self.k.first() < other.k.first() - 0.00001:
            return -1
        if self.k.second() > other.k.second():
            return 1
        elif self.k.second() < other.k.second():
            return -1
        return 0

    def __hash__(self):
        return self.x + 34245 * self.y

    def __repr__(self):
        return "State: {x}, {y}, ({f}, {s})".format(x=self.x, y=self.y, f=self.k.first(), s=self.k.second())

class Pair:
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd
        self.fstNone = fst is None
        self.sndNone = snd is None
        self.dualNone = self.fstNone and self.sndNone

    def first(self):
        return self.fst

    def second(self):
        return self.snd

    def set_first(self, fst):
        self.fst = fst
        self.fstNone = fst is None
        self.dualNone = self.fstNone and self.sndNone

    def set_second(self, snd):
        self.snd = snd
        self.sndNone = snd is None
        self.dualNone = self.fstNone and self.sndNone

    def __eq__(self, other):
        if other is None:
            return False

        if self == other:
            return True

        if not isinstance(other, Pair):
            return False

        if self.dualNone:
            return other.dualNone

        if other.dualNone:
            return False

        if self.fstNone:
            if other.fstNone:
                return self.snd == other.snd
            elif other.sndNone:
                return self.snd == other.fst
            else:
                return False

        elif self.sndNone:
            if other.sndNone:
                return self.fst == other.fst
            elif other.fstNone:
                return self.fst == other.snd
            else:
                return False

        else:
            if self.fst == other.fst:
                return self.snd == other.snd
            elif self.fst == other.snd:
                return self.snd == other.fst
            else:
                return False

    def __hash__(self):
        hash_code = 0 if self.fstNone else hash(self.fst)
        hash_code += 0 if self.sndNone else hash(self.snd)
        return hash_code

    def __repr__(self):
        return "Pair: {f}, {s}".format(f=self.fst, s=self.snd)

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class CellInfo:
    def __init__(self, g=0., rhs=0., cost=0.):
        self.g = g
        self.rhs = rhs
        self.cost = cost

    def __repr__(self):
        return "g: {g}, rhs: {r}, cost: {c}".format(g=self.g, r=self.rhs, c=self.cost)
