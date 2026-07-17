
import requests
import pytest
import yaml
from utils.api_utils import check_login_result,verify_user_in_db

url = "https://dummyjson.com/auth/login"

with open("data/data.yaml", "r", encoding="utf-8") as f:
    test_cases = yaml.safe_load(f)


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
