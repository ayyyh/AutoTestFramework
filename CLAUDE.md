# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 项目概述

针对 DummyJSON 登录接口（`POST https://dummyjson.com/auth/login`）的 API 集成测试套件。使用 pytest + YAML 数据驱动，每个测试发送登录请求并校验 API 响应，成功时进一步与本地 SQLite 数据库交叉校验用户邮箱。

## 项目结构

- `testcases/` — 测试用例（`test_main.py` 参数化主测试，`test_smoke.py` 冒烟测试）
- `utils/api_utils.py` — 公共函数：`check_login_result()` 校验 HTTP 响应，`verify_user_in_db()` 数据库交叉校验
- `data/data.yaml` — YAML 测试用例数据（用例通过 `desc` 字段标识）
- `conftest.py` — 共享 fixture：`db`（每个测试独立的 SQLite 连接）、`print_test_timings`（自动计时）
- `create_db.py` — 初始化本地 `test_db.db`，创建 `users` 表并插入 emilys 测试用户

## 常用命令

```bash
# 初始化本地测试数据库（运行测试前执行一次）
python create_db.py

# 运行所有测试
pytest testcases/ -v

# 按关键字运行单个测试（匹配 YAML 中的 "desc" 字段）
pytest testcases/ -v -k "正确账号密码"

# 仅运行冒烟测试
pytest testcases/test_smoke.py -v

# 并行执行（需安装 pytest-xdist）
pytest testcases/ -v -n auto

# 运行测试并生成 HTML 报告
pytest testcases/ --html=report.html --self-contained-html
```

## 架构

**数据流向：** `data/data.yaml` → pytest `@parametrize` → `test_login(db, case)` → HTTP POST → `check_login_result()` → （成功时）`verify_user_in_db()`

**两阶段校验：**
1. **API 检查**（`check_login_result`）：成功期望 200 + `accessToken`；失败期望非 200。
2. **数据库交叉校验**（`verify_user_in_db`）：登录成功时在 `users` 表中查用户名，断言邮箱与预期值一致。

**conftest.py fixture：**
- `db`（function 作用域）：每个测试独立的 SQLite 连接，测试结束自动关闭。
- `print_test_timings`（autouse=True）：自动为每个用例打印开始/结束时间和耗时。

## 依赖

- `pytest`、`pytest-html`（HTML 报告）、`pytest-xdist`（并行执行）
- `requests`（HTTP 客户端）
- `PyYAML`（YAML 测试用例加载）
- `sqlite3`（标准库）
