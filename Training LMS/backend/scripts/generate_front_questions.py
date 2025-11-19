"""
前厅题库生成脚本 - 第一批50道题目
基于《餐厅前厅运营管理标准手册》
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType
from sqlalchemy.exc import IntegrityError

def create_questions():
    """创建50道前厅题目"""
    db = SessionLocal()

    # 前厅题目数据
    questions = [
        # ========== 通用标准部分 (10道) ==========

        # 1. 仪容仪表 - 单选简单
        {
            "text": "男员工的头发标准是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "前不过眉、侧不过耳、后不过领", "is_correct": True},
                {"label": "B", "text": "可以留长发扎辫子", "is_correct": False},
                {"label": "C", "text": "没有特别要求", "is_correct": False},
                {"label": "D", "text": "只要干净整洁即可", "is_correct": False}
            ],
            "explanation": "根据仪容仪表标准，男士头发要求：前不过眉、侧不过耳、后不过领，保持短发整洁。"
        },

        # 2. 毛巾使用 - 多选中等
        {
            "text": "关于毛巾颜色分类使用，以下说法正确的是？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "蓝色毛巾用于桌面清洁（一次擦拭）", "is_correct": True},
                {"label": "B", "text": "紫色毛巾用于桌面抛光（二次擦拭）", "is_correct": True},
                {"label": "C", "text": "白色毛巾用于洗手间清理", "is_correct": False},
                {"label": "D", "text": "棕色毛巾用于洗手间清理", "is_correct": True}
            ],
            "explanation": "毛巾颜色分类：蓝色-桌面清洁，紫色-桌面抛光，白色-餐具擦拭，棕色-洗手间清理，绿色-椅凳清理。"
        },

        # 3. 托盘使用 - 判断简单
        {
            "text": "使用托盘时应遵循里重外轻、里后外先、里高外低的装盘原则。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "correct_answer": "true",
            "explanation": "托盘装盘原则：里重外轻（重物放内侧），里后外先（先上的放外侧），里高外低（高的放内侧）。"
        },

        # 4. 4D管理 - 单选中等
        {
            "text": "关于地面卫生标准，以下哪项不符合要求？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "地面无水渍、油渍、污渍", "is_correct": False},
                {"label": "B", "text": "地面无杂物、垃圾、食物残渣", "is_correct": False},
                {"label": "C", "text": "地面有少量积水但已标记警示", "is_correct": True},
                {"label": "D", "text": "地脚线无灰尘、蜘蛛网", "is_correct": False}
            ],
            "explanation": "地面卫生标准要求地面干燥、无积水，不能有积水即使标记了警示也不符合标准。"
        },

        # 5. 消防安全 - 多选中等
        {
            "text": "灭火器检查要点包括哪些？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "检查压力表指针处在绿区", "is_correct": True},
                {"label": "B", "text": "保险销和铅封完好，未被开启", "is_correct": True},
                {"label": "C", "text": "喷嘴无变形、开裂及损伤", "is_correct": True},
                {"label": "D", "text": "周围可以堆放少量杂物", "is_correct": False}
            ],
            "explanation": "灭火器检查包括：压力表在绿区、保险销完好、喷嘴完好、周围保持干净禁止堆放杂物。"
        },

        # 6. 客诉处理 - 单选中等 (价值观-帮助顾客)
        {
            "text": "处理客人投诉时，正确的做法是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "先处理情绪，再处理问题；先道歉，再了解情况", "is_correct": True},
                {"label": "B", "text": "先了解情况，再决定是否道歉", "is_correct": False},
                {"label": "C", "text": "先解释原因，再处理问题", "is_correct": False},
                {"label": "D", "text": "立即上报店长，自己不参与处理", "is_correct": False}
            ],
            "explanation": "客诉处理原则：先处理情绪再处理问题，先道歉再了解情况，迅速反应及时处理。"
        },

        # 7. 先进先出 - 判断中等
        {
            "text": "成品、半成品、开封后的原料，应使用标签打印机打印效期标签，而非手写。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "correct_answer": "true",
            "explanation": "根据先进先出规范，成品、半成品、开封后的原料需使用标签打印机打印效期标签（而非手写），标签包括：品名、开封日期、效期日期、操作人。"
        },

        # 8. 垃圾管理 - 单选简单
        {
            "text": "垃圾桶应在多少满时及时更换？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "1/2满", "is_correct": False},
                {"label": "B", "text": "2/3满", "is_correct": True},
                {"label": "C", "text": "3/4满", "is_correct": False},
                {"label": "D", "text": "全满", "is_correct": False}
            ],
            "explanation": "垃圾处理流程要求：垃圾桶2/3满时及时更换，做到一餐一清。"
        },

        # 9. 培训方法 - 多选简单 (价值观-勤劳者为本)
        {
            "text": "四步培训法包括哪些步骤？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "course_id": 1,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "我讲你听", "is_correct": True},
                {"label": "B", "text": "你讲我听", "is_correct": True},
                {"label": "C", "text": "我做你看", "is_correct": True},
                {"label": "D", "text": "你做我看", "is_correct": True}
            ],
            "explanation": "四步培训法：我讲你听（讲解）→你讲我听（验收）→我做你看（示范）→你做我看（检验）。"
        },

        # 10. 三关一闭 - 判断简单
        {
            "text": "三关一闭是指：水关闭、电关闭、燃气关闭、门闭锁。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 1,
            "correct_answer": "true",
            "explanation": "三关一闭标准：水关闭（关水龙头）、电关闭（关不需要的电源）、燃气关闭（关燃气总阀）、门闭锁（锁好门窗）。"
        },

        # ========== 迎宾岗位部分 (15道) ==========

        # 11. 迎宾职责 - 多选简单
        {
            "text": "迎宾岗位的主要职责包括？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "迎接到店客人，带位就坐", "is_correct": True},
                {"label": "B", "text": "送客服务，礼貌告别", "is_correct": True},
                {"label": "C", "text": "排队叫号，维护等位客人体验", "is_correct": True},
                {"label": "D", "text": "制作饮品和甜品", "is_correct": False}
            ],
            "explanation": "迎宾岗位职责包括：迎宾送客、排队叫号、维护等位区、对路过客人店推等，不包括制作饮品（水吧岗位）。"
        },

        # 12. 等位区物料 - 单选中等
        {
            "text": "等位区应准备多少种小吃？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "1-2种", "is_correct": False},
                {"label": "B", "text": "3-5种", "is_correct": True},
                {"label": "C", "text": "6-8种", "is_correct": False},
                {"label": "D", "text": "越多越好", "is_correct": False}
            ],
            "explanation": "等位区准备标准：3-5种小吃，按门店预估量准备，周末/节假日增加1.5-2倍。"
        },

        # 13. 迎客标准 - 判断中等 (价值观-帮助顾客)
        {
            "text": "迎客时应站在距门口2-3米处，看到客人时主动上前迎接2-3步。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "迎客标准：站立位置距门口2-3米，看到客人主动上前迎接2-3步，面带微笑，右手半举引导。"
        },

        # 14. 叫号规则 - 单选困难
        {
            "text": "客人过号后回来，应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "立即安排入座", "is_correct": False},
                {"label": "B", "text": "顺延3桌安排", "is_correct": True},
                {"label": "C", "text": "顺延5桌安排", "is_correct": False},
                {"label": "D", "text": "必须重新取号", "is_correct": False}
            ],
            "explanation": "过号处理规则：叫号3次未到视为过号，过号客人回来后顺延3桌安排。如客人不接受顺延，需重新取号。"
        },

        # 15. 带位原则 - 多选中等
        {
            "text": "带客入座时，桌位安排需考虑哪些因素？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "根据人数安排合适桌位", "is_correct": True},
                {"label": "B", "text": "优先安排靠窗、视野好的位置", "is_correct": True},
                {"label": "C", "text": "有老人/小孩优先安排方便进出的位置", "is_correct": True},
                {"label": "D", "text": "所有客人都安排相同位置", "is_correct": False}
            ],
            "explanation": "桌位安排原则：根据人数安排合适桌位，优先靠窗视野好，有老人小孩安排方便进出，情侣安排相对私密位置。"
        },

        # 16. 拉椅服务 - 单选中等 (价值观-帮助顾客)
        {
            "text": "拉椅服务中，情侣约会时应重点关注？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "关注男性，提供拉椅服务", "is_correct": False},
                {"label": "B", "text": "关注女性，提供拉椅服务", "is_correct": True},
                {"label": "C", "text": "不提供拉椅服务", "is_correct": False},
                {"label": "D", "text": "两人都提供拉椅服务", "is_correct": False}
            ],
            "explanation": "拉椅服务标准：家庭聚餐关注老人/小孩，情侣约会关注女性，商务宴请关注主宾。"
        },

        # 17. 等位区服务 - 判断困难 (价值观-帮助顾客)
        {
            "text": "应提前2-3桌提醒等位客人做好准备，提高服务体验。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "hard",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "叫号提醒服务：提前2-3桌提醒等位客人做好准备，话术：'快到您了，请稍作准备，一会儿会叫到您的号'。"
        },

        # 18. 店推话术 - 单选中等
        {
            "text": "店推时，客人明确表示不需要，应该？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "继续热情推销", "is_correct": False},
                {"label": "B", "text": "礼貌告别'好的，有需要随时欢迎您'", "is_correct": True},
                {"label": "C", "text": "表达不满", "is_correct": False},
                {"label": "D", "text": "询问原因", "is_correct": False}
            ],
            "explanation": "店推注意事项：保持热情但不过分，客人明确表示不需要时，礼貌告别'好的，有需要随时欢迎您'，不强推。"
        },

        # 19. 送客服务 - 多选中等 (价值观-帮助顾客)
        {
            "text": "送客增值服务包括哪些？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "主动询问是否需要打包", "is_correct": True},
                {"label": "B", "text": "提供除味喷雾（有需要的客人）", "is_correct": True},
                {"label": "C", "text": "引导线上好评（体验满意的客人）", "is_correct": True},
                {"label": "D", "text": "要求客人必须好评", "is_correct": False}
            ],
            "explanation": "送客增值服务：主动询问打包需求、提供除味喷雾、引导（而非要求）线上好评。"
        },

        # 20. 下雨天送客 - 单选简单
        {
            "text": "下雨天送客时，应提供什么增值服务？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "提供雨伞", "is_correct": False},
                {"label": "B", "text": "提供一次性雨衣", "is_correct": True},
                {"label": "C", "text": "提供雨鞋", "is_correct": False},
                {"label": "D", "text": "不需要提供任何服务", "is_correct": False}
            ],
            "explanation": "送客服务-天气提醒：下雨天提供一次性雨衣，话术：'外面在下雨，这是雨衣，请您拿着，雨天地滑请注意安全'。"
        },

        # 21. 等位区小吃 - 判断中等
        {
            "text": "周末和节假日的等位区小吃准备量应增加1.5-2倍。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "等位区布置标准：小吃准备3-5种，按门店预估量准备，周末/节假日增加1.5-2倍。"
        },

        # 22. 茶水准备 - 单选中等
        {
            "text": "夏季等位区应提供什么类型的茶水？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "只提供冰水", "is_correct": False},
                {"label": "B", "text": "只提供常温水", "is_correct": False},
                {"label": "C", "text": "提供冰水和常温水", "is_correct": True},
                {"label": "D", "text": "提供热水和温水", "is_correct": False}
            ],
            "explanation": "茶水准备标准：夏季提供冰水和常温水，冬季提供热水和温水。"
        },

        # 23. 取号机充电 - 判断简单 (价值观-勤劳者为本)
        {
            "text": "取号机应在晚市结束后关机充电，确保次日开市前充满电。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "value_diligence",
            "course_id": 1,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "设备物资清点与充电：取号机关机充电，确保次日开市前充满电。对讲机也需充电。"
        },

        # 24. 等位椅收纳 - 单选简单 (价值观-高效协作)
        {
            "text": "闭店时等位区椅子应如何收纳？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "随意摆放", "is_correct": False},
                {"label": "B", "text": "5把椅子为1组，统一规范摆放", "is_correct": True},
                {"label": "C", "text": "10把椅子为1组", "is_correct": False},
                {"label": "D", "text": "全部堆叠在一起", "is_correct": False}
            ],
            "explanation": "等位区收纳标准：5把椅子为1组，统一规范摆放。"
        },

        # 25. 店推物料 - 多选简单
        {
            "text": "店推时应准备哪些物料？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "菜单", "is_correct": True},
                {"label": "B", "text": "活动宣传单页", "is_correct": True},
                {"label": "C", "text": "优惠券、体验券", "is_correct": True},
                {"label": "D", "text": "厨房工具", "is_correct": False}
            ],
            "explanation": "店推物料准备：菜单、活动宣传单页、优惠券、体验券等。"
        },

        # ========== 服务岗位部分 (20道) ==========

        # 26. 服务职责 - 判断简单
        {
            "text": "服务岗位应严格执行工作程序、服务程序和卫生要求，以用户体验为目标。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "服务岗位职责：严格执行工作程序、服务程序和卫生要求，以用户体验为目标，为客人提供友好、良好的服务体验。"
        },

        # 27. 餐具准备 - 单选中等
        {
            "text": "备餐柜餐具应按什么比例准备？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "1:1", "is_correct": False},
                {"label": "B", "text": "1:2或1:3", "is_correct": True},
                {"label": "C", "text": "1:4或1:5", "is_correct": False},
                {"label": "D", "text": "没有固定比例", "is_correct": False}
            ],
            "explanation": "物料准备标准：备餐柜餐具按1:2或1:3比例准备，确保餐中有充足餐具备用。"
        },

        # 28. 斟茶标准 - 单选简单
        {
            "text": "为客人斟茶时，茶水应倒至几分满？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "5分满", "is_correct": False},
                {"label": "B", "text": "7分满", "is_correct": True},
                {"label": "C", "text": "9分满", "is_correct": False},
                {"label": "D", "text": "全满", "is_correct": False}
            ],
            "explanation": "斟倒茶水标准：入座时首次斟茶水至7分满，餐中茶水量少时及时添加至7分满。"
        },

        # 29. 增减餐位 - 多选中等 (价值观-高效协作)
        {
            "text": "减位的正确顺序是什么？（多选并排序）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "座椅→茶杯→餐具→调整间距", "is_correct": True},
                {"label": "B", "text": "餐具→茶杯→座椅→调整间距", "is_correct": False},
                {"label": "C", "text": "调整间距→座椅→茶杯→餐具", "is_correct": False},
                {"label": "D", "text": "茶杯→餐具→座椅→调整间距", "is_correct": False}
            ],
            "explanation": "增减餐位标准：减位顺序是座椅→茶杯→餐具→调整间距；加位顺序是调整间距→餐具/茶杯→座椅。"
        },

        # 30. 加汤标准 - 判断中等 (价值观-帮助顾客)
        {
            "text": "加汤时需要有声提示'您好，帮您加一下汤，小心烫'。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "加汤标准：有声提示'您好，帮您加一下汤，小心烫'，加汤至标准位置（8分满）。"
        },

        # 31. 上菜顺序 - 单选中等
        {
            "text": "建议的上菜顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "素菜→荤菜→锅底", "is_correct": False},
                {"label": "B", "text": "锅底→荤菜→素菜", "is_correct": True},
                {"label": "C", "text": "荤菜→锅底→素菜", "is_correct": False},
                {"label": "D", "text": "随意上菜", "is_correct": False}
            ],
            "explanation": "上菜标准-建议顺序：锅底→荤菜→素菜（酒水、小吃、甜品随时上）。"
        },

        # 32. 巡台服务 - 多选中等
        {
            "text": "巡台服务包括哪些内容？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "加汤、加茶水", "is_correct": True},
                {"label": "B", "text": "调整电磁炉档位", "is_correct": True},
                {"label": "C", "text": "关注客人用餐情况", "is_correct": True},
                {"label": "D", "text": "及时撤走空盘", "is_correct": True}
            ],
            "explanation": "巡台服务内容：定期巡台，加汤加茶，调整电磁炉档位，关注客人用餐情况，及时撤走空盘。"
        },

        # 33. 锅底熬开流程 - 单选困难
        {
            "text": "锅底熬开后的正确流程顺序是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "打沫→分汤→介绍菜品→少量下菜→烫涮菜品→分菜", "is_correct": True},
                {"label": "B", "text": "分汤→打沫→下菜→介绍菜品", "is_correct": False},
                {"label": "C", "text": "介绍菜品→下菜→分汤→打沫", "is_correct": False},
                {"label": "D", "text": "下菜→分汤→打沫→介绍菜品", "is_correct": False}
            ],
            "explanation": "锅底熬开后流程：打沫→分汤→介绍菜品→少量下菜→烫涮菜品→分菜。"
        },

        # 34. 搅锅方法 - 单选中等
        {
            "text": "长时间煮菜时搅锅应该如何操作？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "画圆圈搅动", "is_correct": False},
                {"label": "B", "text": "画倒8字，轻搅锅底", "is_correct": True},
                {"label": "C", "text": "来回直线搅动", "is_correct": False},
                {"label": "D", "text": "不需要搅动", "is_correct": False}
            ],
            "explanation": "搅锅标准：长时间煮菜时及时搅动，画倒8字，轻搅锅底，防止粘锅。"
        },

        # 35. 酒水服务 - 判断中等
        {
            "text": "酒水应由服务员主动为客人倾倒。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "correct_answer": "false",
            "explanation": "斟倒标准：酒水由客人自己倾倒，服务员不主动倒酒（茶水需要服务员主动添加）。"
        },

        # 36. 收台时长 - 单选简单 (价值观-勤劳者为本)
        {
            "text": "小桌收台标准时长是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "1分钟", "is_correct": False},
                {"label": "B", "text": "3分钟", "is_correct": True},
                {"label": "C", "text": "5分钟", "is_correct": False},
                {"label": "D", "text": "10分钟", "is_correct": False}
            ],
            "explanation": "收台标准时长：小桌3分钟，大桌5分钟。"
        },

        # 37. 收台顺序 - 多选困难
        {
            "text": "收台的正确顺序包括？（多选并按顺序）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "关火检查炉具→倒垃圾→玻璃器皿→茶杯→菜盘→筷子/汤漏勺→油碟碗→锅底", "is_correct": True},
                {"label": "B", "text": "倒垃圾→关火→玻璃器皿→茶杯", "is_correct": False},
                {"label": "C", "text": "茶杯→菜盘→筷子→锅底", "is_correct": False},
                {"label": "D", "text": "随意顺序都可以", "is_correct": False}
            ],
            "explanation": "收台顺序：关火检查炉具→倒垃圾→玻璃器皿→茶杯→菜盘→筷子/汤漏勺→油碟碗→锅底。"
        },

        # 38. 擦台步骤 - 单选困难
        {
            "text": "擦台标准有几个步骤？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "3步骤", "is_correct": False},
                {"label": "B", "text": "4步骤", "is_correct": False},
                {"label": "C", "text": "5步骤", "is_correct": True},
                {"label": "D", "text": "6步骤", "is_correct": False}
            ],
            "explanation": "擦台标准5步骤：刮残渣→喷清洁剂→蓝色毛巾擦拭→紫色毛巾抛光→绿色毛巾擦椅凳。"
        },

        # 39. 清洁剂配比 - 单选中等
        {
            "text": "擦台用的清洁剂（洗洁精:水）配比是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "1:5或2:5", "is_correct": False},
                {"label": "B", "text": "1:9或2:8", "is_correct": True},
                {"label": "C", "text": "1:10", "is_correct": False},
                {"label": "D", "text": "不需要稀释", "is_correct": False}
            ],
            "explanation": "擦台清洁剂配比：洗洁精:水=1:9或2:8，用喷壶均匀喷洒在桌面。"
        },

        # 40. 擦拭方向 - 多选中等 (价值观-高效协作)
        {
            "text": "擦台时可采用的擦拭方向有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "按S型擦拭", "is_correct": True},
                {"label": "B", "text": "按回字型擦拭", "is_correct": True},
                {"label": "C", "text": "随意擦拭", "is_correct": False},
                {"label": "D", "text": "只擦中间部分", "is_correct": False}
            ],
            "explanation": "擦台注意事项：擦拭方向按S型或回字型，确保无遗漏，桌面边缘、角落要特别注意。"
        },

        # 41. 三轻原则 - 判断简单
        {
            "text": "收台时应遵循'三轻'原则：轻拿、轻放、轻端。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "收台标准：遵循三轻原则-轻拿、轻放、轻端，避免餐具碰撞发出噪音。"
        },

        # 42. 送客告知 - 单选简单 (价值观-帮助顾客)
        {
            "text": "客人准备买单时，服务员应该？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "不需要告知任何信息", "is_correct": False},
                {"label": "B", "text": "主动告知收银台位置和客人所在桌号", "is_correct": True},
                {"label": "C", "text": "只告知收银台位置", "is_correct": False},
                {"label": "D", "text": "只告知桌号", "is_correct": False}
            ],
            "explanation": "送客标准：主动告知顾客收银台位置，并告诉顾客所在桌号，方便买单。同时询问是否需要打包。"
        },

        # 43. 打包服务 - 判断简单 (价值观-帮助顾客)
        {
            "text": "客人买单时应主动询问是否需要打包。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "送客标准：询问顾客是否需要打包，如需打包及时准备打包用具。"
        },

        # 44. 特色产品介绍 - 多选中等
        {
            "text": "服务员应向客人介绍哪些特色产品？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "锅底", "is_correct": True},
                {"label": "B", "text": "牛肉", "is_correct": True},
                {"label": "C", "text": "云贵精选菜", "is_correct": True},
                {"label": "D", "text": "手作甜品系列", "is_correct": True}
            ],
            "explanation": "带客入座后服务：介绍特色产品包括锅底、牛肉、云贵精选菜、手作甜品系列。"
        },

        # 45. 增值物品 - 多选简单 (价值观-帮助顾客)
        {
            "text": "服务员可提供的增值物品有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "course_id": 1,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "围裙", "is_correct": True},
                {"label": "B", "text": "眼镜布", "is_correct": True},
                {"label": "C", "text": "头绳（发圈）", "is_correct": True},
                {"label": "D", "text": "婴儿椅", "is_correct": True}
            ],
            "explanation": "增值物品提供：围裙、眼镜布、头绳、婴儿椅、手机架、小票夹等。"
        },

        # ========== 水吧岗位部分 (5道) ==========

        # 46. 水吧职责 - 判断简单
        {
            "text": "水吧岗位负责各种饮品、甜品的基底制作，严格控制茶叶和原物料领用，杜绝浪费。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 4,
            "correct_answer": "true",
            "explanation": "水吧岗位职责：负责饮品甜品基底制作，严格控制原物料领用杜绝浪费，维护制作间卫生。"
        },

        # 47. 温度标准 - 单选中等
        {
            "text": "冷饮的标准温度应该是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "0-5℃", "is_correct": True},
                {"label": "B", "text": "5-10℃", "is_correct": False},
                {"label": "C", "text": "10-15℃", "is_correct": False},
                {"label": "D", "text": "常温即可", "is_correct": False}
            ],
            "explanation": "产品制作标准-温度标准：冷饮0-5℃，热饮60-70℃。"
        },

        # 48. 酒水盘点 - 单选困难 (价值观-平等透明)
        {
            "text": "新店期（开业前2个月）酒水盘点频率是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "value_transparency",
            "course_id": 1,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "每天盘点", "is_correct": False},
                {"label": "B", "text": "每周盘点", "is_correct": True},
                {"label": "C", "text": "每月盘点", "is_correct": False},
                {"label": "D", "text": "不定期盘点", "is_correct": False}
            ],
            "explanation": "酒水盘点标准：新店期（开业前2个月）每周盘点一次，稳定期每月盘点一次。"
        },

        # 49. 酒水盘点公式 - 单选中等 (价值观-平等透明)
        {
            "text": "酒水盘点公式是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "course_id": 1,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "前期库存+进货量-售卖量=剩余", "is_correct": True},
                {"label": "B", "text": "进货量-售卖量=剩余", "is_correct": False},
                {"label": "C", "text": "前期库存+进货量=剩余", "is_correct": False},
                {"label": "D", "text": "进货量+售卖量=剩余", "is_correct": False}
            ],
            "explanation": "酒水盘点公式：进货量+前期库存-售卖量=剩余（实际库存应与计算剩余相符）。"
        },

        # 50. 酒水陈列 - 多选简单
        {
            "text": "酒水陈列标准包括？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 1,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "酒水陈列整齐，logo向外", "is_correct": True},
                {"label": "B", "text": "按品种分类摆放", "is_correct": True},
                {"label": "C", "text": "先进先出，近期到期产品前置", "is_correct": True},
                {"label": "D", "text": "可以随意摆放", "is_correct": False}
            ],
            "explanation": "酒水陈列标准：整齐摆放logo向外、按品种分类、先进先出原则、保持酒柜清洁。"
        }
    ]

    try:
        print(f"开始插入{len(questions)}道前厅题目...")
        created_count = 0

        for idx, q_data in enumerate(questions, 1):
            try:
                question = Question(
                    content=q_data["content"],
                    question_type=q_data["question_type"],
                    difficulty=q_data["difficulty"],
                    category=q_data["category"],
                    course_id=q_data.get("course_id"),
                    chapter_id=q_data.get("chapter_id"),
                    options=q_data.get("options"),
                    correct_answer=q_data.get("correct_answer"),
                    explanation=q_data.get("explanation"),
                    created_by=1  # 系统管理员
                )
                db.add(question)
                db.commit()
                created_count += 1
                print(f"[{created_count}/{len(questions)}] 已插入题目：{q_data['content'][:30]}...")

            except IntegrityError as e:
                db.rollback()
                print(f"题目 {idx} 插入失败（可能已存在）: {q_data['content'][:30]}...")
                continue

        print(f"\n✅ 成功插入 {created_count} 道题目！")
        print(f"\n题目统计：")
        print(f"- 单选题：{sum(1 for q in questions if q['question_type'] == QuestionType.SINGLE_CHOICE)}道")
        print(f"- 多选题：{sum(1 for q in questions if q['question_type'] == QuestionType.MULTIPLE_CHOICE)}道")
        print(f"- 判断题：{sum(1 for q in questions if q['question_type'] == QuestionType.TRUE_FALSE)}道")
        print(f"\n难度分布：")
        print(f"- 简单：{sum(1 for q in questions if q['difficulty'] == 'easy')}道")
        print(f"- 中等：{sum(1 for q in questions if q['difficulty'] == 'medium')}道")
        print(f"- 困难：{sum(1 for q in questions if q['difficulty'] == 'hard')}道")
        print(f"\n类别分布：")
        print(f"- 技能类：{sum(1 for q in questions if q['category'] == 'skill')}道")
        print(f"- 价值观类：{sum(1 for q in questions if q['category'].startswith('value_'))}道")

    except Exception as e:
        print(f"❌ 插入题目时发生错误：{str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_questions()
