from . import schoolRoutes
import math
import random
import json

def getRouteLine(schoolName, rounds):
    # 选择路线
    if schoolName == '川农成都':
        routineLine_Data = schoolRoutes.川农成都
    elif schoolName == '川农雅安':
        routineLine_Data = schoolRoutes.川农雅安
    elif schoolName == '川农都江堰':
        routineLine_Data = schoolRoutes.川农都江堰
    # 电子科大两校区
    elif schoolName == '电子科大清水河':
        routineLine_Data = schoolRoutes.电子科大清水河
    elif schoolName == '电子科大沙河':
        routineLine_Data = schoolRoutes.电子科大沙河
    # 电子科大成都学院
    elif schoolName == '电子科大成都学院':
        routineLine_Data = schoolRoutes.电子科大成都学院
    # 西南石油两校区
    elif schoolName == '西油成都':
        routineLine_Data = schoolRoutes.西油成都
    elif schoolName == '西油南充':
        routineLine_Data = random.choice(schoolRoutes.西油南充)
    # 重庆交通大学
    elif schoolName == '重庆交通':
        routineLine_Data = schoolRoutes.重庆交通
    # 轻化工三校区
    elif schoolName == '轻化工李白河':
        routineLine_Data = schoolRoutes.轻化工李白河
    elif schoolName == '轻化工汇南':
        routineLine_Data = schoolRoutes.轻化工汇南
    elif schoolName == '轻化工宜宾':
        routineLine_Data = schoolRoutes.轻化工宜宾
    # 中飞院两校区
    elif schoolName == '中飞院本校':
        routineLine_Data = random.choice(schoolRoutes.中飞院本校)
    elif schoolName == '中飞院天府':
        routineLine_Data = schoolRoutes.中飞院天府
    # 四川卫康
    elif schoolName == '四川卫康':
        routineLine_Data = schoolRoutes.四川卫康
    # 成都大学
    elif schoolName == '成都大学':
        routineLine_Data = random.choice(schoolRoutes.成都大学)
    # 川北医学院
    elif schoolName == '川北医学院':
        routineLine_Data = schoolRoutes.川北医学院
    else:
        raise ValueError("未知的学校名称")

    # 生成routineLine
    def calculate_distance(coord1, coord2):
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        radius = 6371000  # 地球半径，单位米

        # 将经纬度转换为弧度
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # 使用 Haversine 公式计算距离
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = radius * c

        return distance

    json_str = json.dumps(routineLine_Data)
    combined_json_data = json.loads(json_str)
    lag = []

    for i in range(rounds):
        for point in combined_json_data:
            random_number = ''.join(random.choices('0123456789', k=8))
            lat_offset = random.uniform(-0.00001, 0.00001)
            lon_offset = random.uniform(-0.00001, 0.00001)
            point["latitude"] = float(f"{point['Latitude']}{random_number}") + lat_offset
            point["longitude"] = float(f"{point['Longitude']}{random_number}") + lon_offset
            lag.append(point)
    
    first_point = lag[0]
    lag.append(first_point)
    new_points = []

    for i in range(len(lag) - 1):
        point1, point2 = lag[i], lag[i + 1]
        distance = calculate_distance((point1["latitude"], point1["longitude"]),
                                      (point2["latitude"], point2["longitude"]))

        step_length = 10
        num_points = int(distance / step_length)

        for j in range(num_points):
            fraction = (j + 1) / (num_points + 1)
            lat_offset = random.uniform(-0.00002, 0.00002)
            lon_offset = random.uniform(-0.00002, 0.00002)
            lat = point1["latitude"] + fraction * (point2["latitude"] - point1["latitude"]) + lat_offset
            lon = point1["longitude"] + fraction * (point2["longitude"] - point1["longitude"]) + lon_offset
            new_points.append({"latitude": lat, "longitude": lon})

    new_points.append({"latitude": lag[-1]["latitude"], "longitude": lag[-1]["longitude"]})

    new_points_json = []

    for point in new_points:
        new_point_json = {
            "latitude": str(point["latitude"]),
            "longitude": str(point["longitude"])
        }
        new_points_json.append(new_point_json)

    routineLine = new_points_json
    return routineLine
