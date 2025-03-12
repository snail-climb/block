# coding=utf8

# 数据库操作提示
def db_ops_hint(db, table, is_success, msg=None):
    if is_success:
        if msg is not None:
            print(f"【数据库操作】目标: {db}.{table} 执行成功! 受影响行数: {msg}行")
        else:
            print(f"【数据库操作】目标: {db}.{table} 执行成功!")
    else:
        if msg is not None:
            print(f"【数据库操作】目标: {db}.{table} 执行失败!\n异常内容: {msg}")
        else:
            print(f"【数据库操作】目标: {db}.{table} 执行失败!")
