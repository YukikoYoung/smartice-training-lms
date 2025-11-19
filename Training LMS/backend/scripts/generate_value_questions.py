#!/usr/bin/env python3
"""
生成价值观题目脚本
基于企业价值观优化版.md生成10道题目
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType

def create_questions():
    """创建价值观题目"""
    db = SessionLocal()

    questions = [
        # 价值观一：以勤劳者为本（3道）
        {
            "text": '以下哪种行为体现了"以勤劳者为本"的价值观？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "只完成自己的本职工作，不愿承担额外任务", "is_correct": False},
                {"label": "B", "text": "工作时间刷手机，等待下班", "is_correct": False},
                {"label": "C", "text": "完成本岗位工作后，主动询问同事是否需要帮助", "is_correct": True},
                {"label": "D", "text": "遇到问题推卸责任，不愿主动解决", "is_correct": False}
            ]
        },
        {
            "text": '关于主动性与责任感，以下哪些表现属于"超出预期"？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "主动识别并解决影响运营或客户体验的问题", "is_correct": True},
                {"label": "B", "text": "只在被要求时才完成工作", "is_correct": False},
                {"label": "C", "text": "在非工作时间主动学习新知识或提出改进建议", "is_correct": True},
                {"label": "D", "text": "遇到问题逃避或推卸责任", "is_correct": False}
            ]
        },
        {
            "text": "服务员小李在翻台高峰期看到后勤人员忙不过来，主动协助进行桌台清理。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": False},
                {"label": "B", "text": "以勤劳者为本", "is_correct": True},
                {"label": "C", "text": "平等透明", "is_correct": False},
                {"label": "D", "text": "高效协作", "is_correct": False}
            ]
        },

        # 价值观二：帮助顾客（2道）
        {
            "text": '以下哪些行为属于"帮助顾客"价值观中的"超出预期"表现？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "主动观察顾客行为，在顾客请求之前完成服务", "is_correct": True},
                {"label": "B", "text": "客人叫了多次才响应", "is_correct": False},
                {"label": "C", "text": "熟悉产品和流程，能清晰解答客人疑问", "is_correct": True},
                {"label": "D", "text": "迅速、专业地处理投诉，将负面体验转化为好评", "is_correct": True}
            ]
        },
        {
            "text": "食品安全是帮助顾客的底线。发现食材或操作流程有问题时，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "觉得问题不大，继续使用", "is_correct": False},
                {"label": "B", "text": "必须立即上报，停止使用", "is_correct": True},
                {"label": "C", "text": "等到下班后再说", "is_correct": False},
                {"label": "D", "text": "询问其他同事意见后再决定", "is_correct": False}
            ]
        },

        # 价值观三：高效协作（3道）
        {
            "text": '"高效协作"的核心理念是什么？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "只做好自己的工作就行", "is_correct": False},
                {"label": "B", "text": "尊重他人与集体的工作成果与时间", "is_correct": True},
                {"label": "C", "text": "多做多错，少做少错", "is_correct": False},
                {"label": "D", "text": "各扫门前雪，不管他人事", "is_correct": False}
            ]
        },
        {
            "text": '关于跨岗位支持，以下哪种行为属于"需要改进"？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "其他岗位同事请求帮助时能够配合协助", "is_correct": False},
                {"label": "B", "text": "在自身工作完成时，主动观察其他岗位是否需要帮助", "is_correct": False},
                {"label": "C", "text": '"这不是我的活，我不管"，拒绝协助其他岗位同事', "is_correct": True},
                {"label": "D", "text": "清晰传达工作信息，需要配合时主动沟通", "is_correct": False}
            ]
        },
        {
            "text": '交接班时应该如何体现"高效协作"？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "使用公共工具后放回原位", "is_correct": True},
                {"label": "B", "text": "交接班时说明基本情况", "is_correct": True},
                {"label": "C", "text": "详细说明重要事项，如某桌客人的特殊需求", "is_correct": True},
                {"label": "D", "text": "匆忙离开，不做任何交接", "is_correct": False}
            ]
        },

        # 价值观四：平等透明（2道）
        {
            "text": '"平等透明"价值观的核心理念是什么？',
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "不形式主义，不排挤他人", "is_correct": True},
                {"label": "B", "text": "老员工可以享有特权", "is_correct": False},
                {"label": "C", "text": "关系好的同事可以特殊对待", "is_correct": False},
                {"label": "D", "text": "背后说坏话比当面沟通更好", "is_correct": False}
            ]
        },
        {
            "text": '以下哪些行为体现了"平等透明"价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "主动引导并接纳新员工，帮助新员工快速融入团队", "is_correct": True},
                {"label": "B", "text": "形成小团体，有意识地排挤新员工", "is_correct": False},
                {"label": "C", "text": "勇于承认错误并主动改正", "is_correct": True},
                {"label": "D", "text": "对顾客坦诚相待，赢得信任", "is_correct": True}
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
            print(f"[{i}/{len(questions)}] 已插入题目：{q_data['content'][:30]}...")

        print(f"\n✅ 成功插入 {inserted_count} 道价值观题目！")

        # 统计题目分布
        single_choice = sum(1 for q in questions if q["question_type"] == QuestionType.SINGLE_CHOICE)
        multiple_choice = sum(1 for q in questions if q["question_type"] == QuestionType.MULTIPLE_CHOICE)

        easy = sum(1 for q in questions if q["difficulty"] == "easy")
        medium = sum(1 for q in questions if q["difficulty"] == "medium")

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
        print(f"\n价值观分布：")
        print(f"- 以勤劳者为本：{value_diligence}道")
        print(f"- 帮助顾客：{value_customer}道")
        print(f"- 高效协作：{value_collaboration}道")
        print(f"- 平等透明：{value_transparency}道")

    except Exception as e:
        db.rollback()
        print(f"❌ 插入题目失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始生成价值观题目...")
    create_questions()
    print("\n价值观题目生成完成！")
