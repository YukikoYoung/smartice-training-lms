from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Certificate(Base):
    """证书模型"""
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)

    # 证书归属
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")
    exam_record_id = Column(Integer, ForeignKey("exam_records.id"), nullable=True, comment="考试记录ID")

    # 证书信息
    certificate_number = Column(String(50), unique=True, nullable=False, index=True, comment="证书编号")
    title = Column(String(200), nullable=False, comment="证书标题")
    description = Column(String(500), nullable=True, comment="证书描述")

    # 成绩信息
    score = Column(Integer, nullable=True, comment="考试成绩")

    # 发证信息
    issued_at = Column(DateTime(timezone=True), server_default=func.now(), comment="发证时间")
    issuer = Column(String(100), default="SmartIce培训管理系统", comment="发证机构")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")

    # 关联关系
    user = relationship("User", backref="certificates")
    course = relationship("Course", backref="certificates")
    exam_record = relationship("ExamRecord", backref="certificates")

    def __repr__(self):
        return f"<Certificate {self.certificate_number} for User#{self.user_id}>"
