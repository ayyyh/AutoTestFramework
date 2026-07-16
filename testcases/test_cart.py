# testcases/test_cart.py
import pytest
import requests
import allure
import time

CART_URL = "https://dummyjson.com/carts/1"


@allure.feature("购物车模块")
@allure.story("查看购物车")
def test_get_cart(login_token):
    """
    测试查看购物车（依赖登录 Token）
    """
    headers = {"Authorization": f"Bearer {login_token}"}

    with allure.step("发送 GET 请求到 /carts/1"):
        response = requests.get(CART_URL, headers=headers)

    with allure.step("验证状态码为 200"):
        assert response.status_code == 200, f"期望200，实际{response.status_code}"

    with allure.step("验证购物车数据结构"):
        data = response.json()
        assert "id" in data, "购物车缺少 id"
        assert "products" in data, "购物车缺少 products"
        assert len(data["products"]) > 0, "购物车为空"

        # 验证第一个商品有必要的字段
        first_product = data["products"][0]
        assert "id" in first_product
        assert "title" in first_product
        assert "price" in first_product
        assert "quantity" in first_product  # 购物车独有字段
        assert "total" in first_product

    # 避免请求过快
    time.sleep(0.3)


@allure.feature("购物车模块")
@allure.story("购物车添加商品")
def test_add_to_cart(login_token):
    """
    测试向购物车添加商品（POST 请求）
    """
    headers = {"Authorization": f"Bearer {login_token}"}

    # DummyJSON 的添加购物车接口（示例，实际可能需要更多字段）
    add_url = "https://dummyjson.com/carts/add"
    payload = {
        "userId": 1,  # emilys 的用户 ID 是 1
        "products": [
            {"id": 1, "quantity": 2}
        ]
    }

    with allure.step(f"发送 POST 请求到 /carts/add"):
        response = requests.post(add_url, json=payload, headers=headers)

    with allure.step("验证状态码为 200"):
        assert response.status_code in [200,201]
        data = response.json()

    with allure.step("验证响应包含成功信息"):
        assert "id" in data
        assert "products" in data
        # 至少有一个商品
        assert len(data["products"]) > 0

    time.sleep(0.3)