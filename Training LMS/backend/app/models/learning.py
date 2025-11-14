from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class LearningStatus(str, enum.Enum):
    """学习状态"""
    NOT_STARTED = "not_started"  # 未开始
    IN_PROGRESS = "in_progress"  # 学习中
    COMPLETED = "completed"  # 已完成


class ExamStatus(str, enum.Enum):
    """考试状态"""
    NOT_TAKEN = "not_taken"  # 未参加
    IN_PROGRESS = "in_progress"  # 进行中
    PASSED = "passed"  # 通过
    FAILED = "failed"  # 未通过
    PENDING_RETAKE = "pending_retake"  # 等待补考


class ValueScore(str, enum.Enum):
    """价值观评分"""
    NEEDS_IMPROVEMENT = "needs_improvement"  # 需要改进（1分）
    MEETS_EXPECTATIONS = "meets_expectations"  # 符合预期（2分）
    EXCEEDS_EXPECTATIONS = "exceeds_expectations"  # 超出预期（3分）


class CourseProgress(Base):
    """课程学习进度"""
    __tablename__ = "course_progress"

    id = Column(Integer, primary_key=True, index=True)

    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学员ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")

    # 学习状态
    status = Column(SQLEnum(LearningStatus), nullable=False, default=LearningStatus.NOT_STARTED, comment="学习状态")

    # 进度统计
    total_chapters = Column(Integer, default=0, comment="总章节数")
    completed_chapters = Column(Integer, default=0, comment="已完成章节数")
    progress_percentage = Column(Float, default=0.0, comment="完成百分比")

    # 时间记录
    started_at = Column(DateTime(timezone=True), nullable=True, comment="开始学习时间")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")
    last_accessed_at = Column(DateTime(timezone=True), nullable=True, comment="最后访问时间")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User")
    course = relationship("Course")

    def __repr__(self):
        return f"<CourseProgress User#{self.user_id} Course#{self.course_id} ({self.progress_percentage}%)>"


class ChapterProgress(Base):
    """章节学习进度"""
    __tablename__ = "chapter_progress"

    id = Column(Integer, primary_key=True, index=True)

    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学员ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False, comment="章节ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID（冗余，便于查询）")

    # 学习状态
    status = Column(SQLEnum(LearningStatus), nullable=False, default=LearningStatus.NOT_STARTED, comment="学习状态")

    # 进度统计
    total_contents = Column(Integer, default=0, comment="总内容数")
    completed_contents = Column(Integer, default=0, comment="已完成内容数")

    # 章节测验
    quiz_passed = Column(Boolean, default=False, comment="章节测验是否通过")
    quiz_score = Column(Float, nullable=True, comment="章节测验成绩")

    # 时间记录
    started_at = Column(DateTime(timezone=True), nullable=True, comment="开始学习时间")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User")
    chapter = relationship("Chapter")
    course = relationship("Course")

    def __repr__(self):
        return f"<ChapterProgress User#{self.user_id} Chapter#{self.chapter_id}>"


class ExamRecord(Base):
    """考试记录"""
    __tablename__ = "exam_records"

    id = Column(Integer, primary_key=True, index=True)

    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="考生ID")
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False, comment="考试ID")

    # 考试次数
    attempt_number = Column(Integer, default=1, comment="第几次考试（1=首次，2+=补考）")

    # 考试状态
    status = Column(SQLEnum(ExamStatus), nullable=False, default=ExamStatus.NOT_TAKEN, comment="考试状态")

    # 成绩
    score = Column(Float, nullable=True, comment="考试成绩")
    total_questions = Column(Integer, nullable=True, comment="总题数")
    correct_answers = Column(Integer, nullable=True, comment="正确题数")

    # 答题详情（JSON格式）
    # 格式：[{"question_id": 1, "user_answer": "A", "is_correct": true}, ...]
    answers = Column(JSON, nullable=True, comment="答题详情")

    # 时间记录
    started_at = Column(DateTime(timezone=True), nullable=True, comment="开始考试时间")
    submitted_at = Column(DateTime(timezone=True), nullable=True, comment="提交时间")
    graded_at = Column(DateTime(timezone=True), nullable=True, comment="评分时间")

    # 补考相关
    can_retake = Column(Boolean, default=False, comment="是否可以补考")
    next_retake_at = Column(DateTime(timezone=True), nullable=True, comment="下次可补考时间")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User")
    exam = relationship("Exam")

    def __repr__(self):
        return f"<ExamRecord User#{self.user_id} Exam#{self.exam_id} Attempt#{self.attempt_number} ({self.status.value})>"

    @property
    def is_passed(self):
        """是否通过"""
        return self.status == ExamStatus.PASSED

    @property
    def is_first_attempt(self):
        """是否首次考试"""
        return self.attempt_number == 1


class DailyQuizRecord(Base):
    """随堂检测记录（每日5题，非强制）"""
    __tablename__ = "daily_quiz_records"

    id = Column(Integer, primary_key=True, index=True)

    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="学员ID")
    quiz_date = Column(DateTime(timezone=True), nullable=False, comment="检测日期")

    # 检测内容
    question_ids = Column(JSON, nullable=False, comment="题目ID列表（5题）")

    # 成绩
    score = Column(Float, nullable=True, comment="成绩（0-100）")
    correct_answers = Column(Integer, default=0, comment="正确题数")
    total_questions = Column(Integer, default=5, comment="总题数")

    # 答题详情（JSON格式）
    answers = Column(JSON, nullable=True, comment="答题详情")

    # 完成状态
    is_completed = Column(Boolean, default=False, comment="是否完成")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="完成时间")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User")

    def __repr__(self):
        return f"<DailyQuizRecord User#{self.user_id} {self.quiz_date.date()}>"


class ValueAssessment(Base):
    """价值观行为评估（由主管/店长记录）"""
    __tablename__ = "value_assessments"

    id = Column(Integer, primary_key=True, index=True)

    # 关联信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="被评估员工ID")
    assessor_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="评估人ID（主管/店长）")

    # 评估周期
    assessment_period = Column(String(50), nullable=False, comment="评估周期（如：2025-01）")

    # 四大价值观评分
    diligence_score = Column(SQLEnum(ValueScore), nullable=True, comment="以勤劳者为本")
    customer_score = Column(SQLEnum(ValueScore), nullable=True, comment="帮助顾客")
    collaboration_score = Column(SQLEnum(ValueScore), nullable=True, comment="高效协作")
    transparency_score = Column(SQLEnum(ValueScore), nullable=True, comment="平等透明")

    # 评语
    comments = Column(Text, nullable=True, comment="评语（选填）")

    # 优秀案例或问题记录
    notable_behaviors = Column(Text, nullable=True, comment="突出表现或问题行为记录")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User", foreign_keys=[user_id])
    assessor = relationship("User", foreign_keys=[assessor_id])

    def __repr__(self):
        return f"<ValueAssessment User#{self.user_id} Period:{self.assessment_period}>"

    @property
    def average_score(self):
        """平均分（1-3分）"""
        scores = []
        score_map = {
            ValueScore.NEEDS_IMPROVEMENT: 1,
            ValueScore.MEETS_EXPECTATIONS: 2,
            ValueScore.EXCEEDS_EXPECTATIONS: 3,
        }
        for score in [self.diligence_score, self.customer_score, self.collaboration_score, self.transparency_score]:
            if score:
                scores.append(score_map[score])
        return sum(scores) / len(scores) if scores else 0
