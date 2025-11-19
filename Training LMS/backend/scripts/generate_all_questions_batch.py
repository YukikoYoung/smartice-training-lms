#!/usr/bin/env python3
"""
批量生成所有章节题目
为了效率,使用AI辅助生成的核心题目模板
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "/Users/apple/Desktop/知识库/餐饮运营知识库/SmartIce Operation System/培训工具/Training LMS/backend/training_lms.db"

def create_question(content, question_type, category, course_id, chapter_id, 
                    options, correct_answer, explanation, difficulty="MEDIUM"):
    return {
        "text": content,
        "question_type": question_type,
        "category": category,
        "course_id": course_id,
        "chapter_id": chapter_id,
        "difficulty": difficulty,
        "options": json.dumps(options, ensure_ascii=False) if options else None,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "is_active": 1
    }

all_questions = []

# ============ 前厅第2章: 管理岗位流程 (Chapter ID: 2) ============
print("生成前厅第2章题目...")
all_questions.extend([
    # 店长职责
    create_question("店长的核心职责不包括?", "SINGLE_CHOICE", "PROFESSIONAL", 1, 2,
        {"A": "门店整体运营管理", "B": "团队建设与培养", "C": "亲自做菜", "D": "营业数据分析"},
        "C", "店长负责管理而非亲自操作,核心职责是运营、团队、数据。", "EASY"),
    
    create_question("店长每日工作流程的第一步是?", "SINGLE_CHOICE", "PROFESSIONAL", 1, 2,
        {"A": "开业准备", "B": "查看前一日营业数据", "C": "召开班前会", "D": "巡视餐厅"},
        "B", "店长应先查看前一日数据,了解运营情况,再安排当日工作。", "MEDIUM"),
    
    create_question("前厅主管的职责包括哪些?(多选)", "MULTIPLE_CHOICE", "PROFESSIONAL", 1, 2,
        {"A": "现场服务监督", "B": "员工排班管理", "C": "投诉处理", "D": "库存管理"},
        "A,B,C", "主管负责现场监督、排班和投诉处理,库存管理通常由仓管负责。", "MEDIUM"),
    
    create_question("店长应每日查看营业数据,及时调整经营策略。", "TRUE_FALSE", "PROFESSIONAL", 1, 2,
        None, "true", "正确。店长需每日查看数据(营业额、客流、投诉等)并作出调整。", "EASY"),
    
    create_question("主管发现员工服务不规范,应该立即当众批评。", "TRUE_FALSE", "PROFESSIONAL", 1, 2,
        None, "false", "错误。应私下指导,保护员工自尊,体现\"平等透明\"和团队协作精神。", "EASY"),
])

# ============ 前厅第3章: 服务岗位流程 (Chapter ID: 3) ============  
print("生成前厅第3章题目...")
all_questions.extend([
    create_question("服务员迎接客人的标准距离是?", "SINGLE_CHOICE", "PROFESSIONAL", 1, 3,
        {"A": "1米", "B": "2米", "C": "3米", "D": "5米"},
        "C", "根据三米原则,客人距离3米时开始迎接。", "EASY"),
    
    create_question("客人点菜时,服务员应该?", "SINGLE_CHOICE", "PROFESSIONAL", 1, 3,
        {"A": "站在旁边等待", "B": "主动推荐菜品", "C": "催促客人快点", "D": "玩手机"},
        "B", "应主动推荐招牌菜和当日特色菜,帮助客人选择。", "EASY"),
    
    create_question("迎宾员的站位应该在?", "SINGLE_CHOICE", "PROFESSIONAL", 1, 3,
        {"A": "收银台", "B": "店门口或迎宾台前", "C": "厨房门口", "D": "任意位置"},
        "B", "迎宾员标准站位在店门口或迎宾台前,保持端正姿势。", "EASY"),
    
    create_question("传菜员取菜时应检查哪些内容?(多选)", "MULTIPLE_CHOICE", "PROFESSIONAL", 1, 3,
        {"A": "菜品温度", "B": "摆盘完整性", "C": "分量", "D": "餐具清洁"},
        "A,B,C,D", "传菜员应全面检查:温度、摆盘、分量、餐具,确保出品质量。", "MEDIUM"),
    
    create_question("收银员应该核对账单,避免错误。", "TRUE_FALSE", "PROFESSIONAL", 1, 3,
        None, "true", "正确。收银员必须仔细核对账单,避免错收或漏收。", "EASY"),
])

# ============ 厨房第1章: 通用标准与食品安全 (Chapter ID: 4) ============
print("生成厨房第1章题目...")
all_questions.extend([
    create_question("食品安全五要点的第一点是?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 4,
        {"A": "保持清洁", "B": "生熟分开", "C": "完全煮熟", "D": "安全温度"},
        "A", "食品安全五要点:保持清洁、生熟分开、完全煮熟、安全温度、安全原料。", "EASY"),
    
    create_question("肉类烹饪时,中心温度应达到多少度以上?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 4,
        {"A": "60°C", "B": "65°C", "C": "70°C", "D": "75°C"},
        "D", "肉类中心温度必须达到75°C以上,确保完全煮熟。", "MEDIUM"),
    
    create_question("热菜保温应保持在多少度以上?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 4,
        {"A": "50°C", "B": "55°C", "C": "60°C", "D": "65°C"},
        "C", "热菜应保持>60°C,冷菜<5°C,避免细菌滋生。", "MEDIUM"),
    
    create_question("厨房仪容仪表要求包括?(多选)", "MULTIPLE_CHOICE", "PROFESSIONAL", 2, 4,
        {"A": "穿戴厨师服和帽子", "B": "佩戴口罩", "C": "指甲剪短", "D": "不得佩戴首饰"},
        "A,B,C,D", "厨房仪容仪表要求:工服、帽子、口罩、短指甲、无首饰。", "EASY"),
    
    create_question("发现食材过期,应立即使用以免浪费。", "TRUE_FALSE", "PROFESSIONAL", 2, 4,
        None, "false", "错误!绝对禁止使用过期食材,必须立即丢弃。", "EASY"),
    
    create_question("工作前、如厕后、接触生食后都必须洗手。", "TRUE_FALSE", "PROFESSIONAL", 2, 4,
        None, "true", "正确。这是食品安全的基本要求,必须严格执行。", "EASY"),
])

# ============ 厨房第2章: 各岗位操作流程 (Chapter ID: 5) ============
print("生成厨房第2章题目...")
all_questions.extend([
    create_question("切配岗的核心任务是?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "烹饪菜品", "B": "食材初加工和切配", "C": "洗碗", "D": "收银"},
        "B", "切配岗负责食材初加工、切配工作,为烹饪岗提供半成品。", "EASY"),
    
    create_question("红色砧板专门用于?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "蔬菜", "B": "生肉", "C": "海鲜", "D": "熟食"},
        "B", "红色砧板专用于生肉类,严禁混用。", "EASY"),
    
    create_question("绿色砧板用于?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "蔬菜", "B": "生肉", "C": "海鲜", "D": "熟食"},
        "A", "绿色砧板专用于蔬菜类。", "EASY"),
    
    create_question("蓝色砧板用于?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "蔬菜", "B": "生肉", "C": "海鲜", "D": "熟食"},
        "C", "蓝色砧板专用于海鲜类。", "EASY"),
    
    create_question("白色砧板用于?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "蔬菜", "B": "生肉", "C": "海鲜", "D": "熟食"},
        "D", "白色砧板专用于熟食类,要求最高。", "EASY"),
    
    create_question("热菜岗快炒类菜品的出菜时间应为?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "1-2分钟", "B": "3-5分钟", "C": "10-15分钟", "D": "20分钟"},
        "B", "快炒类3-5分钟,烧炖类15-20分钟,蒸煮类8-15分钟。", "MEDIUM"),
    
    create_question("凉菜间操作要求包括?(多选)", "MULTIPLE_CHOICE", "PROFESSIONAL", 2, 5,
        {"A": "专间操作", "B": "二次更衣", "C": "佩戴口罩手套", "D": "即做即用"},
        "A,B,C,D", "凉菜间要求最高:专间、二次更衣、口罩手套、即做即用。", "MEDIUM"),
    
    create_question("洗碗间的标准流程是一刮二洗三冲四消毒五保洁。", "TRUE_FALSE", "PROFESSIONAL", 2, 5,
        None, "true", "正确。洗碗间必须严格按照五步流程操作。", "EASY"),
    
    create_question("不同颜色的砧板可以混用,只要洗干净即可。", "TRUE_FALSE", "PROFESSIONAL", 2, 5,
        None, "false", "错误!必须严格按颜色分类使用,绝对禁止混用。", "EASY"),
])

# ============ 厨房第3章: 设备管理与应急 (Chapter ID: 6) ============
print("生成厨房第3章题目...")
all_questions.extend([
    create_question("刀工中\"丝\"的标准规格是?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 6,
        {"A": "1-2mm粗", "B": "3-5mm粗", "C": "5-10mm粗", "D": "任意粗细"},
        "B", "丝:3-5mm粗、5cm长;片:2-3mm厚;丁:1cm见方。", "MEDIUM"),
    
    create_question("刀工中\"丁\"的标准规格是?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 6,
        {"A": "0.5cm见方", "B": "1cm见方", "C": "2cm见方", "D": "3cm见方"},
        "B", "丁:1cm见方;块:3-5cm见方。", "MEDIUM"),
    
    create_question("油锅起火时正确的处理方法是?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 6,
        {"A": "用水泼", "B": "用锅盖闷灭", "C": "逃跑", "D": "用手扇"},
        "B", "油锅起火立即关火,用锅盖闷灭,切记不可用水!", "EASY"),
    
    create_question("发现燃气泄漏时应该?", "SINGLE_CHOICE", "PROFESSIONAL", 2, 6,
        {"A": "打开抽油烟机", "B": "开窗通风并关闭阀门", "C": "点火查看", "D": "不管"},
        "B", "禁止明火和电器,立即开窗通风、关闭阀门、疏散人员。", "MEDIUM"),
    
    create_question("刀具安全使用要求包括?(多选)", "MULTIPLE_CHOICE", "PROFESSIONAL", 2, 6,
        {"A": "保持锋利", "B": "用完立即清洗归位", "C": "递刀时刀柄朝对方", "D": "可放在台面边缘"},
        "A,B,C", "刀具要锋利、用完归位、递刀柄,禁止放台面边缘!", "MEDIUM"),
    
    create_question("下班前必须检查所有炉灶已关闭。", "TRUE_FALSE", "PROFESSIONAL", 2, 6,
        None, "true", "正确。下班前务必检查炉灶、燃气阀门、电源全部关闭。", "EASY"),
    
    create_question("切伤或烫伤时,应该立即用冷水冲洗。", "TRUE_FALSE", "PROFESSIONAL", 2, 6,
        None, "true", "正确。轻微伤用冷水冲洗→消毒→创可贴;严重伤止血→送医。", "EASY"),
])

# ============ 补充价值观题目(穿插到各章节) ============
print("生成价值观题目...")
all_questions.extend([
    create_question("看到厨房地面有水渍,你应该?", "SINGLE_CHOICE", "VALUE", 2, 5,
        {"A": "绕过去", "B": "立即清理,避免他人滑倒", "C": "等清洁工来", "D": "提醒别人小心"},
        "B", "体现\"高效协作\":主动发现问题并解决,保护团队安全。", "EASY"),
    
    create_question("同事请假,导致你工作量增加,你应该?", "SINGLE_CHOICE", "VALUE", 1, 3,
        {"A": "抱怨", "B": "主动承担,团队协作完成", "C": "拒绝", "D": "要求加班费"},
        "B", "体现\"高效协作\"和\"以勤劳者为本\":团队成员相互支持。", "EASY"),
    
    create_question("发现菜品份量不足,但客人没注意,你应该?", "SINGLE_CHOICE", "VALUE", 2, 5,
        {"A": "装作没看见", "B": "主动补足,确保客人满意", "C": "等客人投诉", "D": "不关我事"},
        "B", "体现\"帮助顾客\":主动维护客人权益,诚信经营。", "EASY"),
    
    create_question("你认为晋升机会应该?", "SINGLE_CHOICE", "VALUE", 1, 2,
        {"A": "给关系好的人", "B": "基于能力和表现,公平透明", "C": "论资排辈", "D": "看领导喜好"},
        "B", "体现\"平等透明\"和\"以勤劳者为本\":晋升公平公正。", "EASY"),
    
    create_question("客人投诉菜品有问题,但厨房说没问题,你应该?", "SINGLE_CHOICE", "VALUE", 1, 3,
        {"A": "站在厨房一边", "B": "以客人感受为准,先道歉再处理", "C": "让客人和厨师争论", "D": "推给主管"},
        "B", "体现\"帮助顾客\":客人满意是第一位,先解决问题。", "EASY"),
])

def insert_questions(questions):
    """批量插入题目"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    inserted = 0
    for q in questions:
        try:
            cursor.execute("""
                INSERT INTO questions
                (content, question_type, category, course_id, chapter_id, difficulty,
                 options, correct_answer, explanation, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q['content'], q['question_type'], q['category'],
                q['course_id'], q['chapter_id'], q['difficulty'],
                q['options'], q['correct_answer'], q['explanation'], q['is_active']
            ))
            inserted += 1
        except Exception as e:
            print(f"❌ 插入失败: {q['content'][:30]}... - {e}")
    
    conn.commit()
    conn.close()
    return inserted

if __name__ == "__main__":
    print("=" * 60)
    print("  批量生成所有章节题目")
    print("=" * 60)
    print(f"\n总题目数: {len(all_questions)}")
    
    # 按章节统计
    chapters = {}
    for q in all_questions:
        key = (q['course_id'], q['chapter_id'])
        chapters[key] = chapters.get(key, 0) + 1
    
    print("\n各章节题目分布:")
    chapter_names = {
        (1, 2): "前厅第2章",
        (1, 3): "前厅第3章",
        (2, 4): "厨房第1章",
        (2, 5): "厨房第2章",
        (2, 6): "厨房第3章"
    }
    for key, count in sorted(chapters.items()):
        print(f"  {chapter_names[key]}: {count}道")
    
    print("\n开始插入数据库...")
    count = insert_questions(all_questions)
    print(f"✅ 成功插入 {count} 道题目!")
