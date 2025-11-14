# Pages Q&A - Web开发问题与解决方案知识库

本文档记录SmartIce培训系统及所有Web开发项目中遇到的问题和解决方案，形成可复用的知识库。

**文档版本**: v1.0
**最后更新**: 2025-11-14
**适用范围**: React + TypeScript + FastAPI项目

---

## 目录

- [1. TypeScript配置问题](#1-typescript配置问题)
- [2. 后端服务问题](#2-后端服务问题)
- [3. 路由参数问题](#3-路由参数问题)
- [4. API类型匹配问题](#4-api类型匹配问题)
- [5. 后端API设计问题](#5-后端api设计问题)
- [6. 诊断流程](#6-诊断流程)

---

## 1. TypeScript配置问题

### 问题1.1: 空白页面 - verbatimModuleSyntax配置导致模块导入错误

**症状**:
```
浏览器显示完全空白页面
控制台错误: Uncaught SyntaxError: The requested module './src/types/index.ts'
does not provide an export named 'Course'
```

**错误根因**:
- `tsconfig.app.json` 中 `verbatimModuleSyntax: true`
- 此配置要求所有类型导入必须使用 `import type` 语法
- 但代码中使用了 `import { Course }` 混合导入类型和值

**解决方案**:
```json
// tsconfig.app.json
{
  "compilerOptions": {
    "verbatimModuleSyntax": false  // 改为false或删除此配置
  }
}
```

**关键教训**:
- ❌ 清除Vite缓存**无法解决**此问题（这是配置问题，不是缓存问题）
- ✅ 这是TypeScript编译器配置问题，需要修改配置文件
- 遇到"空白页+模块导入错误"时，优先检查TypeScript配置

**文件位置**: `frontend/tsconfig.app.json:14`

---

## 2. 后端服务问题

### 问题2.1: 后端连接失败 - ERR_CONNECTION_REFUSED

**症状**:
```
POST http://localhost:8000/api/auth/login net::ERR_CONNECTION_REFUSED
前端显示: "网络连接失败，请检查网络"
```

**错误根因**:
- 后端进程被意外终止（exit code 137）
- 通常发生在清理多个后台进程时

**诊断步骤**:
```bash
# 1. 检查后端健康状态
curl http://localhost:8000/health

# 2. 检查端口占用
lsof -i :8000

# 3. 查看进程状态
ps aux | grep "python3 main.py"
```

**解决方案**:
```bash
# 重启后端服务
cd backend
source venv/bin/activate
python3 main.py
```

**预防措施**:
- 使用独立终端窗口运行前后端服务，避免使用过多后台进程
- 定期清理僵尸进程
- 启动服务前先检查端口是否被占用

---

## 3. 路由参数问题

### 问题3.1: 页面无限加载 - 路由参数名不匹配

**症状**:
```
页面一直显示 "加载课程详情中..." 或 "加载考试信息中..."
网络请求正常，但数据无法渲染
```

**错误根因**:
路由定义与 `useParams` 参数名不一致：

```typescript
// App.tsx - 路由定义
<Route path="/courses/:id" element={<CourseDetailPage />} />
<Route path="/exams/:id" element={<ExamPage />} />

// ❌ 错误 - CourseDetailPage.tsx
const { courseId } = useParams<{ courseId: string }>();

// ❌ 错误 - ExamPage.tsx
const { examId } = useParams<{ examId: string }>();
```

**解决方案**:
```typescript
// ✅ 正确 - 参数名必须与路由定义一致
const { id } = useParams<{ id: string }>();
const courseId = id;  // 如果需要更语义化的变量名

// 或者修改路由定义（不推荐）
<Route path="/courses/:courseId" element={<CourseDetailPage />} />
```

**涉及文件**:
- `frontend/src/App.tsx:53` - `/courses/:id`
- `frontend/src/App.tsx:62` - `/exams/:id`
- `frontend/src/pages/CourseDetailPage.tsx:9`
- `frontend/src/pages/ExamPage.tsx:8`

**关键教训**:
- useParams 的参数名**必须严格匹配**路由定义中的 `:paramName`
- 建议统一使用 `:id` 作为主键参数名，保持一致性
- 这类错误表现为页面能加载但数据无法显示，不会有明显的错误提示

---

## 4. API类型匹配问题

### 问题4.1: 类型错误 - API返回数组但赋值给单个对象

**症状**:
```typescript
// TypeScript编译错误
error TS2345: Argument of type 'CourseProgress[] | null' is not assignable
to parameter of type 'SetStateAction<CourseProgress | null>'
```

**错误根因**:
API设计不一致：
```typescript
// API定义返回数组
getCourseProgress: async (courseId?: number): Promise<CourseProgress[]>

// 但页面期望单个对象
const [progress, setProgress] = useState<CourseProgress | null>(null);
setProgress(progressData);  // progressData是数组，但期望单个对象
```

**解决方案**:
```typescript
// 方案1: 在API层处理（推荐）
const [courseData, progressDataArray] = await Promise.all([
  courseAPI.getDetail(parseInt(courseId)),
  learningAPI.getCourseProgress(parseInt(courseId)).catch(() => []),
]);

setCourse(courseData);
// 取数组第一个元素
setProgress(progressDataArray.length > 0 ? progressDataArray[0] : null);

// 方案2: 修改API定义（需要后端配合）
getCourseProgress: async (courseId: number): Promise<CourseProgress>  // 返回单个对象
```

**涉及文件**:
- `frontend/src/pages/CourseDetailPage.tsx:32-39`
- `frontend/src/api/index.ts:105-112`

**关键教训**:
- API响应类型必须与前端状态类型一致
- 使用TypeScript严格模式可以提前发现这类问题
- 当API返回数组但只需要单个对象时，优先在API调用层处理转换

---

### 问题4.2: 未使用的导入 - TypeScript编译警告

**症状**:
```
error TS6196: 'LoginRequest' is declared but never used
```

**解决方案**:
```typescript
// ❌ 错误
import type { User, LoginRequest } from '../types';

// ✅ 正确 - 删除未使用的导入
import type { User } from '../types';
```

**关键教训**:
- 定期清理未使用的导入
- 使用ESLint的 `no-unused-vars` 规则自动检测

---

### 问题4.3: 调用不存在的API方法

**症状**:
```typescript
error TS2339: Property 'getAllProgress' does not exist on type ...
```

**错误根因**:
```typescript
// ❌ 调用了不存在的方法
learningAPI.getAllProgress()

// ✅ 应该使用已有的方法
learningAPI.getCourseProgress()  // 不传参数获取所有课程进度
```

**解决方案**:
先查看API定义文件，确认可用方法：
```typescript
// src/api/index.ts
export const learningAPI = {
  getCourseProgress: async (courseId?: number): Promise<CourseProgress[]>
  // 没有 getAllProgress 方法
};
```

**涉及文件**:
- `frontend/src/pages/DashboardPage.tsx:26`

---

## 5. 后端API设计问题

### 问题5.1: 前端期望数据不存在 - API响应不完整

**症状**:
```
Uncaught TypeError: Cannot read properties of undefined (reading 'map')
at ExamPage.tsx:315
```

**错误根因**:
后端API返回数据不完整，缺少前端期望的字段：

```python
# ❌ 错误 - start_exam API
return {
    "exam_record_id": exam_record.id,
    "exam_id": exam_record.exam_id,
    "attempt_number": exam_record.attempt_number,
    "started_at": exam_record.started_at,
    "message": "考试已开始"
    # 缺少 questions 字段！
}
```

```typescript
// 前端期望
const data = await examAPI.start(examId);
setQuestions(data.questions);  // questions is undefined!
```

**解决方案**:
修改后端API，补充缺失字段：

```python
# ✅ 正确 - 返回题目列表
@router.post("/{exam_id}/start")
def start_exam_api(exam_id: int, ...):
    exam_record = exam_service.start_exam(db, current_user.id, exam_id)

    # 获取题目列表
    exam = exam_service.get_exam_by_id(db, exam_id)
    questions = []
    if exam and exam.question_ids:
        from ..models.exam import Question
        questions = db.query(Question).filter(
            Question.id.in_(exam.question_ids)
        ).all()
        questions = [QuestionResponse.from_orm(q) for q in questions]

    return {
        "exam_record_id": exam_record.id,
        "exam_id": exam_record.exam_id,
        "attempt_number": exam_record.attempt_number,
        "started_at": exam_record.started_at,
        "questions": questions,  # 新增
        "message": "考试已开始"
    }
```

**涉及文件**:
- `backend/app/routers/exam.py:223-260`
- `frontend/src/pages/ExamPage.tsx:68-79`

**关键教训**:
- 前后端API契约必须明确，建议使用OpenAPI规范文档
- 前端开发前先确认后端API返回的完整数据结构
- 使用TypeScript类型定义强制API响应类型检查

---

## 6. 诊断流程

### 6.1 空白页面诊断流程

```
1. 打开浏览器开发者工具Console
   ↓
2. 查看是否有红色错误
   ↓
3. 如果是"module does not provide export"
   → 检查 tsconfig.app.json 中的 verbatimModuleSyntax 配置
   ↓
4. 如果是"ERR_CONNECTION_REFUSED"
   → 检查后端服务是否运行: curl http://localhost:8000/health
   ↓
5. 如果是"Cannot read properties of undefined"
   → 检查前端期望的数据字段是否存在于API响应中
```

### 6.2 页面无限加载诊断流程

```
1. 打开Network标签，查看API请求
   ↓
2. 如果API请求成功但页面不渲染
   → 检查 useParams 参数名是否与路由定义匹配
   ↓
3. 如果API请求404
   → 检查后端路由是否正确，参数是否正确传递
   ↓
4. 如果API请求500
   → 查看后端日志，检查业务逻辑错误
```

### 6.3 TypeScript编译错误处理流程

```
1. 运行 npm run build 查看完整错误列表
   ↓
2. 按错误类型分类：
   - TS6196 (未使用的导入) → 删除
   - TS2345 (类型不匹配) → 检查API返回类型与状态类型
   - TS2339 (属性不存在) → 检查API定义，确认方法名
   ↓
3. 修复后重新编译验证
```

### 6.4 系统全面检查清单

在测试新功能前，执行以下检查：

```bash
# 1. 后端健康检查
curl http://localhost:8000/health

# 2. 前端服务检查
curl http://localhost:5173

# 3. 数据库数据检查
sqlite3 backend/training_lms.db "SELECT COUNT(*) FROM questions;"

# 4. TypeScript编译检查
cd frontend && npm run build

# 5. 路由配置检查
# 确保所有 useParams 参数名与路由定义一致
grep -r "useParams" frontend/src/pages/
grep "path=" frontend/src/App.tsx
```

---

## 7. 开发最佳实践

### 7.1 路由参数命名规范

**强烈推荐**：统一使用 `:id` 作为主键参数名

```typescript
// ✅ 推荐 - 统一使用 :id
<Route path="/courses/:id" element={<CourseDetailPage />} />
<Route path="/exams/:id" element={<ExamPage />} />
<Route path="/users/:id" element={<UserDetailPage />} />

// 组件中统一处理
const { id } = useParams<{ id: string }>();
const courseId = parseInt(id!);  // 转换为具体的业务ID
```

**避免**：不同页面使用不同参数名
```typescript
// ❌ 不推荐 - 容易混淆
<Route path="/courses/:courseId" element={...} />
<Route path="/exams/:examId" element={...} />
<Route path="/users/:userId" element={...} />
```

### 7.2 API类型定义规范

确保前后端类型一致：

```typescript
// 前端类型定义
export interface ExamStartResponse {
  exam_record_id: number;
  exam_id: number;
  attempt_number: number;
  started_at: string;
  questions: Question[];  // 明确定义期望的字段
  message: string;
}

// API调用时使用类型
const data: ExamStartResponse = await examAPI.start(examId);
```

### 7.3 错误处理模式

```typescript
// 推荐的错误处理模式
const loadData = async () => {
  try {
    setLoading(true);
    setError('');

    const data = await api.fetchData();

    // 防御性检查
    if (!data || !data.requiredField) {
      throw new Error('API响应数据不完整');
    }

    setState(data);
  } catch (err: any) {
    console.error('加载失败:', err);
    setError(err.message || '加载失败');
  } finally {
    setLoading(false);
  }
};
```

### 7.4 提交信息规范

使用统一的commit message格式：

```bash
# 类型: 简短描述（50字符以内）
#
# 详细说明问题和解决方案
#
# 文件位置: file.ts:行号

# 示例
fix: 修复CourseDetailPage路由参数名不匹配导致无限加载

- 将useParams的参数从courseId改为id以匹配App.tsx中的路由定义
- 这是导致课程详情页一直显示'加载课程详情中...'的根本原因
- 路由参数名必须与路由定义中的参数名完全一致

文件: frontend/src/pages/CourseDetailPage.tsx:9
```

---

## 8. 问题汇总表

| 序号 | 问题类型 | 错误信息 | 根本原因 | 解决方案 | 影响范围 |
|------|---------|---------|---------|---------|---------|
| 1 | TypeScript配置 | module does not provide export | verbatimModuleSyntax: true | 改为false | 全局 |
| 2 | 后端服务 | ERR_CONNECTION_REFUSED | 进程被终止 | 重启后端 | 全局 |
| 3 | 路由参数 | 页面无限加载 | useParams参数名不匹配 | 统一使用:id | CourseDetailPage |
| 4 | 路由参数 | 页面无限加载 | useParams参数名不匹配 | 统一使用:id | ExamPage |
| 5 | API类型 | TS2345类型错误 | 数组vs单个对象 | 取数组第一个元素 | CourseDetailPage |
| 6 | 未使用导入 | TS6196警告 | 多余的导入 | 删除未使用导入 | AuthContext |
| 7 | API方法 | TS2339属性不存在 | 调用不存在方法 | 使用正确API方法 | DashboardPage |
| 8 | API设计 | Cannot read 'map' | 缺少questions字段 | 后端返回题目列表 | ExamPage |

---

## 9. 关键经验总结

### 记住的成功模式

1. **TypeScript配置问题不能用缓存清理解决**
   - 空白页 + 模块导入错误 = 配置问题
   - 优先检查 tsconfig.*.json 文件

2. **路由参数名必须严格一致**
   - useParams参数名 = 路由定义中的:paramName
   - 推荐统一使用 `:id`

3. **API类型必须匹配**
   - 返回数组就定义为数组
   - 返回单个对象就定义为单个对象
   - 使用TypeScript严格模式提前发现问题

4. **前后端API契约必须明确**
   - 前端期望的字段必须在后端返回
   - 建议使用OpenAPI文档

5. **系统性诊断流程**
   - 先检查服务是否运行（curl health check）
   - 再检查TypeScript编译（npm run build）
   - 最后检查业务逻辑

---

## 10. 快速参考命令

```bash
# 健康检查
curl http://localhost:8000/health
curl http://localhost:5173

# 检查端口占用
lsof -i :8000
lsof -i :5173

# 重启服务
cd backend && source venv/bin/activate && python3 main.py
cd frontend && npm run dev

# 编译检查
cd frontend && npm run build

# 数据库检查
sqlite3 backend/training_lms.db "SELECT * FROM questions LIMIT 5;"

# 查找路由定义
grep -r "useParams" frontend/src/pages/
grep "path=" frontend/src/App.tsx

# Git提交
git add -A
git commit -m "fix: 简短描述问题"
```

---

## 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2025-11-14 | v1.0 | 初始版本，总结SmartIce LMS考试功能开发中的8个问题 |

---

**维护者**: Claude
**项目**: SmartIce Training LMS
**文档用途**: 积累Web开发经验，形成可复用的问题解决知识库
