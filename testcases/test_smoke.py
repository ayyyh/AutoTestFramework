"""冒烟测试：仅测试 YAML 中正确账号密码那一条用例"""

import pytest
import requests
import sqlite3
import yaml

url = "https://dummyjson.com/auth/login"

# 加载测试用例，只取"正确账号密码"那一条
with open("data/data.yaml", "r", encoding="utf-8") as f:
    all_cases = yaml.safe_load(f)

smoke_case = [c for c in all_cases if c["desc"] == "正确账号密码"][0]


@pytest.fixture()
def db():
    conn = sqlite3.connect("test_db.db")
    yield conn
    conn.close()


def test_smoke_login(db):
    """冒烟测试：正确账号密码登录，验证 API 返回 200 + accessToken，并交叉校验数据库邮箱"""
    print(f"\n🚀 [冒烟测试] 用例: {smoke_case['desc']} (账号: '{smoke_case['username']}')")

    # 1. 发送登录请求
    response = requests.request(
        "post", url,
        json={"username": smoke_case["username"], "password": smoke_case["password"]}
    )

    # 2. 校验 API 响应
    assert response.status_code == 200, f"期望 200，实际 {response.status_code}"
    body = response.json()
    assert "accessToken" in body, "响应体缺少 accessToken"
    print(f"   ✅ API 校验通过 (状态码 200, 含 accessToken)")

    # 3. 数据库交叉校验
    api_username = body.get("username", smoke_case["username"])
    api_email = body.get("email", "")
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users WHERE username = ?", (api_username,))
    row = cursor.fetchone()
    assert row is not None, f"数据库中找不到用户: {api_username}"
    assert row[0] == "emily.johnson@x.dummyjson.com", \
        f"邮箱不一致: API={api_email}, DB={row[0]}"
    print(f"   ✅ 数据库校验通过 (邮箱一致: {row[0]})")
    print(f"   🎉 冒烟测试通过\n")
