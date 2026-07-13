import pytest
import requests
import allure
import time  # 用于降低请求频率，避免触发限流

# 常量定义
PRODUCTS_URL = "https://dummyjson.com/products"
SEARCH_URL = f"{PRODUCTS_URL}/search"

# 测试数据：商品ID列表（可扩展）
TEST_PRODUCT_IDS = [1, 2, 3]


@allure.feature("商品模块")
@allure.story("商品列表")
def test_get_products_list():
    """测试获取商品列表"""
    with allure.step("发送 GET 请求到 /products"):
        response = requests.get(PRODUCTS_URL)

    with allure.step("验证状态码为 200"):
        assert response.status_code == 200, f"期望200，实际{response.status_code}"

    with allure.step("验证响应包含 products 字段且不为空"):
        data = response.json()
        assert "products" in data, "响应中缺少 products 字段"
        assert len(data["products"]) > 0, "products 列表为空"

    with allure.step("验证第一个商品包含关键字段"):
        first = data["products"][0]
        assert "id" in first
        assert "title" in first
        assert "price" in first


@allure.feature("商品模块")
@allure.story("商品详情")
@pytest.mark.parametrize("product_id", TEST_PRODUCT_IDS, ids=lambda x: f"商品ID_{x}")
def test_get_product_detail(product_id):
    """测试获取单个商品详情（参数化）"""
    with allure.step(f"发送 GET 请求到 /products/{product_id}"):
        response = requests.get(f"{PRODUCTS_URL}/{product_id}")

    with allure.step("验证状态码为 200"):
        assert response.status_code == 200

    with allure.step("验证返回的商品 ID 与请求一致"):
        data = response.json()
        assert data["id"] == product_id, f"期望ID {product_id}，实际 {data['id']}"

    with allure.step("验证商品包含关键字段"):
        assert "title" in data
        assert "price" in data
        assert "description" in data

    # 降低请求频率，避免触发服务端限流
    time.sleep(0.3)


@allure.feature("商品模块")
@allure.story("商品搜索")
def test_search_products():
    """测试搜索商品（query 参数）"""
    keyword = "phone"

    with allure.step(f"发送 GET 请求到 /products/search?q={keyword}"):
        response = requests.get(SEARCH_URL, params={"q": keyword})

    with allure.step("验证状态码为 200"):
        assert response.status_code == 200

    with allure.step("验证返回结果包含搜索关键字"):
        data = response.json()
        assert "products" in data
        assert len(data["products"]) > 0, "搜索结果为空"
        # 验证至少一个商品的标题包含关键字（不区分大小写）
        found = any(keyword.lower() in p["title"].lower() for p in data["products"])
        assert found, f"没有找到标题包含 '{keyword}' 的商品"