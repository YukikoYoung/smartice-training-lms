from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class UserRole(str, enum.Enum):
    """用户角色（职级）"""
    L1 = "L1"  # 基层员工
    L2 = "L2"  # 骨干员工
    L3 = "L3"  # 主管
    L4 = "L4"  # 店长/厨师长
    L5 = "L5"  # 区域经理
    L5_PLUS = "L5+"  # 运营负责人


class DepartmentType(str, enum.Enum):
    """部门类型"""
    FRONT_HALL = "front_hall"  # 前厅
    KITCHEN = "kitchen"  # 厨房
    HEADQUARTERS = "headquarters"  # 企业总部（运营负责人、区域经理）


class User(Base):
    """用户数据模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # 用户基本信息
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名（唯一，用于登录）")
    hashed_password = Column(String(200), nullable=False, comment="密码哈希值")
    full_name = Column(String(100), nullable=False, comment="真实姓名")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")

    # 角色与职级
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.L1, comment="职级（L1-L5+）")

    # 组织架构关联
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True, comment="岗位ID")
    store_id = Column(Integer, ForeignKey("stores.id"), nullable=True, comment="门店ID（L1-L4有门店）")
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=True, comment="区域ID（L5区域经理）")
    department_type = Column(SQLEnum(DepartmentType), nullable=True, comment="部门类型（前厅/厨房/总部）")

    # 职位特性（用于权限判断）
    is_store_manager = Column(Boolean, default=False, comment="是否店长（大店长制）")
    is_kitchen_manager = Column(Boolean, default=False, comment="是否厨师长")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员（系统管理员）")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    position = relationship("Position", back_populates="users")
    store = relationship("Store", back_populates="users")
    region = relationship("Region", back_populates="managers")

    def __repr__(self):
        return f"<User {self.username} ({self.role})>"

    @property
    def is_employee(self):
        """是否基层员工（L1-L2）"""
        return self.role in [UserRole.L1, UserRole.L2]

    @property
    def is_supervisor(self):
        """是否主管（L3）"""
        return self.role == UserRole.L3

    @property
    def is_manager(self):
        """是否门店管理层（L4：店长/厨师长）"""
        return self.role == UserRole.L4

    @property
    def is_regional_manager(self):
        """是否区域经理（L5）"""
        return self.role == UserRole.L5

    @property
    def is_operations_director(self):
        """是否运营负责人（L5+）"""
        return self.role == UserRole.L5_PLUS

    @property
    def can_manage_others(self):
        """是否有管理权限（L3及以上）"""
        return self.role in [UserRole.L3, UserRole.L4, UserRole.L5, UserRole.L5_PLUS]
