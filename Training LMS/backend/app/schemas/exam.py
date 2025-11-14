"""
考试系统相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..models.exam import ExamType, QuestionType, QuestionCategory


# ========== Question Schemas ==========

class QuestionOption(BaseModel):
    """题目选项"""
    label: str = Field(..., description="选项标签（A/B/C/D）")
    content: str = Field(..., description="选项内容")
    is_correct: bool = Field(default=False, description="是否正确答案")


class QuestionBase(BaseModel):
    """题目基础Schema"""
    content: str = Field(..., min_length=1, description="题目内容")
    question_type: QuestionType = Field(..., description="题目类型")
    category: QuestionCategory = Field(default=QuestionCategory.SKILL, description="题目分类")
    course_id: Optional[int] = Field(None, gt=0, description="关联课程ID")
    chapter_id: Optional[int] = Field(None, gt=0, description="关联章节ID")
    difficulty: Optional[str] = Field(None, max_length=20, description="难度等级")
    options: Optional[List[Dict[str, Any]]] = Field(None, description="选项列表（JSON）")
    correct_answer: Optional[str] = Field(None, description="正确答案（判断题/简答题）")
    explanation: Optional[str] = Field(None, description="答案解析")
    is_active: bool = Field(default=True, description="是否启用")


class QuestionCreate(QuestionBase):
    """创建题目"""
    pass


class QuestionUpdate(BaseModel):
    """更新题目"""
    content: Optional[str] = Field(None, min_length=1)
    question_type: Optional[QuestionType] = None
    category: Optional[QuestionCategory] = None
    course_id: Optional[int] = Field(None, gt=0)
    chapter_id: Optional[int] = Field(None, gt=0)
    difficulty: Optional[str] = Field(None, max_length=20)
    options: Optional[List[Dict[str, Any]]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    is_active: Optional[bool] = None


class QuestionResponse(QuestionBase):
    """题目响应"""
    id: int
    created_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class QuestionResponseWithoutAnswer(BaseModel):
    """题目响应（不含答案，用于考试）"""
    id: int
    content: str
    question_type: QuestionType
    category: QuestionCategory
    difficulty: Optional[str]
    options: Optional[List[Dict[str, Any]]]  # 选项中不含is_correct字段
    explanation: Optional[str] = None  # 考试时不显示解析

    class Config:
        from_attributes = True


# ========== Exam Schemas ==========

class ExamBase(BaseModel):
    """考试基础Schema"""
    title: str = Field(..., min_length=1, max_length=200, description="考试标题")
    exam_type: ExamType = Field(..., description="考试类型")
    description: Optional[str] = Field(None, description="考试说明")
    course_id: Optional[int] = Field(None, gt=0, description="关联课程ID")
    chapter_id: Optional[int] = Field(None, gt=0, description="关联章节ID")
    total_questions: int = Field(..., gt=0, description="总题数")
    pass_score: float = Field(default=70.0, ge=0, le=100, description="及格分数")
    time_limit: Optional[int] = Field(None, gt=0, description="考试时长（分钟）")
    question_distribution: Optional[Dict[str, int]] = Field(None, description="题目分布配置")
    question_ids: Optional[List[int]] = Field(None, description="题目ID列表（固定考题）")
    allow_retake: bool = Field(default=True, description="是否允许补考")
    max_attempts: int = Field(default=3, gt=0, description="最大考试次数")
    retake_cooldown_days: int = Field(default=3, ge=0, description="补考冷却期（天）")
    is_active: bool = Field(default=True, description="是否启用")


class ExamCreate(ExamBase):
    """创建考试"""
    pass


class ExamUpdate(BaseModel):
    """更新考试"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    exam_type: Optional[ExamType] = None
    description: Optional[str] = None
    course_id: Optional[int] = Field(None, gt=0)
    chapter_id: Optional[int] = Field(None, gt=0)
    total_questions: Optional[int] = Field(None, gt=0)
    pass_score: Optional[float] = Field(None, ge=0, le=100)
    time_limit: Optional[int] = Field(None, gt=0)
    question_distribution: Optional[Dict[str, int]] = None
    question_ids: Optional[List[int]] = None
    allow_retake: Optional[bool] = None
    max_attempts: Optional[int] = Field(None, gt=0)
    retake_cooldown_days: Optional[int] = Field(None, ge=0)
    is_published: Optional[bool] = None
    is_active: Optional[bool] = None


class ExamResponse(ExamBase):
    """考试响应"""
    id: int
    is_published: bool
    created_by: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True


class ExamListResponse(BaseModel):
    """考试列表响应（简化）"""
    id: int
    title: str
    exam_type: ExamType
    total_questions: int
    pass_score: float
    time_limit: Optional[int]
    is_published: bool
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 考试答题相关 Schemas ==========

class AnswerSubmit(BaseModel):
    """提交答案"""
    question_id: int = Field(..., gt=0, description="题目ID")
    user_answer: str = Field(..., description="用户答案")


class ExamSubmit(BaseModel):
    """提交考试"""
    exam_id: int = Field(..., gt=0, description="考试ID")
    answers: List[AnswerSubmit] = Field(..., min_length=1, description="答案列表")
    time_spent: Optional[int] = Field(None, ge=0, description="答题耗时（秒）")


class ExamResult(BaseModel):
    """考试结果"""
    exam_record_id: int
    exam_id: int
    exam_title: str
    score: float
    passed: bool
    attempt_number: int
    max_attempts: int
    can_retake: bool
    next_retake_at: Optional[datetime]
    correct_count: int
    total_questions: int
    time_spent: Optional[int]

    class Config:
        from_attributes = True
