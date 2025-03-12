# coding=utf8

from config.db_config import source_cursor, target_cursor
from config.webhook_config import webhook_prod
from util.robot_util import send_markdown_msg


def sql_exec(expect_sql, actual_sql):
    try:
        source_cursor.execute(expect_sql)
        expect_data = source_cursor.fetchall()
        target_cursor.execute(actual_sql)
        actual_data = target_cursor.fetchall()
    except Exception as e:
        print(f"【监控脚本】SQL执行失败: {e}")
    return expect_data, actual_data


# 监控(参数要求: expect_sql 仅有且必含标题和行数两列; actual_sql仅有且必含行数一列)
def monitor(expect_sql, actual_sql):
    try:
        expect_data, actual_data = sql_exec(expect_sql, actual_sql)
        body = ""
        row_num, succeeded_cnt, failed_cnt = 0, 0, 0
        for expect_row, actual_row in zip(expect_data, actual_data):
            row_num += 1
            expect_num, actual_num = expect_row[1], actual_row[0]
            if expect_num == actual_num:
                succeeded_cnt += 1
            body += f"> {expect_row[0]}: <font color=\"warning\">{expect_num}</font> ~ <font color=\"warning\">{actual_num}</font>\n"
        failed_cnt = row_num - succeeded_cnt
        warn_msg = "\n<font color=\"warning\">警告: 数据存在异常, 请及时处理</font>" if failed_cnt != 0 else ""
        content = f"""
            # <font color=\"info\">**数据监控**</font>
            ## 数据校验
            {body}
            ## 汇总
            > 成功: <font color=\"info\">{succeeded_cnt}</font> 失败: <font color=\"warning\">{failed_cnt}</font>\n\n注: (格式: 应该落表数据量 ~ 实际落表数据量){warn_msg}"""
        send_markdown_msg(webhook_prod, content)
    except Exception as e:
        send_markdown_msg(webhook_prod, "# <font color=\"warning\">**警告: 监控异常**</font>\n> 请及时处理")
        print(f"【监控脚本】异常: {e}")
