"""
厨房题库生成脚本 - 第一批50道题目
基于《餐厅厨房运营标准与岗位工作流程手册》
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
    """创建50道厨房题目"""
    db = SessionLocal()

    # 厨房题目数据
    questions = [
        # ========== 通用标准部分 (15道) ==========

        # 1. 七步洗手法 - 多选中等
        {
            "text": "七步洗手法包括哪些步骤？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "掌心相对，手指并拢相互揉搓", "is_correct": True},
                {"label": "B", "text": "手心对手背沿指缝相互搓擦", "is_correct": True},
                {"label": "C", "text": "掌心相对，沿指缝相互搓擦", "is_correct": True},
                {"label": "D", "text": "螺旋式擦洗手腕", "is_correct": True}
            ],
            "explanation": "七步洗手法7个步骤：掌心揉搓、手心对手背、掌心对掌心指缝、握拳揉搓、搓擦大拇指、指甲旋转搓擦、螺旋式擦洗手腕。"
        },

        # 2. 毛巾颜色 - 单选简单
        {
            "text": "厨房地面清洁应使用什么颜色的毛巾？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "蓝色", "is_correct": False},
                {"label": "B", "text": "绿色", "is_correct": False},
                {"label": "C", "text": "白色", "is_correct": False},
                {"label": "D", "text": "棕色", "is_correct": True}
            ],
            "explanation": "厨房毛巾分色：蓝色-台面清洁，绿色-器具设备，白色-餐具擦拭，棕色-地面清洁。"
        },

        # 3. 84消毒液配比 - 单选困难
        {
            "text": "毛巾消毒使用的84消毒液配比（消毒液:水）是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "1:50", "is_correct": False},
                {"label": "B", "text": "1:100", "is_correct": True},
                {"label": "C", "text": "1:200", "is_correct": False},
                {"label": "D", "text": "1:500", "is_correct": False}
            ],
            "explanation": "毛巾消毒配比：1:100（10ml消毒液+990ml水），有效氯浓度约500mg/L，浸泡30分钟。"
        },

        # 4. 消毒液注意事项 - 判断中等
        {
            "text": "84消毒液可以与洗洁精混合使用，效果更好。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "correct_answer": "false",
            "explanation": "84消毒液与洗洁精不可混用，会产生有毒氯气。消毒后必须用清水冲洗干净。"
        },

        # 5. 4D管理 - 单选简单
        {
            "text": "食品离地应保持多少厘米以上？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "10cm", "is_correct": False},
                {"label": "B", "text": "15cm", "is_correct": False},
                {"label": "C", "text": "25cm", "is_correct": True},
                {"label": "D", "text": "30cm", "is_correct": False}
            ],
            "explanation": "4D管理标准：食品离地25cm以上、离墙5cm以上整齐摆放。"
        },

        # 6. 生熟分离-刀具 - 多选中等
        {
            "text": "关于刀具颜色分类，正确的是？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "红色刀柄用于切生食", "is_correct": True},
                {"label": "B", "text": "蓝色刀柄用于切熟食", "is_correct": True},
                {"label": "C", "text": "黄色刀柄用于过敏原食材", "is_correct": True},
                {"label": "D", "text": "所有刀具可以混用", "is_correct": False}
            ],
            "explanation": "刀具分类：红色-生食，蓝色-熟食，黄色-过敏原。严禁混用。"
        },

        # 7. 冷藏温度 - 单选简单
        {
            "text": "冷藏食材的标准温度范围是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "0-4℃", "is_correct": True},
                {"label": "B", "text": "5-10℃", "is_correct": False},
                {"label": "C", "text": "-5-0℃", "is_correct": False},
                {"label": "D", "text": "10-15℃", "is_correct": False}
            ],
            "explanation": "冷藏标准温度：0-4℃。冷冻温度≤-18℃。"
        },

        # 8. 肉类新鲜度 - 判断中等
        {
            "text": "新鲜肉类用手指按压后应立即回弹，不留凹痕。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "correct_answer": "true",
            "explanation": "新鲜肉类标准：色泽鲜红有光泽、按压立即回弹、无异味、表面干爽不发黏。"
        },

        # 9. 鱼类新鲜度 - 单选中等
        {
            "text": "判断鱼类是否新鲜，应检查哪些方面？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "只看眼睛是否清亮", "is_correct": False},
                {"label": "B", "text": "只闻气味", "is_correct": False},
                {"label": "C", "text": "眼球饱满、鳃片鲜红、鱼鳞紧贴、肉质紧实、无腐臭味", "is_correct": True},
                {"label": "D", "text": "只看颜色", "is_correct": False}
            ],
            "explanation": "鱼类新鲜度综合判断：眼球饱满凸起、鳃片鲜红无异味、鱼鳞紧贴有光泽、肉质紧实有弹性、有海洋鲜腥味无臭味。"
        },

        # 10. 蔬菜新鲜度 - 多选简单
        {
            "text": "新鲜叶菜类的特征有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "叶片翠绿鲜亮", "is_correct": True},
                {"label": "B", "text": "叶片脆嫩有水分感", "is_correct": True},
                {"label": "C", "text": "叶片发黄枯萎", "is_correct": False},
                {"label": "D", "text": "茎部水嫩清脆", "is_correct": True}
            ],
            "explanation": "新鲜叶菜标准：叶片翠绿鲜亮、脆嫩有水分、茎部水嫩清脆、无黄叶枯萎、无病虫害。"
        },

        # 11. 手套使用 - 判断困难
        {
            "text": "处理完生食后，可以继续戴同一副手套处理熟食。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "correct_answer": "false",
            "explanation": "严禁戴同一副手套接触生熟食。处理完生食后必须：脱手套→洗手消毒→戴新手套→处理熟食。"
        },

        # 12. 操作台距离 - 单选中等
        {
            "text": "生食操作台与熟食操作台之间的距离应保持多少米以上？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "1米", "is_correct": False},
                {"label": "B", "text": "2米", "is_correct": True},
                {"label": "C", "text": "3米", "is_correct": False},
                {"label": "D", "text": "没有要求", "is_correct": False}
            ],
            "explanation": "生食与熟食操作台距离应≥2米，中间不可有交叉动线，防止交叉污染。"
        },

        # 13. 温度测量 - 单选困难
        {
            "text": "使用探针式温度计测量冷藏食材时，应如何操作？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "放在食材表面即可", "is_correct": False},
                {"label": "B", "text": "将探针插入食材中心≥5cm，保持10-15秒", "is_correct": True},
                {"label": "C", "text": "快速扫描表面", "is_correct": False},
                {"label": "D", "text": "测量包装外侧温度", "is_correct": False}
            ],
            "explanation": "冷藏食材测量方法：选择最大块食材，探针插入中心≥5cm，保持10-15秒等待读数稳定，每批次测3个不同位置。"
        },

        # 14. 食材验收 - 多选中等
        {
            "text": "食材验收时必检项目包括？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "options": [
                {"label": "A", "text": "供应商资质", "is_correct": True},
                {"label": "B", "text": "温度检查", "is_correct": True},
                {"label": "C", "text": "包装完整性", "is_correct": True},
                {"label": "D", "text": "新鲜度检查", "is_correct": True}
            ],
            "explanation": "验收必检：供应商资质、温度检查、包装完整性、标签信息、新鲜度检查、不合格处理、验收记录。"
        },

        # 15. 豆制品新鲜度 - 判断中等
        {
            "text": "新鲜豆腐的浸泡水应该清澈透明，无浑浊，无异味。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 1,
            "correct_answer": "true",
            "explanation": "新鲜豆腐标准：色泽洁白或淡黄、有弹性、有豆香无酸味、浸泡水清澈透明无浑浊无异味。"
        },

        # ========== 岗位职责部分 (20道) ==========

        # 16. 厨师长职责 - 多选简单 (价值观-高效协作)
        {
            "text": "厨师长的主要职责包括？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "负责厨房日常运营管理", "is_correct": True},
                {"label": "B", "text": "食材验收与质量把控", "is_correct": True},
                {"label": "C", "text": "人员培训与团队建设", "is_correct": True},
                {"label": "D", "text": "只负责烹饪工作", "is_correct": False}
            ],
            "explanation": "厨师长职责：厨房运营管理、食材验收质量把控、菜品研发改良、人员培训团队建设、成本控制、设备维护等。"
        },

        # 17. 洗碗标准 - 单选中等
        {
            "text": "餐具清洗的正确流程是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "去渣→清洗→消毒→沥干", "is_correct": True},
                {"label": "B", "text": "清洗→去渣→消毒→沥干", "is_correct": False},
                {"label": "C", "text": "消毒→清洗→去渣→沥干", "is_correct": False},
                {"label": "D", "text": "去渣→消毒→清洗→沥干", "is_correct": False}
            ],
            "explanation": "餐具清洗流程：去渣（清除食物残渣）→清洗（洗洁精热水）→消毒（高温或消毒液）→沥干（自然晾干或消毒柜）。"
        },

        # 18. 员工餐要求 - 判断简单 (价值观-勤劳者为本)
        {
            "text": "员工餐应保证营养均衡，荤素搭配，不能用剩菜剩饭。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "value_diligence",
            "course_id": 2,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "员工餐标准：营养均衡、荤素搭配、新鲜卫生、不用剩菜剩饭，体现对员工的关爱（以勤劳者为本）。"
        },

        # 19. 切配要求 - 单选中等
        {
            "text": "切配时，刀法的基本要求是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "大小均匀、薄厚一致", "is_correct": True},
                {"label": "B", "text": "越快越好，不管大小", "is_correct": False},
                {"label": "C", "text": "随意切割即可", "is_correct": False},
                {"label": "D", "text": "只要能切断就行", "is_correct": False}
            ],
            "explanation": "切配基本要求：大小均匀、薄厚一致、刀工整齐、符合菜品要求，保证烹饪时受热均匀、口感一致。"
        },

        # 20. 菜房职责 - 多选简单
        {
            "text": "菜房的主要工作包括？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "蔬菜清洗", "is_correct": True},
                {"label": "B", "text": "蔬菜去根去叶", "is_correct": True},
                {"label": "C", "text": "蔬菜分类存放", "is_correct": True},
                {"label": "D", "text": "肉类切配", "is_correct": False}
            ],
            "explanation": "菜房职责：蔬菜清洗、去根去叶、分拣、分类存放等。肉类切配属于切配岗职责。"
        },

        # 21. 料房管理 - 单选中等
        {
            "text": "料房调料应如何摆放？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "随意摆放", "is_correct": False},
                {"label": "B", "text": "按使用频率定位摆放，标签清晰", "is_correct": True},
                {"label": "C", "text": "全部放在地上", "is_correct": False},
                {"label": "D", "text": "混放在一起", "is_correct": False}
            ],
            "explanation": "料房标准：调料按使用频率定位摆放、标签清晰、容器密封、定期检查效期、先进先出。"
        },

        # 22. 明档要求 - 判断中等 (价值观-帮助顾客)
        {
            "text": "明档操作时应保持整洁卫生，动作规范，向顾客展示专业形象。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 2,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "明档标准：保持整洁卫生、动作规范专业、仪容仪表良好、向顾客展示烹饪过程，提升用餐体验（帮助顾客）。"
        },

        # 23. 热菜出餐 - 单选困难
        {
            "text": "热菜出餐的标准时间（从下单到出餐）应控制在多少分钟内？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "3-5分钟", "is_correct": False},
                {"label": "B", "text": "5-8分钟", "is_correct": True},
                {"label": "C", "text": "10-15分钟", "is_correct": False},
                {"label": "D", "text": "没有时间要求", "is_correct": False}
            ],
            "explanation": "热菜出餐标准时间：5-8分钟（从下单到出餐），保证菜品新鲜热乎、口感最佳。"
        },

        # 24. 凉菜卫生 - 多选中等
        {
            "text": "凉菜间的卫生要求有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "专间专用，非凉菜人员不得进入", "is_correct": True},
                {"label": "B", "text": "紫外线消毒", "is_correct": True},
                {"label": "C", "text": "所有工具专用", "is_correct": True},
                {"label": "D", "text": "可以与其他岗位共用工具", "is_correct": False}
            ],
            "explanation": "凉菜间高标准卫生要求：专间专用、非人员不进、紫外线消毒、工具专用、二次更衣、严格消毒。"
        },

        # 25. 荤菜存放 - 单选简单
        {
            "text": "生荤菜应存放在什么温度环境？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "常温", "is_correct": False},
                {"label": "B", "text": "0-4℃冷藏", "is_correct": True},
                {"label": "C", "text": "10-15℃", "is_correct": False},
                {"label": "D", "text": "室外阴凉处", "is_correct": False}
            ],
            "explanation": "生荤菜存放标准：0-4℃冷藏，加膜加盖，标注日期，先进先出，防止交叉污染。"
        },

        # 26. 素菜清洗 - 判断中等
        {
            "text": "蔬菜清洗应先泡后洗，浸泡时间不少于10分钟。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "蔬菜清洗标准：先泡后洗，浸泡≥10分钟（去除农药残留），流水冲洗3遍，沥干水分。"
        },

        # 27. 刀具保养 - 单选中等
        {
            "text": "刀具使用后应如何保养？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "直接放回刀架", "is_correct": False},
                {"label": "B", "text": "清洗消毒后，刀刃朝下放回刀架", "is_correct": True},
                {"label": "C", "text": "用水冲一下即可", "is_correct": False},
                {"label": "D", "text": "随意放置", "is_correct": False}
            ],
            "explanation": "刀具保养：使用后立即清洗→84消毒液（1:100）浸泡30分钟→沥干→刀刃朝下放回对应刀架。"
        },

        # 28. 砧板管理 - 多选中等
        {
            "text": "关于砧板的正确管理方法有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "生熟分离，颜色区分", "is_correct": True},
                {"label": "B", "text": "使用后立即清洗消毒", "is_correct": True},
                {"label": "C", "text": "竖立沥干存放", "is_correct": True},
                {"label": "D", "text": "可以生熟混用", "is_correct": False}
            ],
            "explanation": "砧板管理：生熟分离（红色生、蓝色熟、黄色过敏原）、使用后清洗消毒、竖立沥干、定期更换。"
        },

        # 29. 容器标签 - 单选简单
        {
            "text": "食材容器的标签应包含哪些信息？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "只需要写名称", "is_correct": False},
                {"label": "B", "text": "岗位名+生/熟+容器编号", "is_correct": True},
                {"label": "C", "text": "不需要标签", "is_correct": False},
                {"label": "D", "text": "只写日期", "is_correct": False}
            ],
            "explanation": "容器标签规范：岗位名+生/熟+容器编号（如'切配-生-01'），标签清晰可见，方便管理。"
        },

        # 30. 加工过程温度 - 判断困难
        {
            "text": "生鲜食材取出加工时，每30分钟应测量一次温度，确保≤4℃。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "加工过程温度监控：食材取出后每30分钟测一次温度，应≤4℃，超过4℃需立即放回冷藏柜。"
        },

        # 31. 汤底温度 - 单选中等
        {
            "text": "汤底保温温度应保持在多少℃以上？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "60℃", "is_correct": False},
                {"label": "B", "text": "70℃", "is_correct": False},
                {"label": "C", "text": "75℃", "is_correct": True},
                {"label": "D", "text": "80℃", "is_correct": False}
            ],
            "explanation": "汤底温度标准：沸腾≥98℃，保温≥75℃，低于75℃需重新加热以保证食品安全。"
        },

        # 32. 油温控制 - 单选困难
        {
            "text": "炸薯条应使用什么温度的油？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "120-140℃（低温）", "is_correct": False},
                {"label": "B", "text": "160-180℃（中温）", "is_correct": False},
                {"label": "C", "text": "180-200℃（高温）", "is_correct": True},
                {"label": "D", "text": "200℃以上", "is_correct": False}
            ],
            "explanation": "油温标准：低温120-140℃炸花生坚果，中温160-180℃炸丸子鱼，高温180-200℃炸薯条复炸。"
        },

        # 33. 温度计校准 - 判断中等
        {
            "text": "温度计应每日使用冰水法校准，读数应为0℃（±1℃）。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "correct_answer": "true",
            "explanation": "温度计校准：每日冰水法（冰块+水，读数0℃±1℃）、每周沸水法（沸水，读数100℃±1℃），偏差>2℃需校准或更换。"
        },

        # 34. 冷链管理 - 多选中等
        {
            "text": "冷链温度连续性管理要求有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "小批量取出，一次取1小时用量", "is_correct": True},
                {"label": "B", "text": "在冰盆上操作保持低温", "is_correct": True},
                {"label": "C", "text": "加工完成30秒内放回冷藏", "is_correct": True},
                {"label": "D", "text": "可以常温放置半天", "is_correct": False}
            ],
            "explanation": "冷链管理：小批量取出、冰盆操作保低温、30秒内放回、每小时监控温度≤4℃。"
        },

        # 35. 过敏原管理 - 单选中等 (价值观-帮助顾客)
        {
            "text": "过敏原食材应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "course_id": 2,
            "chapter_id": 2,
            "options": [
                {"label": "A", "text": "与普通食材混放", "is_correct": False},
                {"label": "B", "text": "使用黄色标识专用刀具、砧板、容器", "is_correct": True},
                {"label": "C", "text": "不需要特别标注", "is_correct": False},
                {"label": "D", "text": "随意处理", "is_correct": False}
            ],
            "explanation": "过敏原管理：黄色标识专用工具、专区操作、记录客人过敏史、防止交叉污染，保障顾客安全（帮助顾客）。"
        },

        # ========== 设备管理部分 (10道) ==========

        # 36. 燃气炒炉 - 判断简单
        {
            "text": "使用燃气炒炉前应先打开燃气阀门，再点火。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "燃气炒炉使用顺序：开燃气阀门→点火→调节火力。使用完毕：关火→关燃气阀门。"
        },

        # 37. 蒸饭车使用 - 单选中等
        {
            "text": "蒸饭车使用时，水位应保持在什么位置？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "不需要加水", "is_correct": False},
                {"label": "B", "text": "加至水位线位置", "is_correct": True},
                {"label": "C", "text": "加满水箱", "is_correct": False},
                {"label": "D", "text": "少量即可", "is_correct": False}
            ],
            "explanation": "蒸饭车使用：加水至水位线、检查水位、设置时间温度、蒸制完成排汽后开门、定期除垢清洗。"
        },

        # 38. 刨肉机安全 - 多选中等
        {
            "text": "使用刨肉机的安全注意事项有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "使用推肉棒，不可用手直接推", "is_correct": True},
                {"label": "B", "text": "清洁前必须断电", "is_correct": True},
                {"label": "C", "text": "刀片锋利，小心操作", "is_correct": True},
                {"label": "D", "text": "可以徒手推肉", "is_correct": False}
            ],
            "explanation": "刨肉机安全：使用推肉棒不徒手、清洁前断电、刀片锋利小心、定期保养检修。"
        },

        # 39. 冻库温度 - 单选简单
        {
            "text": "冻库的标准温度应保持在多少℃？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "0℃", "is_correct": False},
                {"label": "B", "text": "-10℃", "is_correct": False},
                {"label": "C", "text": "-18℃至-20℃", "is_correct": True},
                {"label": "D", "text": "-30℃", "is_correct": False}
            ],
            "explanation": "冻库标准温度：-18℃至-20℃，可接受范围-15℃至-22℃，超标需立即调整报修。"
        },

        # 40. 冻库管理 - 判断中等
        {
            "text": "冻库开门时间应尽量缩短，避免温度波动过大。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "冻库管理：开门时间尽量短、一次性取出所需食材、定期除霜、保持密封良好，避免温度波动和能耗增加。"
        },

        # 41. 设备清洁 - 单选中等
        {
            "text": "厨房设备应多久进行一次深度清洁？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "每周", "is_correct": True},
                {"label": "C", "text": "每月", "is_correct": False},
                {"label": "D", "text": "每季度", "is_correct": False}
            ],
            "explanation": "设备清洁：日常清洁（每日）、深度清洁（每周）、定期维护（按设备要求），保持设备良好运转。"
        },

        # 42. 设备故障 - 判断简单 (价值观-高效协作)
        {
            "text": "发现设备故障时，应立即上报并启用备用方案，不得擅自维修。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "course_id": 2,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "设备故障处理：立即上报厨师长→启用备用方案→报修专业人员→禁止擅自拆修，保证安全和协作效率。"
        },

        # 43. 抽排系统 - 单选中等
        {
            "text": "抽排系统应在什么时候开启？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "开始烹饪时", "is_correct": False},
                {"label": "B", "text": "烹饪前15-30分钟", "is_correct": True},
                {"label": "C", "text": "烹饪结束后", "is_correct": False},
                {"label": "D", "text": "不需要开启", "is_correct": False}
            ],
            "explanation": "抽排系统：烹饪前15-30分钟开启、烹饪结束后继续运行15分钟排净油烟、定期清洗油烟管道。"
        },

        # 44. 刀具存放 - 多选简单
        {
            "text": "刀具存放的正确方法有？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "options": [
                {"label": "A", "text": "刀刃朝下放入刀架", "is_correct": True},
                {"label": "B", "text": "分色分类存放", "is_correct": True},
                {"label": "C", "text": "消毒后沥干再存放", "is_correct": True},
                {"label": "D", "text": "可以随意堆放", "is_correct": False}
            ],
            "explanation": "刀具存放：刀刃朝下、分色分类（红蓝黄）、消毒沥干、定位摆放、便于识别拿取。"
        },

        # 45. 菜墩保养 - 判断中等
        {
            "text": "菜墩（砧板）出现深刀痕、开裂、发霉时应立即更换。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 3,
            "correct_answer": "true",
            "explanation": "菜墩管理：定期清洗消毒、竖立沥干、发现深刀痕/开裂/发霉立即更换，避免藏污纳垢滋生细菌。"
        },

        # ========== 应急管理与培训 (5道) ==========

        # 46. 停电应急 - 单选中等 (价值观-高效协作)
        {
            "text": "营业中突然停电，应首先做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "course_id": 2,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "立即离开", "is_correct": False},
                {"label": "B", "text": "保持冷静，关闭所有燃气和电器开关", "is_correct": True},
                {"label": "C", "text": "继续工作", "is_correct": False},
                {"label": "D", "text": "打开冰箱检查", "is_correct": False}
            ],
            "explanation": "停电应急：保持冷静→关闭燃气电器→保护食材（冰箱不开门）→启用应急照明→联系电力部门→协作处理。"
        },

        # 47. 食材变质 - 判断简单 (价值观-帮助顾客)
        {
            "text": "发现食材变质时，应立即隔离、拍照记录、上报，不得继续使用。",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "value_customer",
            "course_id": 2,
            "chapter_id": 4,
            "correct_answer": "true",
            "explanation": "食材变质处理：立即隔离→拍照记录→上报厨师长→填写报损→不得使用，保障食品安全（帮助顾客）。"
        },

        # 48. 人员受伤 - 单选中等
        {
            "text": "厨房人员不慎切伤手指，应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 4,
            "options": [
                {"label": "A", "text": "继续工作", "is_correct": False},
                {"label": "B", "text": "立即清洗消毒、止血包扎、上报主管", "is_correct": True},
                {"label": "C", "text": "用创可贴简单处理继续工作", "is_correct": False},
                {"label": "D", "text": "不需要处理", "is_correct": False}
            ],
            "explanation": "受伤处理：立即停止工作→清洗消毒伤口→止血包扎→上报主管→严重时就医→轻伤戴防水手套后可继续。"
        },

        # 49. 培训周期 - 单选简单 (价值观-勤劳者为本)
        {
            "text": "新员工厨房培训周期一般为多久？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "course_id": 2,
            "chapter_id": 5,
            "options": [
                {"label": "A", "text": "3-7天", "is_correct": False},
                {"label": "B", "text": "1-2周", "is_correct": False},
                {"label": "C", "text": "2-4周", "is_correct": True},
                {"label": "D", "text": "2-3个月", "is_correct": False}
            ],
            "explanation": "培训周期：新员工2-4周（基础技能+岗位实操），体现对员工成长的重视（以勤劳者为本）。"
        },

        # 50. 考核标准 - 多选中等
        {
            "text": "厨房员工考核包括哪些方面？（多选）",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "course_id": 2,
            "chapter_id": 5,
            "options": [
                {"label": "A", "text": "刀工技能", "is_correct": True},
                {"label": "B", "text": "卫生标准", "is_correct": True},
                {"label": "C", "text": "出餐速度", "is_correct": True},
                {"label": "D", "text": "只看态度", "is_correct": False}
            ],
            "explanation": "考核标准：刀工技能、烹饪技术、卫生标准、出餐速度、食品安全、团队协作、工作态度等综合评估。"
        }
    ]

    try:
        print(f"开始插入{len(questions)}道厨房题目...")
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
