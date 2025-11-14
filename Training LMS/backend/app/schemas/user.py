from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..models.user import UserRole, DepartmentType


# ========== 用户基础模型 ==========
class UserBase(BaseModel):
    """用户基础信息"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    full_name: str = Field(..., max_length=100, description="真实姓名")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")


# ========== 用户创建 ==========
class UserCreate(UserBase):
    """用户注册/创建请求"""
    password: str = Field(..., min_length=6, max_length=50, description="密码（至少6位）")
    role: UserRole = Field(default=UserRole.L1, description="职级")
    department_type: Optional[DepartmentType] = Field(None, description="部门类型")
    position_id: Optional[int] = Field(None, description="岗位ID")
    store_id: Optional[int] = Field(None, description="门店ID")
    region_id: Optional[int] = Field(None, description="区域ID")
    is_store_manager: bool = Field(default=False, description="是否店长")
    is_kitchen_manager: bool = Field(default=False, description="是否厨师长")


# ========== 用户登录 ==========
class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(..., description="用户名或手机号")
    password: str = Field(..., description="密码")


# ========== 用户更新 ==========
class UserUpdate(BaseModel):
    """用户信息更新"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6, max_length=50)
    position_id: Optional[int] = None
    store_id: Optional[int] = None
    is_active: Optional[bool] = None


# ========== 用户响应 ==========
class UserResponse(UserBase):
    """用户信息响应（不包含密码）"""
    id: int
    role: UserRole
    department_type: Optional[DepartmentType]
    position_id: Optional[int]
    store_id: Optional[int]
    region_id: Optional[int]
    is_store_manager: bool
    is_kitchen_manager: bool
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== Token 响应 ==========
class Token(BaseModel):
    """JWT Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token 解析数据"""
    user_id: Optional[int] = None
    username: Optional[str] = None
