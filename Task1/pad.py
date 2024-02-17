import ast
import re
import pad_enhanced

# 정수와 리스트를 분리
def parse_input(input_str):
    # 정수와 리스트를 분리
    pattern = re.compile(r'(\d+)\s+(\[.*\])')
    
    match = pattern.match(input_str)
    
    if match:
        # 정수 부분과 리스트 부분 추출
        integer_part = int(match.group(1))
        list_part = eval(match.group(2))
        
        return integer_part, list_part
    else:
        return None

# 회전각으로 방향 판단
def determin_direction(angle):
    if angle == 0 :
        direction = ('Top', 'Vertical')
    elif angle == 90 :
        direction = ('Right', 'horizontal')
    elif angle == 180 :
        direction = ('Bottom', 'Vertical')
    elif angle == 270 :
        direction = ('Left', 'horizontal')
    
    return direction

# 축 회전한 후 exposed side 판단
def determin_exposed_side(pad_shape_len_half, componentY, centerY):
    gap_center_component = centerY - componentY
    
    # 센터가 부품보다 더 위에 위치   
    if gap_center_component >= 0:
        if pad_shape_len_half > gap_center_component:
            return 'Partial'
        else:
            return 'Exposed'
    # 센터가 부품보다 더 아래에 위치
    else:
        if pad_shape_len_half > gap_center_component * -1:
            return 'Partial'
        else:
            return 'Inner'

# Pad의 수 N
pad_num = int(input())

# 부품의 좌표 쌍(minX, minY, maxX, maxY)
component_coordinates = ast.literal_eval(input())

# 패드 형상 리스트, 각 패드 정보 리스트 구현
shape_of_pad_coordinates = [-1]
each_pad_datas = [-1]
cnt = 0
while True:
    input_data = input()
    idx, data = parse_input(input_data)
    if cnt == idx - 1: 
        # Pad Shape 종류의 인덱스와, 좌표 쌍 
        shape_of_pad_coordinates.append(data)
        cnt = idx
    else :
        # Pad의 id, Shape 종류, 회전 각도, 중심좌표쌍
        each_pad_datas.append(data)    
        cnt = -1
        if idx == pad_num:
          break

# 비즈니스 로직 
for i in range(1, pad_num+1):
    # 패드의 형상과 회전각이 주어졌을 때
    if len(each_pad_datas[i]) > 1:
        pad_shape_idx, angle, centerXY = each_pad_datas[i]
        direction = determin_direction(angle)
    # 패드의 형상과 회전각이 주어지지 않았을 때
    else:
        pad_shape_idx = 1
        centerXY = each_pad_datas[i][0]
        a, b, c, d = pad_enhanced.get_vertices(centerXY, abs(shape_of_pad_coordinates[1][0][0]), abs(shape_of_pad_coordinates[1][0][1]))
        vertices = [a, b, c, d]
        for j in range(4):
            vertices[j] = pad_enhanced.rotate_point(vertices[j])
        
        areas = pad_enhanced.area_per_section(vertices)
        direction = pad_enhanced.determin_direction(areas)

    # 수직/수평 여부에 따라서 exposed side 결정
    if direction[1] == 'Vertical':
        pad_shape_len_half = abs(shape_of_pad_coordinates[pad_shape_idx][0][1]) # y값을 패드 형상의 길이로 설정
        componentY = abs(component_coordinates[1][1]) # maxY값을 컴포넌트의 길이로 설정
        centerY = abs(centerXY[1])
    else: # 해당 방향으로 축 회전
        pad_shape_len_half = abs(shape_of_pad_coordinates[pad_shape_idx][0][1]) # y값을 패드 형상의 길이로 설정
        componentY = abs(component_coordinates[1][0]) # maxX값을 컴포넌트의 Y값으로 설정
        centerY = abs(centerXY[0])
    exposed = determin_exposed_side(pad_shape_len_half, componentY, centerY)
    print(i, direction[0], exposed)
    
    
    
    # 어려웠던 점 
    # 변수이름짓기, 축을 회전시켰다는 것을 가정한 것이 좀 헷갈리게 했음 (x랑 y랑 싹다 바꿔준다고 생각했는데 pad_shape_len_half는 항상 y값 그대로 들어감)