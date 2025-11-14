"""
课程管理业务逻辑
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from ..models.course import Course, Chapter, Content
from ..schemas.course import (
    CourseCreate, CourseUpdate,
    ChapterCreate, ChapterUpdate,
    ContentCreate, ContentUpdate
)


# ========== Course CRUD ==========

def create_course(db: Session, course_data: CourseCreate, creator_id: int) -> Course:
    """创建课程"""
    # 检查课程编码是否已存在
    existing_course = db.query(Course).filter(Course.code == course_data.code).first()
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"课程编码 {course_data.code} 已存在"
        )

    course = Course(
        **course_data.model_dump(),
        created_by=creator_id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_course_by_id(db: Session, course_id: int) -> Optional[Course]:
    """根据ID获取课程"""
    return db.query(Course).filter(Course.id == course_id).first()


def get_courses(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    is_active: Optional[bool] = None,
    is_published: Optional[bool] = None,
    department_type: Optional[str] = None,
    category: Optional[str] = None
) -> List[Course]:
    """获取课程列表"""
    query = db.query(Course)

    if is_active is not None:
        query = query.filter(Course.is_active == is_active)
    if is_published is not None:
        query = query.filter(Course.is_published == is_published)
    if department_type:
        query = query.filter(Course.department_type == department_type)
    if category:
        query = query.filter(Course.category == category)

    return query.offset(skip).limit(limit).all()


def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course:
    """更新课程"""
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程 ID {course_id} 不存在"
        )

    # 如果更新code，检查是否重复
    if course_data.code and course_data.code != course.code:
        existing = db.query(Course).filter(Course.code == course_data.code).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"课程编码 {course_data.code} 已存在"
            )

    # 更新字段
    for field, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)
    return course


def delete_course(db: Session, course_id: int) -> bool:
    """删除课程"""
    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程 ID {course_id} 不存在"
        )

    db.delete(course)
    db.commit()
    return True


def publish_course(db: Session, course_id: int) -> Course:
    """发布课程"""
    from datetime import datetime

    course = get_course_by_id(db, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程 ID {course_id} 不存在"
        )

    if course.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="课程已发布"
        )

    course.is_published = True
    course.published_at = datetime.utcnow()
    db.commit()
    db.refresh(course)
    return course


# ========== Chapter CRUD ==========

def create_chapter(db: Session, chapter_data: ChapterCreate) -> Chapter:
    """创建章节"""
    # 验证课程是否存在
    course = get_course_by_id(db, chapter_data.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"课程 ID {chapter_data.course_id} 不存在"
        )

    chapter = Chapter(**chapter_data.model_dump())
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return chapter


def get_chapter_by_id(db: Session, chapter_id: int) -> Optional[Chapter]:
    """根据ID获取章节"""
    return db.query(Chapter).filter(Chapter.id == chapter_id).first()


def get_chapters_by_course(db: Session, course_id: int) -> List[Chapter]:
    """获取课程的所有章节"""
    return db.query(Chapter).filter(
        Chapter.course_id == course_id,
        Chapter.is_active == True
    ).order_by(Chapter.order).all()


def update_chapter(db: Session, chapter_id: int, chapter_data: ChapterUpdate) -> Chapter:
    """更新章节"""
    chapter = get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"章节 ID {chapter_id} 不存在"
        )

    for field, value in chapter_data.model_dump(exclude_unset=True).items():
        setattr(chapter, field, value)

    db.commit()
    db.refresh(chapter)
    return chapter


def delete_chapter(db: Session, chapter_id: int) -> bool:
    """删除章节"""
    chapter = get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"章节 ID {chapter_id} 不存在"
        )

    db.delete(chapter)
    db.commit()
    return True


# ========== Content CRUD ==========

def create_content(db: Session, content_data: ContentCreate) -> Content:
    """创建内容"""
    # 验证章节是否存在
    chapter = get_chapter_by_id(db, content_data.chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"章节 ID {content_data.chapter_id} 不存在"
        )

    content = Content(**content_data.model_dump())
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


def get_content_by_id(db: Session, content_id: int) -> Optional[Content]:
    """根据ID获取内容"""
    return db.query(Content).filter(Content.id == content_id).first()


def get_contents_by_chapter(db: Session, chapter_id: int) -> List[Content]:
    """获取章节的所有内容"""
    return db.query(Content).filter(
        Content.chapter_id == chapter_id,
        Content.is_active == True
    ).order_by(Content.order).all()


def update_content(db: Session, content_id: int, content_data: ContentUpdate) -> Content:
    """更新内容"""
    content = get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"内容 ID {content_id} 不存在"
        )

    for field, value in content_data.model_dump(exclude_unset=True).items():
        setattr(content, field, value)

    db.commit()
    db.refresh(content)
    return content


def delete_content(db: Session, content_id: int) -> bool:
    """删除内容"""
    content = get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"内容 ID {content_id} 不存在"
        )

    db.delete(content)
    db.commit()
    return True
