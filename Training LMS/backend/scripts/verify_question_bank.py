#!/usr/bin/env python3
"""验证题库完整性"""

import sqlite3

DB_PATH = "/Users/apple/Desktop/知识库/餐饮运营知识库/SmartIce Operation System/培训工具/Training LMS/backend/training_lms.db"

def verify_questions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("=" * 70)
    print("                  SmartIce LMS 题库验证报告")
    print("=" * 70)
    
    # 总题目数
    cursor.execute("SELECT COUNT(*) FROM questions WHERE course_id IN (1, 2)")
    total = cursor.fetchone()[0]
    print(f"\n📊 题库总量: {total} 道题")
    
    # 按课程统计
    print("\n" + "=" * 70)
    print("一、各课程题目分布")
    print("=" * 70)
    
    cursor.execute("""
        SELECT 
            CASE 
                WHEN c.id = 1 THEN '前厅运营标准与服务流程'
                WHEN c.id = 2 THEN '厨房运营标准与岗位流程'
            END as course_name,
            c.id as course_id,
            COUNT(q.id) as total_questions
        FROM courses c
        LEFT JOIN questions q ON c.id = q.course_id
        WHERE c.id IN (1, 2)
        GROUP BY c.id
    """)
    
    courses = cursor.fetchall()
    for course_name, course_id, count in courses:
        print(f"\n【{course_name}】")
        print(f"  总题目数: {count} 道")
        
        # 各章节分布
        cursor.execute("""
            SELECT 
                ch.title,
                COUNT(q.id) as count,
                SUM(CASE WHEN q.question_type='SINGLE_CHOICE' THEN 1 ELSE 0 END) as single,
                SUM(CASE WHEN q.question_type='MULTIPLE_CHOICE' THEN 1 ELSE 0 END) as multiple,
                SUM(CASE WHEN q.question_type='TRUE_FALSE' THEN 1 ELSE 0 END) as true_false
            FROM chapters ch
            LEFT JOIN questions q ON ch.id = q.chapter_id AND q.course_id = ?
            WHERE ch.course_id = ?
            GROUP BY ch.id
            ORDER BY ch."order"
        """, (course_id, course_id))
        
        chapters = cursor.fetchall()
        for ch_title, ch_count, single, multiple, tf in chapters:
            print(f"    ├─ {ch_title}: {ch_count}道 (单选{single}, 多选{multiple}, 判断{tf})")
    
    # 题型分布
    print("\n" + "=" * 70)
    print("二、题型分布统计")
    print("=" * 70)
    
    cursor.execute("""
        SELECT 
            question_type,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM questions WHERE course_id IN (1,2)), 1) as percentage
        FROM questions
        WHERE course_id IN (1, 2)
        GROUP BY question_type
    """)
    
    types = cursor.fetchall()
    type_names = {
        'SINGLE_CHOICE': '单选题',
        'MULTIPLE_CHOICE': '多选题',
        'TRUE_FALSE': '判断题'
    }
    
    for qtype, count, pct in types:
        print(f"  {type_names.get(qtype, qtype)}: {count}道 ({pct}%)")
    
    # 难度分布
    print("\n" + "=" * 70)
    print("三、难度分布统计")
    print("=" * 70)
    
    cursor.execute("""
        SELECT 
            difficulty,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM questions WHERE course_id IN (1,2)), 1) as percentage
        FROM questions
        WHERE course_id IN (1, 2)
        GROUP BY difficulty
    """)
    
    difficulties = cursor.fetchall()
    diff_names = {
        'EASY': '简单',
        'MEDIUM': '中等',
        'HARD': '困难'
    }
    
    for diff, count, pct in difficulties:
        print(f"  {diff_names.get(diff, diff)}: {count}道 ({pct}%)")
    
    # 类别分布
    print("\n" + "=" * 70)
    print("四、题目类别统计")
    print("=" * 70)
    
    cursor.execute("""
        SELECT 
            category,
            COUNT(*) as count,
            ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM questions WHERE course_id IN (1,2)), 1) as percentage
        FROM questions
        WHERE course_id IN (1, 2)
        GROUP BY category
    """)
    
    categories = cursor.fetchall()
    cat_names = {
        'PROFESSIONAL': '专业知识题',
        'VALUE': '价值观题'
    }
    
    for cat, count, pct in categories:
        print(f"  {cat_names.get(cat, cat)}: {count}道 ({pct}%)")
    
    # 质量检查
    print("\n" + "=" * 70)
    print("五、质量检查")
    print("=" * 70)
    
    # 检查无选项的选择题
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE question_type IN ('SINGLE_CHOICE', 'MULTIPLE_CHOICE') 
        AND (options IS NULL OR options = '')
        AND course_id IN (1, 2)
    """)
    no_options = cursor.fetchone()[0]
    print(f"  {'✅' if no_options == 0 else '❌'} 选择题选项完整性: {no_options} 道题缺少选项")
    
    # 检查无答案的题目
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE (correct_answer IS NULL OR correct_answer = '')
        AND course_id IN (1, 2)
    """)
    no_answer = cursor.fetchone()[0]
    print(f"  {'✅' if no_answer == 0 else '❌'} 答案完整性: {no_answer} 道题缺少答案")
    
    # 检查无解析的题目
    cursor.execute("""
        SELECT COUNT(*) FROM questions 
        WHERE (explanation IS NULL OR explanation = '')
        AND course_id IN (1, 2)
    """)
    no_explanation = cursor.fetchone()[0]
    print(f"  {'⚠️ ' if no_explanation > 0 else '✅'} 解析完整性: {no_explanation} 道题缺少解析")
    
    print("\n" + "=" * 70)
    print("六、评估结论")
    print("=" * 70)
    
    status = "✅ 优秀" if total >= 150 else "⚠️  合格" if total >= 100 else "❌ 不足"
    print(f"\n  题库状态: {status}")
    print(f"  当前题目: {total} 道")
    print(f"  目标题目: 200-300 道")
    print(f"  完成度: {round(total/200*100, 1)}%")
    
    if total < 200:
        need = 200 - total
        print(f"\n  建议: 再补充约 {need} 道题目达到目标")
    
    print("\n" + "=" * 70)
    print("              题库验证完成!")
    print("=" * 70)
    
    conn.close()

if __name__ == "__main__":
    verify_questions()
