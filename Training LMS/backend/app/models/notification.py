from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class NotificationType(str, enum.Enum):
    """通知类型"""
    SYSTEM = "system"  # 系统通知
    EXAM = "exam"  # 考试通知
    TRAINING = "training"  # 培训通知
    ACHIEVEMENT = "achievement"  # 成就通知


class Notification(Base):
    """消息通知模型"""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    # 接收者
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="接收者ID")

    # 通知内容
    type = Column(
        SQLEnum(NotificationType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        comment="通知类型"
    )
    title = Column(String(200), nullable=False, comment="通知标题")
    content = Column(Text, nullable=False, comment="通知内容")

    # 状态
    is_read = Column(Boolean, default=False, comment="是否已读")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    read_at = Column(DateTime(timezone=True), nullable=True, comment="阅读时间")

    # 关联关系
    user = relationship("User", backref="notifications")

    def __repr__(self):
        return f"<Notification {self.title} to User#{self.user_id}>"
