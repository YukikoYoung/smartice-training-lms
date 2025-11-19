from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class WrongQuestion(Base):
    """错题记录模型"""
    __tablename__ = "wrong_questions"

    id = Column(Integer, primary_key=True, index=True)

    # 归属
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False, comment="题目ID")
    exam_record_id = Column(Integer, ForeignKey("exam_records.id"), nullable=True, comment="考试记录ID")

    # 错题统计
    wrong_count = Column(Integer, default=1, comment="错误次数")
    last_wrong_date = Column(DateTime(timezone=True), server_default=func.now(), comment="最后一次答错时间")

    # 用户答案
    my_answer = Column(Text, nullable=False, comment="用户的错误答案")

    # 掌握状态
    mastered = Column(Boolean, default=False, comment="是否已掌握")
    mastered_at = Column(DateTime(timezone=True), nullable=True, comment="掌握时间")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关联关系
    user = relationship("User", backref="wrong_questions")
    question = relationship("Question", backref="wrong_records")
    exam_record = relationship("ExamRecord", backref="wrong_questions")

    def __repr__(self):
        return f"<WrongQuestion User#{self.user_id} Q#{self.question_id} (x{self.wrong_count})>"
