# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概述

**SmartIce LMS** - 餐饮运营企业培训系统（MVP开发阶段）

- **行业领域**: 餐饮运营管理
- **核心目标**: 通过数字化培训提升员工技能、降低培训成本、提高运营效率
- **技术栈**: FastAPI + SQLAlchemy + SQLite (后端) / React 19 + Vite 7 + TypeScript (前端)
- **当前进度**: 后端100%，前端40%，内容0%（正在开发中）

---

## 快速开始

### 后端启动（端口8000）

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 初始化数据库和示例数据
python3 scripts/init_data.py      # 创建组织、用户、岗位
python3 scripts/init_courses.py   # 导入2门课程

# 启动后端
python3 main.py  # http://localhost:8000

# 访问API文档
open http://localhost:8000/docs
```

### 前端启动（端口5173）

```bash
cd frontend
npm install
npm run dev  # http://localhost:5173
```

### 测试账号

| 用户名 | 密码 | 角色 | 职级 |
|--------|------|------|------|
| admin | admin123 | 运营负责人 | L5+ |
| store_mgr | 123456 | 店长 | L4 |
| waiter001 | 123456 | 服务员 | L1 |

---

## 项目架构

### 后端目录结构（FastAPI）

```
backend/
├── app/
│   ├── core/          # 核心配置
│   │   ├── config.py      # 环境变量配置
│   │   ├── database.py    # SQLAlchemy引擎
│   │   └── security.py    # JWT + bcrypt
│   ├── models/        # 数据模型（17个表，已100%完成）
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── position.py
│   │   ├── course.py
│   │   ├── exam.py
│   │   └── learning.py
│   ├── schemas/       # Pydantic验证（已100%完成）
│   ├── services/      # 业务逻辑（已100%完成）
│   ├── routers/       # API端点（已100%完成）
│   │   ├── auth.py
│   │   ├── course.py
│   │   ├── exam.py
│   │   └── learning.py
│   └── utils/
├── scripts/           # 数据初始化脚本
└── main.py           # 应用入口
```

### 前端目录结构（React 19）

```
frontend/src/
├── pages/            # 页面组件（已完成5个）
│   ├── LoginPage.tsx
│   ├── CoursesPage.tsx
│   ├── CourseDetailPage.tsx
│   ├── ExamPage.tsx
│   └── DashboardPage.tsx
├── components/       # 通用组件
│   └── Layout.tsx
├── api/              # API集成（已完成）
│   ├── client.ts
│   ├── auth.ts
│   └── index.ts
├── contexts/         # React Context
│   └── AuthContext.tsx
├── types/            # TypeScript类型定义
└── App.tsx          # 路由配置
```

---

## 核心概念

### 6级职级体系

```
L5+ (运营负责人) → L5 (区域经理) → L4 (店长/厨师长)
→ L3 (主管) → L2 (骨干员工) → L1 (基层员工)
```

### 17个数据库表

**组织架构（4表）**：users, regions, stores, positions
**课程体系（3表）**：courses, chapters, contents
**考试系统（2表）**：exams, questions
**学习追踪（5表）**：course_progress, chapter_progress, exam_records, daily_quiz_records, value_assessments
**学习路径（3表）**：learning_paths, learning_path_courses, course_prerequisites

### 补考机制

- **最大尝试次数**: 3次
- **补考冷却期**: 3天
- **自动计算**: `next_retake_at`字段（当前时间 + 冷却期）
- **实现位置**: `exam_records`表 + `exam_service.py`

### 4大价值观

1. **以勤劳者为本** (VALUE_DILIGENCE)
2. **帮助顾客** (VALUE_CUSTOMER)
3. **高效协作** (VALUE_COLLABORATION)
4. **平等透明** (VALUE_TRANSPARENCY)

考试题目20-30%为价值观题，主管定期通过`value_assessments`表打分。

---

## 常用命令

### 后端开发

```bash
# 重置数据库（开发环境）
rm backend/training_lms.db
python3 backend/main.py  # 自动创建表结构

# 初始化数据
python3 backend/scripts/init_data.py      # 组织和用户
python3 backend/scripts/init_courses.py   # 课程内容

# 热重载模式（开发，默认）
RELOAD=true python3 main.py

# 生产模式（关闭热重载）
RELOAD=false python3 main.py

# 测试API
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 前端开发

```bash
# 开发模式（热重载）
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 预览生产构建
npm run preview
```

---

## API端点（已100%完成）

### 认证系统（/api/auth）
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录（返回JWT）
- `POST /api/auth/login/form` - OAuth2标准登录
- `GET /api/auth/me` - 获取当前用户信息

### 课程管理（/api/courses）
- `GET /api/courses` - 课程列表（分页、筛选）
- `GET /api/courses/{id}` - 课程详情
- `POST /api/courses` - 创建课程
- `PUT /api/courses/{id}` - 更新课程
- `DELETE /api/courses/{id}` - 删除课程
- `GET /api/courses/{id}/chapters` - 章节列表
- `POST /api/courses/{id}/chapters` - 创建章节
- `GET /api/courses/{course_id}/chapters/{chapter_id}/contents` - 内容列表

### 考试系统（/api/exams）
- `GET /api/exams` - 考试列表
- `GET /api/exams/{id}` - 考试详情
- `POST /api/exams` - 创建考试
- `POST /api/exams/{id}/start` - 开始考试
- `POST /api/exams/{id}/submit` - 提交答案
- `GET /api/exams/{id}/result` - 查看成绩
- `GET /api/exams/{id}/questions` - 获取题目

### 学习进度（/api/learning）
- `POST /api/learning/courses/{id}/start` - 开始学习
- `POST /api/learning/chapters/{id}/complete` - 完成章节
- `GET /api/learning/progress` - 学习进度
- `GET /api/learning/stats` - 学习统计

---

## 开发工作流

### 后端API开发（5步流程）

1. **在`models/`定义SQLAlchemy模型**
2. **在`schemas/`创建Pydantic验证Schema**
3. **在`services/`实现业务逻辑**
4. **在`routers/`创建API端点**
5. **在`main.py`注册路由**

示例：
```python
# 1. models/course.py
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), comment="课程标题")

# 2. schemas/course.py
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)

# 3. services/course_service.py
def create_course(db: Session, course_data: CourseCreate) -> Course:
    course = Course(**course_data.dict())
    db.add(course)
    db.commit()
    return course

# 4. routers/course.py
@router.post("/", response_model=CourseResponse)
def create_course_api(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_course(db, course_data)

# 5. main.py
app.include_router(course.router, prefix="/api/courses", tags=["courses"])
```

### 前端页面开发

1. 在`pages/`创建页面组件
2. 在`api/`添加API调用函数
3. 在`App.tsx`添加路由配置
4. 测试数据加载和交互

---

## 代码规范

### 命名约定
- **文件名**: 小写+下划线 (`user.py`, `course_service.py`)
- **类名**: 大驼峰 (`User`, `CourseProgress`)
- **函数名**: 小写+下划线 (`get_current_user`, `create_course`)
- **常量**: 大写+下划线 (`SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`)

### 必须遵守
1. 所有API端点必须有Docstring
2. 所有数据库字段必须有`comment`
3. 使用类型注解（Type Hints）
4. 使用Enum而非字符串常量
5. 数据库关系使用`relationship()`，避免手动JOIN

---

## 当前开发状态（2025-11-14）

### ✅ 已完成（约45%）

**后端（100%）**
- 17个数据表设计完成
- 认证系统（JWT + bcrypt）
- 所有API端点（auth、course、exam、learning）
- 数据库自动创建和初始化脚本

**前端（40%）**
- 5个核心页面完成
- API集成层完成
- 认证上下文管理完成
- Layout组件完成

### ❌ 待开发（P0优先级）

1. **题库生成**（0/556道题） - **最大瓶颈**
2. **课程内容文件**（0/23个markdown文件）
3. **StudyPage**（章节学习页面）- 员工无法学习内容
4. **管理后台**（用户管理、课程管理、考试管理、数据看板）
5. **测试覆盖**（当前0%）

### 知识库资源（待转化）

- `knowlege/前厅合并文档.md` (1,660行)
- `knowlege/厨房合并文档.md` (3,573行)
- `knowlege/企业价值观优化版.md` (393行)
- `knowlege/人才梯队及发展路径.md` (2,048行)

**总计9,681行运营标准文档，需转化为课程和题目**

---

## 常见问题排查

### 后端启动失败

**端口被占用**
```bash
# 修改main.py端口号
uvicorn.run("main:app", host="0.0.0.0", port=8001)
```

**依赖安装失败**
```bash
# 使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**数据库表不存在**
```bash
# 删除旧数据库重新创建
rm backend/training_lms.db
python3 backend/main.py
python3 backend/scripts/init_data.py
```

### 前端CORS错误

- 确保后端运行在`http://localhost:8000`
- 检查浏览器控制台具体错误
- CORS已配置支持`localhost:5173`等常见开发端口

### 数据库迁移

**开发环境**: 删除`.db`文件重建（简单快速）
**生产环境**: 使用Alembic管理迁移（`pip install alembic`）

---

## 生产部署注意事项

⚠️ **必须修改的配置**

1. **SECRET_KEY**（生成强随机密钥）
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **CORS配置**（限制为实际域名）
   ```python
   allow_origins=["https://training.your-domain.com"]
   ```

3. **DEBUG模式**（关闭）
   ```bash
   DEBUG=False
   ```

4. **数据库**（切换到PostgreSQL）
   ```bash
   DATABASE_URL=postgresql://user:pass@localhost/training_lms
   ```

---

## 相关文档

- **PRD**: `PRD-SmartIce-培训工具-LMS.md` - 完整产品需求文档（31,000+ tokens，分段读取）
- **设计**: `设计.md` - 技术架构、数据模型、UI/UX设计
- **计划**: `计划.md` - 12-13周MVP开发计划
- **README**: `README.md` - 项目介绍和快速开始

**GitHub**: https://github.com/YukikoYoung/smartice-training-lms

---

## 技术栈版本

### 后端
- Python 3.8+ (测试环境3.14)
- FastAPI >= 0.104.0
- SQLAlchemy >= 2.0.23
- Pydantic >= 2.10.0
- python-jose >= 3.3.0 (JWT)
- bcrypt >= 5.0.0

### 前端
- React 19.2.0
- Vite 7.2.2
- TypeScript 5.9.3
- React Router 7.9.6
- Axios 1.13.2

### 数据库
- SQLite (开发)
- PostgreSQL 15+ (生产)
