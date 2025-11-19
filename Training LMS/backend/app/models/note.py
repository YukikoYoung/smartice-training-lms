from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Note(Base):
    """学习笔记模型"""
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)

    # 笔记归属
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, comment="课程ID")
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=True, comment="章节ID（可选）")

    # 笔记内容
    title = Column(String(200), nullable=False, comment="笔记标题")
    content = Column(Text, nullable=False, comment="笔记内容(Markdown)")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    user = relationship("User", backref="notes")
    course = relationship("Course", backref="notes")
    chapter = relationship("Chapter", backref="notes")

    def __repr__(self):
        return f"<Note {self.title} by User#{self.user_id}>"
