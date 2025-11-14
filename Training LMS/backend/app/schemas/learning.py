"""
学习进度相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from ..models.learning import LearningStatus, ExamStatus, ValueScore


# ========== CourseProgress Schemas ==========

class CourseProgressBase(BaseModel):
    """课程学习进度基础Schema"""
    status: LearningStatus = Field(default=LearningStatus.NOT_STARTED, description="学习状态")
    total_chapters: int = Field(default=0, ge=0, description="总章节数")
    completed_chapters: int = Field(default=0, ge=0, description="已完成章节数")
    progress_percentage: float = Field(default=0.0, ge=0, le=100, description="完成百分比")


class CourseProgressCreate(BaseModel):
    """创建课程学习进度"""
    user_id: int = Field(..., gt=0, description="学员ID")
    course_id: int = Field(..., gt=0, description="课程ID")


class CourseProgressUpdate(BaseModel):
    """更新课程学习进度"""
    status: Optional[LearningStatus] = None
    total_chapters: Optional[int] = Field(None, ge=0)
    completed_chapters: Optional[int] = Field(None, ge=0)
    progress_percentage: Optional[float] = Field(None, ge=0, le=100)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_accessed_at: Optional[datetime] = None


class CourseProgressResponse(CourseProgressBase):
    """课程学习进度响应"""
    id: int
    user_id: int
    course_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    last_accessed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== ChapterProgress Schemas ==========

class ChapterProgressBase(BaseModel):
    """章节学习进度基础Schema"""
    status: LearningStatus = Field(default=LearningStatus.NOT_STARTED, description="学习状态")
    total_contents: int = Field(default=0, ge=0, description="总内容数")
    completed_contents: int = Field(default=0, ge=0, description="已完成内容数")
    quiz_passed: bool = Field(default=False, description="章节测验是否通过")
    quiz_score: Optional[float] = Field(None, ge=0, le=100, description="章节测验成绩")


class ChapterProgressCreate(BaseModel):
    """创建章节学习进度"""
    user_id: int = Field(..., gt=0, description="学员ID")
    chapter_id: int = Field(..., gt=0, description="章节ID")
    course_id: int = Field(..., gt=0, description="课程ID")


class ChapterProgressUpdate(BaseModel):
    """更新章节学习进度"""
    status: Optional[LearningStatus] = None
    total_contents: Optional[int] = Field(None, ge=0)
    completed_contents: Optional[int] = Field(None, ge=0)
    quiz_passed: Optional[bool] = None
    quiz_score: Optional[float] = Field(None, ge=0, le=100)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ChapterProgressResponse(ChapterProgressBase):
    """章节学习进度响应"""
    id: int
    user_id: int
    chapter_id: int
    course_id: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== ExamRecord Schemas ==========

class ExamRecordBase(BaseModel):
    """考试记录基础Schema"""
    attempt_number: int = Field(default=1, gt=0, description="第几次考试")
    status: ExamStatus = Field(default=ExamStatus.NOT_TAKEN, description="考试状态")
    score: Optional[float] = Field(None, ge=0, le=100, description="考试成绩")
    total_questions: Optional[int] = Field(None, ge=0, description="总题数")
    correct_answers: Optional[int] = Field(None, ge=0, description="正确题数")
    answers: Optional[List[Dict[str, Any]]] = Field(None, description="答题详情")


class ExamRecordCreate(BaseModel):
    """创建考试记录"""
    user_id: int = Field(..., gt=0, description="考生ID")
    exam_id: int = Field(..., gt=0, description="考试ID")
    attempt_number: int = Field(default=1, gt=0, description="第几次考试")


class ExamRecordUpdate(BaseModel):
    """更新考试记录"""
    status: Optional[ExamStatus] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    total_questions: Optional[int] = Field(None, ge=0)
    correct_answers: Optional[int] = Field(None, ge=0)
    answers: Optional[List[Dict[str, Any]]] = None
    started_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    graded_at: Optional[datetime] = None
    can_retake: Optional[bool] = None
    next_retake_at: Optional[datetime] = None


class ExamRecordResponse(ExamRecordBase):
    """考试记录响应"""
    id: int
    user_id: int
    exam_id: int
    started_at: Optional[datetime]
    submitted_at: Optional[datetime]
    graded_at: Optional[datetime]
    can_retake: bool
    next_retake_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== DailyQuizRecord Schemas ==========

class DailyQuizRecordBase(BaseModel):
    """随堂检测记录基础Schema"""
    quiz_date: datetime = Field(..., description="检测日期")
    question_ids: List[int] = Field(..., min_length=5, max_length=5, description="题目ID列表（5题）")
    score: Optional[float] = Field(None, ge=0, le=100, description="成绩")
    correct_answers: int = Field(default=0, ge=0, le=5, description="正确题数")
    total_questions: int = Field(default=5, description="总题数")
    answers: Optional[List[Dict[str, Any]]] = Field(None, description="答题详情")
    is_completed: bool = Field(default=False, description="是否完成")


class DailyQuizRecordCreate(BaseModel):
    """创建随堂检测记录"""
    user_id: int = Field(..., gt=0, description="学员ID")
    quiz_date: datetime = Field(..., description="检测日期")
    question_ids: List[int] = Field(..., min_length=5, max_length=5, description="题目ID列表")


class DailyQuizRecordUpdate(BaseModel):
    """更新随堂检测记录"""
    score: Optional[float] = Field(None, ge=0, le=100)
    correct_answers: Optional[int] = Field(None, ge=0, le=5)
    answers: Optional[List[Dict[str, Any]]] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class DailyQuizRecordResponse(DailyQuizRecordBase):
    """随堂检测记录响应"""
    id: int
    user_id: int
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ========== ValueAssessment Schemas ==========

class ValueAssessmentBase(BaseModel):
    """价值观评估基础Schema"""
    assessment_period: str = Field(..., min_length=1, max_length=50, description="评估周期（如：2025-01）")
    diligence_score: Optional[ValueScore] = Field(None, description="以勤劳者为本")
    customer_score: Optional[ValueScore] = Field(None, description="帮助顾客")
    collaboration_score: Optional[ValueScore] = Field(None, description="高效协作")
    transparency_score: Optional[ValueScore] = Field(None, description="平等透明")
    comments: Optional[str] = Field(None, description="评语")
    notable_behaviors: Optional[str] = Field(None, description="突出表现或问题行为记录")


class ValueAssessmentCreate(ValueAssessmentBase):
    """创建价值观评估"""
    user_id: int = Field(..., gt=0, description="被评估员工ID")
    assessor_id: int = Field(..., gt=0, description="评估人ID")


class ValueAssessmentUpdate(BaseModel):
    """更新价值观评估"""
    diligence_score: Optional[ValueScore] = None
    customer_score: Optional[ValueScore] = None
    collaboration_score: Optional[ValueScore] = None
    transparency_score: Optional[ValueScore] = None
    comments: Optional[str] = None
    notable_behaviors: Optional[str] = None


class ValueAssessmentResponse(ValueAssessmentBase):
    """价值观评估响应"""
    id: int
    user_id: int
    assessor_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
