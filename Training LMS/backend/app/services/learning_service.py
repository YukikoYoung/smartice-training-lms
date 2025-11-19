"""
学习进度业务逻辑
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from fastapi import HTTPException, status
from ..models.learning import CourseProgress, ChapterProgress, LearningStatus
from ..models.course import Course, Chapter
from ..schemas.learning import (
    CourseProgressCreate, CourseProgressUpdate,
    ChapterProgressCreate, ChapterProgressUpdate
)


# ========== CourseProgress CRUD ==========

def get_or_create_course_progress(db: Session, user_id: int, course_id: int) -> CourseProgress:
    """获取或创建课程学习进度"""
    # 先尝试获取
    progress = db.query(CourseProgress).filter(
        CourseProgress.user_id == user_id,
        CourseProgress.course_id == course_id
    ).first()

    if progress:
        return progress

    # 不存在则创建
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程 ID {course_id} 不存在"
        )

    progress = CourseProgress(
        user_id=user_id,
        course_id=course_id,
        status=LearningStatus.NOT_STARTED,
        total_chapters=len(course.chapters),
        completed_chapters=0,
        progress_percentage=0.0
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def update_course_progress(db: Session, user_id: int, course_id: int, update_data: CourseProgressUpdate) -> CourseProgress:
    """更新课程学习进度"""
    progress = get_or_create_course_progress(db, user_id, course_id)

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(progress, field, value)

    # 自动更新last_accessed_at
    progress.last_accessed_at = datetime.utcnow()

    # 如果状态变为已完成，设置completed_at
    if progress.status == LearningStatus.COMPLETED and not progress.completed_at:
        progress.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(progress)
    return progress


def start_course(db: Session, user_id: int, course_id: int) -> CourseProgress:
    """开始学习课程"""
    progress = get_or_create_course_progress(db, user_id, course_id)

    if progress.status == LearningStatus.NOT_STARTED:
        progress.status = LearningStatus.IN_PROGRESS
        progress.started_at = datetime.utcnow()
        progress.last_accessed_at = datetime.utcnow()
        db.commit()
        db.refresh(progress)

    return progress


def get_user_course_progress(db: Session, user_id: int, course_id: Optional[int] = None) -> List[CourseProgress]:
    """获取用户的课程学习进度"""
    query = db.query(CourseProgress).filter(CourseProgress.user_id == user_id)

    if course_id:
        query = query.filter(CourseProgress.course_id == course_id)

    return query.all()


# ========== ChapterProgress CRUD ==========

def get_or_create_chapter_progress(db: Session, user_id: int, chapter_id: int) -> ChapterProgress:
    """获取或创建章节学习进度"""
    # 先尝试获取
    progress = db.query(ChapterProgress).filter(
        ChapterProgress.user_id == user_id,
        ChapterProgress.chapter_id == chapter_id
    ).first()

    if progress:
        return progress

    # 不存在则创建
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"章节 ID {chapter_id} 不存在"
        )

    progress = ChapterProgress(
        user_id=user_id,
        chapter_id=chapter_id,
        course_id=chapter.course_id,
        status=LearningStatus.NOT_STARTED,
        total_contents=len(chapter.contents),
        completed_contents=0,
        quiz_passed=False
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)
    return progress


def update_chapter_progress(db: Session, user_id: int, chapter_id: int, update_data: ChapterProgressUpdate) -> ChapterProgress:
    """更新章节学习进度"""
    progress = get_or_create_chapter_progress(db, user_id, chapter_id)

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(progress, field, value)

    # 如果状态变为已完成，设置completed_at
    if progress.status == LearningStatus.COMPLETED and not progress.completed_at:
        progress.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(progress)

    # 更新课程进度
    update_course_progress_by_chapter(db, user_id, progress.course_id)

    return progress


def start_chapter(db: Session, user_id: int, chapter_id: int) -> ChapterProgress:
    """开始学习章节"""
    progress = get_or_create_chapter_progress(db, user_id, chapter_id)

    if progress.status == LearningStatus.NOT_STARTED:
        progress.status = LearningStatus.IN_PROGRESS
        progress.started_at = datetime.utcnow()
        db.commit()
        db.refresh(progress)

        # 同时更新课程进度为学习中
        start_course(db, user_id, progress.course_id)

    return progress


def complete_chapter(db: Session, user_id: int, chapter_id: int) -> ChapterProgress:
    """完成章节学习"""
    progress = get_or_create_chapter_progress(db, user_id, chapter_id)

    progress.status = LearningStatus.COMPLETED
    progress.completed_at = datetime.utcnow()
    progress.completed_contents = progress.total_contents

    db.commit()
    db.refresh(progress)

    # 更新课程进度
    update_course_progress_by_chapter(db, user_id, progress.course_id)

    return progress


def update_course_progress_by_chapter(db: Session, user_id: int, course_id: int):
    """根据章节进度更新课程进度"""
    # 获取课程的所有章节进度
    chapter_progresses = db.query(ChapterProgress).filter(
        ChapterProgress.user_id == user_id,
        ChapterProgress.course_id == course_id
    ).all()

    if not chapter_progresses:
        return

    # 获取课程实际的章节总数
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return
    total_chapters = len(course.chapters)

    # 计算已完成章节数
    completed_count = sum(1 for p in chapter_progresses if p.status == LearningStatus.COMPLETED)

    # 更新课程进度
    course_progress = get_or_create_course_progress(db, user_id, course_id)
    course_progress.completed_chapters = completed_count
    course_progress.total_chapters = total_chapters
    course_progress.progress_percentage = (completed_count / total_chapters * 100) if total_chapters > 0 else 0

    # 如果所有章节都完成，标记课程为已完成
    if completed_count == total_chapters and total_chapters > 0:
        course_progress.status = LearningStatus.COMPLETED
        if not course_progress.completed_at:
            course_progress.completed_at = datetime.utcnow()
    elif completed_count > 0:
        course_progress.status = LearningStatus.IN_PROGRESS

    db.commit()


def get_user_chapter_progress(db: Session, user_id: int, course_id: Optional[int] = None) -> List[ChapterProgress]:
    """获取用户的章节学习进度"""
    query = db.query(ChapterProgress).filter(ChapterProgress.user_id == user_id)

    if course_id:
        query = query.filter(ChapterProgress.course_id == course_id)

    return query.all()


# ========== 学习统计 ==========

def get_learning_stats(db: Session, user_id: int) -> dict:
    """获取用户学习统计"""
    # 课程统计
    course_progresses = get_user_course_progress(db, user_id)
    total_courses = len(course_progresses)
    completed_courses = sum(1 for p in course_progresses if p.status == LearningStatus.COMPLETED)
    in_progress_courses = sum(1 for p in course_progresses if p.status == LearningStatus.IN_PROGRESS)

    # 章节统计
    chapter_progresses = get_user_chapter_progress(db, user_id)
    total_chapters = len(chapter_progresses)
    completed_chapters = sum(1 for p in chapter_progresses if p.status == LearningStatus.COMPLETED)

    return {
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "in_progress_courses": in_progress_courses,
        "total_chapters": total_chapters,
        "completed_chapters": completed_chapters,
        "overall_progress": (completed_courses / total_courses * 100) if total_courses > 0 else 0
    }
