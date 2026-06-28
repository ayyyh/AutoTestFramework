import pytest
import sqlite3
import datetime

@pytest.fixture(scope='function')
def db():
    print(1)
    conn = sqlite3.connect("test_db.db")
    yield conn
    conn.close()
    print(2)

# conftest.py
@pytest.fixture(autouse=True)
def print_test_timings():
    # 前置：用例开始前执行
    start = datetime.datetime.now()
    print(f"\n⏰ 用例开始时间: {start.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
    yield
    # 后置：用例结束后执行
    end = datetime.datetime.now()
    duration = (end - start).total_seconds()
    print(f"⏰ 用例结束时间: {end.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}  耗时: {duration:.3f}秒")