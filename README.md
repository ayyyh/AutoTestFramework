# 电商全链路接口自动化测试框架

> 基于 Python + pytest + Requests 构建，覆盖登录、商品、购物车、订单核心业务链路，支持数据驱动、数据库校验、Allure 报告生成。

---

## 项目背景

本项目是一个**接口自动化测试实战项目**，模拟电商系统核心业务流程的接口验证。目标是通过自动化手段，快速回归核心链路，保障系统迭代过程中的接口质量。

---

## 技术栈

| 类别 | 工具/库 |
| :--- | :--- |
| 编程语言 | Python 3.8 |
| 测试框架 | pytest（参数化、fixture、标记） |
| 请求库 | Requests |
| 数据驱动 | PyYAML（YAML 格式测试数据） |
| 数据库校验 | SQLite（验证接口返回与落库数据一致性） |
| 测试报告 | Allure / pytest-html |
| 版本控制 | Git + GitHub |
| 持续集成（规划） | Jenkins |

---

## 项目结构
pythonProject/
├── testcases/
│ ├── test_main.py # 登录模块（含正向/逆向/数据库校验）
│ ├── test_products.py # 商品模块（列表/详情/搜索）
│ ├── test_cart.py # 购物车模块（查看/添加，依赖 Token）
│ └── test_order.py # 订单模块（查看/创建，依赖 Token）
├── utils/
│ └── api_utils.py # 公共工具（断言函数、数据库校验函数）
├── data/
│ └── data.yaml # YAML 格式测试数据
├── conftest.py # pytest 共享 fixture（数据库连接、Token 获取、计时器）
├── pytest.ini # pytest 配置文件（标记、默认参数）
├── requirements.txt # 项目依赖清单
├── create_db.py # 本地测试数据库初始化脚本
└── README.md

---

## 核心功能

### 1. 登录模块（`test_main.py`）
- **正向用例**：正确账号密码登录，验证返回 `accessToken`
- **逆向用例**：密码错误、用户不存在、用户名为空
- **数据库校验**：登录成功后，查询 SQLite 确认用户邮箱与接口返回一致

### 2. 商品模块（`test_products.py`）
- 商品列表查询（验证数据结构、字段完整性）
- 商品详情查询（参数化测试，覆盖多个商品 ID）
- 商品搜索（验证搜索结果包含关键字）

### 3. 购物车模块（`test_cart.py`）
- 查看购物车（依赖登录 Token）
- 添加商品到购物车（依赖 Token，验证返回状态码 201）

### 4. 订单模块（`test_order.py`）
- 查看购物车列表（依赖 Token）
- 创建购物车（模拟下单，依赖 Token，验证商品数量匹配）
- 获取购物车详情（依赖 Token，验证数据一致性）

---

