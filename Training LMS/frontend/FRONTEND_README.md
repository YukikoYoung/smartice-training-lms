# SmartIce 培训系统 - 前端开发文档

## 项目概述

React + TypeScript + Vite 前端应用，配合 FastAPI 后端使用。

## 已完成的功能

### 1. 核心组件

#### Layout 组件 (`src/components/Layout.tsx`)
- ✅ 顶部导航栏：显示用户信息、课程中心、学习看板
- ✅ 退出登录功能
- ✅ 响应式设计（移动端友好）
- ✅ 渐变色主题（紫色系）

### 2. 所有核心页面

#### LoginPage (`src/pages/LoginPage.tsx`)
**功能：**
- ✅ 用户名密码登录
- ✅ 表单验证
- ✅ 错误提示
- ✅ Loading 状态
- ✅ 测试账号提示
- ✅ 登录成功后跳转到课程列表

**测试账号：**
- 店长：store_mgr / 123456
- 服务员：waiter001 / 123456

#### CoursesPage (`src/pages/CoursesPage.tsx`)
**功能：**
- ✅ 显示所有课程列表
- ✅ 课程筛选：全部/必修/选修
- ✅ 课程卡片展示（标题、描述、部门、必修标志）
- ✅ 点击课程跳转到详情页
- ✅ Loading 和错误处理
- ✅ 响应式卡片布局

#### CourseDetailPage (`src/pages/CourseDetailPage.tsx`)
**功能：**
- ✅ 显示课程详细信息
- ✅ 显示课程章节列表
- ✅ "开始学习"按钮（调用 learningAPI.startCourse）
- ✅ 学习进度显示（百分比、进度条）
- ✅ 章节点击（目前为占位功能）
- ✅ 返回课程列表按钮

#### ExamPage (`src/pages/ExamPage.tsx`)
**功能：**
- ✅ 考试信息展示（题数、时长、及格分、重考规则）
- ✅ 开始考试功能
- ✅ 答题界面：
  - 单选题
  - 多选题
  - 判断题
  - 简答题
- ✅ 倒计时功能（自动提交）
- ✅ 答题进度显示
- ✅ 提交考试
- ✅ 考试结果展示（分数、通过状态、正确题数）
- ✅ 重考功能（显示冷却期）

#### DashboardPage (`src/pages/DashboardPage.tsx`)
**功能：**
- ✅ 学习统计卡片：
  - 总课程数
  - 已完成课程
  - 学习中课程
  - 总体进度百分比
- ✅ 课程学习进度列表（进度条、状态标签）
- ✅ 考试记录表格（分数、正确率、提交时间）
- ✅ 点击课程卡片跳转到详情页

### 3. 样式系统

#### 全局样式 (`src/App.css`)
- ✅ 按钮样式（primary、secondary、large、block）
- ✅ 表单样式（input、textarea、select）
- ✅ 警告提示（error、success、warning、info）
- ✅ 加载状态（spinner 动画）
- ✅ 空状态样式
- ✅ 响应式设计
- ✅ 滚动条美化

#### 各页面独立样式
- ✅ LoginPage.css - 渐变背景、卡片布局
- ✅ CoursesPage.css - 网格布局、卡片悬停效果
- ✅ CourseDetailPage.css - 详情卡片、章节列表
- ✅ ExamPage.css - 答题卡片、倒计时、结果展示
- ✅ DashboardPage.css - 统计卡片、进度条、表格
- ✅ Layout.css - 导航栏、页脚

### 4. API 集成

所有页面已集成：
- ✅ authAPI (登录、获取用户信息)
- ✅ courseAPI (课程列表、课程详情)
- ✅ learningAPI (学习进度、开始课程、学习统计)
- ✅ examAPI (考试详情、开始考试、提交答案、考试记录)

## 项目结构

```
frontend/
├── src/
│   ├── api/               # API 服务层（已完成）
│   │   ├── authAPI.ts
│   │   ├── courseAPI.ts
│   │   ├── examAPI.ts
│   │   └── learningAPI.ts
│   ├── components/        # 组件
│   │   ├── Layout.tsx     # ✅ 布局组件
│   │   └── Layout.css
│   ├── contexts/          # Context（已完成）
│   │   └── AuthContext.tsx
│   ├── pages/             # 页面组件
│   │   ├── LoginPage.tsx         # ✅ 登录页
│   │   ├── LoginPage.css
│   │   ├── CoursesPage.tsx       # ✅ 课程列表
│   │   ├── CoursesPage.css
│   │   ├── CourseDetailPage.tsx  # ✅ 课程详情
│   │   ├── CourseDetailPage.css
│   │   ├── ExamPage.tsx          # ✅ 考试页面
│   │   ├── ExamPage.css
│   │   ├── DashboardPage.tsx     # ✅ 学习看板
│   │   └── DashboardPage.css
│   ├── types/             # 类型定义（已完成）
│   │   └── index.ts
│   ├── App.tsx            # ✅ 路由配置
│   ├── App.css            # ✅ 全局样式
│   └── main.tsx
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 快速启动

### 1. 安装依赖（如果还没安装）

```bash
cd frontend
npm install
```

### 2. 启动后端服务

**重要：前端依赖后端 API，必须先启动后端！**

```bash
# 在项目根目录的 backend 文件夹
cd ../backend
python3 main.py

# 后端服务将运行在 http://localhost:8000
```

### 3. 启动前端开发服务器

```bash
cd ../frontend
npm run dev

# 前端服务将运行在 http://localhost:5173
```

### 4. 打开浏览器

访问：http://localhost:5173

## 使用流程

### 用户登录
1. 打开应用自动跳转到登录页
2. 使用测试账号登录：
   - 用户名：`store_mgr`
   - 密码：`123456`
3. 登录成功后自动跳转到课程列表

### 浏览课程
1. 在课程中心可以看到所有课程
2. 使用顶部的标签筛选：全部/必修/选修
3. 点击课程卡片查看详情

### 学习课程
1. 在课程详情页点击"开始学习"按钮
2. 系统会记录学习进度
3. 可以看到章节列表（点击章节功能待开发）
4. 进度条会实时显示学习进度

### 参加考试
1. 通过路由 `/exams/:examId` 访问考试页面
2. 阅读考试须知后点击"开始考试"
3. 答题支持：
   - 单选题：点击选项
   - 多选题：勾选多个选项
   - 判断题：选择正确/错误
   - 简答题：输入文本答案
4. 注意倒计时，时间到会自动提交
5. 提交后查看成绩和详细结果

### 查看学习看板
1. 点击顶部导航的"学习看板"
2. 查看学习统计：总课程数、完成情况、总体进度
3. 查看所有课程的学习进度
4. 查看考试记录和成绩

### 退出登录
1. 点击右上角的"退出登录"按钮
2. 自动跳转到登录页

## API 接口说明

前端调用的后端 API（Base URL: `http://localhost:8000`）：

### 认证相关
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息

### 课程相关
- `GET /api/courses` - 获取课程列表
- `GET /api/courses/:id` - 获取课程详情

### 学习相关
- `POST /api/learning/courses/:id/start` - 开始学习课程
- `GET /api/learning/courses/:id/progress` - 获取课程进度
- `GET /api/learning/progress` - 获取所有学习进度
- `GET /api/learning/stats` - 获取学习统计

### 考试相关
- `GET /api/exams/:id` - 获取考试详情
- `POST /api/exams/:id/start` - 开始考试
- `POST /api/exams/:id/submit` - 提交考试
- `GET /api/exams/records` - 获取考试记录

## 响应式设计

所有页面已适配移动端：

- **桌面端**（> 768px）：卡片网格布局、完整导航栏
- **平板**（768px）：自适应卡片、简化导航
- **手机**（< 768px）：单列布局、移动优化

## 待开发功能

### 优先级 P0（需要后端 API 支持）
- [ ] 章节学习页面（点击章节后的内容展示）
- [ ] 课程内容播放器（视频/音频/文档）
- [ ] 章节完成标记功能

### 优先级 P1（增强功能）
- [ ] 个人资料页面
- [ ] 修改密码功能
- [ ] 学习提醒通知
- [ ] 课程搜索功能
- [ ] 学习笔记功能

### 优先级 P2（可选功能）
- [ ] 深色模式
- [ ] 多语言支持
- [ ] 离线学习支持
- [ ] 学习记录导出

## 设计特点

### 1. 颜色方案
- **主色调**：紫色渐变（#667eea → #764ba2）
- **背景色**：浅灰 (#f5f7fa)
- **卡片色**：白色 (#ffffff)
- **文字色**：深灰 (#2d3748)
- **辅助色**：灰蓝 (#718096)

### 2. 交互设计
- 按钮悬停：上移 2px + 阴影增强
- 卡片悬停：上移 4px + 边框高亮
- Loading 状态：旋转动画
- 进度条：渐变填充动画
- 倒计时：最后 5 分钟红色警告

### 3. 用户体验
- 所有操作都有 Loading 状态
- 所有错误都有友好提示
- 空状态有引导文案
- 表单验证实时反馈
- 移动端字体大小优化（防止自动放大）

## 构建生产版本

```bash
npm run build

# 构建产物在 dist/ 目录
# 可以使用任何静态服务器部署
```

### 预览生产版本

```bash
npm run preview
```

## 常见问题

### 1. 网络错误（Network Error）
**原因**：后端服务未启动或端口不对

**解决**：
```bash
# 检查后端是否运行
curl http://localhost:8000/health

# 如果没响应，启动后端
cd backend && python3 main.py
```

### 2. CORS 错误
**原因**：后端 CORS 配置未包含前端地址

**解决**：检查后端 `main.py` 的 CORS 配置中是否包含 `http://localhost:5173`

### 3. 401 Unauthorized
**原因**：Token 过期或未登录

**解决**：
1. 重新登录
2. 检查 localStorage 中的 token
3. 检查后端 JWT 配置

### 4. 页面空白
**原因**：JavaScript 错误

**解决**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 标签的错误信息
3. 查看 Network 标签的请求状态

## 开发建议

### 1. 添加新页面
```typescript
// 1. 在 src/pages/ 创建组件
export const NewPage: React.FC = () => {
  return <div>New Page</div>;
};

// 2. 在 App.tsx 添加路由
<Route path="/new" element={<NewPage />} />
```

### 2. 调用 API
```typescript
import { courseAPI } from '../api/courseAPI';

// 在组件中使用
const [data, setData] = useState([]);

useEffect(() => {
  const loadData = async () => {
    try {
      const result = await courseAPI.getList();
      setData(result);
    } catch (error) {
      console.error(error);
    }
  };
  loadData();
}, []);
```

### 3. 添加新样式
```css
/* 在对应的 .css 文件中添加 */
.new-component {
  background: white;
  padding: 1rem;
  border-radius: 8px;
}
```

## 性能优化建议

1. **代码分割**：使用 React.lazy 懒加载页面
2. **图片优化**：使用 WebP 格式、懒加载
3. **缓存策略**：使用 React Query 或 SWR 管理请求
4. **打包优化**：分析 bundle 大小，移除未使用的依赖

## 技术栈

- **框架**：React 18
- **语言**：TypeScript
- **构建工具**：Vite
- **路由**：React Router v6
- **HTTP 客户端**：Axios
- **样式**：纯 CSS（无 UI 库）

## 联系方式

如有问题，请查看：
- 后端文档：`../backend/README.md`
- 项目文档：`../README.md`
- GitHub Issues：https://github.com/YukikoYoung/smartice-training-lms

---

**开发完成时间**：2025-11-14
**开发者**：Claude Code
**版本**：v1.0.0 MVP
