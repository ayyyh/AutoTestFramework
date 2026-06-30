# 接口自动化测试框架

## 技术栈
- Python + Requests + pytest
- YAML 数据驱动
- SQLite 数据库校验
- pytest-xdist 并行执行

## 项目结构
- testcases/ ：存放所有测试用例
- utils/     ：公共工具函数（断言、数据库操作）
- data/      ：YAML 格式测试数据
- conftest.py：共享 fixture（数据库连接、计时器）

## 快速开始
1. 运行 `create_db.py` 初始化本地测试数据库
2. 执行 `pytest testcases/ -v` 运行所有用例
3. 执行 `pytest -n auto` 并行运行（需安装 pytest-xdist）
