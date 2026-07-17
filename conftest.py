import pytest
import sqlite3
import datetime
import requests
import os
# 全局禁用代理
os.environ['HTTP_PROXY'] = ''
os.environ['HTTPS_PROXY'] = ''
os.environ['NO_PROXY'] = '*'


@pytest.fixture(scope='function')
def db():
    # print(1)
    conn = sqlite3.connect("test_db.db")
    yield conn
    conn.close()
    # print(2)

# conftest.py 新增内容（放在现有 db fixture 后面）
@pytest.fixture(scope="session")
def login_token():
    """登录并返回 accessToken，session 级别只登录一次"""
    login_url = "https://dummyjson.com/auth/login"
    payload = {"username": "emilys", "password": "emilyspass"}
    response = requests.post(login_url, json=payload)
    assert response.status_code == 200
    token = response.json()["accessToken"]
    print(f"\n🔑 登录成功，Token 已获取（仅供购物车测试使用）")
    return token

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