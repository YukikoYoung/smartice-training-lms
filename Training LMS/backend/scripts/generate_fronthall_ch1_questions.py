#!/usr/bin/env python3
"""
生成前厅第1章题目 - 通用管理标准
包含服务礼仪、仪容仪表、毛巾使用、托盘使用等内容
目标: 80-100道题
"""

import sqlite3
import json
from datetime import datetime

# 数据库连接
DB_PATH = "/Users/apple/Desktop/知识库/餐饮运营知识库/SmartIce Operation System/培训工具/Training LMS/backend/training_lms.db"

# 课程和章节ID
COURSE_ID = 1  # 前厅课程
CHAPTER_ID = 1  # 第1章:通用管理标准

def create_question(content, question_type, category, options, correct_answer, explanation, difficulty="MEDIUM"):
    """创建题目数据结构"""
    return {
        "text": content,
        "question_type": question_type,  # SINGLE_CHOICE, MULTIPLE_CHOICE, TRUE_FALSE
        "category": category,  # PROFESSIONAL, VALUE
        "course_id": COURSE_ID,
        "chapter_id": CHAPTER_ID,
        "difficulty": difficulty,  # EASY, MEDIUM, HARD
        "options": json.dumps(options, ensure_ascii=False) if options else None,
        "correct_answer": correct_answer,
        "explanation": explanation,
        "is_active": 1
    }

# 题目列表
questions = []

# ============ 服务礼仪 - 单选题 ============
questions.extend([
    create_question(
        content="遇到客人时,统一使用的问候语是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "您好", "B": "欢迎", "C": "早上好", "D": "嗨"},
        correct_answer="A",
        explanation="标准问候语统一使用\"您好\",简洁专业。",
        difficulty="EASY"
    ),
    create_question(
        content="根据\"三米原则\",客人距离多少米时应开始微笑问候?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "1米", "B": "2米", "C": "3米", "D": "5米"},
        correct_answer="C",
        explanation="三米原则:客人距离3米时开始微笑问候,2米时准备服务,1米时对话。",
        difficulty="EASY"
    ),
    create_question(
        content="在走廊遇到客人时,正确的做法是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "继续快速通过", "B": "停下侧身让道并问候", "C": "低头快走", "D": "假装没看见"},
        correct_answer="B",
        explanation="应停下脚步,侧身让出通道,面带微笑问候客人。",
        difficulty="EASY"
    ),
    create_question(
        content="客人向你走来时,应该?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "原地等待", "B": "主动迎上前2-3步", "C": "转身离开", "D": "继续工作"},
        correct_answer="B",
        explanation="应主动迎上前2-3步,微笑问候并询问需要什么帮助。",
        difficulty="EASY"
    ),
    create_question(
        content="服务态度的\"四要求\"中,不包括以下哪项?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "热情", "B": "友善", "C": "快速", "D": "耐心"},
        correct_answer="C",
        explanation="服务态度四要求是:热情、友善、耐心、尊重。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="遇到客人投诉时,正确的处理顺序是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "先处理后道歉", "B": "先道歉后处理", "C": "先解释后处理", "D": "立即找主管"},
        correct_answer="B",
        explanation="标准流程是\"先道歉后处理\",首先向客人道歉,再解决问题。",
        difficulty="EASY"
    ),
    create_question(
        content="男士头发长度标准是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "前不过眉、侧不过耳、后不过领", "B": "任意长度", "C": "全部剃光", "D": "遮住耳朵"},
        correct_answer="A",
        explanation="男士发型标准:前不过眉、侧不过耳、后不过领。",
        difficulty="EASY"
    ),
    create_question(
        content="男士指甲长度不应超过指尖多少?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "1mm", "B": "2mm", "C": "3mm", "D": "5mm"},
        correct_answer="B",
        explanation="指甲不超过指尖2mm,保持干净整洁。",
        difficulty="EASY"
    ),
    create_question(
        content="女士工作时头发应该如何处理?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "自然披肩", "B": "梳成马尾或盘起", "C": "染成彩色", "D": "随意散开"},
        correct_answer="B",
        explanation="女士头发应梳理整洁,梳成马尾、用发卷捆住或盘起。",
        difficulty="EASY"
    ),
    create_question(
        content="以下哪种行为是严格禁止的?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "佩戴婚戒", "B": "涂指甲油", "C": "戴手表", "D": "化淡妆"},
        correct_answer="B",
        explanation="严禁留长指甲、涂指甲油,可佩戴婚戒/手表,前厅可化淡妆。",
        difficulty="EASY"
    ),
])

# ============ 毛巾使用 - 单选题 ============
questions.extend([
    create_question(
        content="蓝色毛巾的用途是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "餐具擦拭", "B": "桌面清洁(一次擦拭)", "C": "洗手间清理", "D": "椅凳清理"},
        correct_answer="B",
        explanation="蓝色毛巾用于桌面清洁(一次擦拭),清除食物残渣和污渍。",
        difficulty="EASY"
    ),
    create_question(
        content="紫色毛巾的用途是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "桌面抛光(二次擦拭)", "B": "餐具擦拭", "C": "洗手间清理", "D": "椅凳清理"},
        correct_answer="A",
        explanation="紫色毛巾用于桌面抛光(二次擦拭),在蓝色毛巾清洁后使用。",
        difficulty="EASY"
    ),
    create_question(
        content="白色毛巾专门用于?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "桌面清洁", "B": "餐具擦拭", "C": "洗手间", "D": "地面"},
        correct_answer="B",
        explanation="白色毛巾专门用于擦拭餐具,要求最高清洁度。",
        difficulty="EASY"
    ),
    create_question(
        content="棕色毛巾的使用区域是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "桌面", "B": "餐具", "C": "洗手间", "D": "椅凳"},
        correct_answer="C",
        explanation="棕色毛巾用于洗手间清理,清洁台面、镜面等。",
        difficulty="EASY"
    ),
    create_question(
        content="绿色毛巾用于清洁?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "桌面", "B": "餐具", "C": "洗手间", "D": "椅凳"},
        correct_answer="D",
        explanation="绿色毛巾用于清洁椅子、凳子。",
        difficulty="EASY"
    ),
    create_question(
        content="84消毒液与水的配比是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "1:5", "B": "1:9", "C": "1:10", "D": "1:20"},
        correct_answer="B",
        explanation="84消毒液与水的比例是1:9,即1毫升消毒液加9毫升水。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="毛巾消毒浸泡时间应为?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "10分钟", "B": "20分钟", "C": "30分钟", "D": "60分钟"},
        correct_answer="C",
        explanation="毛巾应在84消毒液中浸泡30分钟进行消毒。",
        difficulty="EASY"
    ),
    create_question(
        content="毛巾每日更换几次?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "1次", "B": "2次", "C": "3次", "D": "4次"},
        correct_answer="B",
        explanation="毛巾每日两次更换:14:00-14:30午市后,22:00-22:30晚市后。",
        difficulty="EASY"
    ),
    create_question(
        content="毛巾应多久检查并更换一次?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "每10天", "B": "每15天", "C": "每20天", "D": "每30天"},
        correct_answer="C",
        explanation="每20天检查毛巾状态,对不合格毛巾淘汰更换。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="桌面清洁的正确顺序是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "先紫后蓝", "B": "先蓝后紫", "C": "只用蓝色", "D": "只用紫色"},
        correct_answer="B",
        explanation="先用蓝色毛巾擦拭清洁,再用紫色毛巾抛光。",
        difficulty="EASY"
    ),
])

# ============ 多选题 ============
questions.extend([
    create_question(
        content="\"五声服务\"包括哪些?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "客来有迎声",
            "B": "客问有答声",
            "C": "客走有送声",
            "D": "客等有歉声",
            "E": "服务有谢声"
        },
        correct_answer="A,B,C,D,E",
        explanation="五声服务包括:迎声、答声、送声、歉声、谢声,是服务标准的核心。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="仪容仪表中严禁的行为有哪些?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "浓妆艳抹",
            "B": "留长指甲",
            "C": "涂指甲油",
            "D": "戴夸张首饰"
        },
        correct_answer="A,B,C,D",
        explanation="以上都是严禁的行为,必须保持专业整洁的形象。",
        difficulty="EASY"
    ),
    create_question(
        content="毛巾分色使用的目的包括?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "避免交叉污染",
            "B": "提高卫生标准",
            "C": "便于管理",
            "D": "节约成本"
        },
        correct_answer="A,B,C",
        explanation="分色使用的目的是避免交叉污染、提高卫生标准、便于管理,而非节约成本。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="84消毒液使用时应注意哪些事项?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "不可与洗洁精混用",
            "B": "必须先清洗再消毒",
            "C": "消毒后需清水冲洗",
            "D": "建议佩戴手套"
        },
        correct_answer="A,B,C,D",
        explanation="所有选项都是84消毒液使用的重要安全注意事项。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="服务态度的核心要求包括?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "热情",
            "B": "友善",
            "C": "耐心",
            "D": "尊重"
        },
        correct_answer="A,B,C,D",
        explanation="服务态度的四个核心要求:热情、友善、耐心、尊重。",
        difficulty="EASY"
    ),
    create_question(
        content="以下哪些是严禁的服务行为?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "对客人不理不睬",
            "B": "与客人争吵",
            "C": "在客人面前吃东西",
            "D": "玩手机"
        },
        correct_answer="A,B,C,D",
        explanation="以上都是严禁的服务行为,违反将受到处罚。",
        difficulty="EASY"
    ),
    create_question(
        content="正确的毛巾清洗流程包括哪些步骤?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "用洗洁精加热水清洗",
            "B": "清水冲洗干净",
            "C": "84消毒液浸泡30分钟",
            "D": "清水冲洗后晾干"
        },
        correct_answer="A,B,C,D",
        explanation="完整流程:洗洁精清洗→冲净→消毒浸泡→冲洗→晾干。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="男士工作着装要求包括?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "工服干净整洁",
            "B": "工牌佩戴规范",
            "C": "穿黑色鞋",
            "D": "黑色或深色袜子"
        },
        correct_answer="A,B,C,D",
        explanation="男士着装所有要求都必须遵守,保持专业形象。",
        difficulty="EASY"
    ),
])

# ============ 判断题 ============
questions.extend([
    create_question(
        content="工作中遇到客人,应暂停工作优先让客人通行。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="true",
        explanation="正确。工作中遇到客人应暂停工作或避让,优先让客人通行。",
        difficulty="EASY"
    ),
    create_question(
        content="如果客人没有看到我,可以不用主动问候。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。所有岗位遇到客人时必须主动问候,不论客人是否看到。",
        difficulty="EASY"
    ),
    create_question(
        content="男士可以留长胡须,只要保持干净即可。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。严禁留长胡须,面容必须干净整洁。",
        difficulty="EASY"
    ),
    create_question(
        content="不同颜色的毛巾严禁交叉使用。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="true",
        explanation="正确。每种颜色的毛巾只能用于指定区域,严禁交叉使用。",
        difficulty="EASY"
    ),
    create_question(
        content="84消毒液可以和洗洁精混合使用,效果更好。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误!84消毒液与洗洁精不可混用,会产生有毒氯气,非常危险。",
        difficulty="EASY"
    ),
    create_question(
        content="毛巾可以裁剪成小块使用,更方便。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。毛巾不得裁剪使用,必须保持完整性。",
        difficulty="EASY"
    ),
    create_question(
        content="遇到客人投诉,应该先解释情况,再道歉。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。正确顺序是\"先道歉后处理\",首先向客人道歉。",
        difficulty="EASY"
    ),
    create_question(
        content="只要工作服干净,有轻微皱褶也没关系。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。工作服必须干净整洁、无异味、无皱褶。",
        difficulty="EASY"
    ),
    create_question(
        content="蓝色毛巾擦完桌面后,可以直接用来擦餐具。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误!餐具只能用白色毛巾擦拭,严禁使用其他颜色毛巾。",
        difficulty="EASY"
    ),
    create_question(
        content="毛巾消毒浸泡时间可以缩短到15分钟以节省时间。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。必须浸泡30分钟才能达到消毒效果,不可缩短。",
        difficulty="EASY"
    ),
])

# ============ 价值观题目(穿插) ============
questions.extend([
    create_question(
        content="客人消费金额较低时,我们应该?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "减少服务关注",
            "B": "一视同仁,尊重每一位客人",
            "C": "优先服务高消费客人",
            "D": "简化服务流程"
        },
        correct_answer="B",
        explanation="体现\"帮助顾客\"和\"平等透明\"价值观:尊重每一位客人,不论消费高低。",
        difficulty="EASY"
    ),
    create_question(
        content="发现同事服务不规范时,你应该?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "假装没看见",
            "B": "善意提醒,共同进步",
            "C": "向领导打小报告",
            "D": "无所谓,不关我事"
        },
        correct_answer="B",
        explanation="体现\"高效协作\"价值观:团队成员相互帮助,共同提升服务质量。",
        difficulty="EASY"
    ),
    create_question(
        content="客人用餐高峰期,你负责的区域非常忙碌,而同事相对空闲,你应该?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "独自应对,不麻烦别人",
            "B": "主动请同事帮忙,协作完成",
            "C": "抱怨分配不公",
            "D": "降低服务标准应付"
        },
        correct_answer="B",
        explanation="体现\"高效协作\"价值观:团队成员相互补台,确保服务质量。",
        difficulty="EASY"
    ),
    create_question(
        content="你认为勤奋工作最重要的价值是?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "会得到领导认可和回报",
            "B": "避免被批评",
            "C": "能比别人做得少",
            "D": "只是完成任务"
        },
        correct_answer="A",
        explanation="体现\"以勤劳者为本\":勤奋工作会得到认可,表现优秀会有晋升机会。",
        difficulty="EASY"
    ),
    create_question(
        content="当客人提出特殊需求(如需要儿童餐椅)时,你应该?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "告诉客人我们没有",
            "B": "主动想办法满足,如借用其他区域的",
            "C": "让客人自己想办法",
            "D": "推给主管处理"
        },
        correct_answer="B",
        explanation="体现\"帮助顾客\"价值观:主动发现并满足顾客需求,用心服务。",
        difficulty="EASY"
    ),
    create_question(
        content="对于公司的规章制度和服务标准,你的态度应该是?",
        question_type="SINGLE_CHOICE",
        category="VALUE",
        options={
            "A": "公开透明,人人平等遵守",
            "B": "领导执行严格,员工可以灵活",
            "C": "看心情执行",
            "D": "形式主义,走过场"
        },
        correct_answer="A",
        explanation="体现\"平等透明\"价值观:制度面前人人平等,公开透明执行。",
        difficulty="EASY"
    ),
])

# ============ 补充综合题目 ============
questions.extend([
    create_question(
        content="十字礼貌用语包括以下哪个?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "您好", "B": "嗨", "C": "喂", "D": "什么事"},
        correct_answer="A",
        explanation="十字礼貌用语包括:您好、请、谢谢、对不起、再见、请稍等、麻烦您、不客气、欢迎光临、慢走。",
        difficulty="EASY"
    ),
    create_question(
        content="客人身体不适时,正确的处理第一步是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "立即叫120", "B": "询问情况", "C": "通知主管", "D": "什么都不做"},
        correct_answer="B",
        explanation="先询问情况,然后提供帮助(水/药),必要时拨打120,同时通知主管。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="发生结账纠纷时,应该如何处理?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "与客人争论",
            "B": "保持冷静,核对账单,请收银员/主管处理",
            "C": "直接给客人打折",
            "D": "让客人自己看账单"
        },
        correct_answer="B",
        explanation="保持冷静,核对账单,请收银员或主管处理,不可擅自打折。",
        difficulty="MEDIUM"
    ),
    create_question(
        content="毛巾晚市消毒的时间是?",
        question_type="SINGLE_CHOICE",
        category="PROFESSIONAL",
        options={"A": "20:00-20:30", "B": "21:00-21:30", "C": "22:00-22:30", "D": "23:00-23:30"},
        correct_answer="C",
        explanation="毛巾每日两次更换和消毒:14:00-14:30(午市后)和22:00-22:30(晚市后)。",
        difficulty="EASY"
    ),
])

# ============ 再补充一些高质量题目达到80题 ============
questions.extend([
    create_question(
        content="女士是否可以涂指甲油上班?",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。严禁留长指甲、涂指甲油,保持手部干净整洁。",
        difficulty="EASY"
    ),
    create_question(
        content="问候时应该保持微笑,眼神友善。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="true",
        explanation="正确。问候时必须保持微笑,眼神友善,可配合点头手势。",
        difficulty="EASY"
    ),
    create_question(
        content="如果客人没有投诉,服务中的小失误可以不用道歉。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。发现服务失误应主动道歉,体现专业服务态度。",
        difficulty="EASY"
    ),
    create_question(
        content="工作服可以穿到餐厅外面,方便下班直接回家。",
        question_type="TRUE_FALSE",
        category="PROFESSIONAL",
        options=None,
        correct_answer="false",
        explanation="错误。工作服不得穿出餐厅,下班前应更换便服。",
        difficulty="EASY"
    ),
    create_question(
        content="上班前应该检查哪些内容?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "整理仪容仪表",
            "B": "检查工作用品",
            "C": "参加班前会",
            "D": "检查工作区域卫生"
        },
        correct_answer="A,B,C,D",
        explanation="上班前10分钟应完成:仪容仪表整理、工作用品检查、参加班前会、检查工作区域。",
        difficulty="EASY"
    ),
    create_question(
        content="下班前的必做事项包括?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "清理工作区域",
            "B": "补充消耗物品",
            "C": "填写交接班记录",
            "D": "向主管汇报工作"
        },
        correct_answer="A,B,C,D",
        explanation="下班前必须:清理区域、补充物品、填写交接记录、向主管汇报。",
        difficulty="EASY"
    ),
    create_question(
        content="在餐厅内严禁的行为有?(多选)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "奔跑",
            "B": "大声喧哗",
            "C": "吃东西",
            "D": "玩手机"
        },
        correct_answer="A,B,C,D",
        explanation="餐厅内严禁奔跑、大声喧哗、吃东西、玩手机,保持专业形象。",
        difficulty="EASY"
    ),
    create_question(
        content="处理客人投诉的正确步骤是?(多选,按顺序)",
        question_type="MULTIPLE_CHOICE",
        category="PROFESSIONAL",
        options={
            "A": "立即道歉",
            "B": "认真倾听",
            "C": "立即处理",
            "D": "跟进确认"
        },
        correct_answer="A,B,C,D",
        explanation="投诉处理四步骤:立即道歉→认真倾听→立即处理→跟进确认。",
        difficulty="MEDIUM"
    ),
])

def insert_questions(questions):
    """将题目插入数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    inserted_count = 0
    for q in questions:
        try:
            cursor.execute("""
                INSERT INTO questions
                (content, question_type, category, course_id, chapter_id, difficulty,
                 options, correct_answer, explanation, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q['content'],
                q['question_type'],
                q['category'],
                q['course_id'],
                q['chapter_id'],
                q['difficulty'],
                q['options'],
                q['correct_answer'],
                q['explanation'],
                q['is_active']
            ))
            inserted_count += 1
        except Exception as e:
            print(f"❌ 插入题目失败: {q['content'][:30]}... - {e}")

    conn.commit()
    conn.close()

    return inserted_count

if __name__ == "__main__":
    print("=" * 60)
    print("  前厅第1章题目生成 - 通用管理标准")
    print("=" * 60)
    print(f"\n课程ID: {COURSE_ID}")
    print(f"章节ID: {CHAPTER_ID}")
    print(f"题目总数: {len(questions)}")

    # 统计题型分布
    single_choice = sum(1 for q in questions if q['question_type'] == 'SINGLE_CHOICE')
    multiple_choice = sum(1 for q in questions if q['question_type'] == 'MULTIPLE_CHOICE')
    true_false = sum(1 for q in questions if q['question_type'] == 'TRUE_FALSE')

    professional = sum(1 for q in questions if q['category'] == 'PROFESSIONAL')
    value = sum(1 for q in questions if q['category'] == 'VALUE')

    print(f"\n题型分布:")
    print(f"  - 单选题: {single_choice}道")
    print(f"  - 多选题: {multiple_choice}道")
    print(f"  - 判断题: {true_false}道")

    print(f"\n类别分布:")
    print(f"  - 专业题: {professional}道")
    print(f"  - 价值观题: {value}道")

    print(f"\n开始插入数据库...")
    count = insert_questions(questions)
    print(f"✅ 成功插入 {count} 道题目!")

    print("\n" + "=" * 60)
    print("  题目生成完成!")
    print("=" * 60)
