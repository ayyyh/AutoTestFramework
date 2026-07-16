"""
订单模块（模拟）接口自动化测试
覆盖：查看购物车列表、创建购物车（模拟下单）
依赖：登录 Token（从 fixture 获取）
"""
import pytest
import requests
import allure
import time

CARTS_URL = "https://dummyjson.com/carts"


@allure.feature("订单模块")
@allure.story("查看购物车列表")
def test_get_carts(login_token):
    """
    测试获取所有购物车（需登录）
    """
    headers = {"Authorization": f"Bearer {login_token}"}

    with allure.step("发送 GET 请求到 /carts"):
        response = requests.get(CARTS_URL, headers=headers)

    with allure.step("验证状态码为 200"):
        assert response.status_code == 200, f"期望200，实际{response.status_code}"

    with allure.step("验证返回数据结构"):
        data = response.json()
        assert "carts" in data, "响应缺少 carts 字段"
        assert len(data["carts"]) > 0, "购物车列表为空"

        # 验证第一个购物车的基本结构
        first_cart = data["carts"][0]
        assert "id" in first_cart
        assert "products" in first_cart
        assert "total" in first_cart  # 订单总金额

    time.sleep(0.3)


@allure.feature("订单模块")
@allure.story("创建购物车（模拟下单）")
def test_create_cart(login_token):
    """
    测试创建新的购物车（模拟下单）
    要求：需要 userId 和商品列表
    """
    headers = {"Authorization": f"Bearer {login_token}"}

    # 请求体：用户 ID 为 1（emilys），添加两个商品
    payload = {
        "userId": 1,
        "products": [
            {"id": 1, "quantity": 2},
            {"id": 2, "quantity": 1}
        ]
    }

    with allure.step("发送 POST 请求到 /carts/add"):
        response = requests.post(f"{CARTS_URL}/add", json=payload, headers=headers)

    with allure.step("验证状态码为 201（资源创建成功）"):
        assert response.status_code == 201, f"期望201，实际{response.status_code}"

    with allure.step("验证返回的购物车数据"):
        data = response.json()
        assert "id" in data, "创建失败，缺少 id"
        assert "products" in data, "创建失败，缺少 products"
        assert len(data["products"]) == len(payload["products"]), "商品数量不匹配"

        # 验证第一个商品是否匹配
        first_product = data["products"][0]
        assert first_product["id"] == payload["products"][0]["id"], "商品ID不匹配"
        assert first_product["quantity"] == payload["products"][0]["quantity"], "数量不匹配"

    time.sleep(0.3)


@allure.feature("订单模块")
@allure.story("获取单个购物车详情")
def test_get_cart_detail(login_token):
    """
    测试获取指定购物车的详情（需登录）
    先获取购物车列表，取第一个 ID，再查详情
    """
    headers = {"Authorization": f"Bearer {login_token}"}

    # 步骤1：获取购物车列表
    with allure.step("获取购物车列表"):
        list_response = requests.get(CARTS_URL, headers=headers)
        assert list_response.status_code == 200
        carts_data = list_response.json()
        assert len(carts_data["carts"]) > 0, "没有购物车，无法测试详情"
        cart_id = carts_data["carts"][0]["id"]

    # 步骤2：查询该购物车详情
    with allure.step(f"获取购物车 ID={cart_id} 的详情"):
        detail_url = f"{CARTS_URL}/{cart_id}"
        detail_response = requests.get(detail_url, headers=headers)

    with allure.step("验证状态码为 200"):
        assert detail_response.status_code == 200

    with allure.step("验证详情数据与列表数据一致"):
        detail_data = detail_response.json()
        assert detail_data["id"] == cart_id, "ID 不一致"
        assert "products" in detail_data
        assert "total" in detail_data

    time.sleep(0.3)