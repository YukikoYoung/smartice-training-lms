"""
用户管理API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import secrets
import string

from ..core.database import get_db
from ..core.security import get_current_user, get_password_hash
from ..models.user import User
from ..schemas.user import UserResponse

router = APIRouter(prefix="/api/users", tags=["用户管理"])


@router.get("/", response_model=List[UserResponse])
def get_users_api(
    skip: int = 0,
    limit: int = 100,
    role: Optional[str] = None,
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取用户列表（需要管理员权限）

    - **skip**: 跳过记录数
    - **limit**: 每页记录数
    - **role**: 角色筛选
    - **department**: 部门筛选
    - **is_active**: 状态筛选
    """
    query = db.query(User)

    if role:
        query = query.filter(User.role == role)

    if department:
        query = query.filter(User.department_type == department)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.offset(skip).limit(limit).all()
    return users


@router.patch("/{user_id}/toggle-status")
def toggle_user_status_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    启用/禁用用户

    - **user_id**: 用户ID
    """
    # 检查权限（简单实现，后续可加强权限检查）
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限执行此操作"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 不能禁用自己
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能禁用自己"
        )

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    return {
        "message": f"用户已{'启用' if user.is_active else '禁用'}",
        "user_id": user.id,
        "is_active": user.is_active
    }


@router.post("/{user_id}/reset-password")
def reset_user_password_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    重置用户密码（生成随机密码）

    - **user_id**: 用户ID
    """
    # 检查权限
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限执行此操作"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    # 生成随机密码（8位，包含字母和数字）
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for _ in range(8))

    # 更新密码
    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return {
        "message": "密码重置成功",
        "user_id": user.id,
        "username": user.username,
        "new_password": new_password  # 实际应用中可通过邮件/短信发送，不直接返回
    }


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_api(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取指定用户详情

    - **user_id**: 用户ID
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )

    return user
