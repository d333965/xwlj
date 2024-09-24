# settings.py
from tortoise import Tortoise

TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',  # MySQL or Mariadb
            'credentials': {
                'host': '127.0.0.1',
                'port': '3306',
                'user': 'root',
                'password': '333965lq',
                'database': 'legym',
                'minsize': 1,
                'maxsize': 5,
                'charset': 'utf8mb4',
                "echo": True
            }
        },
    },
    'apps': {
        'models': {
            'models': ['app.mysql.models', "aerich.models"],  # 修改这里
            'default_connection': 'default'
        }
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}

def get_tortoise_config():
    return TORTOISE_ORM

# 删除这行
# Tortoise.init(config=get_tortoise_config())