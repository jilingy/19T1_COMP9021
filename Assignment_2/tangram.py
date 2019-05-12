import math

def available_coloured_pieces(file):
    filestring = file.read()
    str_list = filestring.split('d="')
    p = []
    points = []
    colours = []
    for item in str_list[1:]:
        try:
            list_link = item.split('" ')[0]
            p.append(list_link)
        except:
            pass

    for i in range(len(p)):
        point=[]
        split_words = p[i].split()
        length = len(split_words)
        for j in range(length):
           if split_words[j].isdigit() and split_words[j + 1].isdigit():
                point.append((int(split_words[j]), int(split_words[j + 1])))
        points.append(point)

    str_list2 = filestring.split('fill="')
    for item2 in str_list2[1:]:
        try:
            list_link2 = item2.split('"/')[0]
            colours.append(list_link2)
        except:
            pass
    dictionary = {}
    dictionary.update(zip(colours, points))
    return dictionary


#如果是正的，说明P2在P1P3的右边，角度小于180，也就是凸的。
#如果是负的，说明P2在P1P3的左边，角度会大于180，那就是凹的。
def cross(point_list): #叉积
    # (c.x-a.x)*(b.y-a.y)-(c.y-a.y)*(b.x-a.x)
    # x:point_list[i][0]  y:point_list[i][1]
    #对于最后一个点pn，还要和起始的两个点p0,p1判断一次。
    for i in range(-2,len(point_list)-2):
        if (point_list[0][0] - point_list[-2][0]) * (point_list[-1][1] - point_list[-2][1]) - (
                point_list[0][1] - point_list[-2][1]) * (point_list[-1][0] - point_list[-2][0]) > 0:

            if ((point_list[i+2][0] - point_list[i][0]) * (point_list[i+1][1] - point_list[i][1]) - (point_list[i+2][1] - point_list[i][1]) * (point_list[i+1][0] - point_list[i][0])) > 0:
                continue #如果>0就是凸边形
            else:
                return False #如果<0就是凹边形
        if (point_list[0][0] - point_list[-2][0]) * (point_list[-1][1] - point_list[-2][1]) - (
                point_list[0][1] - point_list[-2][1]) * (point_list[-1][0] - point_list[-2][0]) < 0:
            if ((point_list[i+2][0] - point_list[i][0]) * (point_list[i+1][1] - point_list[i][1]) - (point_list[i+2][1] - point_list[i][1]) * (point_list[i+1][0] - point_list[i][0])) < 0:
                continue #如果>0就是凸边形
            else:
                return False #如果<0就是凹边形
        if (point_list[0][0] - point_list[-2][0]) * (point_list[-1][1] - point_list[-2][1]) - (
                point_list[0][1] - point_list[-2][1]) * (point_list[-1][0] - point_list[-2][0]) == 0:
            return False
    return True


#跨立实验
def cross_experiment(p1,p2,p3):
    x1 = p2[0]-p1[0]
    y1 = p2[1]-p1[1]
    x2 = p3[0]-p1[0]
    y2 = p3[1]-p1[1]
    return x1*y2-x2*y1


#判断两线段是否相交
def IsNotIntersec(point_list): 
    l2=[]
    new_point_list=[]
    if len(point_list) == 3:
        return True

    if len(point_list)>3:
        for i in range(-1,len(point_list)-1):
            l=[]
            p1=point_list[i]
            p2=point_list[i+1]

            l.append(p1)
            l.append(p2)
            new_point_list = [x for x in point_list if x not in l]#里面装的是除了p1,p2的所有点
            for j in range(len(new_point_list)-1):
                p3=new_point_list[j]
                p4=new_point_list[j+1]
                # 快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
                if (max(p1[0], p2[0]) >= min(p3[0], p4[0]) and max(p3[0], p4[0]) >= min(p1[0], p2[0]) and max(p1[1], p2[1]) >= min(p3[1], p4[1]) and max(p3[1], p4[1]) >= min(p1[1], p2[1])):  # 矩形2最高端大于矩形最低端
                    #print('矩形相交')
                    if (cross_experiment(p1, p2, p3) * cross_experiment(p1, p2, p4) <= 0
                            and cross_experiment(p3, p4, p1) * cross_experiment(p3, p4, p2) <= 0):
                        return False
    return True


#每个碎片进行判断， 如果有一个value不是那么就不是valid的
#cross三点判断叉积
def are_valid(coloured_pieces):
    #print(coloured_pieces)
    if coloured_pieces =={}:
        return True
    point_list = []
    for keys,values in coloured_pieces.items():
        point_list.append(values)
    for i in range(len(point_list)):
        if len(point_list[i]) < 3:
            return False
    for i in range(len(point_list)):
        if cross(point_list[i]):
            continue
        else:
            return False
    for i in range(len(point_list)):
        if IsNotIntersec(point_list[i]) == True:
            continue
        else:
            return False
    return True


#判断边长
def compare_edges(pieces_1_points,pieces_2_points):
    edges1=[]
    edges2 =[]
    for i in range(-1, len(pieces_1_points)-1):
        length=math.sqrt(((pieces_1_points[i][0]-pieces_1_points[i+1][0])**2)+((pieces_1_points[i][1]-pieces_1_points[i+1][1])**2))
        edges1.append(length)
    for i in range(-1, len(pieces_2_points)-1):
        length=math.sqrt(((pieces_2_points[i][0]-pieces_2_points[i+1][0])**2)+((pieces_2_points[i][1]-pieces_2_points[i+1][1])**2))
        edges2.append(length)
    edges1=sorted(edges1)
    edges2=sorted(edges2)
    if edges1 != edges2:
        return False
    else:
        return True


#判断角度
def compare_angles(pieces_1_points,pieces_2_points):
    angle1=[]
    angle2=[]
    lx=[]
    ly = []
    for i in range(-2, len(pieces_1_points)-2):
        p1_dy1 = pieces_1_points[i][1] - pieces_1_points[i + 1][1]
        p1_dx1 = pieces_1_points[i][0] - pieces_1_points[i + 1][0]
        p1_dy2 = pieces_1_points[i+2][1] - pieces_1_points[i + 1][1]
        p1_dx2 = pieces_1_points[i+2][0] - pieces_1_points[i + 1][0]

        length1= p1_dx1 ** 2 + p1_dy1 ** 2
        length2 = p1_dx2 ** 2 + p1_dy2 ** 2
        cos=(p1_dx1*p1_dx2+p1_dy1*p1_dy2)/(math.sqrt(length1)*math.sqrt(length2))
        p1_angle_1=math.degrees(math.acos(cos))
        angle1.append(p1_angle_1)

    for i in range(-2, len(pieces_2_points) - 2):
        p2_dy1 = pieces_2_points[i][1] - pieces_2_points[i + 1][1]
        p2_dx1 = pieces_2_points[i][0] - pieces_2_points[i + 1][0]
        p2_dy2 = pieces_2_points[i + 2][1] - pieces_2_points[i + 1][1]
        p2_dx2 = pieces_2_points[i + 2][0] - pieces_2_points[i + 1][0]

        length1= p2_dx1 ** 2 + p2_dy1 ** 2
        length2 = p2_dx2 ** 2 + p2_dy2 ** 2

        cos=(p2_dx1*p2_dx2+p2_dy1*p2_dy2)/(math.sqrt(length1)*math.sqrt(length2))
        p2_angle_1 = math.degrees(math.acos(cos))
        angle2.append(p2_angle_1)

    angle1 = sorted(angle1)
    angle2 = sorted(angle2)

    if angle1 != angle2:
        return False
    else:
        return True


#假设颜色相等，判断坐标个数（边的条数）  *
#颜色相等，判断边的长度是否相等
def are_identical_sets_of_coloured_pieces(pieces_1, pieces_2):
    #如果字典的长度不一样肯定是多了或者少了图形
    if len(pieces_1) != len(pieces_2):
        return False
    #如果1的keys不在2里面说明2少了一个碎片
    #如果1的keys在2里面，并且value的长度不相等，说明两个图形不一样
    for keys1 in pieces_1.keys():
        if not keys1 in pieces_2:
            return False
        elif keys1 in pieces_2:
            if len(pieces_1[keys1]) != len(pieces_2[keys1]):
                return False
    for keys1 in pieces_1.keys():
        if compare_angles(pieces_1[keys1],pieces_2[keys1]) != True:
            return False
    for keys1 in pieces_1.keys():
        if compare_edges(pieces_1[keys1],pieces_2[keys1]) != True:
            return False
    return True


def Get_Areas(coloured_pieces_1):
    areas = 0
    for values in coloured_pieces_1.values():
        area = 0
        if (len(values) < 3):
            return False
        for i in range(0, len(values) - 1):
            p1 = values[i]
            p2 = values[i + 1]
            triArea = (p1[0] * p2[1] - p2[0] * p1[1]) / 2
            area += triArea
        fn = (values[-1][0] * values[0][1] - values[0][0] * values[-1][1]) / 2
        areas+=abs(area+fn)
    return areas


def count_point(coloured_pieces_1,coloured_pieces_2):
    list1=[]
    list2=[]
    for values1 in coloured_pieces_1.values():
        for i in range(len(values1)):
            list1.append(values1[i])
    for values2 in coloured_pieces_2.values():
        for i in range(len(values2)):
            list2.append(values2[i])
    list1_2 = list1 + list2
    for i in list1_2:
        if list1_2.count(i) == 1:
            return False
    return True


def is_solution(coloured_pieces_1,coloured_pieces_2):
    if int(Get_Areas(coloured_pieces_1)) != int(Get_Areas(coloured_pieces_2)):
        return False
    if count_point(coloured_pieces_1,coloured_pieces_2) == False:
        return False
    return True

