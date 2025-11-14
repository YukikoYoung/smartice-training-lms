#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化20道样题到数据库，用于验证考试流程

运行方式:
cd backend
source venv/bin/activate
python3 scripts/init_sample_questions.py
"""

import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.core.database import engine
from app.models.exam import Exam, Question, QuestionType, QuestionCategory, ExamType


def load_questions_from_json():
    """从JSON文件加载题目数据"""
    json_path = os.path.join(os.path.dirname(__file__), 'sample_questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_sample_questions(db: Session):
    """创建20道样题"""
    questions_data = load_questions_from_json()

    questions = []
    for i, q_data in enumerate(questions_data, 1):
        # 转换枚举类型
        question_type_map = {
            "single_choice": QuestionType.SINGLE_CHOICE,
            "multiple_choice": QuestionType.MULTIPLE_CHOICE,
            "true_false": QuestionType.TRUE_FALSE,
        }

        category_map = {
            "VALUE_DILIGENCE": QuestionCategory.VALUE_DILIGENCE,
            "VALUE_CUSTOMER": QuestionCategory.VALUE_CUSTOMER,
            "VALUE_COLLABORATION": QuestionCategory.VALUE_COLLABORATION,
            "VALUE_TRANSPARENCY": QuestionCategory.VALUE_TRANSPARENCY,
            "FOH_HYGIENE": QuestionCategory.SKILL,
            "FOH_SERVICE": QuestionCategory.SKILL,
            "FOH_CASHIER": QuestionCategory.SKILL,
            "FOH_MANAGEMENT": QuestionCategory.SKILL,
            "FOH_SAFETY": QuestionCategory.SKILL,
            "BOH_SAFETY": QuestionCategory.SKILL,
            "BOH_HYGIENE": QuestionCategory.SKILL,
            "BOH_OPERATION": QuestionCategory.SKILL,
        }

        question = Question(
            content=q_data["content"],
            question_type=question_type_map[q_data["question_type"]],
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            explanation=q_data["explanation"],
            category=category_map[q_data["category"]],
            difficulty=q_data["difficulty"],
            is_active=True
        )
        db.add(question)
        questions.append(question)
        print(f"✓ 创建题目 {i}/20: {q_data['content'][:30]}...")

    db.commit()

    # 刷新以获取ID
    for q in questions:
        db.refresh(q)

    print(f"\n✅ 成功创建20道样题")

    return questions


def create_sample_exam(db: Session, questions: list):
    """创建一个测试考试"""
    # 获取所有题目ID
    question_ids = [q.id for q in questions]

    exam = Exam(
        title="SmartIce培训系统-综合测试卷（样题版）",
        description="包含前厅、厨房、价值观三大类题目，用于验证考试系统功能",
        exam_type=ExamType.CHAPTER_QUIZ,
        course_id=1,  # 假设关联到第一门课程
        total_questions=20,
        pass_score=60,
        time_limit=30,  # 30分钟
        allow_retake=True,
        max_attempts=3,
        retake_cooldown_days=3,
        is_published=True,
        is_active=True,
        question_ids=question_ids  # 使用JSON字段存储题目ID列表
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    print(f"\n✅ 成功创建考试: {exam.title}")
    print(f"   考试ID: {exam.id}")
    print(f"   题目数量: {exam.total_questions}")
    print(f"   及格分数: {exam.pass_score}")
    print(f"   时间限制: {exam.time_limit}分钟")
    print(f"   题目IDs: {question_ids}")

    return exam


def main():
    """主函数"""
    print("=" * 60)
    print("SmartIce LMS - 初始化20道样题")
    print("=" * 60)

    # 创建数据库会话
    db = Session(bind=engine)

    try:
        # 检查是否已有题目
        existing_count = db.query(Question).count()
        if existing_count > 0:
            print(f"\n⚠️  数据库中已有 {existing_count} 道题目")
            response = input("是否清空现有题目并重新创建？(y/n): ")
            if response.lower() != 'y':
                print("❌ 操作取消")
                return

            # 清空现有数据
            db.query(Exam).filter(Exam.title.like("%样题%")).delete()
            db.query(Question).delete()
            db.commit()
            print("✓ 已清空现有数据")

        # 创建题目
        print("\n📝 开始创建20道样题...")
        questions = create_sample_questions(db)

        # 创建考试
        print("\n📋 开始创建测试考试...")
        exam = create_sample_exam(db, questions)

        # 统计信息
        print("\n" + "=" * 60)
        print("✅ 初始化完成！")
        print("=" * 60)
        print(f"题目总数: 20道")
        print(f"  - 价值观题: 6道 (单选3、多选2、判断1)")
        print(f"  - 前厅题: 7道 (单选4、多选1、判断2)")
        print(f"  - 厨房题: 7道 (单选5、多选1、判断1)")
        print(f"\n考试名称: {exam.title}")
        print(f"考试ID: {exam.id}")
        print(f"\n🧪 测试流程:")
        print(f"1. 启动后端: cd backend && python3 main.py")
        print(f"2. 启动前端: cd frontend && npm run dev")
        print(f"3. 登录系统: http://localhost:5173/login")
        print(f"4. 参加考试: http://localhost:5173/exams/{exam.id}")
        print(f"5. 提交答案并查看成绩")

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
