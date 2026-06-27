# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 项目概述

针对 DummyJSON 登录接口（`POST https://dummyjson.com/auth/login`）的 API 集成测试套件。使用 pytest 框架，测试用例通过 YAML 文件参数化加载。每个测试发送登录请求，同时校验 API 响应和本地 SQLite 数据库的一致性。

## 常用命令

```bash
# 初始化本地测试数据库（运行测试前执行一次）
python create_db.py

# 运行所有登录测试
pytest test_main.py -v

# 按关键字运行单个测试（匹配 YAML 中的 "desc" 字段）
pytest test_main.py -v -k "正确账号密码"

# 运行测试并生成 HTML 报告
pytest test_main.py --html=report.html --self-contained-html
```

## 架构

**每个测试用例包含两阶段校验：**
1. **API 检查**（`check_login_result`）：校验 HTTP 状态码 — 成功时期望返回 200 且响应体包含 `accessToken`；失败时期望返回非 200。
2. **数据库交叉校验**（`verify_user_in_db`）：登录成功时，在本地 SQLite 的 `users` 表中查找返回的用户名，断言邮箱与预期值一致（`emily.johnson@x.dummyjson.com`）。

**数据流向：** `data.yaml` → pytest `@parametrize` → `test_login(db, case)` → HTTP POST → 响应校验 → （可选）数据库查询。

**重复文件：** `testcode.py` 与 `test_main.py` 内容完全相同。只需保留 `test_main.py`，应删除 `testcode.py`。

**数据库初始化：** `create_db.py` 创建 `test_db.db`，包含一张 `users` 表并插入一条测试用户数据（`emilys` / `emily.johnson@x.dummyjson.com`）。`db` fixture 为每个测试打开一个新的数据库连接。

## 依赖

- `pytest`、`pytest-html`（HTML 报告生成）
- `requests`（HTTP 客户端）
- `PyYAML`（YAML 测试用例加载）
- `sqlite3`（标准库，本地数据库）
