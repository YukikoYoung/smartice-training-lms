#!/usr/bin/env python3
"""
生成前厅题目批次3
生成60道题目，涵盖服务细节、客户场景和价值观实践
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType

def create_questions():
    """创建前厅批次3题目（60道）"""
    db = SessionLocal()

    questions = [
        # === 服务流程细节（15道）===
        {
            "text": "客人进门时，服务员应该在多远的距离开始问候？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "1米以内", "is_correct": False},
                {"label": "B", "text": "3米左右", "is_correct": True},
                {"label": "C", "text": "5米以上", "is_correct": False},
                {"label": "D", "text": "等客人走到面前", "is_correct": False}
            ]
        },
        {
            "text": '标准问候语"欢迎光临"之后应该怎么说？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "请问几位？", "is_correct": True},
                {"label": "B", "text": "请随便坐", "is_correct": False},
                {"label": "C", "text": "今天人很多", "is_correct": False},
                {"label": "D", "text": "需要菜单吗？", "is_correct": False}
            ]
        },
        {
            "text": "引领客人入座时，服务员应该走在客人的哪个位置？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "正前方1-2步", "is_correct": True},
                {"label": "B", "text": "正后方跟随", "is_correct": False},
                {"label": "C", "text": "左侧并行", "is_correct": False},
                {"label": "D", "text": "右侧并行", "is_correct": False}
            ]
        },
        {
            "text": "为客人拉椅子时，应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "从客人右侧拉椅", "is_correct": True},
                {"label": "B", "text": "等客人准备坐下时轻推椅子", "is_correct": True},
                {"label": "C", "text": "力度要适中，避免推得太猛", "is_correct": True},
                {"label": "D", "text": "不需要帮助客人拉椅", "is_correct": False}
            ]
        },
        {
            "text": "递送菜单时的正确做法是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "双手递送，菜单正面朝向客人", "is_correct": True},
                {"label": "B", "text": "从客人右侧递送", "is_correct": True},
                {"label": "C", "text": "先递给长辈或女士", "is_correct": True},
                {"label": "D", "text": "直接放在桌上让客人自取", "is_correct": False}
            ]
        },
        {
            "text": "客人点餐时，服务员应该采取什么姿态？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "站在客人左后侧，微微侧身", "is_correct": True},
                {"label": "B", "text": "直接站在客人面前", "is_correct": False},
                {"label": "C", "text": "坐在客人旁边", "is_correct": False},
                {"label": "D", "text": "离远一点等客人叫", "is_correct": False}
            ]
        },
        {
            "text": "客人点完餐后，服务员应该做什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "重复确认点餐内容", "is_correct": True},
                {"label": "B", "text": "告知大概出餐时间", "is_correct": True},
                {"label": "C", "text": "推荐特色菜或套餐", "is_correct": False},
                {"label": "D", "text": "收回菜单并感谢", "is_correct": True}
            ]
        },
        {
            "text": "上菜时的标准报菜词格式是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "您好，这是您的XX菜，请慢用", "is_correct": True},
                {"label": "B", "text": "XX菜来了", "is_correct": False},
                {"label": "C", "text": "您的菜好了", "is_correct": False},
                {"label": "D", "text": "直接上菜不说话", "is_correct": False}
            ]
        },
        {
            "text": "上热菜或汤时，应该特别注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": '提醒客人"小心烫"', "is_correct": True},
                {"label": "B", "text": "放在离客人稍远的位置", "is_correct": True},
                {"label": "C", "text": "使用隔热垫或托盘", "is_correct": True},
                {"label": "D", "text": "快速放下就行", "is_correct": False}
            ]
        },
        {
            "text": "客人用餐过程中，服务员应该多久巡台一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "3-5分钟", "is_correct": True},
                {"label": "B", "text": "10分钟", "is_correct": False},
                {"label": "C", "text": "15分钟", "is_correct": False},
                {"label": "D", "text": "等客人叫再过去", "is_correct": False}
            ]
        },
        {
            "text": "发现客人的菜品快吃完时，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "主动询问是否需要加菜或其他服务", "is_correct": True},
                {"label": "B", "text": "立即撤走空盘", "is_correct": False},
                {"label": "C", "text": "等客人全部吃完再询问", "is_correct": False},
                {"label": "D", "text": "不需要特别做什么", "is_correct": False}
            ]
        },
        {
            "text": "撤换骨碟、烟灰缸的时机是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "骨碟有3个以上残渣时", "is_correct": True},
                {"label": "B", "text": "烟灰缸有2个以上烟头时", "is_correct": True},
                {"label": "C", "text": "客人示意需要更换时", "is_correct": True},
                {"label": "D", "text": "等客人用完餐再统一更换", "is_correct": False}
            ]
        },
        {
            "text": "客人要求结账时，服务员应该怎么做？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "确认台号和消费金额", "is_correct": True},
                {"label": "B", "text": "询问支付方式", "is_correct": True},
                {"label": "C", "text": "核对账单无误后递给客人", "is_correct": True},
                {"label": "D", "text": "直接告诉客人金额", "is_correct": False}
            ]
        },
        {
            "text": "送客时的标准服务流程包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "帮助客人整理物品", "is_correct": True},
                {"label": "B", "text": "引领客人到门口", "is_correct": True},
                {"label": "C", "text": '说"谢谢光临，欢迎下次再来"', "is_correct": True},
                {"label": "D", "text": "直接在原地说再见", "is_correct": False}
            ]
        },
        {
            "text": "翻台清理时，正确的顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "收餐具→清理桌面→消毒→摆台", "is_correct": True},
                {"label": "B", "text": "清理桌面→收餐具→摆台→消毒", "is_correct": False},
                {"label": "C", "text": "消毒→收餐具→清理→摆台", "is_correct": False},
                {"label": "D", "text": "摆台→收餐具→清理→消毒", "is_correct": False}
            ]
        },

        # === 客户服务场景（15道）===
        {
            "text": "客人投诉菜品不新鲜，服务员应该怎么处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即道歉并撤下菜品", "is_correct": True},
                {"label": "B", "text": "通知主管或店长", "is_correct": True},
                {"label": "C", "text": "询问客人是否需要更换或退款", "is_correct": True},
                {"label": "D", "text": "解释说菜品是新鲜的", "is_correct": False}
            ]
        },
        {
            "text": "客人反映上菜太慢，应该如何回应？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "道歉并立即到厨房确认进度，告知客人预计时间", "is_correct": True},
                {"label": "B", "text": "解释说厨房很忙", "is_correct": False},
                {"label": "C", "text": "说其他客人也在等", "is_correct": False},
                {"label": "D", "text": "建议客人先吃其他菜", "is_correct": False}
            ]
        },
        {
            "text": "客人不小心打翻了水杯，服务员应该怎么做？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": '说"没关系"安抚客人情绪', "is_correct": True},
                {"label": "B", "text": "立即用毛巾清理桌面和地面", "is_correct": True},
                {"label": "C", "text": "更换湿掉的餐具和台布", "is_correct": True},
                {"label": "D", "text": "责怪客人不小心", "is_correct": False}
            ]
        },
        {
            "text": "客人要求调整空调温度，但其他客人可能不同意，应该怎么处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "婉转询问附近其他客人意见，寻求平衡方案", "is_correct": True},
                {"label": "B", "text": "直接拒绝客人要求", "is_correct": False},
                {"label": "C", "text": "按照第一个提出的客人要求调整", "is_correct": False},
                {"label": "D", "text": "告诉客人无法调整", "is_correct": False}
            ]
        },
        {
            "text": "客人询问某道菜的具体做法和食材，服务员不清楚时应该怎么办？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "如实告知不清楚，立即询问厨房后回复", "is_correct": True},
                {"label": "B", "text": "随便编一个答案", "is_correct": False},
                {"label": "C", "text": "推荐客人点其他菜", "is_correct": False},
                {"label": "D", "text": "告诉客人这是商业秘密", "is_correct": False}
            ]
        },
        {
            "text": "客人带了小孩，服务员可以提供哪些额外服务？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "提供儿童座椅", "is_correct": True},
                {"label": "B", "text": "提供儿童餐具", "is_correct": True},
                {"label": "C", "text": "推荐适合儿童的菜品", "is_correct": True},
                {"label": "D", "text": "帮忙照看小孩", "is_correct": False}
            ]
        },
        {
            "text": "发现客人遗落物品，正确的处理流程是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即上交前台或主管", "is_correct": True},
                {"label": "B", "text": "登记物品详情和发现时间地点", "is_correct": True},
                {"label": "C", "text": "尝试联系客人归还", "is_correct": True},
                {"label": "D", "text": "自行保管", "is_correct": False}
            ]
        },
        {
            "text": "客人要求打包，服务员应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "使用干净的打包盒", "is_correct": True},
                {"label": "B", "text": "分类打包，避免串味", "is_correct": True},
                {"label": "C", "text": "提醒客人尽快食用", "is_correct": True},
                {"label": "D", "text": "把所有菜混在一起打包", "is_correct": False}
            ]
        },
        {
            "text": "客人询问厕所位置，服务员应该怎么回答？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "用手势指引并清晰描述路线", "is_correct": True},
                {"label": "B", "text": "只说在那边", "is_correct": False},
                {"label": "C", "text": "让客人自己找", "is_correct": False},
                {"label": "D", "text": "说不清楚", "is_correct": False}
            ]
        },
        {
            "text": "客人表示对服务很满意，服务员应该如何回应？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "真诚感谢并表示会继续努力", "is_correct": True},
                {"label": "B", "text": "说这是应该的不用谢", "is_correct": False},
                {"label": "C", "text": "沉默不回应", "is_correct": False},
                {"label": "D", "text": "立即要求客人给好评", "is_correct": False}
            ]
        },
        {
            "text": "高峰期客人需要等位，服务员应该如何安抚？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "告知大概等候时间", "is_correct": True},
                {"label": "B", "text": "提供等候区座位或饮用水", "is_correct": True},
                {"label": "C", "text": "定期更新排队进度", "is_correct": True},
                {"label": "D", "text": "让客人自己等不管", "is_correct": False}
            ]
        },
        {
            "text": "客人对账单有疑问，认为金额不对，应该怎么处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "耐心核对账单每一项，如有错误立即更正并道歉", "is_correct": True},
                {"label": "B", "text": "坚持账单是对的", "is_correct": False},
                {"label": "C", "text": "让客人自己去前台问", "is_correct": False},
                {"label": "D", "text": "说系统自动生成的不会错", "is_correct": False}
            ]
        },
        {
            "text": "客人有特殊饮食要求（如过敏、忌口），服务员应该怎么做？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "详细记录客人的要求", "is_correct": True},
                {"label": "B", "text": "与厨房明确沟通", "is_correct": True},
                {"label": "C", "text": "上菜时再次确认", "is_correct": True},
                {"label": "D", "text": "觉得麻烦就不管", "is_correct": False}
            ]
        },
        {
            "text": "客人需要发票，服务员应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "询问抬头信息并协助前台开具", "is_correct": True},
                {"label": "B", "text": "告诉客人无法开发票", "is_correct": False},
                {"label": "C", "text": "让客人自己去前台办理", "is_correct": False},
                {"label": "D", "text": "说发票已经用完", "is_correct": False}
            ]
        },
        {
            "text": "客人询问是否有WiFi密码，应该怎么回答？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "礼貌告知WiFi名称和密码", "is_correct": True},
                {"label": "B", "text": "说没有WiFi", "is_correct": False},
                {"label": "C", "text": "说不知道密码", "is_correct": False},
                {"label": "D", "text": "让客人用自己的流量", "is_correct": False}
            ]
        },

        # === 价值观实践场景（15道）===
        {
            "text": '早班服务员小王提前15分钟到岗，主动帮助清洁还未完成的区域。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '以下哪些行为违背了"以勤劳者为本"的价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "工作时间频繁刷手机", "is_correct": True},
                {"label": "B", "text": "看到忙碌的同事也不主动帮忙", "is_correct": True},
                {"label": "C", "text": "只做分内工作，多一点都不愿意做", "is_correct": True},
                {"label": "D", "text": "完成工作后主动学习新技能", "is_correct": False}
            ]
        },
        {
            "text": '客人的孩子不小心打翻了汤，服务员小李立即拿来干净毛巾，先帮孩子擦手避免烫伤，再清理桌面。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "以勤劳者为本", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '关于"帮助顾客"价值观，以下哪些做法是正确的？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "观察客人需求，主动提供服务", "is_correct": True},
                {"label": "B", "text": "真诚对待每一位客人，不分贵贱", "is_correct": True},
                {"label": "C", "text": "把客人的需求放在第一位", "is_correct": True},
                {"label": "D", "text": "只为给小费的客人提供好服务", "is_correct": False}
            ]
        },
        {
            "text": '高峰期，收银员发现服务员人手不够，主动帮忙传菜和清理桌面。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "高效协作", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '以下哪些行为违背了"高效协作"的价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": '说"这不是我的工作"拒绝帮忙', "is_correct": True},
                {"label": "B", "text": "交接班时不交代重要信息", "is_correct": True},
                {"label": "C", "text": "用完公共工具不归位", "is_correct": True},
                {"label": "D", "text": "主动分享工作经验", "is_correct": False}
            ]
        },
        {
            "text": '新员工小张刚入职，老员工小陈主动教他服务流程和注意事项。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": False},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": '关于"平等透明"价值观，以下哪些做法是错误的？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "老员工拉帮结派，排挤新员工", "is_correct": True},
                {"label": "B", "text": "犯了错不承认，推卸责任", "is_correct": True},
                {"label": "C", "text": "背后说同事坏话", "is_correct": True},
                {"label": "D", "text": "主动帮助新员工融入团队", "is_correct": False}
            ]
        },
        {
            "text": '服务员小美发现客人遗落了贵重物品，立即上交并帮助联系失主。这体现了哪些价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "高效协作", "is_correct": False}
            ]
        },
        {
            "text": '面对工作中的失误，正确的态度是什么？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "勇于承认错误并主动改正", "is_correct": True},
                {"label": "B", "text": "推卸给其他同事", "is_correct": False},
                {"label": "C", "text": "隐瞒不报", "is_correct": False},
                {"label": "D", "text": "找各种理由解释", "is_correct": False}
            ]
        },
        {
            "text": '主管分配任务时，小李主动承担了最繁重的部分。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": False},
                {"label": "C", "text": "帮助顾客", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '客人点了过敏食材，服务员小王记得之前客人提过过敏史，主动提醒并建议更换菜品。这体现了什么价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "以勤劳者为本", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '团队协作中，最重要的是什么？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "互相支持，共同完成目标", "is_correct": True},
                {"label": "B", "text": "只管自己的工作", "is_correct": False},
                {"label": "C", "text": "推卸责任", "is_correct": False},
                {"label": "D", "text": "只听从领导安排", "is_correct": False}
            ]
        },
        {
            "text": '发现同事在服务流程上有问题，应该怎么做？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "私下友善提醒并分享正确做法", "is_correct": True},
                {"label": "B", "text": "当众指责", "is_correct": False},
                {"label": "C", "text": "向领导打小报告", "is_correct": False},
                {"label": "D", "text": "不管不问", "is_correct": False}
            ]
        },
        {
            "text": '一个优秀的餐饮服务员应该具备哪些品质？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "勤劳主动，不怕辛苦", "is_correct": True},
                {"label": "B", "text": "真诚待客，用心服务", "is_correct": True},
                {"label": "C", "text": "团队协作，互相帮助", "is_correct": True},
                {"label": "D", "text": "只做分内工作", "is_correct": False}
            ]
        },

        # === 团队协作与沟通（15道）===
        {
            "text": "与厨房沟通时，应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "清晰表达台号和菜品信息", "is_correct": True},
                {"label": "B", "text": "态度礼貌，互相尊重", "is_correct": True},
                {"label": "C", "text": "紧急催菜时说明原因", "is_correct": True},
                {"label": "D", "text": "大声喊叫甚至责骂", "is_correct": False}
            ]
        },
        {
            "text": "发现同事服务态度不好，应该怎么办？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "私下善意提醒并了解原因", "is_correct": True},
                {"label": "B", "text": "当众批评", "is_correct": False},
                {"label": "C", "text": "不管不问", "is_correct": False},
                {"label": "D", "text": "向客人解释是同事的问题", "is_correct": False}
            ]
        },
        {
            "text": "交接班时，必须交代清楚的信息包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "当前在座客人的情况", "is_correct": True},
                {"label": "B", "text": "预订和等位信息", "is_correct": True},
                {"label": "C", "text": "待处理的特殊要求", "is_correct": True},
                {"label": "D", "text": "个人的情绪和抱怨", "is_correct": False}
            ]
        },
        {
            "text": "同事请假，工作量增加，应该持什么态度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "理解并主动分担，团队互助", "is_correct": True},
                {"label": "B", "text": "抱怨同事总请假", "is_correct": False},
                {"label": "C", "text": "拒绝承担额外工作", "is_correct": False},
                {"label": "D", "text": "消极怠工", "is_correct": False}
            ]
        },
        {
            "text": "新员工培训期间，老员工应该怎么做？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "耐心教导服务流程和技巧", "is_correct": True},
                {"label": "B", "text": "分享工作经验和注意事项", "is_correct": True},
                {"label": "C", "text": "鼓励并给予正面反馈", "is_correct": True},
                {"label": "D", "text": "嘲笑新员工的失误", "is_correct": False}
            ]
        },
        {
            "text": "发现同事拿了公司物品，应该怎么办？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "私下劝说同事归还，必要时上报管理层", "is_correct": True},
                {"label": "B", "text": "视而不见", "is_correct": False},
                {"label": "C", "text": "当众揭发", "is_correct": False},
                {"label": "D", "text": "自己也拿一点", "is_correct": False}
            ]
        },
        {
            "text": "同事之间产生矛盾，应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "私下沟通，坦诚交流，寻求理解", "is_correct": True},
                {"label": "B", "text": "冷战不说话", "is_correct": False},
                {"label": "C", "text": "在背后说坏话", "is_correct": False},
                {"label": "D", "text": "拉拢其他同事孤立对方", "is_correct": False}
            ]
        },
        {
            "text": "领班安排的工作不合理时，应该怎么反馈？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "礼貌提出意见和建议，说明具体原因", "is_correct": True},
                {"label": "B", "text": "背后抱怨", "is_correct": False},
                {"label": "C", "text": "直接拒绝执行", "is_correct": False},
                {"label": "D", "text": "消极对抗", "is_correct": False}
            ]
        },
        {
            "text": "看到同事被客人无理刁难，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "主动上前协助处理，缓解同事压力", "is_correct": True},
                {"label": "B", "text": "看热闹", "is_correct": False},
                {"label": "C", "text": "装作没看见", "is_correct": False},
                {"label": "D", "text": "事后嘲笑同事", "is_correct": False}
            ]
        },
        {
            "text": "团队会议上，应该持什么态度？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "积极参与讨论，提出建设性意见", "is_correct": True},
                {"label": "B", "text": "认真倾听他人发言", "is_correct": True},
                {"label": "C", "text": "尊重不同意见", "is_correct": True},
                {"label": "D", "text": "玩手机不参与", "is_correct": False}
            ]
        },
        {
            "text": "工作中遇到问题，正确的做法是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "主动寻求帮助或向上级汇报", "is_correct": True},
                {"label": "B", "text": "隐瞒问题", "is_correct": False},
                {"label": "C", "text": "拖延不处理", "is_correct": False},
                {"label": "D", "text": "把问题丢给别人", "is_correct": False}
            ]
        },
        {
            "text": "店长表扬了同事的工作，你应该持什么态度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "真诚祝贺，以同事为榜样", "is_correct": True},
                {"label": "B", "text": "嫉妒不满", "is_correct": False},
                {"label": "C", "text": "觉得是领导偏心", "is_correct": False},
                {"label": "D", "text": "背后说同事坏话", "is_correct": False}
            ]
        },
        {
            "text": "在餐厅工作，团队精神的核心是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "互相支持，共同进步", "is_correct": True},
                {"label": "B", "text": "以大局为重，顾全整体", "is_correct": True},
                {"label": "C", "text": "坦诚沟通，相互信任", "is_correct": True},
                {"label": "D", "text": "各自为战，互相竞争", "is_correct": False}
            ]
        },
        {
            "text": "使用公共区域（如员工休息室、更衣室）时，应该遵守什么规则？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "保持整洁，用后清理", "is_correct": True},
                {"label": "B", "text": "物品归位，方便他人使用", "is_correct": True},
                {"label": "C", "text": "不大声喧哗，尊重他人休息", "is_correct": True},
                {"label": "D", "text": "随意乱放物品", "is_correct": False}
            ]
        },
        {
            "text": "作为餐饮从业者，职业素养的体现包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "准时上班，不迟到早退", "is_correct": True},
                {"label": "B", "text": "保持良好的个人卫生和形象", "is_correct": True},
                {"label": "C", "text": "持续学习，提升服务技能", "is_correct": True},
                {"label": "D", "text": "工作时随便穿着", "is_correct": False}
            ]
        }
    ]

    try:
        inserted_count = 0
        for i, q_data in enumerate(questions, 1):
            # 创建题目对象
            question = Question(
                content=q_data["content"],
                question_type=q_data["question_type"],
                difficulty=q_data["difficulty"],
                category=q_data["category"],
                options=q_data["options"]
            )

            db.add(question)
            db.commit()
            db.refresh(question)

            inserted_count += 1
            print(f"[{i}/{len(questions)}] 已插入题目：{q_data['content'][:40]}...")

        print(f"\n✅ 成功插入 {inserted_count} 道前厅批次3题目！")

        # 统计题目分布
        single_choice = sum(1 for q in questions if q["question_type"] == QuestionType.SINGLE_CHOICE)
        multiple_choice = sum(1 for q in questions if q["question_type"] == QuestionType.MULTIPLE_CHOICE)

        easy = sum(1 for q in questions if q["difficulty"] == "easy")
        medium = sum(1 for q in questions if q["difficulty"] == "medium")
        hard = sum(1 for q in questions if q["difficulty"] == "hard")

        skill = sum(1 for q in questions if q["category"] == "skill")
        value_diligence = sum(1 for q in questions if q["category"] == "value_diligence")
        value_customer = sum(1 for q in questions if q["category"] == "value_customer")
        value_collaboration = sum(1 for q in questions if q["category"] == "value_collaboration")
        value_transparency = sum(1 for q in questions if q["category"] == "value_transparency")

        print(f"\n题目统计：")
        print(f"- 单选题：{single_choice}道")
        print(f"- 多选题：{multiple_choice}道")
        print(f"\n难度分布：")
        print(f"- 简单：{easy}道")
        print(f"- 中等：{medium}道")
        print(f"- 困难：{hard}道")
        print(f"\n类别分布：")
        print(f"- 技能类：{skill}道")
        print(f"- 价值观（勤劳）：{value_diligence}道")
        print(f"- 价值观（顾客）：{value_customer}道")
        print(f"- 价值观（协作）：{value_collaboration}道")
        print(f"- 价值观（透明）：{value_transparency}道")

    except Exception as e:
        db.rollback()
        print(f"❌ 插入题目失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始生成前厅批次3题目（60道）...")
    create_questions()
    print("\n前厅批次3题目生成完成！")
