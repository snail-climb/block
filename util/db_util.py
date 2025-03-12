# coding=utf8
from config.db_config import connect, cursor, source_cursor, target_connect, target_cursor
from util.common_util import db_ops_hint


# 数据库同步
def db_sync(source_db, target_db):
    print("-------- -------- -------- -------- START -------- -------- -------- --------")
    table_list = ()
    try:
        target_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {target_db}")
        target_cursor.execute(f"USE {target_db}")
        source_cursor.execute(f"SHOW TABLES FROM {source_db}")
        table_list = source_cursor.fetchall()
        for table_row in table_list:
            table = table_row[0]
            source_cursor.execute(f"SHOW CREATE TABLE {source_db}.{table}")
            ddl_list = source_cursor.fetchall()
            for ddl_row in ddl_list:
                # ddl = ddl_row[1].replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
                ddl = ddl_row[1]
                target_cursor.execute(ddl)
                source_cursor.execute(f"DESCRIBE {source_db}.{table}")
                source_columns = [f"`{column[0]}`" for column in source_cursor.fetchall()]
                columns = ", ".join(source_columns)
                placeholders = ", ".join(["%s"] * len(source_columns))
                cross_db_data_sync(target_db,
                                   table,
                                   f"SELECT * FROM {source_db}.{table}",
                                   f"INSERT INTO {target_db}.{table} ({columns}) VALUES ({placeholders})")
        target_connect.commit()
        db_ops_hint(target_db, table_list, True)
    except Exception as e:
        db_ops_hint(target_db, table_list, False, e)
    print("-------- -------- -------- -------- E N D -------- -------- -------- --------")


# 同库: 表数据同步 (INSERT INTO ... SELECT ...)
def same_db_data_sync(db, table, main_sql, pre_sql=None):
    try:
        if pre_sql is not None:
            cursor.execute(pre_sql)
        affected_rows = cursor.execute(main_sql)
        connect.commit()
        db_ops_hint(db, table, True, affected_rows)
    except Exception as e:
        db_ops_hint(db, table, False, e)


# 跨库: 表数据同步 (INSERT INTO ...; SELECT ...;)
def cross_db_data_sync(target_db, target_table, source_sql, target_sql, pre_sql=None, is_enable_transaction=False):
    source_data, target_data = (), ()
    try:
        if is_enable_transaction:
            target_cursor.execute(f"SELECT * FROM {target_db}.{target_table}")
            target_data = target_cursor.fetchall()
        if pre_sql is not None:
            target_cursor.execute(pre_sql)
        source_cursor.execute(source_sql)
        source_data = source_cursor.fetchall()
        affected_rows = target_cursor.executemany(target_sql, source_data)
        target_connect.commit()
        db_ops_hint(target_db, target_table, True, affected_rows)
    except Exception as e:
        if is_enable_transaction:
            target_cursor.execute(f"TRUNCATE TABLE {target_db}.{target_table}")
            target_cursor.executemany(target_sql, target_data)
            target_connect.commit()
        db_ops_hint(target_db, target_table, False, e)
