from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class ExamType(str, enum.Enum):
    """考试类型"""
    CHAPTER_QUIZ = "chapter_quiz"  # 章节小测验（短平快，5-8题）
    WEEKLY_TEST = "weekly_test"  # 每周小测验（10-15题）
    MONTHLY_EXAM = "monthly_exam"  # 每月大考（20-30题）
    DAILY_QUIZ = "daily_quiz"  # 随堂检测（每日5题，非强制）
    FINAL_EXAM = "final_exam"  # 期末考试（课程结束）
    PROBATION_EXAM = "probation_exam"  # 试用期考核


class QuestionType(str, enum.Enum):
    """题目类型"""
    SINGLE_CHOICE = "single_choice"  # 单选题
    MULTIPLE_CHOICE = "multiple_choice"  # 多选题
    TRUE_FALSE = "true_false"  # 判断题
    SHORT_ANSWER = "short_answer"  # 简答题（暂不实现）


class QuestionCategory(str, enum.Enum):
    """题目分类（用于价值观融入）"""
    SKILL = "skill"  # 岗位技能（70-80%）
    VALUE_DILIGENCE = "value_diligence"  # 以勤劳者为本
    VALUE_CUSTOMER = "value_customer"  # 帮助顾客
    VALUE_COLLABORATION = "value_collaboration"  # 高效协作
    VALUE_TRANSPARENCY = "value_transparency"  # 平等透明


class Question(Base):
    """题目模型"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    # 题目内容
    content = Column(Text, nullable=False, comment="题目内容")
    question_type = Column(SQLEnum(QuestionType, values_callable=lambda x: [e.value for e in x]), nullable=False, comment="题目类型")
    category = Column(SQLEnum(QuestionCategory, values_callable=lambda x: [e.value for e in x]), nullable=False, default=QuestionCategory.SKILL, comment="题目分类")

    # 关联课程/章节（用于题库分类）
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True, comment="关联课程ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True, comment="关联章节ID")

    # 难度等级
    difficulty = Column(String(20), nullable=True, comment="难度（简单/中等/困难）")

    # 选项（JSON格式存储）
    # 格式：[{"label": "A", "content": "选项内容", "is_correct": true}, ...]
    options = Column(JSON, nullable=True, comment="选项列表（JSON）")

    # 正确答案（用于判断题和简答题）
    correct_answer = Column(Text, nullable=True, comment="正确答案")

    # 解析
    explanation = Column(Text, nullable=True, comment="答案解析")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 创建者
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建者ID")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    course = relationship("Course", foreign_keys=[course_id])
    chapter = relationship("Chapter", foreign_keys=[chapter_id])
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Question {self.id} ({self.question_type.value})>"

    @property
    def is_value_question(self):
        """是否企业价值观题目"""
        return self.category != QuestionCategory.SKILL


class Exam(Base):
    """考试模型"""
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    title = Column(String(200), nullable=False, comment="考试标题")
    exam_type = Column(SQLEnum(ExamType), nullable=False, comment="考试类型")
    description = Column(Text, nullable=True, comment="考试说明")

    # 关联课程/章节
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=True, comment="关联课程ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True, comment="关联章节ID")

    # 考试设置
    total_questions = Column(Integer, nullable=False, comment="总题数")
    pass_score = Column(Float, nullable=False, default=70.0, comment="及格分数")
    time_limit = Column(Integer, nullable=True, comment="考试时长限制（分钟），null表示不限时")

    # 题目配置（JSON格式）
    # 格式：{"skill": 15, "value": 5} 表示技能题15道，价值观题5道
    question_distribution = Column(JSON, nullable=True, comment="题目分布配置")

    # 题目ID列表（JSON格式，固定题目）
    # 如果为null，则从题库随机抽题
    question_ids = Column(JSON, nullable=True, comment="题目ID列表（固定考题）")

    # 补考设置
    allow_retake = Column(Boolean, default=True, comment="是否允许补考")
    max_attempts = Column(Integer, default=3, comment="最大考试次数")
    retake_cooldown_days = Column(Integer, default=3, comment="补考冷却期（天）")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")
    is_published = Column(Boolean, default=False, comment="是否已发布")

    # 创建者
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建者ID")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")
    published_at = Column(DateTime(timezone=True), nullable=True, comment="发布时间")

    # 关联关系
    course = relationship("Course", foreign_keys=[course_id])
    chapter = relationship("Chapter", foreign_keys=[chapter_id])
    creator = relationship("User", foreign_keys=[created_by])

    def __repr__(self):
        return f"<Exam {self.title} ({self.exam_type.value})>"

    @property
    def is_chapter_quiz(self):
        """是否章节小测验"""
        return self.exam_type == ExamType.CHAPTER_QUIZ

    @property
    def is_daily_quiz(self):
        """是否随堂检测"""
        return self.exam_type == ExamType.DAILY_QUIZ

    @property
    def is_formal_exam(self):
        """是否正式考试（周测/月考）"""
        return self.exam_type in [ExamType.WEEKLY_TEST, ExamType.MONTHLY_EXAM, ExamType.FINAL_EXAM]
