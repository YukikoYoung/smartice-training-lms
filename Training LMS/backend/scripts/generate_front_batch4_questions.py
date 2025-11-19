#!/usr/bin/env python3
"""
生成前厅题目批次4
生成15道题目，涵盖客诉处理、消防管理、垃圾管理、设备管理、培训标准
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType, QuestionCategory

def create_questions():
    """创建前厅批次4题目（15道）"""
    db = SessionLocal()

    questions = [
        # === 客诉处理标准（3题）===
        {
            "content": "处理客户投诉时，正确的第一步应该是什么？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.VALUE_CUSTOMER.value,
            "options": [
                {"label": "A", "text": "先了解问题原因", "is_correct": False},
                {"label": "B", "text": "先处理情绪，再处理问题", "is_correct": True},
                {"label": "C", "text": "先查找责任人", "is_correct": False},
                {"label": "D", "text": "先联系店长", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "客诉处理原则：先处理情绪，再处理问题；先道歉，再了解情况。"
        },
        {
            "content": "以下哪些情况属于第一类客诉（员工/主管可处理）？",
            "question_type": QuestionType.MULTIPLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.VALUE_CUSTOMER.value,
            "options": [
                {"label": "A", "text": "菜品口味偏差（不是变质或异物）", "is_correct": True},
                {"label": "B", "text": "上菜速度慢", "is_correct": True},
                {"label": "C", "text": "菜品中有异物", "is_correct": False},
                {"label": "D", "text": "服务态度一般性问题", "is_correct": True}
            ],
            "correct_answer": "A,B,D",
            "explanation": "第一类客诉包括：菜品口味偏差、上菜速度慢、服务态度一般性问题、餐具不够干净（无食品安全问题）、环境卫生小问题。菜品中有异物属于第二类客诉，需要主管处理。"
        },
        {
            "content": "客户在线上平台发表了差评，应该在多长时间内回复？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.VALUE_CUSTOMER.value,
            "options": [
                {"label": "A", "text": "12小时内", "is_correct": False},
                {"label": "B", "text": "24小时内", "is_correct": True},
                {"label": "C", "text": "48小时内", "is_correct": False},
                {"label": "D", "text": "一周内", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "线上评价管理标准：24小时内回复所有评价（好评感谢，差评道歉并说明），对差评进行电话回访。"
        },

        # === 消防日常管理（3题）===
        {
            "content": "应急电源及安全指示牌应该多久检查一次？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "每周", "is_correct": True},
                {"label": "C", "text": "每月", "is_correct": False},
                {"label": "D", "text": "每季度", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "应急电源及安全指示牌每周放一次电，检查设备运转是否正常。"
        },
        {
            "content": "以下关于消防管理的说法，哪些是正确的？",
            "question_type": QuestionType.MULTIPLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "安全出口通道不能堆放任何物品", "is_correct": True},
                {"label": "B", "text": "消防喷淋脱落可以用封箱带粘上", "is_correct": False},
                {"label": "C", "text": "需要定时查看灭火器保质期", "is_correct": True},
                {"label": "D", "text": "消火栓需要定期放水检查", "is_correct": True}
            ],
            "correct_answer": "A,C,D",
            "explanation": "消防日常管理标准：安全出口通道不堆放任何物品；消防喷淋脱落不要用封箱带粘或胶水固定；定时查看灭火器保质期；消火栓定期放水检查。"
        },
        {
            "content": "灭火器保质期快到时，应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "继续使用到过期", "is_correct": False},
                {"label": "B", "text": "及时上报更换", "is_correct": True},
                {"label": "C", "text": "自行购买新的", "is_correct": False},
                {"label": "D", "text": "等到年检时统一更换", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "定时查看各区域灭火器保质期，快过期及时上报更换。"
        },

        # === 垃圾管理标准（3题）===
        {
            "content": "垃圾桶应该在什么时候更换？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "完全满了再更换", "is_correct": False},
                {"label": "B", "text": "2/3满时及时更换", "is_correct": True},
                {"label": "C", "text": "每小时更换一次", "is_correct": False},
                {"label": "D", "text": "有客人投诉时更换", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "垃圾桶2/3满时及时更换，一餐一清，每餐结束后集中清理。"
        },
        {
            "content": "以下哪些属于厨余垃圾？",
            "question_type": QuestionType.MULTIPLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "剩菜剩饭", "is_correct": True},
                {"label": "B", "text": "食物残渣", "is_correct": True},
                {"label": "C", "text": "纸巾", "is_correct": False},
                {"label": "D", "text": "酒瓶", "is_correct": False}
            ],
            "correct_answer": "A,B",
            "explanation": "垃圾分类：厨余垃圾包括剩菜剩饭等食物残渣；其他垃圾包括纸巾等；可回收物包括酒瓶、易拉罐等。"
        },
        {
            "content": "垃圾应该在什么时候统一清运至指定区域？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "午市收市", "is_correct": False},
                {"label": "B", "text": "晚市收市", "is_correct": True},
                {"label": "C", "text": "每餐结束后", "is_correct": False},
                {"label": "D", "text": "开市前", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "垃圾处理流程：一餐一清（每餐结束后集中清理），晚市收市统一清运至指定区域。"
        },

        # === 能源与设备管理（3题）===
        {
            "content": "\"三关一闭\"标准中的\"三关\"指的是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "关闭所有水龙头", "is_correct": True},
                {"label": "B", "text": "关闭所有不需要的电源", "is_correct": True},
                {"label": "C", "text": "关闭燃气总阀", "is_correct": True},
                {"label": "D", "text": "关闭所有门窗", "is_correct": False}
            ],
            "correct_answer": "A,B,C",
            "explanation": "三关一闭标准：水关闭、电关闭、燃气关闭、门闭锁。关闭所有门窗属于\"一闭\"。"
        },
        {
            "content": "设备出现故障短时间内无法解决时，正确的做法是什么？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "暂停营业等待维修", "is_correct": False},
                {"label": "B", "text": "采用应急方案并向店长报备", "is_correct": True},
                {"label": "C", "text": "自行拆卸维修", "is_correct": False},
                {"label": "D", "text": "忽略继续营业", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "设备出现故障立即上报，及时解决；短时间内不能解决的，采用应急方案并向店长报备。"
        },
        {
            "content": "冰箱内食品应该如何存放？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.SKILL.value,
            "options": [
                {"label": "A", "text": "生熟可以混放", "is_correct": False},
                {"label": "B", "text": "生熟必须分离", "is_correct": True},
                {"label": "C", "text": "只要加盖就可以混放", "is_correct": False},
                {"label": "D", "text": "温度正常即可混放", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "检查冰箱内食品是否生熟分离，温度是否正常。生熟分离是食品安全的基本要求。"
        },

        # === 培训标准（3题）===
        {
            "content": "\"四步培训法\"的正确顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.VALUE_COLLABORATION.value,
            "options": [
                {"label": "A", "text": "我讲你听 → 我做你看 → 你讲我听 → 你做我看", "is_correct": False},
                {"label": "B", "text": "我讲你听 → 你讲我听 → 我做你看 → 你做我看", "is_correct": True},
                {"label": "C", "text": "我做你看 → 你做我看 → 我讲你听 → 你讲我听", "is_correct": False},
                {"label": "D", "text": "你讲我听 → 我讲你听 → 你做我看 → 我做你看", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "四步培训法：第一步我讲你听（讲解流程）→ 第二步你讲我听（验收学习成果）→ 第三步我做你看（示范操作）→ 第四步你做我看（检验实际操作）。"
        },
        {
            "content": "以下哪些是培训时应该遵循的原则？",
            "question_type": QuestionType.MULTIPLE_CHOICE.value,
            "difficulty": "medium",
            "category": QuestionCategory.VALUE_COLLABORATION.value,
            "options": [
                {"label": "A", "text": "有问题及时沟通解决", "is_correct": True},
                {"label": "B", "text": "可以只提问题不给解决办法", "is_correct": False},
                {"label": "C", "text": "需要耐心引导，不要轻易训斥", "is_correct": True},
                {"label": "D", "text": "每天关注训练成果和人员状态", "is_correct": True}
            ],
            "correct_answer": "A,C,D",
            "explanation": "培训关键点：做到及时沟通，有问题及时解决；不能只提问题不给解决办法；不要轻易训斥店员，需耐心引导；每天关注人员训练和工作成果。"
        },
        {
            "content": "\"四步培训法\"中的第二步\"你讲我听\"的主要目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE.value,
            "difficulty": "easy",
            "category": QuestionCategory.VALUE_COLLABORATION.value,
            "options": [
                {"label": "A", "text": "锻炼员工表达能力", "is_correct": False},
                {"label": "B", "text": "验收学习成果，检验是否理解到位", "is_correct": True},
                {"label": "C", "text": "让员工自己总结经验", "is_correct": False},
                {"label": "D", "text": "节省培训师讲解时间", "is_correct": False}
            ],
            "correct_answer": "B",
            "explanation": "第二步\"你讲我听\"的目的是验收学习成果，检验员工是否理解到位。"
        }
    ]

    try:
        # 创建题目
        created_count = 0
        for q_data in questions:
            question = Question(**q_data)
            db.add(question)
            created_count += 1

        db.commit()
        print(f"✅ 成功创建 {created_count} 道题目")

        # 统计题目总数
        total_count = db.query(Question).count()
        print(f"📊 当前题库总数: {total_count} 道")

    except Exception as e:
        db.rollback()
        print(f"❌ 创建题目失败: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_questions()
