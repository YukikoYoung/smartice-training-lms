# SmartIce LMS 测试文档

## 📋 测试概述

本项目使用 **pytest** 作为测试框架,提供了完整的单元测试和集成测试覆盖。

### 测试文件结构

```
backend/tests/
├── README.md               # 本文档
├── conftest.py            # Pytest配置和共享夹具
├── test_auth.py           # 认证API测试
├── test_courses.py        # 课程API测试
└── test_exams.py          # 考试API测试
```

### 测试覆盖范围

- ✅ **认证模块** (test_auth.py)
  - 用户登录(正确密码、错误密码、不存在的用户)
  - 获取当前用户信息
  - Token验证
  - OAuth2表单登录

- ✅ **课程模块** (test_courses.py)
  - 课程列表查询
  - 课程详情获取
  - 按部门筛选
  - 课程搜索
  - 章节内容查询
  - 权限控制(管理员创建课程)

- ✅ **考试模块** (test_exams.py)
  - 考试列表和详情
  - 开始考试
  - 获取考试题目
  - 提交答案(正确/错误)
  - 查看考试结果
  - 权限验证

---

## 🚀 快速开始

### 安装测试依赖

```bash
cd backend
pip install pytest pytest-cov httpx
```

### 运行所有测试

```bash
pytest
```

### 运行特定测试文件

```bash
# 只测试认证模块
pytest tests/test_auth.py

# 只测试课程模块
pytest tests/test_courses.py

# 只测试考试模块
pytest tests/test_exams.py
```

### 运行特定测试类或函数

```bash
# 运行TestAuth类的所有测试
pytest tests/test_auth.py::TestAuth

# 运行单个测试函数
pytest tests/test_auth.py::TestAuth::test_login_success
```

---

## 📊 测试输出

### 详细输出模式

```bash
pytest -v
```

### 显示测试覆盖率

```bash
pytest --cov=app --cov-report=html
```

生成的覆盖率报告在 `htmlcov/index.html`

### 显示详细错误信息

```bash
pytest -vv --tb=long
```

---

## 🏷️ 测试标记(Markers)

使用标记可以选择性运行特定类型的测试:

```bash
# 只运行认证相关测试
pytest -m auth

# 只运行课程相关测试
pytest -m course

# 只运行考试相关测试
pytest -m exam

# 运行单元测试
pytest -m unit

# 运行集成测试
pytest -m integration
```

---

## 🧪 编写测试

### 使用夹具(Fixtures)

`conftest.py` 提供了常用的测试夹具:

```python
def test_example(client, auth_headers, test_user):
    """
    - client: FastAPI测试客户端
    - auth_headers: 已认证的请求头
    - test_user: 测试用户对象
    """
    response = client.get("/api/some-endpoint", headers=auth_headers)
    assert response.status_code == 200
```

### 可用夹具列表

| 夹具名 | 说明 | 作用域 |
|--------|------|--------|
| `db_session` | 测试数据库会话 | function |
| `client` | FastAPI测试客户端 | function |
| `test_organization` | 测试组织 | function |
| `test_position` | 测试职位 | function |
| `test_user` | 测试用户(L1员工) | function |
| `admin_user` | 管理员用户(L5+) | function |
| `auth_headers` | 普通用户认证头 | function |
| `admin_headers` | 管理员认证头 | function |

### 测试模板

```python
import pytest

@pytest.mark.course  # 添加标记
class TestNewFeature:
    """新功能测试类"""

    def test_success_case(self, client, auth_headers):
        """测试成功场景"""
        response = client.get("/api/endpoint", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "expected_field" in data

    def test_error_case(self, client):
        """测试错误场景"""
        response = client.get("/api/endpoint")  # 没有认证

        assert response.status_code == 401
```

---

## 🧰 常用命令

### 运行并生成HTML报告

```bash
pytest --html=report.html --self-contained-html
```

### 只运行失败的测试

```bash
pytest --lf  # last failed
```

### 停在第一个失败的测试

```bash
pytest -x
```

### 并行运行测试(需要pytest-xdist)

```bash
pip install pytest-xdist
pytest -n 4  # 使用4个进程
```

### 查看最慢的10个测试

```bash
pytest --durations=10
```

---

## 📝 测试数据

测试使用**内存SQLite数据库**,每个测试函数独立:

- ✅ 测试开始时创建数据库
- ✅ 测试结束后自动清理
- ✅ 各测试之间完全隔离
- ✅ 无需手动清理数据

### 测试用户

**普通用户** (test_user):
- 用户名: `testuser`
- 密码: `testpass123`
- 职位: 服务员(L1)
- 部门: 前厅

**管理员** (admin_user):
- 用户名: `admin`
- 密码: `admin123`
- 职位: 运营负责人(L5+)
- 部门: 管理层

---

## 🔍 调试测试

### 使用pdb调试

```python
def test_something(client):
    response = client.get("/api/endpoint")
    import pdb; pdb.set_trace()  # 在这里暂停
    assert response.status_code == 200
```

### 打印详细日志

```bash
pytest -s  # 显示print输出
pytest --log-cli-level=DEBUG  # 显示DEBUG日志
```

---

## ✅ 持续集成(CI)

### GitHub Actions示例

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          cd backend
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📈 测试覆盖率目标

| 模块 | 当前覆盖率 | 目标覆盖率 |
|------|-----------|-----------|
| 认证(auth) | ~80% | 90% |
| 课程(course) | ~70% | 85% |
| 考试(exam) | ~75% | 85% |
| 学习(learning) | ~0% | 80% |
| **总体** | **~60%** | **85%** |

---

## 🎯 后续计划

### 待添加的测试

- [ ] **学习进度API测试** (test_learning.py)
  - 开始课程学习
  - 完成章节
  - 查看学习进度
  - 学习统计

- [ ] **用户管理API测试** (test_users.py)
  - 用户CRUD
  - 角色权限

- [ ] **数据看板API测试** (test_dashboard.py)
  - 学习统计
  - 考试统计
  - 员工排行

- [ ] **性能测试** (test_performance.py)
  - API响应时间
  - 并发测试
  - 负载测试

---

## 📚 参考资料

- [Pytest官方文档](https://docs.pytest.org/)
- [FastAPI测试指南](https://fastapi.tiangolo.com/tutorial/testing/)
- [SQLAlchemy测试最佳实践](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

---

## 🤝 贡献指南

编写新测试时请遵循:

1. **命名规范**: 测试文件以`test_`开头
2. **清晰描述**: 测试函数名要说明测试内容
3. **适当标记**: 使用`@pytest.mark`添加标记
4. **文档注释**: 每个测试添加docstring说明
5. **独立测试**: 测试之间不应有依赖关系
6. **边界测试**: 测试正常、异常、边界情况

---

**最后更新**: 2025-11-15
**维护者**: SmartIce开发团队
