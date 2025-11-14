"""
学习进度API路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.learning import (
    CourseProgressResponse, ChapterProgressResponse,
    ExamRecordResponse, DailyQuizRecordResponse,
    ValueAssessmentResponse
)
from ..services import learning_service

router = APIRouter(prefix="/api/learning", tags=["learning"])


# ========== 课程进度API ==========

@router.post("/courses/{course_id}/start", response_model=CourseProgressResponse)
def start_course_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    开始学习课程

    - 创建或更新课程学习进度
    - 设置状态为IN_PROGRESS
    - 记录开始时间

    - **course_id**: 课程ID
    """
    return learning_service.start_course(db, current_user.id, course_id)


@router.get("/courses/progress", response_model=List[CourseProgressResponse])
def get_my_course_progress_api(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的课程学习进度

    - **course_id**: 课程ID（可选，不传则返回所有课程进度）
    """
    return learning_service.get_user_course_progress(db, current_user.id, course_id)


@router.get("/courses/{course_id}/progress", response_model=CourseProgressResponse)
def get_course_progress_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取特定课程的学习进度

    - **course_id**: 课程ID
    """
    progress = learning_service.get_or_create_course_progress(db, current_user.id, course_id)
    return progress


# ========== 章节进度API ==========

@router.post("/chapters/{chapter_id}/start", response_model=ChapterProgressResponse)
def start_chapter_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    开始学习章节

    - 创建或更新章节学习进度
    - 设置状态为IN_PROGRESS
    - 自动更新课程进度为学习中

    - **chapter_id**: 章节ID
    """
    return learning_service.start_chapter(db, current_user.id, chapter_id)


@router.post("/chapters/{chapter_id}/complete", response_model=ChapterProgressResponse)
def complete_chapter_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    完成章节学习

    - 标记章节为已完成
    - 自动更新课程进度百分比
    - 如果所有章节完成，自动标记课程为已完成

    - **chapter_id**: 章节ID
    """
    return learning_service.complete_chapter(db, current_user.id, chapter_id)


@router.get("/chapters/progress", response_model=List[ChapterProgressResponse])
def get_my_chapter_progress_api(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的章节学习进度

    - **course_id**: 课程ID（可选，不传则返回所有章节进度）
    """
    return learning_service.get_user_chapter_progress(db, current_user.id, course_id)


@router.get("/chapters/{chapter_id}/progress", response_model=ChapterProgressResponse)
def get_chapter_progress_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取特定章节的学习进度

    - **chapter_id**: 章节ID
    """
    progress = learning_service.get_or_create_chapter_progress(db, current_user.id, chapter_id)
    return progress


# ========== 学习统计API ==========

@router.get("/stats")
def get_learning_stats_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学习统计数据

    返回：
    - **total_courses**: 总课程数
    - **completed_courses**: 已完成课程数
    - **in_progress_courses**: 学习中课程数
    - **total_chapters**: 总章节数
    - **completed_chapters**: 已完成章节数
    - **overall_progress**: 整体学习进度百分比
    """
    return learning_service.get_learning_stats(db, current_user.id)
