import requests
import json
import pytest
import sqlite3

import yaml

url = "https://dummyjson.com/auth/login"

with open("data.yaml", "r", encoding="utf-8") as f:
    test_cases = yaml.safe_load(f)

# with open("data.json", "r", encoding="utf-8") as f:
#     test_cases = json.load(f)


@pytest.fixture()
def db():
    conn = sqlite3.connect("test_db.db")
    yield conn
    conn.close()


def check_login_result(response, expected):
    if expected == "success":
        if response.status_code == 200 and "accessToken" in response.json():
            return True, ""
        else:
            return False, f"期望成功，但状态码为 {response.status_code}"
    else:
        if response.status_code != 200:
            return True, ""
        else:
            return False, "期望失败，但竟然登录成功了"


def verify_user_in_db(conn, username, api_email):
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return False, f"数据库中找不到用户: {username}"
    db_email = result[0]
    if db_email == api_email:
        return True, "邮箱校验一致"
    else:
        return False, f"邮箱不一致，接口返回: {api_email}, 数据库: {db_email}"


@pytest.mark.parametrize("case", test_cases, ids=lambda c: c["desc"])
def test_login(db, case):
    print(f"👉 [本地修改] 测试：{case['desc']} (账号: '{case['username']}')")
    method = 'post'
    response = requests.request(method, url, json={"username": case["username"], "password": case["password"]})
    is_passed, error_msg = check_login_result(response, case["expect"])
    assert is_passed, error_msg
    if case["expect"] == "success" and response.status_code == 200:
        api_username = response.json().get("username", case["username"])
        is_db_ok, db_msg = verify_user_in_db(db, api_username, "emily.johnson@x.dummyjson.com")
        assert is_db_ok, db_msg
        print(f"   📊 数据库校验: {db_msg}")
    print(f"   ✅ 通过\n")
