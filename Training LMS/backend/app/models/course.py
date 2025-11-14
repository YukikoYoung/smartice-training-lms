from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from .user import DepartmentType
import enum


class ContentType(str, enum.Enum):
    """内容类型"""
    VIDEO = "video"  # 视频
    DOCUMENT = "document"  # 文档（PDF、图文）
    IMAGE = "image"  # 图片
    AUDIO = "audio"  # 音频


class Course(Base):
    """课程模型"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    title = Column(String(200), nullable=False, comment="课程标题")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="课程编码")
    description = Column(Text, nullable=True, comment="课程描述")
    cover_image = Column(String(500), nullable=True, comment="课程封面图片URL")

    # 分类与归属
    department_type = Column(SQLEnum(DepartmentType), nullable=True, comment="适用部门（前厅/厨房/全部）")
    category = Column(String(100), nullable=True, comment="课程分类（如：岗位技能、企业价值观、安全规范）")

    # 适用对象
    target_positions = Column(Text, nullable=True, comment="适用岗位（JSON数组，如：['服务员','收银员']）")
    target_levels = Column(Text, nullable=True, comment="适用职级（JSON数组，如：['L1','L2']）")

    # 前置课程（必须先完成的课程）
    prerequisite_course_ids = Column(Text, nullable=True, comment="前置课程ID列表（JSON数组）")

    # 课程属性
    estimated_duration = Column(Integer, nullable=True, comment="预计学习时长（分钟）")
    difficulty_level = Column(String(20), nullable=True, comment="难度等级（初级/中级/高级）")

    # 版本管理
    version = Column(String(20), default="1.0", comment="课程版本号")
    is_published = Column(Boolean, default=False, comment="是否已发布")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_mandatory = Column(Boolean, default=False, comment="是否必修")

    # 创建者
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建者ID")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    published_at = Column(DateTime(timezone=True), nullable=True, comment="发布时间")

    # 关联关系
    chapters = relationship("Chapter", back_populates="course", cascade="all, delete-orphan", order_by="Chapter.order")
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Course {self.title} (v{self.version})>"

    @property
    def total_chapters(self):
        """总章节数"""
        return len(self.chapters)

    @property
    def is_entry_level(self):
        """是否入职必修课程"""
        return self.is_mandatory and "入职" in (self.category or "")


class Chapter(Base):
    """章节模型"""
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)

    # 所属课程
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="所属课程ID")

    # 基本信息
    title = Column(String(200), nullable=False, comment="章节标题")
    description = Column(Text, nullable=True, comment="章节描述")
    order = Column(Integer, nullable=False, default=0, comment="章节顺序（从1开始）")

    # 章节属性
    estimated_duration = Column(Integer, nullable=True, comment="预计学习时长（分钟）")

    # 是否有章节测验
    has_quiz = Column(Boolean, default=True, comment="是否有章节小测验")
    quiz_pass_score = Column(Float, default=70.0, comment="章节测验及格分数")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    course = relationship("Course", back_populates="chapters")
    contents = relationship("Content", back_populates="chapter", cascade="all, delete-orphan", order_by="Content.order")

    def __repr__(self):
        return f"<Chapter {self.title} (Ch{self.order})>"

    @property
    def total_contents(self):
        """内容数量"""
        return len(self.contents)


class Content(Base):
    """内容模型（视频、文档、图片等）"""
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, index=True)

    # 所属章节
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False, comment="所属章节ID")

    # 基本信息
    title = Column(String(200), nullable=False, comment="内容标题")
    content_type = Column(SQLEnum(ContentType), nullable=False, comment="内容类型（视频/文档/图片）")
    order = Column(Integer, nullable=False, default=0, comment="内容顺序（从1开始）")

    # 内容位置
    file_url = Column(String(500), nullable=True, comment="文件URL（视频/PDF/图片地址）")
    file_size = Column(Integer, nullable=True, comment="文件大小（字节）")
    duration = Column(Integer, nullable=True, comment="视频/音频时长（秒）")

    # 文本内容（用于文档类型）
    text_content = Column(Text, nullable=True, comment="文本内容（Markdown格式）")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    chapter = relationship("Chapter", back_populates="contents")

    def __repr__(self):
        return f"<Content {self.title} ({self.content_type.value})>"

    @property
    def is_video(self):
        """是否视频内容"""
        return self.content_type == ContentType.VIDEO

    @property
    def is_document(self):
        """是否文档内容"""
        return self.content_type == ContentType.DOCUMENT
