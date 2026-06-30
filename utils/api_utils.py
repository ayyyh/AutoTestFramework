import pytest
import sqlite3
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