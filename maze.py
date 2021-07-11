import sys
import matplotlib.pyplot as plt
from random import randint

width = 0
height = 0
# 递归深度的修改，默认递归深度不能超过900，超过需要手动设置
# 特别需要注意的是不同系统都各自的理论递归最大深度
width = eval(input("请输入迷宫的长度："))
height = eval(input("请输入迷宫的宽度："))
sys.setrecursionlimit(width * height)
visited = []
temp = []
track = []


# 初始化访问列表，所有的边都先设置为False
def init_VisitedList():
    global visited
    visited = []
    for y in range(0,height):
        line = []
        for x in range(0,width):
            line.append(False)
        visited.append(line)
    return visited


# 根据算法画出横边【X1,X2]或者竖边[y1,y2]
def drawLine(X1, y1, X2, y2):
    plt.plot([X1, X2], [y1, y2], color="black")


# 根据算法需要移除相应的边，构成迷宫中的通路
def removeLine(X1, y1, X2, y2):
    plt.plot([X1, X2], [y1, y2], color="white")
    # temp.append((X1, y1))
    # temp.append((y1, y2))


# 获取边
def get_edges(x, y):
    result = []
    # 对应一个单元格的四边，从x，y开始往右上角到x+1,y+1
    result.append((x, y, x, y + 1))
    result.append((x + 1, y, x + 1, y + 1))
    result.append((x, y, x + 1, y))
    result.append((x, y + 1, x + 1, y + 1))

    return result


# 绘制单元格
def drawCell(x, y):
    edges = get_edges(x, y)  # edges是一个列表包含一个单元格四条边
    for item in edges:
        # 对应get_edges()函数4个append，画出四条边
        drawLine(item[0], item[1], item[2], item[3])


# 获得共同的边，参数获得两对xy能得到两个单元格的所有边
def get_CommonEdge(cell1_x, cell1_y, cell2_x, cell2_y):
    # 先获取X1，y1这个单元格的所有边
    edges1 = get_edges(cell1_x, cell1_y)
    # 获取另外一个单元的所有边放置在集合中（会先自动去重）
    edges2 = get_edges(cell2_x, cell2_y)
    # 遍历判断是否是公共边
    for edge in edges1:
        if edge in edges2:
            return edge
    return None


# 初始化边列表，这个作为主体表，跟前面的访问列表一起构建迷宫。
# 将所有的边都设置为数值形式方便算法操作
def init_EdgeList():
    edges = set()
    for x in range(width):
        for y in range(height):
            cellEdges = get_edges(x, y)
            for edge in cellEdges:
                edges.add(edge)
    return edges  # 这个列表包含了所有非重合的边


# 确认是否是有效位置，去掉列表中无效的单元格和边
def justy_ValidPosition(x, y):
    if x < 0 or x >= width:
        return False
    elif y < 0 or y >= height:
        return False
    else:
        return True


# 负责打乱的函数，决定随机往四周哪个单元凿墙
def shuffle(dX, dY):
    for t in range(4):
        # t=0，1，2，3.i和j也一样
        i = randint(0, 3)
        j = randint(0, 3)
        dX[i], dX[j] = dX[j], dX[i]
        dY[i], dY[j] = dY[j], dY[i]


# 核心算法：做深度优先找迷宫的出口，一开始访问列表visited全为False.
# 递归深度:大约为 width*height

def DFS(X, Y, edgeList, visited):
    # 四个值分别对应四个方向（从dfs算法求解迷宫得到灵感）
    dX = [0, 0, -1, 1]
    dY = [-1, 1, 0, 0]
    shuffle(dX, dY)  # 每次递归dx和dy都会重置
    for i in range(len(dX)):
        # 随机选择一个没有走过的方向凿墙,for循环四次，确保会遍历单元格的所有邻居，进而遍历全部单元格
        nextX = X + dX[i]
        nextY = Y + dY[i]
        if justy_ValidPosition(nextX, nextY):
            if not visited[nextY][nextX]:
                visited[nextY][nextX] = True  # 标记为走过
                commonEdge = get_CommonEdge(X, Y, nextX, nextY)
                if commonEdge in edgeList:
                    edgeList.remove(commonEdge)  # 有公共边，不是临界单元，凿墙
                    # global track
                    # track.append(commonEdge)
                DFS(nextX, nextY, edgeList, visited)


x = int(width / 2)
y = int(height / 2)
cnt = 0
isgo = 0

# 设置x，y轴刻度等长，axis用于设置xy轴
plt.axis('equal')
# 设置图像标题
plt.title('Maze generation')
# 初始化边列表
edgeList = init_EdgeList()
# 初始化访问列表
visited = init_VisitedList()
DFS(0, 0, edgeList, visited)
edgeList.remove((0, 0, 0, 1))
edgeList.remove((width, height - 1, width, height))
# 绘制所有没被删除的边
for edge in edgeList:
    drawLine(edge[0], edge[1], edge[2], edge[3])  # 横线：02，竖线：13
    if edge[0] == x and edge[1] == y:
        if edge[1] == y:
            cnt += 1
    if edge[2] == x + 1 and edge[3] == y + 1:
        if edge[1] == y or edge[1] == y + 1:
            cnt += 1
plt.show()

print(x, y, cnt)
for edge in edgeList:
    if edge[0] == x and edge[2] == x:
        isgo = isgo + 1
print(isgo)

# print(sorted(list(edgeList)))
# print(len(sorted(list(edgeList))))
