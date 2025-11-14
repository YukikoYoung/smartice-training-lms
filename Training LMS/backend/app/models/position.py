from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
from .user import DepartmentType


class Position(Base):
    """岗位模型"""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, comment="岗位名称（如：服务员、收银员、切配岗）")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="岗位编码（如：FH_WAITER、KC_PREP）")
    description = Column(Text, nullable=True, comment="岗位描述")

    # 部门归属
    department_type = Column(SQLEnum(DepartmentType), nullable=False, comment="部门类型（前厅/厨房/总部）")

    # 岗位分组（用于知识库映射）
    group = Column(String(100), nullable=True, comment="岗位组（如：服务组、烹饪组、管理组）")

    # 职级要求（用于晋升参考，不强制）
    recommended_level = Column(String(20), nullable=True, comment="推荐职级（如：L1-L2）")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    users = relationship("User", back_populates="position")

    def __repr__(self):
        return f"<Position {self.name} ({self.department_type.value})>"

    @property
    def is_front_hall_position(self):
        """是否前厅岗位"""
        return self.department_type == DepartmentType.FRONT_HALL

    @property
    def is_kitchen_position(self):
        """是否厨房岗位"""
        return self.department_type == DepartmentType.KITCHEN

    @property
    def is_headquarters_position(self):
        """是否总部岗位"""
        return self.department_type == DepartmentType.HEADQUARTERS
