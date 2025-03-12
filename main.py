# coding=utf8
from util.db_util import db_sync
from util.monitor_util import monitor

if __name__ == "__main__":
    # 数据库同步
    db_sync("test", "test_bak")
    # 监控推送
    monitor("""
        select '标题1', count(*) from test.xxx
        union all
        select '标题2', count(*) from test.xxx
    """, """
        select count(*) from test_bak.xxx
        union all
        select count(*) from test_bak.xxx
    """)
