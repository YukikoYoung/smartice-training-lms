from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import logging

from ..core.database import get_db
from ..core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from ..models.user import User
from ..schemas.user import UserCreate, UserLogin, UserResponse, Token

router = APIRouter(prefix="/api/auth", tags=["认证"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册（由管理员创建用户）

    - **username**: 用户名（3-50字符，唯一）
    - **full_name**: 真实姓名
    - **phone**: 手机号（可选，唯一）
    - **password**: 密码（至少6位）
    - **role**: 职级（L1-L5+）
    - **department_type**: 部门类型（前厅/厨房/总部）
    """
    try:
        logger.info(f"收到注册请求: username={user_data.username}")

        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

        # 检查手机号是否已存在
        if user_data.phone:
            existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号已被注册"
                )

        # 创建用户
        logger.debug("开始哈希密码...")
        hashed_password = get_password_hash(user_data.password)
        logger.debug("密码哈希成功")

        new_user = User(
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role,
            department_type=user_data.department_type,
            position_id=user_data.position_id,
            store_id=user_data.store_id,
            region_id=user_data.region_id,
            is_store_manager=user_data.is_store_manager,
            is_kitchen_manager=user_data.is_kitchen_manager,
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"用户创建成功: id={new_user.id}")
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"注册失败: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"注册失败: {str(e)}"
        )


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录

    - **username**: 用户名或手机号
    - **password**: 密码

    返回 JWT Token
    """
    # 支持用户名或手机号登录
    user = db.query(User).filter(
        (User.username == user_data.username) | (User.phone == user_data.username)
    ).first()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    # 生成 Token
    access_token = create_access_token(data={"user_id": user.id, "username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/login/form", response_model=Token)
def login_form(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 标准登录接口（用于 Swagger UI 测试）

    - **username**: 用户名或手机号
    - **password**: 密码
    """
    user = db.query(User).filter(
        (User.username == form_data.username) | (User.phone == form_data.username)
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    access_token = create_access_token(data={"user_id": user.id, "username": user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前登录用户信息

    需要在请求头中携带 Token:
    ```
    Authorization: Bearer <your_token>
    ```
    """
    return current_user
