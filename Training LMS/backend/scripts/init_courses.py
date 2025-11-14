"""
课程内容初始化脚本
将knowlege目录下的运营标准文档导入为真实课程数据
"""
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal, engine, Base
from app.models import (
    User, Course, Chapter, Content,
    DepartmentType, ContentType
)
from datetime import datetime


def init_courses():
    """初始化课程数据"""
    print("=" * 60)
    print("开始导入课程内容...")
    print("=" * 60)

    db = SessionLocal()

    try:
        # 获取创建者（admin用户）
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("❌ 错误：未找到admin用户，请先运行 init_data.py")
            return

        creator_id = admin_user.id
        print(f"\n✓ 找到创建者：{admin_user.full_name} (ID: {creator_id})")

        # ========== 1. 前厅运营标准课程 ==========
        print("\n[1/2] 创建前厅运营标准课程...")

        course_fronthall = Course(
            title="前厅运营标准与服务流程",
            code="FH-OPS-001",
            description="餐厅前厅全岗位运营管理标准手册，包含通用管理标准、服务礼仪、各岗位工作流程等核心内容。",
            department_type=DepartmentType.FRONT_HALL,
            category="岗位技能",
            is_mandatory=True,
            version="VN202501-MERGED",
            created_by=creator_id
        )
        db.add(course_fronthall)
        db.flush()
        print(f"  ✓ 课程创建：{course_fronthall.title}")

        # 章节1: 通用管理标准
        chapter_fh_1 = Chapter(
            course_id=course_fronthall.id,
            title="通用管理标准",
            description="前厅所有岗位必须遵守的基础标准",
            order=1,
            has_quiz=True
        )
        db.add(chapter_fh_1)
        db.flush()

        # 章节1内容
        contents_fh_1 = [
            Content(
                chapter_id=chapter_fh_1.id,
                title="通用服务礼仪 - 客人问候标准、服务态度标准",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch1/service-etiquette.md",
                duration=900,  # 15分钟 = 900秒
                order=1
            ),
            Content(
                chapter_id=chapter_fh_1.id,
                title="仪容仪表标准 - 男士/女士仪容仪表规范、着装标准",
                content_type=ContentType.VIDEO,
                file_url="/content/fronthall/ch1/appearance-standards.mp4",
                duration=1200,  # 20分钟 = 1200秒
                order=2
            ),
            Content(
                chapter_id=chapter_fh_1.id,
                title="毛巾使用标准 - 分色使用、清洗消毒、定位摆放",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch1/towel-usage.md",
                duration=600,  # 10分钟 = 600秒
                order=3
            ),
            Content(
                chapter_id=chapter_fh_1.id,
                title="托盘使用标准 - 装盘原则、行走步伐、安全注意事项",
                content_type=ContentType.VIDEO,
                file_url="/content/fronthall/ch1/tray-usage.mp4",
                duration=900,  # 15分钟 = 900秒
                order=4
            ),
        ]
        db.add_all(contents_fh_1)
        print(f"    - 章节1：{chapter_fh_1.title} ({len(contents_fh_1)}个内容)")

        # 章节2: 管理岗位
        chapter_fh_2 = Chapter(
            course_id=course_fronthall.id,
            title="管理岗位工作流程",
            description="店长、前厅主管的岗位职责与工作流程",
            order=2,
            has_quiz=True
        )
        db.add(chapter_fh_2)
        db.flush()

        contents_fh_2 = [
            Content(
                chapter_id=chapter_fh_2.id,
                title="店长岗位职责",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch2/manager-duties.md",
                duration=1500,  # 25分钟 = 1500秒
                order=1,
            ),
            Content(
                chapter_id=chapter_fh_2.id,
                title="店长每日工作流程",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch2/manager-daily-workflow.md",
                duration=1800,  # 30分钟 = 1800秒
                order=2,
            ),
            Content(
                chapter_id=chapter_fh_2.id,
                title="前厅主管岗位职责",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch2/supervisor-duties.md",
                duration=1200,  # 20分钟 = 1200秒
                order=3,
            ),
        ]
        db.add_all(contents_fh_2)
        print(f"    - 章节2：{chapter_fh_2.title} ({len(contents_fh_2)}个内容)")

        # 章节3: 服务岗位
        chapter_fh_3 = Chapter(
            course_id=course_fronthall.id,
            title="服务岗位工作流程",
            description="服务员、收银员、迎宾员、传菜员等岗位标准",
            order=3,
            has_quiz=True
        )
        db.add(chapter_fh_3)
        db.flush()

        contents_fh_3 = [
            Content(
                chapter_id=chapter_fh_3.id,
                title="服务员工作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/fronthall/ch3/waiter-workflow.mp4",
                duration=2100,  # 35分钟 = 2100秒
                order=1,
            ),
            Content(
                chapter_id=chapter_fh_3.id,
                title="收银员工作流程",
                content_type=ContentType.DOCUMENT,
                file_url="/content/fronthall/ch3/cashier-workflow.md",
                duration=1200,  # 20分钟 = 1200秒
                order=2,
            ),
            Content(
                chapter_id=chapter_fh_3.id,
                title="迎宾员工作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/fronthall/ch3/greeter-workflow.mp4",
                duration=900,  # 15分钟 = 900秒
                order=3,
            ),
            Content(
                chapter_id=chapter_fh_3.id,
                title="传菜员工作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/fronthall/ch3/runner-workflow.mp4",
                duration=1200,  # 20分钟 = 1200秒
                order=4,
            ),
        ]
        db.add_all(contents_fh_3)
        print(f"    - 章节3：{chapter_fh_3.title} ({len(contents_fh_3)}个内容)")

        print(f"  ✓ 前厅课程完成：3章节，{len(contents_fh_1) + len(contents_fh_2) + len(contents_fh_3)}个内容")

        # ========== 2. 厨房运营标准课程 ==========
        print("\n[2/2] 创建厨房运营标准课程...")

        course_kitchen = Course(
            title="厨房运营标准与岗位流程",
            code="KC-OPS-001",
            description="餐厅厨房运营标准与各岗位工作流程手册，包含通用管理标准、食品安全、各岗位操作流程、设备管理等。",
            department_type=DepartmentType.KITCHEN,
            category="岗位技能",
            is_mandatory=True,
            version="VN202510-R3",
            created_by=creator_id
        )
        db.add(course_kitchen)
        db.flush()
        print(f"  ✓ 课程创建：{course_kitchen.title}")

        # 章节1: 通用管理标准
        chapter_kc_1 = Chapter(
            course_id=course_kitchen.id,
            title="通用管理标准与食品安全",
            description="厨房所有岗位必须遵守的基础标准和食品安全规范",
            order=1,
            has_quiz=True
        )
        db.add(chapter_kc_1)
        db.flush()

        contents_kc_1 = [
            Content(
                chapter_id=chapter_kc_1.id,
                title="仪容仪表标准",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch1/appearance-standards.mp4",
                duration=900,  # 15分钟 = 900秒
                order=1,
            ),
            Content(
                chapter_id=chapter_kc_1.id,
                title="毛巾使用与4D管理",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch1/towel-4d.md",
                duration=1200,  # 20分钟 = 1200秒
                order=2,
            ),
            Content(
                chapter_id=chapter_kc_1.id,
                title="食品安全标准",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch1/food-safety.mp4",
                duration=1800,  # 30分钟 = 1800秒
                order=3,
            ),
            Content(
                chapter_id=chapter_kc_1.id,
                title="进销存管理",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch1/inventory-management.md",
                duration=1500,  # 25分钟 = 1500秒
                order=4,
            ),
        ]
        db.add_all(contents_kc_1)
        print(f"    - 章节1：{chapter_kc_1.title} ({len(contents_kc_1)}个内容)")

        # 章节2: 各岗位操作流程
        chapter_kc_2 = Chapter(
            course_id=course_kitchen.id,
            title="各岗位操作流程",
            description="厨师长、切配岗、热菜岗、凉菜岗等核心岗位工作流程",
            order=2,
            has_quiz=True
        )
        db.add(chapter_kc_2)
        db.flush()

        contents_kc_2 = [
            Content(
                chapter_id=chapter_kc_2.id,
                title="厨师长管理流程",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch2/chef-workflow.md",
                duration=1800,  # 30分钟 = 1800秒
                order=1,
            ),
            Content(
                chapter_id=chapter_kc_2.id,
                title="切配岗操作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch2/prep-workflow.mp4",
                duration=1500,  # 25分钟 = 1500秒
                order=2,
            ),
            Content(
                chapter_id=chapter_kc_2.id,
                title="热菜岗操作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch2/hot-dish-workflow.mp4",
                duration=1800,  # 30分钟 = 1800秒
                order=3,
            ),
            Content(
                chapter_id=chapter_kc_2.id,
                title="凉菜岗操作流程",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch2/cold-dish-workflow.mp4",
                duration=1200,  # 20分钟 = 1200秒
                order=4,
            ),
            Content(
                chapter_id=chapter_kc_2.id,
                title="洗碗间操作流程",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch2/dishwash-workflow.md",
                duration=900,  # 15分钟 = 900秒
                order=5,
            ),
        ]
        db.add_all(contents_kc_2)
        print(f"    - 章节2：{chapter_kc_2.title} ({len(contents_kc_2)}个内容)")

        # 章节3: 设备管理与应急处理
        chapter_kc_3 = Chapter(
            course_id=course_kitchen.id,
            title="设备管理与应急处理",
            description="厨房设备使用、维护、应急预案",
            order=3,
            has_quiz=True
        )
        db.add(chapter_kc_3)
        db.flush()

        contents_kc_3 = [
            Content(
                chapter_id=chapter_kc_3.id,
                title="刀具与菜墩使用",
                content_type=ContentType.VIDEO,
                file_url="/content/kitchen/ch3/knife-usage.mp4",
                duration=900,  # 15分钟 = 900秒
                order=1,
            ),
            Content(
                chapter_id=chapter_kc_3.id,
                title="厨房设备操作指南",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch3/equipment-guide.md",
                duration=1500,  # 25分钟 = 1500秒
                order=2,
            ),
            Content(
                chapter_id=chapter_kc_3.id,
                title="应急预案处理",
                content_type=ContentType.DOCUMENT,
                file_url="/content/kitchen/ch3/emergency-plans.md",
                duration=1200,  # 20分钟 = 1200秒
                order=3,
            ),
        ]
        db.add_all(contents_kc_3)
        print(f"    - 章节3：{chapter_kc_3.title} ({len(contents_kc_3)}个内容)")

        print(f"  ✓ 厨房课程完成：3章节，{len(contents_kc_1) + len(contents_kc_2) + len(contents_kc_3)}个内容")

        # 提交事务
        print("\n[3/3] 提交数据...")
        db.commit()
        print("  ✓ 数据提交成功！")

        print("\n" + "=" * 60)
        print("课程导入完成！")
        print("=" * 60)
        print("\n已创建课程：")
        print(f"  1. {course_fronthall.title} ({course_fronthall.code})")
        print(f"     - 3个章节，{len(contents_fh_1) + len(contents_fh_2) + len(contents_fh_3)}个学习内容")
        print(f"  2. {course_kitchen.title} ({course_kitchen.code})")
        print(f"     - 3个章节，{len(contents_kc_1) + len(contents_kc_2) + len(contents_kc_3)}个学习内容")
        print("=" * 60)
        print("\n💡 提示：")
        print("  - 这些课程已基于knowlege/目录下的运营标准文档创建")
        print("  - file_url是预留的文件路径，实际文件需要后续上传")
        print("  - 可通过API /api/courses/查看所有课程")
        print("  - 可通过Swagger UI (http://localhost:8000/docs)测试")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_courses()
