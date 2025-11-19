"""
数据验证脚本 - 检查所有题目数据是否符合标准
运行时机：
1. 扩充题库后
2. 提交代码前
3. 部署前
"""
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from sqlalchemy import text as sql_text

def validate_question_data():
    """验证所有题目数据"""
    db = SessionLocal()

    print("="*60)
    print("   SmartIce LMS 题库数据验证")
    print("="*60)
    print()

    try:
        cursor = db.execute(sql_text("SELECT id, content, options, question_type FROM questions"))
        questions = cursor.fetchall()

        total = len(questions)
        errors = []
        warnings = []

        for question_id, content, options_str, question_type in questions:
            # 检查1：题目内容不能为空
            if not content or len(content.strip()) == 0:
                errors.append(f"题目 {question_id}: 题目内容为空")

            # 检查2：选择题和多选题必须有选项
            if question_type in ['single_choice', 'multiple_choice']:
                if not options_str:
                    errors.append(f"题目 {question_id}: {question_type}类型题目缺少选项")
                    continue

                try:
                    options = json.loads(options_str)

                    # 检查2.1：选项必须是列表
                    if not isinstance(options, list):
                        errors.append(f"题目 {question_id}: 选项不是列表格式")
                        continue

                    # 检查2.2：选项数量至少2个
                    if len(options) < 2:
                        errors.append(f"题目 {question_id}: 选项少于2个")

                    # 检查2.3：每个选项必须是字典
                    for i, opt in enumerate(options):
                        if not isinstance(opt, dict):
                            errors.append(f"题目 {question_id}: 第{i+1}个选项不是字典格式")
                            continue

                        # 检查2.4：必须有label字段
                        if 'label' not in opt:
                            errors.append(f"题目 {question_id}: 第{i+1}个选项缺少label字段")

                        # 检查2.5：必须有text字段（不是content）
                        if 'text' not in opt:
                            if 'content' in opt:
                                errors.append(f"题目 {question_id}: 第{i+1}个选项使用了错误的字段名'content'，应该是'text'")
                            else:
                                errors.append(f"题目 {question_id}: 第{i+1}个选项缺少text字段")

                        # 检查2.6：必须有is_correct字段
                        if 'is_correct' not in opt:
                            warnings.append(f"题目 {question_id}: 第{i+1}个选项缺少is_correct字段")

                    # 检查2.7：至少有一个正确答案
                    correct_count = sum(1 for opt in options if opt.get('is_correct', False))
                    if correct_count == 0:
                        warnings.append(f"题目 {question_id}: 没有标记正确答案")

                except json.JSONDecodeError:
                    errors.append(f"题目 {question_id}: 选项JSON格式错误")

            # 检查3：判断题不应该有选项（允许null）
            elif question_type == 'true_false':
                if options_str and options_str != 'null':
                    warnings.append(f"题目 {question_id}: 判断题不应该有选项数据")

        # 输出报告
        print(f"📊 验证统计")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"总题目数: {total}")
        print(f"错误数量: {len(errors)}")
        print(f"警告数量: {len(warnings)}")
        print()

        if errors:
            print("❌ 发现错误：")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for error in errors[:20]:  # 只显示前20个
                print(f"  • {error}")
            if len(errors) > 20:
                print(f"  ... 还有{len(errors)-20}个错误")
            print()

        if warnings:
            print("⚠️  警告信息：")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for warning in warnings[:10]:  # 只显示前10个
                print(f"  • {warning}")
            if len(warnings) > 10:
                print(f"  ... 还有{len(warnings)-10}个警告")
            print()

        if not errors and not warnings:
            print("✅ 所有数据验证通过！")
            print()

        print("="*60)

        return len(errors) == 0

    except Exception as e:
        print(f"❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = validate_question_data()
    sys.exit(0 if success else 1)
