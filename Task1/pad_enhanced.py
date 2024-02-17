import math

def get_vertices(center, pad_width, pad_hight):
    x, y = center
    return (x-pad_width, y+pad_hight), (x+pad_width, y+pad_hight), (x+pad_width, y-pad_hight), (x-pad_width, y-pad_hight)

# 시계방향으로 45도 회전
def rotate_point(point):
    x, y = point
    angle_radians = math.radians(-45)
    
    x_rotated = x * math.cos(angle_radians) - y * math.sin(angle_radians)
    y_rotated = x * math.sin(angle_radians) + y * math.cos(angle_radians)

    return round(x_rotated, 1), round(y_rotated, 1)

# 교점의 범위 제한해주기, 범위를 벗어나면 false
# input: 패드의 좌표 abcd, 교졈(x, y) output: T/F
def check_range(vertices, point):
    a, b, c, d = vertices
    x, y = point
    
    minX, minY, maxX, maxY = min(a[0], b[0], c[0], d[0]), min(a[1], b[1], c[1], d[1]), max(a[0], b[0], c[0], d[0]), max(a[1], b[1], c[1], d[1])
    if (minX <= x <= maxX) and (minY <= y <= maxY):
        return True
    else:
        return False
    
# 어느 사분면에 속하는 점인지 체크    
# return value ex)[1,4] -> 1, 4 사분면에 속하는 점
def check_section(point):
    x, y = point
    section = []
    if x >= 0 and y >=0:
        section.append(1)
    if x >= 0 and y <=0:
        section.append(2)
    if x <= 0 and y <=0:
        section.append(3)
    if x <= 0 and y >=0:
        section.append(4)    
    return section
    
# 두 점으로 이루어진 직선과 x, y 절편의 교점 찾기
def find_intersection(x1, y1, x2, y2):
    # 기울기 계산
    if x2 - x1 != 0 :
      m = (y2 - y1) / (x2 - x1) 
    else:
      float('inf')  # 기울기가 무한대일 경우를 고려
    
    # 직선의 방정식: y - y1 = m(x - x1)
    # x축과의 교점 계산: y = 0
    if m != 0:
      x_intercept = x1 - y1 / m 
    else:
      x_intercept = x1 
    
    # y축과의 교점 계산: x = 0
    y_intercept = y1 - m * x1
    
    return (x_intercept, 0), (0, y_intercept)

# 절편과의 교점과 꼭지점 모조리 찾아서 사분면 구분하여 넣기
# 순서 중요! 1, 3 사분면 -> y절편, 꼭짓점, x절편, 0
# 순서 중요! 2, 4 사분면 -> x절편, 꼭짓점, y절편, 0
def get_section_points(vertices):
    section_points = [[], [], [], [], []]
    intercept_x = [[], [], [], [], []]
    intercept_y = [[], [], [], [], []]
    # 절편과의 교점 모조리 찾아서 넣기
    for i in range(len(vertices)):
        
        # 각 사분면에 해당하는 꼭지점 찾아서 넣기
        for section in check_section(vertices[i]):
            section_points[section].append(vertices[i])
        
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
    
        x_intercept, y_intercept = find_intersection(x1, y1, x2, y2)

        
        if check_range(vertices, x_intercept) :
            for section in check_section(x_intercept):
                intercept_x[section].insert(0, x_intercept)
                
        if check_range(vertices, y_intercept) :
            for section in check_section(y_intercept):
                intercept_y[section].append(y_intercept)
                    
    for i in range(1, 5):
        if i == 1:
            intercept_x[i].sort(reverse=True)
            intercept_y[i].sort()
            section_points[i] = intercept_y[i] + section_points[i] + intercept_x[i] + [(0,0)]
        elif i == 2:
            intercept_x[i].sort()
            intercept_y[i].sort()
            section_points[i] = intercept_x[i] + section_points[i] + intercept_y[i] + [(0,0)]
        elif i == 3:
            intercept_x[i].sort()
            intercept_y[i].sort(reverse=True)
            section_points[i] = intercept_y[i] + section_points[i] + intercept_x[i] + [(0,0)]
        elif i == 4:
            intercept_x[i].sort(reverse=True)
            intercept_y[i].sort(reverse=True)
            section_points[i] = intercept_x[i] + section_points[i] + intercept_y[i] + [(0,0)]
            
    for i in range(1, 5):
        section_points[i] = list(section_points[i])
            
    return section_points

# 특정 섹션의 도형 면적 구하기 
def area_per_section(vertices):
    section_points = get_section_points(vertices)
    
    area_per_sections = [-1, 0, 0, 0, 0]
    # 사분면 한번씩 돌기
    idx = 0
    for points_per_section in section_points:
        
        area = 0.0
        n = len(points_per_section)
        
        if n < 2:
            idx += 1
            continue
        
        # 각 사분면에 존재하는 점들로 면적 구하기
        for i in range(n):
            x1, y1 = points_per_section[i]
            x2, y2 = points_per_section[(i + 1) % n]
            area += (x1 * y2 - x2 * y1)

        area_per_sections[idx] = abs(area) / 2.0
        idx += 1
        
    return area_per_sections  

# 섹션당 면적으로 방향을 계산
def determin_direction(area_per_sections):
    max_value = max(area_per_sections)
    directions = [-1, ('Top', 'Vertical'), ('Right', 'horizontal'), ('Bottom', 'Vertical'), ('Left', 'horizontal')]
    # 방향이 2개 이상일떄
    if area_per_sections.count(max_value) > 1:
        section_idxs = [index for index, value in enumerate(area_per_sections) if value == max_value]
        direction = ''
        for idx in section_idxs:
            direction += directions[idx][0]
        if set(section_idxs) == {1, 3}: # topBottom일때는 수평일 수 없음
            direction = (direction, 'Vertical')
        else: # 나머지 경우는 안따져도 되니까 다 수평
            direction = (direction, 'horizontal')
    else:
        direction = directions[area_per_sections.index(max_value)]
    return direction

# 여기서는 도형의 좌표를 주면 그 도형의 사분면 별 면적과, Direction을 알려줌
if __name__ == "__main__":
    # vertices = [(1, 2), (2, 1), (-1, -2), (-2, -1)]  
    vertices = [(4, 1), (6, 0), (3, -5), (1, -4)] 

    print(area_per_section(vertices))
    print(determin_direction(area_per_section(vertices)))
    # 다각형과 직선의 교점 찾기
    # intersection_points = get_section_points(vertices)
    # print("다각형과 직선의 범위내 교점:", intersection_points)

    # 각 사분면에 속하는 꼭짓점의 개수 계산
    # quadrant_counts = count_vertices_in_quadrants(vertices)
    # print("각 사분면에 속하는 꼭짓점의 개수:", quadrant_counts)

    # for i in range(4):
    #     vertices[i] = rotate_point(vertices[i])
    # print(vertices)