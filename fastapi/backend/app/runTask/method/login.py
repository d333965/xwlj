import requests, json, time, hashlib, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from fastapi.responses import JSONResponse
# 登录获取accessToken, schoolId, campusId
def LoginGetInfo(userName, password):

    def get_dynamic_key(a1):
        # 提取子字符串
        dest = a1[2:5]
        nptr = a1[4:8]
        v2 = a1[-1]
        
        # 转换为整数
        dest_int = int(dest)
        nptr_int = int(nptr)
        v2_int = int(v2)
        
        # 计算差值
        v3 = dest_int - nptr_int
        if v3 >= 0:
            v4 = v3
        else:
            v4 = -v3
        
        # 左移操作
        v5 = v4 << v2_int
        
        # 固定字符串
        fixed_str = "402881ea7c39c5d5017c39d143a8062b"
        
        # 格式化字符串
        formatted_str = f"{v5}{fixed_str}"
        
        return formatted_str

    # 1. 获取当前时间戳
    timestamp = str(int(time.time() * 1000))


    # 2. 生成动态密钥
    dynamic_key = get_dynamic_key(timestamp)


    # 3. 将动态密钥转换为字节
    dynamic_key_bytes = dynamic_key[0:16].encode()


    # 结合字段
    data_to_hash = f"{userName}{password}1"

    # 添加盐
    salt = "itauVfnexHiRigZ6"
    data_to_hash_with_salt = data_to_hash + salt

    # 使用 SHA-1 计算哈希
    signdigital_hs = hashlib.sha1(data_to_hash_with_salt.encode()).hexdigest()


    # 6. 定义加密内容
    plaintext = json.dumps({
        "entrance": "1",
        "password": password,
        "phone": userName,
        "signDigital": signdigital_hs,
        "userName": userName,
        "authType": "Bearer",
        "baseUrl": "https://cpes.legym.cn/",
        "page": "",
        "type": ""
    })

    # 7. 将明文进行PKCS5Padding填充
    block_size = AES.block_size  # AES的块大小是16字节
    padded_plaintext = pad(plaintext.encode(), block_size)

    # 8. 使用AES算法和ECB模式进行加密
    key = dynamic_key_bytes  # 将动态密钥转换为字节
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)

    # 9. 将加密结果转换为Base64
    encrypted_base64 = base64.b64encode(ciphertext).decode('utf-8')

    # 10. 生成最终的JSON结构
    output = {
        "t": timestamp,
        "pyd": encrypted_base64
    }

    # 11. 定义请求的 URL
    url = "https://cpes.legym.cn/authorization/user/v2/manage/login"

    # 12. 定义请求头
    headers = {
        "Host": "cpes.legym.cn",
        "charset": "UTF-8",
        "content-type": "application/json",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/4.8.1"
    }

    # 13. 发送 POST 请求
    response = requests.post(url, headers=headers, json=output)

    # 14. 检查响应状态码
    if response.status_code == 200:
        # 15. 获取返回的 "t" 和 "pyd"
        response_data = response.json()
        received_timestamp = response_data["data"]["t"]
        encrypted_pyd = response_data["data"]["pyd"]

        # 16. 生成解密密钥
        decryption_key = get_dynamic_key(str(received_timestamp))
        decryption_key_bytes = decryption_key[0:16].encode()

        # 17. 解密 pyd
        ciphertext_bytes = base64.b64decode(encrypted_pyd)
        decryptor = AES.new(decryption_key_bytes, AES.MODE_ECB)
        decrypted_padded_plaintext = unpad(decryptor.decrypt(ciphertext_bytes), block_size)

        # 18. 打印解密结果
        login_response = decrypted_padded_plaintext.decode('utf-8')
        
        # 将 JSON 字符串解析为字典
        data = json.loads(login_response)

        # 提取所需的信息
        accessToken = data['accessToken']
        schoolId = data['schoolId']
        userId = data['id']
        return accessToken, schoolId, userId
    else:
        return "账号密码错误"


#获取学期ID
def getsemesterId(accessToken, schoolId):
    url = 'https://cpes.legym.cn/education/semester/getCurrent'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + accessToken,
        'Organization': schoolId,
        'User-Agent': 'okhttp/4.8.1'
    }
    body = {}
    response = requests.get(url, headers=headers, json=body)
    if response.status_code == 200:
        data = response.json()
        semesterId = data['data']['id']
        return semesterId
    else:
        print('获取semesterId失败', response)

def Oct_SecretKey(userId, schoolId):
    # 模拟从 userId 和 schoolId 提取子字符串
    dest = userId[3:6]  # 从 userId 的第 4 个字符开始，取 3 个字符
    v14 = schoolId[4:7]  # 从 schoolId 的第 5 个字符开始，取 3 个字符
    v13 = userId[9:12]   # 从 userId 的第 10 个字符开始，取 3 个字符

    # 硬编码的字符串
    static_key = "3e0783d6891a4a3e9521dcb6bb341560"

    # 拼接字符串
    running_key = f"{dest}{v14}{v13}{static_key}"

    # 提取前16个字符
    extracted_key = running_key[:16]
    
    # 将提取的字符串转换为hex格式
    hex_encoded_key = extracted_key.encode("utf-8").hex()
    
    return hex_encoded_key