"""
Pytest配置文件
提供测试夹具(fixtures)和共享配置
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.models.user import User
from app.models.organization import Store, Region
from app.models.position import Position
from app.core.security import get_password_hash
from main import app


# 测试数据库引擎(使用内存SQLite)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    创建测试数据库会话
    每个测试函数独立的数据库会话
    """
    # 创建所有表
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # 测试结束后清理所有表
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    创建测试客户端
    覆盖默认的数据库依赖
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_region(db_session):
    """创建测试区域"""
    region = Region(
        name="测试区域",
        code="TEST01"
    )
    db_session.add(region)
    db_session.commit()
    db_session.refresh(region)
    return region


@pytest.fixture(scope="function")
def test_organization(db_session, test_region):
    """创建测试门店(用于兼容旧测试代码)"""
    store = Store(
        name="测试餐厅",
        code="STORE01",
        region_id=test_region.id,
        phone="1234567890"
    )
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)
    return store


@pytest.fixture(scope="function")
def test_position(db_session):
    """创建测试职位"""
    from app.models.user import DepartmentType
    position = Position(
        name="服务员",
        code="FH_WAITER_TEST",
        department_type=DepartmentType.FRONT_HALL,
        recommended_level="L1"
    )
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)
    return position


@pytest.fixture(scope="function")
def test_user(db_session, test_organization, test_position):
    """创建测试用户"""
    from app.models.user import UserRole, DepartmentType
    user = User(
        username="testuser",
        full_name="测试用户",
        hashed_password=get_password_hash("testpass123"),
        store_id=test_organization.id,
        position_id=test_position.id,
        role=UserRole.L1,
        department_type=DepartmentType.FRONT_HALL,
        phone="13800138000",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
def admin_user(db_session, test_region):
    """创建测试管理员用户"""
    from app.models.user import UserRole, DepartmentType

    # 创建管理员职位
    admin_position = Position(
        name="运营负责人",
        code="HQ_OPERATIONS_MANAGER",
        department_type=DepartmentType.HEADQUARTERS,
        recommended_level="L5+"
    )
    db_session.add(admin_position)
    db_session.commit()

    # 创建管理员用户(L5+不需要门店,关联区域)
    admin = User(
        username="admin",
        full_name="管理员",
        hashed_password=get_password_hash("admin123"),
        region_id=test_region.id,
        position_id=admin_position.id,
        role=UserRole.L5_PLUS,
        department_type=DepartmentType.HEADQUARTERS,
        phone="13900139000",
        is_active=True
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """
    获取认证头
    返回包含JWT token的headers
    """
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpass123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(client, admin_user):
    """
    获取管理员认证头
    返回包含JWT token的headers
    """
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# 测试数据常量
TEST_USER_DATA = {
    "username": "newuser",
    "password": "newpass123",
    "real_name": "新用户",
    "phone": "13700137000"
}

TEST_COURSE_DATA = {
    "title": "测试课程",
    "department": "FRONTHALL",
    "target_level": "L1",
    "description": "这是一个测试课程"
}

TEST_EXAM_DATA = {
    "title": "测试考试",
    "department": "FRONTHALL",
    "target_level": "L1",
    "duration_minutes": 60,
    "total_score": 100,
    "passing_score": 80
}
