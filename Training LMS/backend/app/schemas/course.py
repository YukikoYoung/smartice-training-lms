"""
课程管理相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.user import DepartmentType
from ..models.course import ContentType


# ========== Content Schemas ==========

class ContentBase(BaseModel):
    """内容基础Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="内容标题")
    content_type: ContentType = Field(..., description="内容类型")
    order: int = Field(default=0, ge=0, description="内容顺序")
    file_url: Optional[str] = Field(None, max_length=500, description="文件URL")
    file_size: Optional[int] = Field(None, ge=0, description="文件大小（字节）")
    duration: Optional[int] = Field(None, ge=0, description="视频/音频时长（秒）")
    text_content: Optional[str] = Field(None, description="文本内容（Markdown格式）")
    is_active: bool = Field(default=True, description="是否启用")


class ContentCreate(ContentBase):
    """创建内容"""
    chapter_id: int = Field(..., gt=0, description="所属章节ID")


class ContentUpdate(BaseModel):
    """更新内容"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content_type: Optional[ContentType] = None
    order: Optional[int] = Field(None, ge=0)
    file_url: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    duration: Optional[int] = Field(None, ge=0)
    text_content: Optional[str] = None
    is_active: Optional[bool] = None


class ContentResponse(ContentBase):
    """内容响应"""
    id: int
    chapter_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== Chapter Schemas ==========

class ChapterBase(BaseModel):
    """章节基础Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="章节标题")
    description: Optional[str] = Field(None, description="章节描述")
    order: int = Field(..., ge=1, description="章节顺序")
    estimated_duration: Optional[int] = Field(None, ge=0, description="预计学习时长（分钟）")
    has_quiz: bool = Field(default=True, description="是否有章节小测验")
    quiz_pass_score: float = Field(default=70.0, ge=0, le=100, description="测验及格分数")
    is_active: bool = Field(default=True, description="是否启用")


class ChapterCreate(ChapterBase):
    """创建章节"""
    course_id: int = Field(..., gt=0, description="所属课程ID")


class ChapterUpdate(BaseModel):
    """更新章节"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    order: Optional[int] = Field(None, ge=1)
    estimated_duration: Optional[int] = Field(None, ge=0)
    has_quiz: Optional[bool] = None
    quiz_pass_score: Optional[float] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None


class ChapterResponse(ChapterBase):
    """章节响应"""
    id: int
    course_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    contents: List[ContentResponse] = []

    class Config:
        from_attributes = True


# ========== Course Schemas ==========

class CourseBase(BaseModel):
    """课程基础Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="课程标题")
    code: str = Field(..., min_length=1, max_length=50, description="课程编码（唯一）")
    description: Optional[str] = Field(None, description="课程描述")
    cover_image: Optional[str] = Field(None, max_length=500, description="封面图片URL")
    department_type: Optional[DepartmentType] = Field(None, description="适用部门")
    category: Optional[str] = Field(None, max_length=100, description="课程分类")
    target_positions: Optional[str] = Field(None, description="适用岗位（JSON数组）")
    target_levels: Optional[str] = Field(None, description="适用职级（JSON数组）")
    prerequisite_course_ids: Optional[str] = Field(None, description="前置课程ID列表（JSON数组）")
    estimated_duration: Optional[int] = Field(None, ge=0, description="预计学习时长（分钟）")
    difficulty_level: Optional[str] = Field(None, max_length=20, description="难度等级")
    is_mandatory: bool = Field(default=False, description="是否必修")
    is_active: bool = Field(default=True, description="是否启用")


class CourseCreate(CourseBase):
    """创建课程"""
    pass


class CourseUpdate(BaseModel):
    """更新课程"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    department_type: Optional[DepartmentType] = None
    category: Optional[str] = Field(None, max_length=100)
    target_positions: Optional[str] = None
    target_levels: Optional[str] = None
    prerequisite_course_ids: Optional[str] = None
    estimated_duration: Optional[int] = Field(None, ge=0)
    difficulty_level: Optional[str] = Field(None, max_length=20)
    version: Optional[str] = Field(None, max_length=20)
    is_published: Optional[bool] = None
    is_mandatory: Optional[bool] = None
    is_active: Optional[bool] = None


class CourseResponse(CourseBase):
    """课程响应"""
    id: int
    version: str
    is_published: bool
    created_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    published_at: Optional[datetime]
    chapters: List[ChapterResponse] = []

    class Config:
        from_attributes = True


class CourseListResponse(BaseModel):
    """课程列表响应（不含章节详情）"""
    id: int
    title: str
    code: str
    description: Optional[str]
    cover_image: Optional[str]
    department_type: Optional[DepartmentType]
    category: Optional[str]
    estimated_duration: Optional[int]
    difficulty_level: Optional[str]
    version: str
    is_published: bool
    is_mandatory: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
