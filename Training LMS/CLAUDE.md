# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 项目概述

**SmartIce LMS** - 餐饮运营企业培训系统（MVP开发阶段）

- **行业领域**: 餐饮运营管理
- **核心目标**: 通过数字化培训提升员工技能、降低培训成本、提高运营效率
- **技术栈**: FastAPI + SQLAlchemy + SQLite (后端) / React 19 + Vite 7 + TypeScript (前端)
- **当前进度**: 后端100%，前端90%，内容20%（正在开发中）

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
│   │   ├── learning.py
│   │   ├── notification.py
│   │   ├── note.py
│   │   ├── wrong_question.py
│   │   └── certificate.py
│   ├── schemas/       # Pydantic验证（已100%完成）
│   ├── services/      # 业务逻辑（已100%完成）
│   ├── routers/       # API端点（已100%完成）
│   │   ├── auth.py
│   │   ├── course.py
│   │   ├── exam.py
│   │   ├── learning.py
│   │   ├── stats.py
│   │   ├── user.py
│   │   └── feature.py    # 辅助功能（通知、笔记、错题本等）
│   └── utils/
├── scripts/           # 数据初始化脚本
└── main.py           # 应用入口
```

### 前端目录结构（React 19）

```
frontend/src/
├── pages/            # 页面组件（已完成18个）
│   ├── LoginPage.tsx
│   ├── CoursesPage.tsx
│   ├── CourseDetailPage.tsx
│   ├── ExamPage.tsx
│   ├── StudyPage.tsx
│   ├── DashboardPage.tsx
│   ├── NotificationsPage.tsx    # 消息通知
│   ├── NotesPage.tsx             # 学习笔记
│   ├── WrongQuestionsPage.tsx    # 错题本
│   ├── CertificatesPage.tsx      # 我的证书
│   ├── LeaderboardPage.tsx       # 学习排行榜
│   ├── SearchPage.tsx            # 全局搜索
│   ├── ProfilePage.tsx           # 个人资料
│   └── (5个管理后台页面)
├── components/       # 通用组件
│   ├── Layout.tsx
│   ├── AdminLayout.tsx
│   └── common/       # 可复用UI组件
├── api/              # API集成（已完成）
│   ├── client.ts     # axios配置和拦截器
│   ├── auth.ts
│   ├── feature.ts    # 辅助功能API
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
**辅助功能（4表）**：notifications, notes, wrong_questions, certificates

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
- `GET /api/auth/me` - 获取当前用户信息

### 课程管理（/api/courses）
- `GET /api/courses` - 课程列表（分页、筛选）
- `GET /api/courses/{id}` - 课程详情
- `POST /api/courses` - 创建课程
- `PUT /api/courses/{id}` - 更新课程
- `DELETE /api/courses/{id}` - 删除课程
- `GET /api/courses/{id}/chapters` - 章节列表
- `POST /api/courses/{id}/chapters` - 创建章节

### 考试系统（/api/exams）
- `GET /api/exams` - 考试列表
- `GET /api/exams/{id}` - 考试详情
- `POST /api/exams` - 创建考试
- `POST /api/exams/{id}/start` - 开始考试
- `POST /api/exams/{id}/submit` - 提交答案
- `GET /api/exams/{id}/result` - 查看成绩
- `GET /api/exams/questions` - 获取题目列表（管理后台）

### 学习进度（/api/learning）
- `POST /api/learning/courses/{id}/start` - 开始学习
- `POST /api/learning/chapters/{id}/complete` - 完成章节
- `GET /api/learning/progress` - 学习进度
- `GET /api/learning/stats` - 学习统计

### 辅助功能（/api/features）
- `GET /api/features/notifications` - 获取通知列表
- `PUT /api/features/notifications/{id}/read` - 标记已读
- `GET /api/features/notes` - 获取笔记列表
- `POST /api/features/notes` - 创建笔记
- `GET /api/features/wrong-questions` - 获取错题列表
- `PUT /api/features/wrong-questions/{id}/master` - 标记已掌握
- `GET /api/features/certificates` - 获取证书列表
- `GET /api/features/leaderboard` - 获取排行榜
- `GET /api/features/search` - 全局搜索
- `GET /api/features/profile` - 获取个人资料
- `PUT /api/features/profile` - 更新个人资料

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

### API响应格式
- **后端统一使用snake_case**: `full_name`, `created_at`, `is_active`
- **前端TypeScript接口匹配snake_case**: 保持与后端一致
- **列表端点直接返回数组**: `return [...]` 而非 `return {"data": [...]}`

### 必须遵守
1. 所有API端点必须有Docstring
2. 所有数据库字段必须有`comment`
3. 使用类型注解（Type Hints）
4. 使用Enum而非字符串常量
5. 数据库关系使用`relationship()`，避免手动JOIN

---

## 当前开发状态（2025-11-19）

### ✅ 已完成（约85%）

**后端（100%）**
- 17个数据表设计完成
- 认证系统（JWT + bcrypt）
- 所有API端点（auth、course、exam、learning、stats、feature）
- 数据库自动创建和初始化脚本
- 题目验证脚本（validate_question_data.py）

**前端（90%）**
- 核心员工端页面完成（课程浏览、考试答题、学习进度）
- 辅助功能页面完成（通知、笔记、错题本、证书、排行榜、搜索、个人资料）
- 管理后台完成（Dashboard、题库管理、考试管理、用户管理、课程管理）
- API集成层完成（已对接所有后端API）
- 认证上下文管理完成
- Layout和AdminLayout组件完成

**题库内容（78.4%）**
- 已生成436道题目（目标556道）
- 支持单选、多选、判断题型
- 覆盖技能类和价值观类题目
- 数据格式100%验证通过

### ❌ 待开发（P0优先级）

1. **题库扩充**（436/556道题）- 还需生成120道题
2. **课程内容文件**（0/46个markdown文件）
3. **考试功能测试**（创建正式考试并测试）
4. **自动化测试**（当前0%）

### 知识库资源（待转化）

- `knowlege/前厅合并文档.md` (1,660行)
- `knowlege/厨房合并文档.md` (3,573行)
- `knowlege/企业价值观优化版.md` (393行)
- `knowlege/人才梯队及发展路径.md` (2,048行)

**总计9,681行运营标准文档，需转化为课程和题目**

---

## 重要开发注意事项

### FastAPI路由顺序规则 ⚠️

**关键原则：具体路由必须在参数路由之前定义**

FastAPI使用**首次匹配**原则，一旦找到匹配的路由就停止查找。

**错误示例**：
```python
@router.get("/{exam_id}")           # ❌ 参数路由在前
@router.get("/questions")           # ❌ 会被上面路由匹配，永远无法触发
```

**正确示例**：
```python
@router.get("/questions")           # ✅ 具体路由在前
@router.get("/count")               # ✅ 具体路由在前
@router.get("/{exam_id}")           # ✅ 参数路由在后
```

**推荐路由顺序**：
```python
# 1. 集合操作
@router.get("/")
@router.post("/")

# 2. 具名资源（最重要！必须在参数路由之前）
@router.get("/count")
@router.get("/questions")
@router.get("/records")
@router.get("/search")

# 3. 子资源操作
@router.post("/{id}/publish")
@router.post("/{id}/start")

# 4. 单个资源（参数路由放最后）
@router.get("/{id}")
@router.put("/{id}")
@router.delete("/{id}")
```

**常见错误**：已发生3次路由顺序问题（详见PagesQ&A.md问题#17, #22）

---

### 前后端数据格式一致性

**枚举值命名规范**：后端使用小写蛇形命名，前端必须匹配

**后端（Python）**：
```python
class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"      # 小写蛇形
    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
```

**前端（TypeScript）**：
```typescript
// ✅ 正确 - 匹配后端
interface Question {
  question_type: 'single_choice' | 'multiple_choice' | 'true_false';
}

// ❌ 错误 - 大小写不匹配会导致筛选失败
interface Question {
  question_type: 'SINGLE_CHOICE' | 'MULTIPLE_CHOICE';
}
```

**常见错误**：枚举值大小写不匹配导致筛选和搜索失效（详见PagesQ&A.md问题#23）

---

### API分页限制

**重要**：后端API默认有分页限制，管理后台需要显式传递`limit`参数

```typescript
// ❌ 错误 - 只返回前50条（默认limit=50）
const response = await apiClient.get('/api/exams/questions');

// ✅ 正确 - 获取所有数据（当前436道题）
const response = await apiClient.get('/api/exams/questions', {
  params: { limit: 500 }  // 足够显示所有题目
});
```

**分页参数**：
- `skip`: 偏移量（默认0）
- `limit`: 每页数量（默认50）
- **后端最大限制**: 1000 (exam.py:119)
- **前端建议值**: 500（足够显示当前436道题，未来可扩展至1000道）

**前后端配置**：
- 后端：`backend/app/routers/exam.py:119`
  ```python
  limit: int = Query(50, ge=1, le=1000)  # 最大1000
  ```
- 前端：`frontend/src/pages/QuestionManagementPage.tsx:63`
  ```typescript
  params: { limit: 500 }
  ```

**常见错误**：
- 忘记传递limit导致数据不完整（详见PagesQ&A.md问题#23）
- 前后端limit不匹配导致422错误（详见PagesQ&A.md问题#25）

---

### 前端API调用统一模式

**必须使用`apiClient`而非直接使用`axios`**

```typescript
// ❌ 错误 - 绕过token自动注入
import axios from 'axios';
const token = localStorage.getItem('token');
const response = await axios.get(`${API_URL}/api/stats`, {
  headers: { Authorization: `Bearer ${token}` }
});

// ✅ 正确 - 自动注入token
import { apiClient } from '../api/client';
const response = await apiClient.get('/api/stats/dashboard');
```

**apiClient优势**：
- 自动从`localStorage.getItem('access_token')`读取token
- 统一错误处理
- 请求/响应拦截器

**常见错误**：直接使用axios导致401错误（详见PagesQ&A.md问题#21, #22）

---

### 数据库Enum值管理

**SQLAlchemy Enum缓存问题**：数据库enum值必须与Python enum定义一致

**错误场景**：
```sql
-- 数据库中存储的是大写
UPDATE questions SET question_type = 'SINGLE_CHOICE';

-- 但Python定义是小写
class QuestionType(str, Enum):
    SINGLE_CHOICE = "single_choice"

-- 结果：LookupError: 'SINGLE_CHOICE' is not among the defined enum values
```

**解决方案**：
1. 删除数据库：`rm backend/training_lms.db`
2. 重新初始化：`python3 backend/main.py`
3. 导入数据：`python3 backend/scripts/init_data.py`

**预防措施**：
- 使用脚本生成数据，避免手动UPDATE
- 保持Python enum定义与数据库值一致

**常见错误**：Enum缓存不一致导致500错误（详见PagesQ&A.md问题#21）

---

### Token存储键名一致性

**前端localStorage键名必须统一**

```typescript
// ❌ 错误 - 存储和读取键名不一致
localStorage.setItem('token', response.data.access_token);     // 存储为'token'
const token = localStorage.getItem('access_token');            // 读取'access_token'

// ✅ 正确 - 统一使用'access_token'
localStorage.setItem('access_token', response.data.access_token);
const token = localStorage.getItem('access_token');
```

**标准键名**：`access_token`（与后端响应字段一致）

**常见错误**：键名不一致导致token读取失败（详见PagesQ&A.md问题#21）

---

### 题库扩充数据格式标准 ⚠️

**关键原则：严格遵守数据格式标准，避免前端显示错误**

这是经过多次修复总结的标准格式，任何偏差都会导致前端ValidationError。

**正确的题目数据格式**：
```python
{
    "content": "题目内容",
    "question_type": QuestionType.SINGLE_CHOICE.value,  # ⚠️ 必须使用.value
    "difficulty": "easy",  # ⚠️ 字符串，不是枚举（无DifficultyLevel枚举）
    "category": QuestionCategory.SKILL.value,  # ⚠️ 必须使用.value
    "options": [  # ⚠️ 必须是字典数组
        {
            "label": "A",
            "text": "选项内容",  # ⚠️ 必须是"text"，不能是"content"
            "is_correct": False
        },
        {"label": "B", "text": "...", "is_correct": True},
        {"label": "C", "text": "...", "is_correct": False},
        {"label": "D", "text": "...", "is_correct": False}
    ],
    "correct_answer": "B",
    "explanation": "答案解析"
}
```

**常见错误（会导致前端崩溃）**：

1. ❌ 选项使用"content"字段
   ```python
   {"label": "A", "content": "错误", "is_correct": False}  # 错误
   {"label": "A", "text": "正确", "is_correct": False}     # 正确
   ```

2. ❌ 未使用枚举的.value
   ```python
   "question_type": QuestionType.SINGLE_CHOICE  # 错误，会存储枚举对象
   "question_type": QuestionType.SINGLE_CHOICE.value  # 正确，存储"single_choice"
   ```

3. ❌ difficulty使用枚举
   ```python
   "difficulty": DifficultyLevel.EASY.value  # 错误，该枚举不存在
   "difficulty": "easy"  # 正确，直接使用字符串
   ```

4. ❌ 选项格式错误
   ```python
   "options": ["选项1", "选项2"]  # 错误，字符串数组
   "options": {"A": "选项1", "B": "选项2"}  # 错误，字典格式
   "options": [{"label": "A", "text": "选项1", ...}]  # 正确
   ```

**题库扩充工作流**：
```bash
# 1. 创建生成脚本（参考existing脚本）
cd backend/scripts
cp generate_front_batch3_questions.py generate_new_batch.py

# 2. 编辑脚本，严格按照格式标准编写

# 3. 运行生成脚本
python3 generate_new_batch.py

# 4. 立即验证数据格式（必须！）
python3 scripts/validate_question_data.py

# 5. 刷新前端查看（必须强制刷新）
# Mac: Cmd + Shift + R
# Windows: Ctrl + Shift + R
```

**数据验证脚本**：
- 位置：`backend/scripts/validate_question_data.py`
- 用途：检查所有题目的数据格式
- 运行时机：每次扩充题库后必须运行
- 预期结果：0错误，0警告

**常见错误历史**（详见PagesQ&A.md v2.0）：
- 问题#24: 268道题使用"content"字段导致ValidationError
- 问题#25: 前后端limit参数不匹配导致422错误
- SQLAlchemy Enum配置错误导致LookupError

---

## 常见问题排查

### 后端启动失败

**端口被占用**
```bash
# 查找并杀死占用进程
lsof -ti:8000 | xargs kill -9
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
- CORS已配置支持`localhost:5173`和`localhost:5174`等常见开发端口

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

- **PagesQ&A.md** - Web开发问题与解决方案知识库（v2.0，记录25个常见问题，2,776行）
- **前端完整性检查报告.md** - 前端开发完成度检查
- **项目完整性检查报告.md** - 系统整体完成度检查
- **README.md** - 项目介绍和快速开始

**GitHub**: https://github.com/YukikoYoung/smartice-training-lms

**重要**：遇到开发问题时，优先查看`PagesQ&A.md`，已记录25个常见问题的完整解决方案，包括：
- 数据格式错误（268道题"content"→"text"字段修复）
- 前后端参数不匹配（limit限制导致422错误）
- SQLAlchemy Enum配置问题
- 路由顺序问题
- Token存储问题

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
