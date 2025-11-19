"""
FastAPI主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, course, exam, learning, user, stats, feature


# 导入所有模型（确保创建表）
from app.models import (
    User, Region, Store, Position,
    Course, Chapter, Content,
    Exam, Question,
    CourseProgress, ChapterProgress, ExamRecord, DailyQuizRecord, ValueAssessment,
    Notification, Note, WrongQuestion, Certificate
)


# 创建数据库表
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建表
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")
    yield
    # 关闭时清理（如果需要）


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="SmartIce培训管理系统 - 餐饮运营员工培训平台",
    lifespan=lifespan
)

# ========== HTTP请求日志中间件 ==========
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"\n{'='*60}")
    print(f"[HTTP] {request.method} {request.url.path}")
    print(f"[HTTP] Headers: {dict(request.headers)}")
    print(f"{'='*60}\n")
    response = await call_next(request)
    print(f"[HTTP] Response Status: {response.status_code}")
    return response

# 配置CORS - 必须在路由注册之前!
# 开发模式允许常见的开发端口
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # 额外的Vite端口
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5500",  # VS Code Live Server默认端口
        "http://127.0.0.1:5500",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "null",  # 支持直接打开HTML文件（file://协议）
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
    expose_headers=["*"],
    max_age=3600,
)

# 注册路由
app.include_router(auth.router)  # 认证路由
app.include_router(user.router)  # 用户管理路由
app.include_router(course.router)  # 课程管理路由
app.include_router(exam.router)  # 考试系统路由
app.include_router(learning.router)  # 学习进度路由
app.include_router(stats.router)  # 统计数据路由
app.include_router(feature.router)  # 辅助功能路由 (通知、笔记、错题、证书等)

# 配置静态文件服务
# 挂载backend/content目录，允许前端访问课程内容文件（Markdown、视频等）
content_dir = os.path.join(os.path.dirname(__file__), "content")
if not os.path.exists(content_dir):
    os.makedirs(content_dir)
    print(f"[静态文件] 创建content目录: {content_dir}")

app.mount("/content", StaticFiles(directory=content_dir), name="content")
print(f"[静态文件] 已挂载静态文件目录: {content_dir}")


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "SmartIce培训管理系统API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    import os

    # 支持两种启动模式:
    # 开发模式: reload=True (会创建reloader进程+worker进程)
    # 生产/测试模式: reload=False (单进程)
    reload_mode = os.getenv("RELOAD", "true").lower() == "true"

    print(f"\n{'='*60}")
    print(f"  启动模式: {'开发模式(reload)' if reload_mode else '生产模式(单进程)'}")
    print(f"{'='*60}\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload_mode,
        log_level="info"
    )
