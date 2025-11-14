from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Region(Base):
    """区域模型（由L5区域经理管理）"""
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, unique=True, comment="区域名称（如：成都区域、重庆区域）")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="区域编码（如：CD、CQ）")
    description = Column(Text, nullable=True, comment="区域描述")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否启用")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    stores = relationship("Store", back_populates="region", cascade="all, delete-orphan")
    managers = relationship("User", back_populates="region")  # L5区域经理

    def __repr__(self):
        return f"<Region {self.name}>"


class Store(Base):
    """门店模型"""
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String(100), nullable=False, comment="门店名称（如：春熙路店、IFS店）")
    code = Column(String(50), nullable=False, unique=True, index=True, comment="门店编码（如：CD001）")
    address = Column(String(200), nullable=True, comment="门店地址")
    phone = Column(String(20), nullable=True, comment="门店电话")

    # 组织架构
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False, comment="所属区域ID")

    # 状态
    is_active = Column(Boolean, default=True, comment="是否营业")

    # 时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), comment="更新时间")

    # 关联关系
    region = relationship("Region", back_populates="stores")
    users = relationship("User", back_populates="store")  # 该门店的所有员工（L1-L4）

    def __repr__(self):
        return f"<Store {self.name} ({self.code})>"

    @property
    def store_manager(self):
        """获取店长（L4 + is_store_manager=True）"""
        return next((user for user in self.users if user.is_store_manager), None)

    @property
    def kitchen_manager(self):
        """获取厨师长（L4 + is_kitchen_manager=True）"""
        return next((user for user in self.users if user.is_kitchen_manager), None)

    @property
    def front_hall_staff(self):
        """获取前厅员工"""
        from .user import DepartmentType
        return [user for user in self.users if user.department_type == DepartmentType.FRONT_HALL]

    @property
    def kitchen_staff(self):
        """获取厨房员工"""
        from .user import DepartmentType
        return [user for user in self.users if user.department_type == DepartmentType.KITCHEN]
