# coding=utf8
import pymysql

# 源数据库配置
source_db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "port": 3306,
    "charset": "utf8mb4"
}

# 目标数据库配置
target_db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "123456",
    "port": 3306,
    "charset": "utf8mb4"
}

# 同库
connect = pymysql.connect(host=target_db_config["host"], user=target_db_config["user"],
                          password=target_db_config["password"], port=target_db_config["port"],
                          charset=target_db_config["charset"])
cursor = connect.cursor()

# 跨库
source_connect = pymysql.connect(host=source_db_config["host"], user=source_db_config["user"],
                                 password=source_db_config["password"], port=source_db_config["port"],
                                 charset=source_db_config["charset"])
source_cursor = source_connect.cursor()
target_connect = pymysql.connect(host=target_db_config["host"], user=target_db_config["user"],
                                 password=target_db_config["password"], port=target_db_config["port"],
                                 charset=target_db_config["charset"])
target_cursor = target_connect.cursor()
