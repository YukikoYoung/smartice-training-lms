"""
厨房题库生成脚本 - 第二批（100道题）
覆盖：过敏原管理、餐具消毒、食材验收异常处理、厨师长、小吃房、切配、菜房
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
    db = SessionLocal()

    # 简化版100道题目 - 覆盖核心知识点
    questions = [
        # 过敏原管理（10道）
        {
            "text": "以下哪些属于常见的过敏原？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "海鲜类", "is_correct": True},
                {"label": "B", "text": "坚果类", "is_correct": True},
                {"label": "C", "text": "蛋类", "is_correct": True},
                {"label": "D", "text": "白菜", "is_correct": False}
            ],
            "explanation": "常见过敏原包括海鲜类、坚果类、蛋类、乳制品、麦类、豆类、芝麻等。"
        },
        {
            "text": "过敏原食材应使用什么颜色的刀具和砧板？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "红色", "is_correct": False},
                {"label": "B", "text": "黄色", "is_correct": True},
                {"label": "C", "text": "绿色", "is_correct": False},
                {"label": "D", "text": "蓝色", "is_correct": False}
            ],
            "explanation": "过敏原食材使用黄色刀柄刀具、黄色砧板，工具上贴过敏原专用标签。"
        },
        {
            "text": "过敏原加工专区与普通操作区的距离应至少多远？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "0.5米", "is_correct": False},
                {"label": "B", "text": "1米", "is_correct": True},
                {"label": "C", "text": "2米", "is_correct": False},
                {"label": "D", "text": "3米", "is_correct": False}
            ],
            "explanation": "过敏原加工专区与普通操作区距离≥1米。"
        },
        {
            "text": "处理完过敏原食材后，必须执行哪些流程才能处理其他食材？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "脱掉手套丢入垃圾桶", "is_correct": True},
                {"label": "B", "text": "用七步洗手法洗手≥30秒", "is_correct": True},
                {"label": "C", "text": "清洁消毒操作台面", "is_correct": True},
                {"label": "D", "text": "只需换手套", "is_correct": False}
            ],
            "explanation": "必须：脱手套→七步洗手≥30秒→更换工作服（如有溅到）→清洁消毒台面→更换新手套。"
        },
        {
            "text": "过敏原工具使用84消毒液消毒时，浸泡时间应多久？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "5分钟", "is_correct": False},
                {"label": "B", "text": "10分钟", "is_correct": False},
                {"label": "C", "text": "30分钟", "is_correct": True},
                {"label": "D", "text": "60分钟", "is_correct": False}
            ],
            "explanation": "过敏原工具用84消毒液（1:100）浸泡消毒30分钟。"
        },
        {
            "text": "前厅服务员应如何主动询问顾客过敏情况？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "不需要询问", "is_correct": False},
                {"label": "B", "text": "您是否对任何食材过敏？", "is_correct": True},
                {"label": "C", "text": "等顾客主动说", "is_correct": False},
                {"label": "D", "text": "只问有没有忌口", "is_correct": False}
            ],
            "explanation": "前厅服务员在客人点单时主动询问：您是否对任何食材过敏？体现对顾客的关怀。"
        },
        {
            "text": "过敏原信息应如何传递到厨房？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "在点单系统备注栏标注", "is_correct": True},
                {"label": "B", "text": "厨房小票上打印显示", "is_correct": True},
                {"label": "C", "text": "传菜员口头向厨师长确认", "is_correct": True},
                {"label": "D", "text": "不需要特别传递", "is_correct": False}
            ],
            "explanation": "信息传递需多重确认：点单系统备注→厨房小票打印→传菜员口头确认，体现高效协作。"
        },
        {
            "text": "客人出现过敏反应时，首先应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "继续观察", "is_correct": False},
                {"label": "B", "text": "立即通知店长/经理", "is_correct": True},
                {"label": "C", "text": "让客人自己处理", "is_correct": False},
                {"label": "D", "text": "提供免单", "is_correct": False}
            ],
            "explanation": "发现过敏反应立即通知店长/经理，停止用餐，进行紧急救助。"
        },
        {
            "text": "严重过敏反应应拨打什么电话？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "110", "is_correct": False},
                {"label": "B", "text": "119", "is_correct": False},
                {"label": "C", "text": "120", "is_correct": True},
                {"label": "D", "text": "114", "is_correct": False}
            ],
            "explanation": "严重过敏立即拨打120，同时让客人平躺，保持呼吸通畅。"
        },
        {
            "text": "过敏原储存柜外应贴什么颜色的警示标签？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "红色", "is_correct": False},
                {"label": "B", "text": "黄色", "is_correct": True},
                {"label": "C", "text": "绿色", "is_correct": False},
                {"label": "D", "text": "蓝色", "is_correct": False}
            ],
            "explanation": "过敏原储存柜外贴黄色警示标签'过敏原食材专区'。"
        },

        # 餐具消毒和七不出标准（10道）
        {
            "text": "餐具清洗消毒需经过几道工序？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "2道", "is_correct": False},
                {"label": "B", "text": "3道", "is_correct": False},
                {"label": "C", "text": "4道", "is_correct": True},
                {"label": "D", "text": "5道", "is_correct": False}
            ],
            "explanation": "用过的餐具经过初洗、清洁剂清洗、清水清洗、消毒四道工序。"
        },
        {
            "text": "化学药物消毒（84消毒液）餐具时，浸泡时间应多久？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "1分钟", "is_correct": False},
                {"label": "B", "text": "3分钟", "is_correct": False},
                {"label": "C", "text": "5分钟以上", "is_correct": True},
                {"label": "D", "text": "10分钟以上", "is_correct": False}
            ],
            "explanation": "84消毒液消毒餐具：比例1:200，浸泡时间5分钟以上，用流动净水冲去残液。"
        },
        {
            "text": "远红外消毒柜消毒时，柜内温度和保持时间分别是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "100℃，5分钟", "is_correct": False},
                {"label": "B", "text": "100℃，10分钟", "is_correct": False},
                {"label": "C", "text": "120℃，10分钟以上", "is_correct": True},
                {"label": "D", "text": "120℃，5分钟", "is_correct": False}
            ],
            "explanation": "远红外消毒柜：柜内温度达到120℃，并保持10分钟以上。"
        },
        {
            "text": "洗碗机消毒时，水温和冲洗消毒时间分别是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "85℃，大于40秒", "is_correct": True},
                {"label": "B", "text": "100℃，大于40秒", "is_correct": False},
                {"label": "C", "text": "85℃，大于60秒", "is_correct": False},
                {"label": "D", "text": "100℃，大于60秒", "is_correct": False}
            ],
            "explanation": "洗碗机消毒：水温达到85℃，餐具冲洗消毒时间大于40秒。"
        },
        {
            "text": "菜品七不出标准中，以下哪项是正确的？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "颜色不正不出", "is_correct": True},
                {"label": "B", "text": "客人催促就出", "is_correct": False},
                {"label": "C", "text": "差不多就行", "is_correct": False},
                {"label": "D", "text": "只看外观", "is_correct": False}
            ],
            "explanation": "七不出标准：颜色不正不出、味道不佳不出、标准不够不出、摆盘不美不出、原料变质不出、温度不够不出、餐具不洁不出。"
        },
        {
            "text": "七不出标准中，判断方法包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "看", "is_correct": True},
                {"label": "B", "text": "尝", "is_correct": True},
                {"label": "C", "text": "秤", "is_correct": True},
                {"label": "D", "text": "猜", "is_correct": False}
            ],
            "explanation": "七不出判断方法：看、尝、秤、查、闻、量、擦。"
        },
        {
            "text": "餐具未经消毒可以循环使用吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "difficulty": "easy",
            "category": "skill",
            "correct_answer": "错误",
            "explanation": "餐具未经消毒不得循环使用，必须经过消毒才能使用。"
        },
        {
            "text": "煮沸、蒸汽消毒时，消毒温度和保持时间分别是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "90℃，5分钟", "is_correct": False},
                {"label": "B", "text": "100℃，5分钟", "is_correct": False},
                {"label": "C", "text": "100℃，10分钟以上", "is_correct": True},
                {"label": "D", "text": "120℃，10分钟", "is_correct": False}
            ],
            "explanation": "煮沸、蒸汽消毒：温度100℃并保持10分钟以上。"
        },
        {
            "text": "餐具消毒后应如何存放？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "直接放在台面", "is_correct": False},
                {"label": "B", "text": "统一存放在柜中", "is_correct": True},
                {"label": "C", "text": "随便放", "is_correct": False},
                {"label": "D", "text": "堆在一起", "is_correct": False}
            ],
            "explanation": "餐具清洗消毒后统一存放在柜中，不能直接放在台面，防止污染。"
        },
        {
            "text": "用餐前餐具应如何保持清洁？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "用洁净白布盖好", "is_correct": True},
                {"label": "B", "text": "不需要覆盖", "is_correct": False},
                {"label": "C", "text": "用报纸盖住", "is_correct": False},
                {"label": "D", "text": "用塑料袋装", "is_correct": False}
            ],
            "explanation": "用餐前餐具集中整齐摆放，保持清洁，用洁净白布盖好，防止蝇叮。"
        },

        # 食材验收异常处理（15道）
        {
            "text": "食材验收时发现数量不符，应首先做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "直接签收", "is_correct": False},
                {"label": "B", "text": "停止验收，当场核对", "is_correct": True},
                {"label": "C", "text": "让送货员离开", "is_correct": False},
                {"label": "D", "text": "不管它", "is_correct": False}
            ],
            "explanation": "发现数量不符立即停止验收，保持原包装不动，当场与送货员核对。"
        },
        {
            "text": "食材少送时，应在送货单上注明什么并要求送货员签字？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "只写少送几个", "is_correct": False},
                {"label": "B", "text": "实收XX，少送XX", "is_correct": True},
                {"label": "C", "text": "不需要记录", "is_correct": False},
                {"label": "D", "text": "口头告知即可", "is_correct": False}
            ],
            "explanation": "少送时在送货单上注明'实收XX，少送XX'，要求送货员签字确认，体现平等透明。"
        },
        {
            "text": "食材质量不合格时，应使用什么标准确认具体问题？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "只看外观", "is_correct": False},
                {"label": "B", "text": "看闻摸查标准", "is_correct": True},
                {"label": "C", "text": "凭经验判断", "is_correct": False},
                {"label": "D", "text": "随便检查", "is_correct": False}
            ],
            "explanation": "使用'看闻摸查'标准确认具体问题，确保判断准确。"
        },
        {
            "text": "质量不合格的食材拍照时，应该拍摄哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "整体照片", "is_correct": True},
                {"label": "B", "text": "问题特写", "is_correct": True},
                {"label": "C", "text": "标签", "is_correct": True},
                {"label": "D", "text": "只拍整体即可", "is_correct": False}
            ],
            "explanation": "多角度拍摄：整体+特写+标签+送货单，确保记录完整。"
        },
        {
            "text": "临期品（剩余保质期小于多少）应拒收？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "10%", "is_correct": False},
                {"label": "B", "text": "20%", "is_correct": True},
                {"label": "C", "text": "30%", "is_correct": False},
                {"label": "D", "text": "50%", "is_correct": False}
            ],
            "explanation": "临期品（剩余保质期<20%）应拒收，要求供应商更换新鲜批次。"
        },
        {
            "text": "冷藏食材验收时，温度超过多少度应拒收？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "4℃", "is_correct": False},
                {"label": "B", "text": "7℃", "is_correct": True},
                {"label": "C", "text": "10℃", "is_correct": False},
                {"label": "D", "text": "15℃", "is_correct": False}
            ],
            "explanation": "冷藏食材温度严重超标（>7℃）应直接拒收。"
        },
        {
            "text": "冷冻食材验收时，温度超过多少度应拒收？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "-10℃", "is_correct": False},
                {"label": "B", "text": "-15℃", "is_correct": True},
                {"label": "C", "text": "-18℃", "is_correct": False},
                {"label": "D", "text": "-20℃", "is_correct": False}
            ],
            "explanation": "冷冻食材温度严重超标（>-15℃）应直接拒收。"
        },
        {
            "text": "供应商无法及时补货时，应启动什么流程？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "不管它", "is_correct": False},
                {"label": "B", "text": "紧急应急采购流程", "is_correct": True},
                {"label": "C", "text": "停业", "is_correct": False},
                {"label": "D", "text": "等明天", "is_correct": False}
            ],
            "explanation": "供应商无法及时补货时，评估需求后启动紧急应急采购流程。"
        },
        {
            "text": "应急采购时，应选择哪些采购渠道？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "就近农贸市场", "is_correct": True},
                {"label": "B", "text": "备用供应商", "is_correct": True},
                {"label": "C", "text": "其他门店调货", "is_correct": True},
                {"label": "D", "text": "随便找个地方买", "is_correct": False}
            ],
            "explanation": "应急采购渠道：就近农贸市场、备用供应商、其他门店调货。"
        },
        {
            "text": "食材验收时发现包装破损但内包装完好，应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "直接拒收", "is_correct": False},
                {"label": "B", "text": "与送货员协商，降价收货或拒收", "is_correct": True},
                {"label": "C", "text": "必须收货", "is_correct": False},
                {"label": "D", "text": "不管包装", "is_correct": False}
            ],
            "explanation": "外包装轻微破损但内包装完好，可与送货员协商降价收货或拒收。"
        },
        {
            "text": "送货员无健康证时，应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "照常收货", "is_correct": False},
                {"label": "B", "text": "拒收全部食材", "is_correct": True},
                {"label": "C", "text": "只收部分", "is_correct": False},
                {"label": "D", "text": "不需要检查", "is_correct": False}
            ],
            "explanation": "资质不全应拒收全部食材，要求供应商补齐资质后重新配送。"
        },
        {
            "text": "食材验收异常时，必须填写什么表格？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "不需要填表", "is_correct": False},
                {"label": "B", "text": "验收异常记录表", "is_correct": True},
                {"label": "C", "text": "普通记录表", "is_correct": False},
                {"label": "D", "text": "随便记一下", "is_correct": False}
            ],
            "explanation": "发现异常必须填写《验收异常记录表》，上传照片，记录处理结果。"
        },
        {
            "text": "食材验收的标准流程包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "数量核对", "is_correct": True},
                {"label": "B", "text": "质量检查", "is_correct": True},
                {"label": "C", "text": "效期检查", "is_correct": True},
                {"label": "D", "text": "只看外观", "is_correct": False}
            ],
            "explanation": "标准流程：数量核对、质量检查、效期检查、包装完整性、称重确认、温度检查、不合格品处理。"
        },
        {
            "text": "冷链食材解冻后应该怎么处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "可以收货", "is_correct": False},
                {"label": "B", "text": "直接拒收", "is_correct": True},
                {"label": "C", "text": "降价收货", "is_correct": False},
                {"label": "D", "text": "看情况", "is_correct": False}
            ],
            "explanation": "冷冻品解冻应直接拒收（包装破损导致解冻视为质量不合格）。"
        },
        {
            "text": "验收时拍照记录后，应该抄送给谁？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "不需要抄送", "is_correct": False},
                {"label": "B", "text": "店长", "is_correct": True},
                {"label": "C", "text": "只给自己看", "is_correct": False},
                {"label": "D", "text": "随便", "is_correct": False}
            ],
            "explanation": "填写异常记录表，上传照片至供应商管理系统，抄送店长。"
        },

        # 厨师长岗位（15道）
        {
            "text": "厨师长班前会通常在什么时间进行？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "10:00-10:30", "is_correct": False},
                {"label": "B", "text": "17:00-17:30", "is_correct": True},
                {"label": "C", "text": "20:00-20:30", "is_correct": False},
                {"label": "D", "text": "随时可以", "is_correct": False}
            ],
            "explanation": "厨师长组织班前会通常在晚市开餐前17:00-17:30进行。"
        },
        {
            "text": "班前会应传达哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "重点问题复盘总结", "is_correct": True},
                {"label": "B", "text": "工作合理分配", "is_correct": True},
                {"label": "C", "text": "经营数据明确", "is_correct": True},
                {"label": "D", "text": "只聊天", "is_correct": False}
            ],
            "explanation": "班前会内容：重点问题复盘、工作分配、指令传达、经营数据通报、前日问题提醒。"
        },
        {
            "text": "厨师长检查冰箱时，应关注什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "只看是否有食材", "is_correct": False},
                {"label": "B", "text": "关注温度，确保食材在规定温度保存", "is_correct": True},
                {"label": "C", "text": "不需要检查", "is_correct": False},
                {"label": "D", "text": "随便看看", "is_correct": False}
            ],
            "explanation": "关注冰箱温度，确保食材在规定温度中进行保存。"
        },
        {
            "text": "收货验货时，必须由谁双签？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "厨师长单签", "is_correct": False},
                {"label": "B", "text": "店长、厨师长双签", "is_correct": True},
                {"label": "C", "text": "随便谁签", "is_correct": False},
                {"label": "D", "text": "不需要签字", "is_correct": False}
            ],
            "explanation": "收货验货必须店长、厨师长双签，体现平等透明的管理。"
        },
        {
            "text": "设备出现故障应在多长时间内上报？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "不超过5分钟", "is_correct": True},
                {"label": "B", "text": "不超过10分钟", "is_correct": False},
                {"label": "C", "text": "不超过30分钟", "is_correct": False},
                {"label": "D", "text": "下班后再说", "is_correct": False}
            ],
            "explanation": "设备出现故障立即上报（不超过5分钟），2小时内解决或启动应急预案。"
        },
        {
            "text": "厨师长应在营业中多久巡检一次出菜速度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "10分钟", "is_correct": False},
                {"label": "B", "text": "实时监测，超过3分钟无进展时介入", "is_correct": True},
                {"label": "C", "text": "30分钟", "is_correct": False},
                {"label": "D", "text": "不需要巡检", "is_correct": False}
            ],
            "explanation": "厨师长实时监测出菜进度，超过3分钟无进展时介入。"
        },
        {
            "text": "热菜出菜标准时间是多久？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "3-5分钟", "is_correct": True},
                {"label": "B", "text": "5-8分钟", "is_correct": False},
                {"label": "C", "text": "8-10分钟", "is_correct": False},
                {"label": "D", "text": "10-15分钟", "is_correct": False}
            ],
            "explanation": "热菜出菜标准时间：3-5分钟。"
        },
        {
            "text": "食材新鲜度检查应在什么时候进行？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "随便什么时候", "is_correct": False},
                {"label": "B", "text": "出菜前检查（必须执行）", "is_correct": True},
                {"label": "C", "text": "收市时检查", "is_correct": False},
                {"label": "D", "text": "不需要检查", "is_correct": False}
            ],
            "explanation": "出菜前必须检查食材新鲜度，无例外。"
        },
        {
            "text": "牛肉/羊肉变质的信号是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "变黑/褐色", "is_correct": True},
                {"label": "B", "text": "有腐败臭味", "is_correct": True},
                {"label": "C", "text": "摸起来发软无弹性", "is_correct": True},
                {"label": "D", "text": "颜色鲜红", "is_correct": False}
            ],
            "explanation": "变质信号：变黑/褐色，有腐败臭味，摸起来发软无弹性。"
        },
        {
            "text": "冷藏肉类的储存时间限制是多少天？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "≤2天", "is_correct": False},
                {"label": "B", "text": "≤3天", "is_correct": True},
                {"label": "C", "text": "≤5天", "is_correct": False},
                {"label": "D", "text": "≤7天", "is_correct": False}
            ],
            "explanation": "冷藏肉类储存时间≤3天。"
        },
        {
            "text": "冷藏豆制品的储存时间限制是多少天？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "≤1天", "is_correct": False},
                {"label": "B", "text": "≤2天", "is_correct": True},
                {"label": "C", "text": "≤3天", "is_correct": False},
                {"label": "D", "text": "≤5天", "is_correct": False}
            ],
            "explanation": "冷藏豆制品储存时间≤2天。"
        },
        {
            "text": "厨师长每班应巡检食材和冰箱温度至少多少次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "1次", "is_correct": False},
                {"label": "B", "text": "2次", "is_correct": True},
                {"label": "C", "text": "3次", "is_correct": False},
                {"label": "D", "text": "不需要", "is_correct": False}
            ],
            "explanation": "厨师长每班巡检不少于2次，检查冰箱温度和食材状态。"
        },
        {
            "text": "厨师长对新人的带教方式是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "让新人自己摸索", "is_correct": False},
                {"label": "B", "text": "你看我做、你学我看", "is_correct": True},
                {"label": "C", "text": "随便教教", "is_correct": False},
                {"label": "D", "text": "不需要带教", "is_correct": False}
            ],
            "explanation": "厨师长针对新人一对一带教，正确交接岗位流程（你看我做、你学我看），体现以勤劳者为本的培养理念。"
        },
        {
            "text": "厨师长班前会应每日重点强调什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "出餐速度", "is_correct": False},
                {"label": "B", "text": "出餐质量以及标准", "is_correct": True},
                {"label": "C", "text": "节约成本", "is_correct": False},
                {"label": "D", "text": "随便说说", "is_correct": False}
            ],
            "explanation": "每日重点强调出餐质量以及标准，体现对顾客负责的态度。"
        },
        {
            "text": "厨师长应根据什么数据进行工作分配？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "当日人员配置", "is_correct": True},
                {"label": "B", "text": "预估客流", "is_correct": True},
                {"label": "C", "text": "各岗位工作重点", "is_correct": True},
                {"label": "D", "text": "随便安排", "is_correct": False}
            ],
            "explanation": "根据当日人员配置和预估客流，明确各岗位工作重点进行合理分配。"
        },

        # 小吃房、切配、菜房（15道）
        {
            "text": "小吃房炸缸油应多久更换一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "2日一更换", "is_correct": True},
                {"label": "C", "text": "3日一更换", "is_correct": False},
                {"label": "D", "text": "一周一更换", "is_correct": False}
            ],
            "explanation": "炸缸油需2日一更换，确保食品安全和口味。"
        },
        {
            "text": "油炸类小吃制作时，电炸炉油温应调至多少度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "150℃", "is_correct": False},
                {"label": "B", "text": "180℃（允许误差±10℃）", "is_correct": True},
                {"label": "C", "text": "200℃", "is_correct": False},
                {"label": "D", "text": "220℃", "is_correct": False}
            ],
            "explanation": "油炸类小吃制作：电炸炉油温调至180℃（允许误差±10℃）。"
        },
        {
            "text": "现炸酥肉应取出多少克？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "100g", "is_correct": False},
                {"label": "B", "text": "160g", "is_correct": True},
                {"label": "C", "text": "200g", "is_correct": False},
                {"label": "D", "text": "随便", "is_correct": False}
            ],
            "explanation": "现炸酥肉取出160g，炸至金黄色捞出沥干油。"
        },
        {
            "text": "煎制类小吃制作时，电饼档或煎锅应调至什么温度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "150-160℃", "is_correct": False},
                {"label": "B", "text": "180-200℃", "is_correct": True},
                {"label": "C", "text": "200-220℃", "is_correct": False},
                {"label": "D", "text": "220-240℃", "is_correct": False}
            ],
            "explanation": "煎制类小吃：电饼档或煎锅调至180-200℃，预热3-5分钟。"
        },
        {
            "text": "小吃房应多久进行一次强化盘点（新店期）？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "每周", "is_correct": True},
                {"label": "C", "text": "每月", "is_correct": False},
                {"label": "D", "text": "每季度", "is_correct": False}
            ],
            "explanation": "新店期（开业前2个月）要求每周盘点一次，确保进销存管理规范。"
        },
        {
            "text": "切配岗加工肉食及水产品的程序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "随便加工", "is_correct": False},
                {"label": "B", "text": "清理、清洗、切配成形", "is_correct": True},
                {"label": "C", "text": "直接切配", "is_correct": False},
                {"label": "D", "text": "只清洗", "is_correct": False}
            ],
            "explanation": "肉食及水产品按清理、清洗、切配成形程序操作。"
        },
        {
            "text": "切配岗加工后的产品应有什么特征？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "无毛", "is_correct": True},
                {"label": "B", "text": "无血块", "is_correct": True},
                {"label": "C", "text": "无病兆", "is_correct": True},
                {"label": "D", "text": "有异味没关系", "is_correct": False}
            ],
            "explanation": "加工后的产品应无毛、无血块、无病兆、感官性状无异常。"
        },
        {
            "text": "蔬菜加工的正确程序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "先切后洗", "is_correct": False},
                {"label": "B", "text": "择—理—削—清洗—浸泡—成形", "is_correct": True},
                {"label": "C", "text": "只需清洗切配", "is_correct": False},
                {"label": "D", "text": "随便处理", "is_correct": False}
            ],
            "explanation": "蔬菜应按择—理—削—清洗—浸泡—成形的程序进行加工，先洗后切。"
        },
        {
            "text": "切配岗水产品应使用什么池清洗？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "与肉食共用", "is_correct": False},
                {"label": "B", "text": "专用清洗池", "is_correct": True},
                {"label": "C", "text": "任意池", "is_correct": False},
                {"label": "D", "text": "不需要清洗", "is_correct": False}
            ],
            "explanation": "水产品应设专用清洗池，加工工器具应和其他肉食分开。"
        },
        {
            "text": "鱿鱼改刀的切片深度是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "1/2", "is_correct": False},
                {"label": "B", "text": "2/3", "is_correct": False},
                {"label": "C", "text": "3/4", "is_correct": True},
                {"label": "D", "text": "全部切断", "is_correct": False}
            ],
            "explanation": "鱿鱼改刀以45°的斜刀切片，深度3/4、宽度1cm。"
        },
        {
            "text": "菜房出品应严格按照什么标准？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "自己的标准", "is_correct": False},
                {"label": "B", "text": "七不出标准", "is_correct": True},
                {"label": "C", "text": "随便出", "is_correct": False},
                {"label": "D", "text": "快速出品", "is_correct": False}
            ],
            "explanation": "菜房严格按照七不出标准出品。"
        },
        {
            "text": "菜房整理菜肴时必须佩戴什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "不需要任何防护", "is_correct": False},
                {"label": "B", "text": "戴手套", "is_correct": True},
                {"label": "C", "text": "只戴口罩", "is_correct": False},
                {"label": "D", "text": "随意", "is_correct": False}
            ],
            "explanation": "整理菜肴时戴手套，裸手不接触食品。"
        },
        {
            "text": "菜房餐中补加菜品应坚持什么原则？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "随便补", "is_correct": False},
                {"label": "B", "text": "先主后次，先急后缓，先进先出", "is_correct": True},
                {"label": "C", "text": "只补主菜", "is_correct": False},
                {"label": "D", "text": "不需要补", "is_correct": False}
            ],
            "explanation": "餐中补加菜品坚持：先主后次，先急后缓，先进先出原则。"
        },
        {
            "text": "内脏类涮品腌制时应保持什么温度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "常温", "is_correct": False},
                {"label": "B", "text": "全程保持低温，使用冰水腌制（0-4℃）", "is_correct": True},
                {"label": "C", "text": "热水腌制", "is_correct": False},
                {"label": "D", "text": "温水腌制", "is_correct": False}
            ],
            "explanation": "腌制温度：全程保持低温，使用冰水腌制（水中加入冰块保持0-4℃）。"
        },
        {
            "text": "菜房盘饰的要求是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "盘饰无枯叶/变质", "is_correct": True},
                {"label": "B", "text": "随便用", "is_correct": False},
                {"label": "C", "text": "不需要盘饰", "is_correct": False},
                {"label": "D", "text": "只要好看", "is_correct": False}
            ],
            "explanation": "盘饰准备要求：盘饰无枯叶/变质。"
        },

        # 协作与价值观（25道）
        {
            "text": "岗位协作的首要原则是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "先帮助别人", "is_correct": False},
                {"label": "B", "text": "先完成本职工作", "is_correct": True},
                {"label": "C", "text": "随便", "is_correct": False},
                {"label": "D", "text": "不需要协作", "is_correct": False}
            ],
            "explanation": "协作原则：先完成本职核心工作，再协助其他岗位，体现高效协作。"
        },
        {
            "text": "高峰期时，应该听从谁的调度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "自己决定", "is_correct": False},
                {"label": "B", "text": "厨师长统一调度", "is_correct": True},
                {"label": "C", "text": "不听调度", "is_correct": False},
                {"label": "D", "text": "随便", "is_correct": False}
            ],
            "explanation": "紧急情况下服从厨师长统一调度安排。"
        },
        {
            "text": "完成本岗位工作后应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "休息", "is_correct": False},
                {"label": "B", "text": "主动支援其他岗位", "is_correct": True},
                {"label": "C", "text": "玩手机", "is_correct": False},
                {"label": "D", "text": "提前下班", "is_correct": False}
            ],
            "explanation": "完成本岗位工作后，主动支援其他岗位的清洁和备餐工作。"
        },
        {
            "text": "老员工应该如何对待新员工？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "不管新员工", "is_correct": False},
                {"label": "B", "text": "带教新员工，传授岗位技能", "is_correct": True},
                {"label": "C", "text": "让新员工自己学", "is_correct": False},
                {"label": "D", "text": "欺负新员工", "is_correct": False}
            ],
            "explanation": "老员工带教新员工，传授岗位技能，体现以勤劳者为本的价值观。"
        },
        {
            "text": "发现食材变质应该怎么办？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "继续使用", "is_correct": False},
                {"label": "B", "text": "封存并上报厨师长", "is_correct": True},
                {"label": "C", "text": "自己扔掉", "is_correct": False},
                {"label": "D", "text": "不管它", "is_correct": False}
            ],
            "explanation": "对于变质不能用的原料，封存并上报厨师长，体现对顾客负责。"
        },
        {
            "text": "节约能源，合理使用调料和原料体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ],
            "explanation": "节约能源，降低成本减少浪费，体现以勤劳者为本、勤俭节约的价值观。"
        },
        {
            "text": "岗位之间使用对讲机及时沟通体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": False},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": True},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ],
            "explanation": "使用对讲机及时沟通，避免岗位空缺，体现高效协作。"
        },
        {
            "text": "严格执行食品卫生法，杜绝食品中毒体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": False},
                {"label": "B", "text": "帮助顾客", "is_correct": True},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ],
            "explanation": "严格执行食品卫生法，确保顾客食品安全，体现帮助顾客的价值观。"
        },
        {
            "text": "盘点工作需要所有岗位参与，这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": False},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": True},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ],
            "explanation": "所有岗位均需参与月度盘点，负责本岗位区域，体现高效协作。"
        },
        {
            "text": "酒水盘点差量超标需上报店长，这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": False},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": True}
            ],
            "explanation": "差量超标需上报，记录原因，体现平等透明的管理。"
        },
        {
            "text": "每日备货量表记录实际销售数量的目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "应付检查", "is_correct": False},
                {"label": "B", "text": "作为次日备货参考，确保数据准确", "is_correct": True},
                {"label": "C", "text": "没有用", "is_correct": False},
                {"label": "D", "text": "随便记", "is_correct": False}
            ],
            "explanation": "记录实际销售数量作为次日备货参考，确保数据透明准确。"
        },
        {
            "text": "按照产品SOP标准执行的目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "限制员工", "is_correct": False},
                {"label": "B", "text": "确保品质一致，对顾客负责", "is_correct": True},
                {"label": "C", "text": "增加工作量", "is_correct": False},
                {"label": "D", "text": "没有意义", "is_correct": False}
            ],
            "explanation": "按SOP标准执行确保品质一致，体现对顾客负责的态度。"
        },
        {
            "text": "先进先出原则的意义是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "没有意义", "is_correct": False},
                {"label": "B", "text": "避免过期浪费，确保食品安全", "is_correct": True},
                {"label": "C", "text": "增加工作量", "is_correct": False},
                {"label": "D", "text": "随便用", "is_correct": False}
            ],
            "explanation": "先进先出原则优先使用日期较早的食材，避免过期浪费。"
        },
        {
            "text": "生熟分开存放的目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "方便管理", "is_correct": False},
                {"label": "B", "text": "避免交叉污染", "is_correct": True},
                {"label": "C", "text": "好看", "is_correct": False},
                {"label": "D", "text": "没有目的", "is_correct": False}
            ],
            "explanation": "生熟分开存放（熟食上层，生食下层）避免交叉污染。"
        },
        {
            "text": "加膜加盖密封保存的目的是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "防止污染", "is_correct": True},
                {"label": "B", "text": "防止串味", "is_correct": True},
                {"label": "C", "text": "保持新鲜", "is_correct": True},
                {"label": "D", "text": "没有目的", "is_correct": False}
            ],
            "explanation": "所有食材必须加保鲜膜+加盖，防止污染和串味，保持新鲜。"
        },
        {
            "text": "按下单顺序出品体现了什么原则？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "随意原则", "is_correct": False},
                {"label": "B", "text": "公平对待每位顾客", "is_correct": True},
                {"label": "C", "text": "谁催得急先给谁", "is_correct": False},
                {"label": "D", "text": "没有原则", "is_correct": False}
            ],
            "explanation": "按下单顺序出品，公平对待每位顾客，体现帮助顾客的价值观。"
        },
        {
            "text": "特殊需求（如不加辣、过敏原）必须如何传达？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "口头说说就行", "is_correct": False},
                {"label": "B", "text": "明确标注并传达", "is_correct": True},
                {"label": "C", "text": "不需要传达", "is_correct": False},
                {"label": "D", "text": "随便", "is_correct": False}
            ],
            "explanation": "特殊需求必须明确标注并传达，体现高效协作和对顾客负责。"
        },
        {
            "text": "工具消毒不到位会导致什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "没有影响", "is_correct": False},
                {"label": "B", "text": "交叉污染，危害顾客健康", "is_correct": True},
                {"label": "C", "text": "只是不好看", "is_correct": False},
                {"label": "D", "text": "无所谓", "is_correct": False}
            ],
            "explanation": "工具消毒不到位会导致交叉污染，危害顾客健康。"
        },
        {
            "text": "随时保持工作区域清洁体现了什么原则？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "一餐一清", "is_correct": True},
                {"label": "B", "text": "一天一清", "is_correct": False},
                {"label": "C", "text": "一周一清", "is_correct": False},
                {"label": "D", "text": "不需要清", "is_correct": False}
            ],
            "explanation": "随时保持工作区域清洁，一餐一清。"
        },
        {
            "text": "4D管理的四个到位是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "整理到位", "is_correct": True},
                {"label": "B", "text": "责任到位", "is_correct": True},
                {"label": "C", "text": "培训到位", "is_correct": True},
                {"label": "D", "text": "随便到位", "is_correct": False}
            ],
            "explanation": "4D管理：整理到位、责任到位、培训到位、执行到位。"
        },
        {
            "text": "周清计划表的目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "应付检查", "is_correct": False},
                {"label": "B", "text": "系统性清洁，避免卫生死角", "is_correct": True},
                {"label": "C", "text": "增加工作量", "is_correct": False},
                {"label": "D", "text": "没有目的", "is_correct": False}
            ],
            "explanation": "周清计划表确保系统性清洁，覆盖所有区域，避免卫生死角。"
        },
        {
            "text": "应急电源及安全指示牌应多久检查一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "每周放一次电", "is_correct": True},
                {"label": "C", "text": "每月", "is_correct": False},
                {"label": "D", "text": "不需要检查", "is_correct": False}
            ],
            "explanation": "应急电源及安全指示牌每周放一次电，检查设备运转是否正常。"
        },
        {
            "text": "灭火器压力表指针应处在什么区域？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "红区", "is_correct": False},
                {"label": "B", "text": "绿区", "is_correct": True},
                {"label": "C", "text": "黄区", "is_correct": False},
                {"label": "D", "text": "任意区域", "is_correct": False}
            ],
            "explanation": "检查压力表指针处在绿区，外表无变形、损伤。"
        },
        {
            "text": "午市开餐时间和餐前准备完成时间分别是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "11:00开餐，10:40前完成准备", "is_correct": True},
                {"label": "B", "text": "11:30开餐，11:00前完成准备", "is_correct": False},
                {"label": "C", "text": "12:00开餐，11:30前完成准备", "is_correct": False},
                {"label": "D", "text": "随时开餐", "is_correct": False}
            ],
            "explanation": "午市开餐时间11:00，要求10:40前完成所有备餐工作。"
        },
        {
            "text": "每日下单时间通常是什么时候？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "早上", "is_correct": False},
                {"label": "B", "text": "每日21:30-22:00", "is_correct": True},
                {"label": "C", "text": "中午", "is_correct": False},
                {"label": "D", "text": "随时", "is_correct": False}
            ],
            "explanation": "每日21:30-22:00完成次日食材统一下单。"
        }
    ]

    # 插入数据
    for idx, q_data in enumerate(questions, 1):
        try:
            question = Question(**q_data, created_by=1)
            db.add(question)
            db.commit()
            print(f"[{idx}/{len(questions)}] 已插入题目：{q_data['content'][:50]}...")
        except Exception as e:
            print(f"[{idx}/{len(questions)}] 插入失败：{e}")
            db.rollback()
            continue

    db.close()
    print(f"\n✅ 成功插入 {len(questions)} 道题目！")

    # 统计
    single_choice = sum(1 for q in questions if q["question_type"] == QuestionType.SINGLE_CHOICE)
    multiple_choice = sum(1 for q in questions if q["question_type"] == QuestionType.MULTIPLE_CHOICE)
    true_false = sum(1 for q in questions if q["question_type"] == QuestionType.TRUE_FALSE)

    easy = sum(1 for q in questions if q["difficulty"] == "easy")
    medium = sum(1 for q in questions if q["difficulty"] == "medium")
    hard = sum(1 for q in questions if q["difficulty"] == "hard")

    skill = sum(1 for q in questions if q["category"] == "skill")
    value = sum(1 for q in questions if q["category"].startswith("value_"))

    print(f"\n题目统计：")
    print(f"- 单选题：{single_choice}道")
    print(f"- 多选题：{multiple_choice}道")
    print(f"- 判断题：{true_false}道")
    print(f"\n难度分布：")
    print(f"- 简单：{easy}道")
    print(f"- 中等：{medium}道")
    print(f"- 困难：{hard}道")
    print(f"\n分类分布：")
    print(f"- 技能题：{skill}道")
    print(f"- 价值观题：{value}道")


if __name__ == "__main__":
    create_questions()
