import requests,random
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
###############跑步任务
def runTask( day_goals, accessToken, semesterId, routine_line,runType,OctSecretKey):
        ###################获取 limitationsGoalsSexInfoId
        url = "https://cpes.legym.cn/running/app/getRunningLimit"

        headers = {
            'Authorization': 'Bearer' + accessToken,
            "Host": "cpes.legym.cn",
            "charset": "UTF-8",
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.8.1"
        }

        body = {
            "semesterId": semesterId,
        }

        response = requests.post(url, headers=headers, json=body)
        limitationsGoalsSexInfoId = response.json().get("data", {}).get("limitationsGoalsSexInfoId")

        if runType == '定点跑':
            signPoint = [
                    {
                        "signPoint": "8a97812c870b919c018712d63af4669d",
                        "state": 0
                    },
                    {
                        "signPoint": "8a97812c870b919c018712d63af4669c",
                        "state": 0
                    },
                    {
                        "signPoint": "8a97812c870b919c018712d63af2668b",
                        "state": 0
                    }
                ]
        else:
            signPoint = []
        # 创建包含选项的列表
        selected_option = "Mate 40 Pro"
        random_number = day_goals + round(random.uniform(0, 0.2), 4)
        random_number_avePace = random.randint(420000, 500000) #改步频7`30~8`20
        result = random_number * random_number_avePace  # 相乘
        random_number_keepTime = int(result) // 1000  # 取千位以上的数值
        random_calorie = random.randint(100, 120)
        random_paceNumber = random.randint(3200,4000)

        effectiveMileage = random_number
        effectivePart = 1
        calorie = random_calorie
        avePace = random_number_avePace
        keepTime = random_number_keepTime
        paceNumber = random_paceNumber
        totalMileage = random_number
        totalPart = 0



        # 获取当前日期和时间，包括秒数
        current_datetime = datetime.now()
        current_datetime = current_datetime - timedelta(minutes=random.randint(1, 40))

        # 格式化时间，包括秒数
        endtime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # 将endtime字符串转换为datetime对象
        endtime_as_datetime = datetime.strptime(endtime, "%Y-%m-%d %H:%M:%S")

        # 计算endtime的前10分钟
        ten_minutes_ago = endtime_as_datetime - timedelta(seconds=keepTime)
        signTime_ago = endtime_as_datetime + timedelta(milliseconds=5000)
        # 格式化前10分钟的时间，包括秒数
        signTime = signTime_ago.strftime("%Y-%m-%d %H:%M:%S")
        starttime = ten_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

        # signdigital======================================================================
        import hashlib
        # 将字段值连接在一起
        data_to_hash = f"{effectiveMileage}{effectivePart}{starttime}{calorie}{avePace}{keepTime}{paceNumber}{totalMileage}{totalPart}"

        # 追加盐
        salt = "itauVfnexHiRigZ6"
        data_to_hash_with_salt = data_to_hash + salt

        # 使用SHA-1哈希算法计算哈希值
        signdigital_hs = hashlib.sha1(data_to_hash_with_salt.encode()).hexdigest()

        signdigital = signdigital_hs
        # ===================================================================================
        # oct======================================================================
        # 使用字典形式
        content_dict = {
            "rt":	runType,
            "lcs":	effectiveMileage,
            "bs":	paceNumber,
            "bf":	0,
            "zlc":	effectiveMileage,
            "tp":	0,
            "em":	effectiveMileage,
            "ep":	1,
            "uer":	"",
            "st":	starttime,
            "et":	endtime,
            "kll":	calorie,
            "ap":	avePace,
            "xq":	semesterId,
            "jf":	1,
            "lid":	limitationsGoalsSexInfoId,
            "sv":	"14",
            "app":	"3.10.0",
            "dt":	selected_option,
            "kt":	keepTime
        }

        # 手动构建JSON字符串，确保使用正确的缩进和制表符
        content_text = "{\n"
        for key, value in content_dict.items():
            if isinstance(value, str):
                content_text += f'\t"{key}":\t"{value}",\n'
            else:
                content_text += f'\t"{key}":\t{value},\n'
        content_text = content_text.rstrip(',\n') + "\n}"

        # 将Hex格式的密钥转换为字节数组
        key = bytes.fromhex(OctSecretKey)

        # 将JSON内容转换为字节数组，确保使用UTF-8编码
        content_bytes = content_text.encode('utf-8')

        # 使用AES/ECB/PKCS5Padding模式进行加密
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_bytes = cipher.encrypt(pad(content_bytes, AES.block_size))

        # 将加密后的字节数组转换为Base64格式
        encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
        # 将 Base64 字符串每 64 个字符插入一个换行符，并在末尾添加换行符
        oct = '\n'.join([encrypted_base64[i:i+64] for i in range(0, len(encrypted_base64), 64)]) + '\n'
        # ===================================================================================

        url = "https://cpes.legym.cn/running/app/v3/upload"

        headers = {
            "charset": "UTF-8",
            "authorization": "Bearer " + accessToken,
            "content-type": "application/json",
            "accept-encoding": "gzip",
            "user-agent": "okhttp/4.8.1"
        }

        body = {
            "appVersion": "3.10.0",
            "avePace": avePace,
            "calorie": calorie,
            "deviceType": selected_option,
            "effectiveMileage": effectiveMileage,
            "effectivePart": effectivePart,
            "endTime": endtime,
            "gpsMileage": random_number,
            "keepTime": keepTime,
            "limitationsGoalsSexInfoId": limitationsGoalsSexInfoId,
            "oct": oct,
            "paceNumber": paceNumber,
            "paceRange": 0,
            "routineLine":routine_line,
            "scoringType": 1,
            "semesterId": semesterId,
            "signDigital": signdigital,
            "signPoint": signPoint,
            "signTime": signTime,
            "startTime": starttime,
            "systemVersion": "14",
            "totalMileage": totalMileage,
            "totalPart": totalPart,
            "type": runType,
            "uneffectiveReason": ""
        }
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json().get("message")
        else:
            print('跑步请求失败',response.text)
