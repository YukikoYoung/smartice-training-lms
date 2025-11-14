"""
初始化数据脚本
创建示例的区域、门店、岗位、用户数据
"""
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models import (
    User, UserRole, DepartmentType,
    Region, Store, Position
)
from app.core.security import get_password_hash


def init_data():
    """初始化示例数据"""
    # 首先创建所有表
    print("=" * 60)
    print("开始初始化数据...")
    print("=" * 60)

    print("\n[0/5] 创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("  ✓ 数据库表创建完成")

    db = SessionLocal()

    try:
        # 1. 创建区域
        print("\n[1/5] 创建区域...")
        region_chengdu = Region(
            name="成都区域",
            code="CD",
            description="成都市区域管理"
        )
        db.add(region_chengdu)
        db.flush()  # 获取ID
        print(f"  ✓ 创建区域：{region_chengdu.name}")

        # 2. 创建门店
        print("\n[2/5] 创建门店...")
        store_chunxilu = Store(
            name="春熙路店",
            code="CD001",
            address="成都市锦江区春熙路",
            phone="028-12345678",
            region_id=region_chengdu.id
        )
        db.add(store_chunxilu)
        db.flush()
        print(f"  ✓ 创建门店：{store_chunxilu.name}")

        # 3. 创建岗位
        print("\n[3/5] 创建岗位...")
        positions = [
            # 前厅岗位
            Position(name="店长", code="MANAGER", department_type=DepartmentType.FRONT_HALL, group="管理组", recommended_level="L4"),
            Position(name="前厅主管", code="FH_SUPERVISOR", department_type=DepartmentType.FRONT_HALL, group="管理组", recommended_level="L3"),
            Position(name="服务员", code="FH_WAITER", department_type=DepartmentType.FRONT_HALL, group="服务组", recommended_level="L1-L2"),
            Position(name="收银员", code="FH_CASHIER", department_type=DepartmentType.FRONT_HALL, group="服务组", recommended_level="L1-L2"),
            Position(name="迎宾员", code="FH_GREETER", department_type=DepartmentType.FRONT_HALL, group="服务组", recommended_level="L1-L2"),
            Position(name="传菜员", code="FH_RUNNER", department_type=DepartmentType.FRONT_HALL, group="后勤组", recommended_level="L1-L2"),
            Position(name="保洁员", code="FH_CLEANER", department_type=DepartmentType.FRONT_HALL, group="后勤组", recommended_level="L1-L2"),
            # 厨房岗位
            Position(name="厨师长", code="KC_CHEF", department_type=DepartmentType.KITCHEN, group="管理组", recommended_level="L4"),
            Position(name="后厨主管", code="KC_SUPERVISOR", department_type=DepartmentType.KITCHEN, group="管理组", recommended_level="L3"),
            Position(name="切配岗", code="KC_PREP", department_type=DepartmentType.KITCHEN, group="烹饪组", recommended_level="L1-L2"),
            Position(name="热菜岗", code="KC_HOT", department_type=DepartmentType.KITCHEN, group="烹饪组", recommended_level="L1-L2"),
            # 总部岗位
            Position(name="运营负责人", code="HQ_OPS_DIRECTOR", department_type=DepartmentType.HEADQUARTERS, group="企业管理", recommended_level="L5+"),
            Position(name="区域经理", code="HQ_REGIONAL_MANAGER", department_type=DepartmentType.HEADQUARTERS, group="区域管理", recommended_level="L5"),
        ]
        db.add_all(positions)
        db.flush()
        print(f"  ✓ 创建岗位：{len(positions)}个")

        # 获取岗位引用
        pos_manager = next(p for p in positions if p.code == "MANAGER")
        pos_waiter = next(p for p in positions if p.code == "FH_WAITER")
        pos_chef = next(p for p in positions if p.code == "KC_CHEF")
        pos_ops_director = next(p for p in positions if p.code == "HQ_OPS_DIRECTOR")
        pos_regional_manager = next(p for p in positions if p.code == "HQ_REGIONAL_MANAGER")

        # 4. 创建用户
        print("\n[4/5] 创建用户...")
        users = [
            # 运营负责人（L5+）
            User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="张总",
                phone="13800000001",
                role=UserRole.L5_PLUS,
                department_type=DepartmentType.HEADQUARTERS,
                position_id=pos_ops_director.id,
                is_active=True,
                is_superuser=True
            ),
            # 区域经理（L5）
            User(
                username="regional_mgr",
                hashed_password=get_password_hash("123456"),
                full_name="李经理",
                phone="13800000002",
                role=UserRole.L5,
                department_type=DepartmentType.HEADQUARTERS,
                region_id=region_chengdu.id,
                position_id=pos_regional_manager.id,
                is_active=True
            ),
            # 店长（L4）
            User(
                username="store_mgr",
                hashed_password=get_password_hash("123456"),
                full_name="王店长",
                phone="13800000003",
                role=UserRole.L4,
                department_type=DepartmentType.FRONT_HALL,
                store_id=store_chunxilu.id,
                position_id=pos_manager.id,
                is_store_manager=True,
                is_active=True
            ),
            # 厨师长（L4）
            User(
                username="chef",
                hashed_password=get_password_hash("123456"),
                full_name="赵厨师长",
                phone="13800000004",
                role=UserRole.L4,
                department_type=DepartmentType.KITCHEN,
                store_id=store_chunxilu.id,
                position_id=pos_chef.id,
                is_kitchen_manager=True,
                is_active=True
            ),
            # 服务员（L1）
            User(
                username="waiter001",
                hashed_password=get_password_hash("123456"),
                full_name="小王",
                phone="13800000005",
                role=UserRole.L1,
                department_type=DepartmentType.FRONT_HALL,
                store_id=store_chunxilu.id,
                position_id=pos_waiter.id,
                is_active=True
            ),
        ]
        db.add_all(users)
        db.flush()
        print(f"  ✓ 创建用户：{len(users)}个")
        for user in users:
            print(f"     - {user.username} ({user.full_name}) - {user.role.value}")

        # 5. 提交事务
        print("\n[5/5] 提交数据...")
        db.commit()
        print("  ✓ 数据提交成功！")

        print("\n" + "=" * 60)
        print("数据初始化完成！")
        print("=" * 60)
        print("\n默认登录账号：")
        print("  运营负责人: admin / admin123")
        print("  区域经理: regional_mgr / 123456")
        print("  店长: store_mgr / 123456")
        print("  厨师长: chef / 123456")
        print("  服务员: waiter001 / 123456")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_data()
