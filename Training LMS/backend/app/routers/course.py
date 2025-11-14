"""
课程管理API路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse, CourseListResponse,
    ChapterCreate, ChapterUpdate, ChapterResponse,
    ContentCreate, ContentUpdate, ContentResponse
)
from ..services import course_service

router = APIRouter(prefix="/api/courses", tags=["courses"])


# ========== Course API ==========

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course_api(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建课程

    - **title**: 课程标题
    - **code**: 课程编码（唯一）
    - **description**: 课程描述
    - **department_type**: 适用部门（前厅/厨房/总部）
    - **category**: 课程分类
    - **is_mandatory**: 是否必修
    """
    return course_service.create_course(db, course_data, current_user.id)


@router.get("/", response_model=List[CourseListResponse])
def get_courses_api(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    is_active: Optional[bool] = None,
    is_published: Optional[bool] = None,
    department_type: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取课程列表

    - **skip**: 跳过记录数（分页）
    - **limit**: 每页记录数
    - **is_active**: 是否启用
    - **is_published**: 是否已发布
    - **department_type**: 部门类型筛选
    - **category**: 分类筛选
    """
    return course_service.get_courses(db, skip, limit, is_active, is_published, department_type, category)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取课程详情（含章节）

    - **course_id**: 课程ID
    """
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="课程不存在")
    return course


@router.put("/{course_id}", response_model=CourseResponse)
def update_course_api(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新课程

    - **course_id**: 课程ID
    """
    return course_service.update_course(db, course_id, course_data)


@router.delete("/{course_id}")
def delete_course_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除课程

    - **course_id**: 课程ID
    """
    course_service.delete_course(db, course_id)
    return {"message": "课程删除成功"}


@router.post("/{course_id}/publish", response_model=CourseResponse)
def publish_course_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发布课程

    - **course_id**: 课程ID
    """
    return course_service.publish_course(db, course_id)


# ========== Chapter API ==========

@router.post("/{course_id}/chapters", response_model=ChapterResponse, status_code=201)
def create_chapter_api(
    course_id: int,
    chapter_data: ChapterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建章节

    - **course_id**: 课程ID
    - **title**: 章节标题
    - **order**: 章节顺序
    - **has_quiz**: 是否有测验
    """
    # 确保chapter_data中的course_id与URL中的一致
    chapter_data.course_id = course_id
    return course_service.create_chapter(db, chapter_data)


@router.get("/{course_id}/chapters", response_model=List[ChapterResponse])
def get_chapters_api(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取课程的所有章节

    - **course_id**: 课程ID
    """
    return course_service.get_chapters_by_course(db, course_id)


@router.get("/chapters/{chapter_id}", response_model=ChapterResponse)
def get_chapter_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取章节详情（含内容列表）

    - **chapter_id**: 章节ID
    """
    chapter = course_service.get_chapter_by_id(db, chapter_id)
    if not chapter:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="章节不存在")
    return chapter


@router.put("/chapters/{chapter_id}", response_model=ChapterResponse)
def update_chapter_api(
    chapter_id: int,
    chapter_data: ChapterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新章节

    - **chapter_id**: 章节ID
    """
    return course_service.update_chapter(db, chapter_id, chapter_data)


@router.delete("/chapters/{chapter_id}")
def delete_chapter_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除章节

    - **chapter_id**: 章节ID
    """
    course_service.delete_chapter(db, chapter_id)
    return {"message": "章节删除成功"}


# ========== Content API ==========

@router.post("/chapters/{chapter_id}/contents", response_model=ContentResponse, status_code=201)
def create_content_api(
    chapter_id: int,
    content_data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建内容

    - **chapter_id**: 章节ID
    - **title**: 内容标题
    - **content_type**: 内容类型（video/document/image/audio）
    - **file_url**: 文件URL
    """
    content_data.chapter_id = chapter_id
    return course_service.create_content(db, content_data)


@router.get("/chapters/{chapter_id}/contents", response_model=List[ContentResponse])
def get_contents_api(
    chapter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取章节的所有内容

    - **chapter_id**: 章节ID
    """
    return course_service.get_contents_by_chapter(db, chapter_id)


@router.get("/contents/{content_id}", response_model=ContentResponse)
def get_content_api(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取内容详情

    - **content_id**: 内容ID
    """
    content = course_service.get_content_by_id(db, content_id)
    if not content:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="内容不存在")
    return content


@router.put("/contents/{content_id}", response_model=ContentResponse)
def update_content_api(
    content_id: int,
    content_data: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新内容

    - **content_id**: 内容ID
    """
    return course_service.update_content(db, content_id, content_data)


@router.delete("/contents/{content_id}")
def delete_content_api(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除内容

    - **content_id**: 内容ID
    """
    course_service.delete_content(db, content_id)
    return {"message": "内容删除成功"}
