"""
前厅题库生成脚本 - 第二批（100道题）
覆盖：收银、迎宾、水吧、传菜、保洁、店长主管深入内容
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

    questions = [
        # ========== 收银岗位（30道）==========

        # 收银系统操作（8道）
        {
            "text": "收银系统的13项基础操作中，不包括以下哪项？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "登录、开台、点菜", "is_correct": False},
                {"label": "B", "text": "转台、并台、结算", "is_correct": False},
                {"label": "C", "text": "会员充值管理", "is_correct": True},
                {"label": "D", "text": "估清/限量设置", "is_correct": False}
            ],
            "explanation": "13项基础操作包括：登录、开台、点菜、退菜/赠菜、转台/转菜、并台、结算、验券、扫码支付、优惠、反结算、估清/限量、报表，不包括会员充值管理。"
        },
        {
            "text": "开具发票时应严格按照什么金额开具？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "账单原价金额", "is_correct": False},
                {"label": "B", "text": "实付金额", "is_correct": True},
                {"label": "C", "text": "客人要求的任意金额", "is_correct": False},
                {"label": "D", "text": "优惠前金额", "is_correct": False}
            ],
            "explanation": "按实付金额开具发票，严禁多开或代开发票。"
        },
        {
            "text": "发票库存剩余多少时需要报备申购？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "少于500元", "is_correct": False},
                {"label": "B", "text": "少于1万元", "is_correct": True},
                {"label": "C", "text": "少于5万元", "is_correct": False},
                {"label": "D", "text": "完全用完后", "is_correct": False}
            ],
            "explanation": "发票库存剩余少于1万元时需报备申购，确保不断货。"
        },
        {
            "text": "收银日报和优免明细表应发送到哪些群？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "汇总群", "is_correct": True},
                {"label": "B", "text": "收银群", "is_correct": True},
                {"label": "C", "text": "员工群", "is_correct": False},
                {"label": "D", "text": "管理群", "is_correct": False}
            ],
            "explanation": "收银日报和优免明细表应发送到汇总群和收银群。"
        },
        {
            "text": "闭店时，营业现金应如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "直接带回家保管", "is_correct": False},
                {"label": "B", "text": "放入保险柜并锁好", "is_correct": True},
                {"label": "C", "text": "交给店长带走", "is_correct": False},
                {"label": "D", "text": "放在收银台抽屉", "is_correct": False}
            ],
            "explanation": "晚班下班前清点营业现金和备用现金，营业现金放入保险柜，锁好保险柜，钥匙放到指定位置。每周一由店长存入指定银行账户。"
        },
        {
            "text": "观察点菜情况时，发现什么异常应及时沟通？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "菜品重复", "is_correct": True},
                {"label": "B", "text": "锅底重复", "is_correct": True},
                {"label": "C", "text": "连台情况", "is_correct": True},
                {"label": "D", "text": "客人聊天", "is_correct": False}
            ],
            "explanation": "发现菜品/锅底重复、连台等异常情况应及时沟通，避免出错。"
        },
        {
            "text": "收银员在低峰期应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_collaboration",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "玩手机休息", "is_correct": False},
                {"label": "B", "text": "协助前厅其他岗位", "is_correct": True},
                {"label": "C", "text": "站在收银台等客人", "is_correct": False},
                {"label": "D", "text": "提前下班", "is_correct": False}
            ],
            "explanation": "低峰期协助前厅其他岗位体现高效协作的价值观。"
        },
        {
            "text": "收银员负责客用茶水准备工作吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "收银员负责准备前厅的客用茶水。"
        },

        # 预定管理（8道）
        {
            "text": "接听电话预定时，应在响铃几声内接听？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "1声", "is_correct": False},
                {"label": "B", "text": "3声", "is_correct": True},
                {"label": "C", "text": "5声", "is_correct": False},
                {"label": "D", "text": "10声", "is_correct": False}
            ],
            "explanation": "电话预定标准流程要求响铃3声内接听。"
        },
        {
            "text": "电话预定时的自报门店话术是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "喂，你好", "is_correct": False},
                {"label": "B", "text": "您好，XX餐厅，很高兴为您服务，请问有什么可以帮到您？", "is_correct": True},
                {"label": "C", "text": "您好，请问预定吗？", "is_correct": False},
                {"label": "D", "text": "XX餐厅，你好", "is_correct": False}
            ],
            "explanation": "自报门店话术：您好，XX餐厅，很高兴为您服务，请问有什么可以帮到您？"
        },
        {
            "text": "电话预定流程中，以下哪个步骤的顺序是正确的？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "记录手机号→确认预定信息→安排座位", "is_correct": False},
                {"label": "B", "text": "确认预定信息→安排座位→核实信息→记录手机号", "is_correct": True},
                {"label": "C", "text": "安排座位→记录手机号→确认预定信息", "is_correct": False},
                {"label": "D", "text": "核实信息→确认预定信息→记录手机号", "is_correct": False}
            ],
            "explanation": "正确流程：自报门店→确认预定信息（称呼、人数、时间）→安排座位并告知→确认特殊要求→核实信息→记录手机号→礼貌致谢→顾客先挂断→登记并同步。"
        },
        {
            "text": "微信预定应在多长时间内回复？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "5分钟", "is_correct": False},
                {"label": "B", "text": "10分钟", "is_correct": True},
                {"label": "C", "text": "30分钟", "is_correct": False},
                {"label": "D", "text": "1小时", "is_correct": False}
            ],
            "explanation": "微信预定标准流程要求10分钟内回复。"
        },
        {
            "text": "微信预定到店前多久应提醒确认？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "10分钟", "is_correct": False},
                {"label": "B", "text": "30分钟", "is_correct": False},
                {"label": "C", "text": "1小时", "is_correct": True},
                {"label": "D", "text": "2小时", "is_correct": False}
            ],
            "explanation": "到店前1小时提醒确认，体现对顾客的关怀和细致服务。"
        },
        {
            "text": "折扣/免单预定时，必须由谁签字确认？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "收银员", "is_correct": False},
                {"label": "B", "text": "店长", "is_correct": True},
                {"label": "C", "text": "主管", "is_correct": False},
                {"label": "D", "text": "任意管理人员", "is_correct": False}
            ],
            "explanation": "折扣/免单预定需确认折扣/免单权限来源，必须由店长签字确认，体现平等透明的管理原则。"
        },
        {
            "text": "预定登记后，应该如何同步信息给门店人员？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_collaboration",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "通过系统通知", "is_correct": True},
                {"label": "B", "text": "通过微信群通知", "is_correct": True},
                {"label": "C", "text": "口头告知部分员工", "is_correct": False},
                {"label": "D", "text": "不需要同步", "is_correct": False}
            ],
            "explanation": "预定登记后应通过系统或微信群通知门店人员，确保信息及时传达，体现高效协作。"
        },
        {
            "text": "电话预定时，应该等待顾客先挂断电话再挂断。",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "value_customer",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "电话预定标准流程中明确要求顾客先挂断电话，体现对顾客的尊重。"
        },

        # 顾客寄存和买单服务（6道）
        {
            "text": "顾客酒水寄存时，需要填写哪些信息？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "姓名", "is_correct": True},
                {"label": "B", "text": "日期", "is_correct": True},
                {"label": "C", "text": "品名和数量", "is_correct": True},
                {"label": "D", "text": "身份证号", "is_correct": False}
            ],
            "explanation": "酒水寄存需填写存酒卡，包括姓名、日期、品名、数量，并单独标识存放。"
        },
        {
            "text": "顾客寄存生日蛋糕时，应该询问什么信息？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "桌号", "is_correct": True},
                {"label": "B", "text": "顾客姓名和电话", "is_correct": True},
                {"label": "C", "text": "存放冷藏或冷冻", "is_correct": True},
                {"label": "D", "text": "蛋糕价格", "is_correct": False}
            ],
            "explanation": "生日蛋糕寄存需注明桌号、顾客姓名、电话，询问存放冷藏或冷冻，做好记录。"
        },
        {
            "text": "买单服务的标准话术中，应引导客人使用什么支付方式？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "现金支付", "is_correct": False},
                {"label": "B", "text": "扫码支付", "is_correct": True},
                {"label": "C", "text": "刷卡支付", "is_correct": False},
                {"label": "D", "text": "挂账", "is_correct": False}
            ],
            "explanation": "买单话术：直接扫码输入金额就可以买单了，会自动使用优惠券。"
        },
        {
            "text": "买单时的标准服务流程顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "打印清单→核对→询问开票→引导支付→送客", "is_correct": True},
                {"label": "B", "text": "引导支付→打印清单→核对→询问开票→送客", "is_correct": False},
                {"label": "C", "text": "核对→打印清单→引导支付→询问开票→送客", "is_correct": False},
                {"label": "D", "text": "打印清单→引导支付→核对→询问开票→送客", "is_correct": False}
            ],
            "explanation": "正确流程：1.打印消费清单并与客人核对 2.引导扫码支付，告知自动使用优惠 3.询问是否需要开票 4.礼貌送客。"
        },
        {
            "text": "买单时提供的增值服务包括什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "衣物除味喷雾", "is_correct": True},
                {"label": "B", "text": "免费洗车", "is_correct": False},
                {"label": "C", "text": "代客泊车", "is_correct": False},
                {"label": "D", "text": "免费打包", "is_correct": False}
            ],
            "explanation": "买单话术中提到：这里有衣物除味的喷雾可以使用。"
        },
        {
            "text": "顾客行李寄存时，取行李时应该核对什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "姓名和手机号", "is_correct": True},
                {"label": "B", "text": "身份证", "is_correct": False},
                {"label": "C", "text": "消费金额", "is_correct": False},
                {"label": "D", "text": "预定信息", "is_correct": False}
            ],
            "explanation": "行李寄存时填写存放单（姓名、手机号），取行李时核对这些信息。"
        },

        # 收银财务管理（8道）
        {
            "text": "账单分类整理时，哪些类型的单据需要单独分类存放？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "折扣单", "is_correct": True},
                {"label": "B", "text": "免单", "is_correct": True},
                {"label": "C", "text": "挂账单", "is_correct": True},
                {"label": "D", "text": "普通消费单", "is_correct": False}
            ],
            "explanation": "折扣/免单/挂账/反结账单需单独分类存放，便于核查和管理，体现平等透明的财务管理。"
        },
        {
            "text": "核对折扣、免单、挂账等行为时，必须检查什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "客人身份", "is_correct": False},
                {"label": "B", "text": "收银小票签字流程", "is_correct": True},
                {"label": "C", "text": "客人满意度", "is_correct": False},
                {"label": "D", "text": "员工工龄", "is_correct": False}
            ],
            "explanation": "核对折扣、免单、挂账等行为的收银小票签字流程，确保审批流程规范透明。"
        },
        {
            "text": "收银日报表数据必须与什么保持一致？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "收银系统", "is_correct": True},
                {"label": "B", "text": "第三方平台实际核销情况", "is_correct": True},
                {"label": "C", "text": "店长估算", "is_correct": False},
                {"label": "D", "text": "历史平均数据", "is_correct": False}
            ],
            "explanation": "日报表数据必须与收银系统一致，各项第三方数据与第三方平台实际核销情况需一致。"
        },
        {
            "text": "后台导出反结算数据后，应与什么核对？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "收银系统数据", "is_correct": False},
                {"label": "B", "text": "门店存档反结算单", "is_correct": True},
                {"label": "C", "text": "店长记录", "is_correct": False},
                {"label": "D", "text": "第三方平台", "is_correct": False}
            ],
            "explanation": "后台导出反结算数据需与门店存档反结算单核对，确保数据准确。"
        },
        {
            "text": "收银员餐前准备时，需要根据什么信息设置估清菜品？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "昨天的销售情况", "is_correct": False},
                {"label": "B", "text": "厨房信息", "is_correct": True},
                {"label": "C", "text": "客人预定情况", "is_correct": False},
                {"label": "D", "text": "个人经验", "is_correct": False}
            ],
            "explanation": "根据厨房信息在系统中设置估清菜品，产品恢复后及时解除估清设置。"
        },
        {
            "text": "收银系统登录后，需要测试哪些设备？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "打印机（打印纸充足）", "is_correct": True},
                {"label": "B", "text": "验钞机", "is_correct": True},
                {"label": "C", "text": "点菜机", "is_correct": True},
                {"label": "D", "text": "电视机", "is_correct": False}
            ],
            "explanation": "系统准备包括：收银系统登录测试、打印机测试（打印纸充足）、验钞机测试、点菜机测试。"
        },
        {
            "text": "收银员应保持收银台整洁，这属于哪项岗位职责？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "收银岗位职责明确要求保持吧台整洁。"
        },
        {
            "text": "收银员需要熟悉线上线下优惠卡券使用规定吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "收银岗位职责要求熟悉线上线下优惠卡券使用规定。"
        },

        # ========== 迎宾岗位深入（20道）==========

        # 设备准备与等位区（6道）
        {
            "text": "取号机测试出票前，应确保什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "前一日已充电", "is_correct": True},
                {"label": "B", "text": "当天充电1小时", "is_correct": False},
                {"label": "C", "text": "连接电源线", "is_correct": False},
                {"label": "D", "text": "更换电池", "is_correct": False}
            ],
            "explanation": "取号机已于前一日充电，餐前测试出票功能。"
        },
        {
            "text": "对讲机应测试什么频道？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "频道8", "is_correct": False},
                {"label": "B", "text": "频道12", "is_correct": False},
                {"label": "C", "text": "频道16", "is_correct": True},
                {"label": "D", "text": "频道20", "is_correct": False}
            ],
            "explanation": "通讯设备测试要求对讲机已于前一日充电，测试频道16。"
        },
        {
            "text": "等位区小吃准备时，周末/节假日应增加多少倍？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "1倍", "is_correct": False},
                {"label": "B", "text": "1.5-2倍", "is_correct": True},
                {"label": "C", "text": "2-3倍", "is_correct": False},
                {"label": "D", "text": "3-4倍", "is_correct": False}
            ],
            "explanation": "小吃准备：3-5种小吃，按门店预估量准备，周末/节假日增加1.5-2倍。"
        },
        {
            "text": "夏季茶水准备应提供哪些选项？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "冰水", "is_correct": True},
                {"label": "B", "text": "常温水", "is_correct": True},
                {"label": "C", "text": "热水", "is_correct": False},
                {"label": "D", "text": "温水", "is_correct": False}
            ],
            "explanation": "茶水准备：夏季提供冰水和常温水，冬季提供热水和温水，体现对顾客的细致关怀。"
        },
        {
            "text": "等位区增值物品应包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "除味喷雾", "is_correct": True},
                {"label": "B", "text": "充电线", "is_correct": True},
                {"label": "C", "text": "WIFI密码卡", "is_correct": True},
                {"label": "D", "text": "免费饮料", "is_correct": False}
            ],
            "explanation": "增值物品包括：除味喷雾、充电线、WIFI密码卡，提升客户体验。"
        },
        {
            "text": "迎宾应站立在距门口多远的位置？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "1米", "is_correct": False},
                {"label": "B", "text": "2-3米", "is_correct": True},
                {"label": "C", "text": "5米", "is_correct": False},
                {"label": "D", "text": "门口正中间", "is_correct": False}
            ],
            "explanation": "迎客标准：站立位置距门口2-3米处，保持良好站姿。"
        },

        # 迎客服务标准（8道）
        {
            "text": "看到客人时，应主动上前几步迎接？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "1步", "is_correct": False},
                {"label": "B", "text": "2-3步", "is_correct": True},
                {"label": "C", "text": "5步", "is_correct": False},
                {"label": "D", "text": "原地不动", "is_correct": False}
            ],
            "explanation": "迎客姿态：看到客人时主动上前迎接（2-3步）。"
        },
        {
            "text": "迎客手势的正确做法是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "左手半举，手心向上，五指并拢", "is_correct": False},
                {"label": "B", "text": "右手半举，手心向上，五指并拢", "is_correct": True},
                {"label": "C", "text": "双手举起挥手", "is_correct": False},
                {"label": "D", "text": "双手交叉胸前", "is_correct": False}
            ],
            "explanation": "迎客手势：右手半举，手心向上，五指并拢，微笑并用挥手手势传递友善。"
        },
        {
            "text": "迎客话术的标准说法是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "你好，欢迎光临", "is_correct": False},
                {"label": "B", "text": "您好，欢迎光临XX餐厅", "is_correct": True},
                {"label": "C", "text": "欢迎欢迎", "is_correct": False},
                {"label": "D", "text": "请进请进", "is_correct": False}
            ],
            "explanation": "迎客话术：您好，欢迎光临XX餐厅。"
        },
        {
            "text": "客人到店后，应首先询问什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "是否有预定", "is_correct": False},
                {"label": "B", "text": "几位用餐", "is_correct": True},
                {"label": "C", "text": "想吃什么", "is_correct": False},
                {"label": "D", "text": "有什么忌口", "is_correct": False}
            ],
            "explanation": "询问人数：请问几位用餐呢？然后再根据人数和当前就餐情况判断安排。"
        },
        {
            "text": "有位可以直接入座时，应该说什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "自己找位置坐", "is_correct": False},
                {"label": "B", "text": "您好，这边请，我带您入座", "is_correct": True},
                {"label": "C", "text": "那边有空位", "is_correct": False},
                {"label": "D", "text": "随便坐", "is_correct": False}
            ],
            "explanation": "有位直接入座话术：您好，这边请，我带您入座。"
        },
        {
            "text": "需要等位时，正确的话术是？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "客人太多了，你们等会儿吧", "is_correct": False},
                {"label": "B", "text": "您好，现在客人比较多，需要稍等X分钟左右，我帮您取个号，您可以在等位区稍作休息", "is_correct": True},
                {"label": "C", "text": "人太多了，要等很久", "is_correct": False},
                {"label": "D", "text": "你们先等着，有位置叫你们", "is_correct": False}
            ],
            "explanation": "需要等位话术：您好，现在客人比较多，需要稍等X分钟左右，我帮您取个号，您可以在等位区稍作休息。"
        },
        {
            "text": "预定确认时，应核对哪些信息？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "姓氏", "is_correct": True},
                {"label": "B", "text": "人数", "is_correct": True},
                {"label": "C", "text": "预定时间", "is_correct": True},
                {"label": "D", "text": "客人职业", "is_correct": False}
            ],
            "explanation": "确认预定信息需核对：姓氏、人数、预定时间。"
        },
        {
            "text": "迎宾岗位应对路过客人主动进行店推，这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_diligence",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ],
            "explanation": "主动对路过客人进行店推，介绍门店特色和优惠活动，体现勤劳主动的工作态度。"
        },

        # 送客服务（6道）
        {
            "text": "送客时应提供哪些增值服务？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "薄荷糖", "is_correct": True},
                {"label": "B", "text": "雨衣", "is_correct": True},
                {"label": "C", "text": "橡皮筋", "is_correct": True},
                {"label": "D", "text": "免费打车", "is_correct": False}
            ],
            "explanation": "送客服务提供的增值物品包括：薄荷糖、雨衣、橡皮筋等，体现对顾客的细致关怀。"
        },
        {
            "text": "迎宾岗位负责维护哪些区域的环境卫生？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "门店门口", "is_correct": True},
                {"label": "B", "text": "等位区", "is_correct": True},
                {"label": "C", "text": "厨房", "is_correct": False},
                {"label": "D", "text": "洗手间", "is_correct": False}
            ],
            "explanation": "迎宾负责维护门店门口及等位区环境卫生，因为门口印象是客人对品牌的第一印象。"
        },
        {
            "text": "门店满座时，迎宾应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "告诉客人没位置了", "is_correct": False},
                {"label": "B", "text": "开始排队叫号，与服务组时刻保持沟通", "is_correct": True},
                {"label": "C", "text": "让客人自己找位置", "is_correct": False},
                {"label": "D", "text": "建议客人去其他餐厅", "is_correct": False}
            ],
            "explanation": "在餐厅满座时开始排队叫号，与服务组时刻保持沟通安排好等位客人排号叫号。"
        },
        {
            "text": "迎宾的服务目标是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "让顾客快速入座", "is_correct": False},
                {"label": "B", "text": "让顾客开心进店，满意离店", "is_correct": True},
                {"label": "C", "text": "完成排号任务", "is_correct": False},
                {"label": "D", "text": "维护门口秩序", "is_correct": False}
            ],
            "explanation": "迎宾的服务目标是让顾客开心进店，满意离店，使用标准话术用语，体现帮助顾客的价值观。"
        },
        {
            "text": "迎宾检查门口玻璃门窗有污渍时应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "等保洁来清理", "is_correct": False},
                {"label": "B", "text": "立即擦拭", "is_correct": True},
                {"label": "C", "text": "记录下来晚上再清理", "is_correct": False},
                {"label": "D", "text": "不管它", "is_correct": False}
            ],
            "explanation": "检查门口玻璃门窗是否干净，有污渍立即擦拭，确保门店第一印象良好。"
        },
        {
            "text": "迎宾应使用标准话术用语服务客人吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "迎宾岗位职责要求使用标准话术用语，确保服务专业规范。"
        },

        # ========== 水吧岗位深入（20道）==========

        # 产品制作标准（8道）
        {
            "text": "水吧制作热饮的温度标准是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "50-60℃", "is_correct": False},
                {"label": "B", "text": "60-70℃", "is_correct": True},
                {"label": "C", "text": "70-80℃", "is_correct": False},
                {"label": "D", "text": "80-90℃", "is_correct": False}
            ],
            "explanation": "温度标准：冷饮0-5℃，热饮60-70℃。"
        },
        {
            "text": "水吧制作冷饮的温度标准是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "0-5℃", "is_correct": True},
                {"label": "B", "text": "5-10℃", "is_correct": False},
                {"label": "C", "text": "10-15℃", "is_correct": False},
                {"label": "D", "text": "15-20℃", "is_correct": False}
            ],
            "explanation": "温度标准：冷饮0-5℃，热饮60-70℃。"
        },
        {
            "text": "产品制作时必须佩戴哪些防护用品？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "口罩", "is_correct": True},
                {"label": "B", "text": "发帽", "is_correct": True},
                {"label": "C", "text": "一次性手套", "is_correct": True},
                {"label": "D", "text": "护目镜", "is_correct": False}
            ],
            "explanation": "卫生操作要求佩戴口罩、发帽、一次性手套。"
        },
        {
            "text": "水吧产品制作应按什么顺序？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "按自己喜欢的顺序", "is_correct": False},
                {"label": "B", "text": "按出单顺序", "is_correct": True},
                {"label": "C", "text": "按制作难度", "is_correct": False},
                {"label": "D", "text": "按客人催促情况", "is_correct": False}
            ],
            "explanation": "出品标准要求按出单顺序制作。"
        },
        {
            "text": "水吧制作产品时，可以随意更改配方比例吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "按配方制作，不随意更改比例，确保产品质量稳定。"
        },
        {
            "text": "产品制作前必须检查哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "出品单对应放置", "is_correct": True},
                {"label": "B", "text": "看清特殊需求备注", "is_correct": True},
                {"label": "C", "text": "按配方规定分量", "is_correct": True},
                {"label": "D", "text": "客人是否催单", "is_correct": False}
            ],
            "explanation": "制作标准：出品单对应放置，看清特殊需求备注，按配方规定分量。"
        },
        {
            "text": "产品出品前应检查哪些品质要素？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "颜色", "is_correct": True},
                {"label": "B", "text": "口感", "is_correct": True},
                {"label": "C", "text": "温度", "is_correct": True},
                {"label": "D", "text": "价格", "is_correct": False}
            ],
            "explanation": "品质检查包括：颜色、口感、温度。"
        },
        {
            "text": "水吧岗位应严格按产品SOP出品，这体现了什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "对顾客负责，确保产品质量稳定", "is_correct": True},
                {"label": "B", "text": "增加工作难度", "is_correct": False},
                {"label": "C", "text": "限制员工创新", "is_correct": False},
                {"label": "D", "text": "降低工作效率", "is_correct": False}
            ],
            "explanation": "严格按SOP出品确保产品质量稳定，体现帮助顾客、对顾客负责的价值观。"
        },

        # 酒水管理（12道）
        {
            "text": "新店期（开业前2个月）酒水盘点频次是多久一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "每天", "is_correct": False},
                {"label": "B", "text": "每周", "is_correct": True},
                {"label": "C", "text": "每月", "is_correct": False},
                {"label": "D", "text": "每季度", "is_correct": False}
            ],
            "explanation": "新店期（开业前2个月）每周盘点一次，稳定期每月盘点一次。"
        },
        {
            "text": "门店稳定期酒水盘点频次是多久一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "每周", "is_correct": False},
                {"label": "B", "text": "每月", "is_correct": True},
                {"label": "C", "text": "每季度", "is_correct": False},
                {"label": "D", "text": "每半年", "is_correct": False}
            ],
            "explanation": "稳定期（门店稳定后）每月盘点一次。"
        },
        {
            "text": "酒水盘点的标准公式是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "进货量-售卖量=剩余", "is_correct": False},
                {"label": "B", "text": "进货量+前期库存-售卖量=剩余", "is_correct": True},
                {"label": "C", "text": "前期库存-售卖量+进货量=剩余", "is_correct": False},
                {"label": "D", "text": "进货量+售卖量-前期库存=剩余", "is_correct": False}
            ],
            "explanation": "酒水盘点公式：进货量+前期库存-售卖量=剩余。"
        },
        {
            "text": "周盘酒水差量超过多少瓶需上报店长？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "3瓶", "is_correct": False},
                {"label": "B", "text": "5瓶", "is_correct": True},
                {"label": "C", "text": "10瓶", "is_correct": False},
                {"label": "D", "text": "20瓶", "is_correct": False}
            ],
            "explanation": "差量超过标准需上报店长：周盘超过5瓶，月盘超过20瓶，体现平等透明的管理原则。"
        },
        {
            "text": "月盘酒水差量超过多少瓶需上报店长？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_transparency",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "5瓶", "is_correct": False},
                {"label": "B", "text": "10瓶", "is_correct": False},
                {"label": "C", "text": "20瓶", "is_correct": True},
                {"label": "D", "text": "30瓶", "is_correct": False}
            ],
            "explanation": "差量超过标准需上报店长：周盘超过5瓶，月盘超过20瓶。"
        },
        {
            "text": "酒水盘点时发现差量，应查找哪些原因？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "破损", "is_correct": True},
                {"label": "B", "text": "赠送", "is_correct": True},
                {"label": "C", "text": "私用", "is_correct": True},
                {"label": "D", "text": "天气原因", "is_correct": False}
            ],
            "explanation": "发现差量及时查找原因：破损、赠送、私用等。"
        },
        {
            "text": "酒水补货的原则是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "日均营业用量×3天", "is_correct": False},
                {"label": "B", "text": "日均营业用量×7天+20%安全库存", "is_correct": True},
                {"label": "C", "text": "日均营业用量×14天", "is_correct": False},
                {"label": "D", "text": "日均营业用量×30天", "is_correct": False}
            ],
            "explanation": "补货原则：保证日均营业用量×7天+20%安全库存。"
        },
        {
            "text": "酒水补货时应检查哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "生产日期", "is_correct": True},
                {"label": "B", "text": "保质期", "is_correct": True},
                {"label": "C", "text": "外包装完好性", "is_correct": True},
                {"label": "D", "text": "品牌知名度", "is_correct": False}
            ],
            "explanation": "补货时检查：生产日期、保质期、外包装完好性。"
        },
        {
            "text": "酒水陈列应遵循什么原则？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "先进后出", "is_correct": False},
                {"label": "B", "text": "先进先出", "is_correct": True},
                {"label": "C", "text": "随意摆放", "is_correct": False},
                {"label": "D", "text": "贵的在前", "is_correct": False}
            ],
            "explanation": "先进先出原则，近期到期产品前置。"
        },
        {
            "text": "酒水陈列时，logo应朝向哪里？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "向内", "is_correct": False},
                {"label": "B", "text": "向外", "is_correct": True},
                {"label": "C", "text": "向上", "is_correct": False},
                {"label": "D", "text": "向下", "is_correct": False}
            ],
            "explanation": "酒水陈列整齐，logo向外。"
        },
        {
            "text": "酒水应按什么方式摆放？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "随意摆放", "is_correct": False},
                {"label": "B", "text": "按品种分类摆放", "is_correct": True},
                {"label": "C", "text": "按价格高低摆放", "is_correct": False},
                {"label": "D", "text": "按颜色深浅摆放", "is_correct": False}
            ],
            "explanation": "按品种分类摆放，整齐规范。"
        },
        {
            "text": "酒水盘点应由水吧岗位负责吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "正确",
            "explanation": "酒水清点工作已调整至水吧岗位负责。"
        },

        # ========== 传菜保洁岗位（30道）==========

        # 传菜专员 - 十不出品（10道）
        {
            "text": "十不出品标准中，以下哪项是正确的？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "餐具破损不传", "is_correct": True},
                {"label": "B", "text": "客人催单就传", "is_correct": False},
                {"label": "C", "text": "厨房出品就传", "is_correct": False},
                {"label": "D", "text": "份量稍少也传", "is_correct": False}
            ],
            "explanation": "十不出品第1条：餐具破损不传。"
        },
        {
            "text": "以下哪些属于十不出品标准？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "盘饰不符不传", "is_correct": True},
                {"label": "B", "text": "菜品异味不传", "is_correct": True},
                {"label": "C", "text": "菜品异物不传", "is_correct": True},
                {"label": "D", "text": "客人不催不传", "is_correct": False}
            ],
            "explanation": "十不出品包括：盘饰不符、菜品异味、菜品异物等都不传。"
        },
        {
            "text": "摆盘不对的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第5条：摆盘不对不传。"
        },
        {
            "text": "份量不足的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第6条：份量不足不传。"
        },
        {
            "text": "菜单不在的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第7条：菜单不在不传。"
        },
        {
            "text": "颜色不对的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第8条：颜色不对不传。"
        },
        {
            "text": "菜品不符（与菜单描述不符）的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第9条：菜品不符不传。"
        },
        {
            "text": "台号不清的菜品可以传吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "十不出品第10条：台号不清不传。"
        },
        {
            "text": "执行十不出品标准体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_customer",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "帮助顾客，确保出品质量", "is_correct": True},
                {"label": "B", "text": "增加工作量", "is_correct": False},
                {"label": "C", "text": "为难厨房", "is_correct": False},
                {"label": "D", "text": "降低效率", "is_correct": False}
            ],
            "explanation": "十不出品标准确保菜品质量，体现帮助顾客、对顾客负责的价值观。"
        },
        {
            "text": "传菜员发现菜品不符合十不出品标准时应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "直接传给客人", "is_correct": False},
                {"label": "B", "text": "拒绝传菜，与厨房沟通", "is_correct": True},
                {"label": "C", "text": "自己简单处理一下再传", "is_correct": False},
                {"label": "D", "text": "告诉客人将就一下", "is_correct": False}
            ],
            "explanation": "发现不符合标准的菜品应拒绝传菜，与厨房沟通解决。"
        },

        # 传菜服务标准（10道）
        {
            "text": "传菜时，托盘上物品摆放的原则是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "轻物放重物前，重物放身前", "is_correct": True},
                {"label": "B", "text": "重物放轻物前，轻物放身前", "is_correct": False},
                {"label": "C", "text": "随意摆放", "is_correct": False},
                {"label": "D", "text": "重物放最上面", "is_correct": False}
            ],
            "explanation": "传菜标准：重物放身前，轻物放重物前。"
        },
        {
            "text": "传菜时可以重叠、压菜吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "传菜标准明确要求菜品不重叠、不压菜。"
        },
        {
            "text": "传菜时应按什么顺序传菜？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "按自己方便的顺序", "is_correct": False},
                {"label": "B", "text": "按出品先后顺序，加急菜单优先", "is_correct": True},
                {"label": "C", "text": "按菜品重量", "is_correct": False},
                {"label": "D", "text": "按客人催促情况", "is_correct": False}
            ],
            "explanation": "按出品先后顺序传菜，加急菜单优先出品。"
        },
        {
            "text": "上酸汤锅底时的特别介绍话术是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "您好，这是您的锅底", "is_correct": False},
                {"label": "B", "text": "您好，这是我们的特色非遗锅底，很多客人觉得味道好，层次丰富是因为我们的配料表非常的干净，自然发酵出来的味道就非常天然。", "is_correct": True},
                {"label": "C", "text": "您好，锅底来了", "is_correct": False},
                {"label": "D", "text": "这是酸汤锅底，请慢用", "is_correct": False}
            ],
            "explanation": "上酸汤锅底时特别介绍：您好，这是我们的特色非遗锅底，很多客人觉得味道好，层次丰富是因为我们的配料表非常的干净，自然发酵出来的味道就非常天然。"
        },
        {
            "text": "上菜的正确顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "素菜→荤菜→锅底", "is_correct": False},
                {"label": "B", "text": "锅底→荤菜、小吃、甜品饮品→素菜", "is_correct": True},
                {"label": "C", "text": "荤菜→素菜→锅底", "is_correct": False},
                {"label": "D", "text": "随机上菜", "is_correct": False}
            ],
            "explanation": "上菜顺序：锅底→荤菜、小吃、甜品饮品→素菜。"
        },
        {
            "text": "传菜员核对出餐小票时，必须检查什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "菜品价格", "is_correct": False},
                {"label": "B", "text": "菜品出品是否符合十不出品标准", "is_correct": True},
                {"label": "C", "text": "客人是否在座", "is_correct": False},
                {"label": "D", "text": "厨房是否忙碌", "is_correct": False}
            ],
            "explanation": "核对出餐小票时必须检查菜品出品是否符合十不出品标准。"
        },
        {
            "text": "传菜到客人桌上后应该做什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "报菜名", "is_correct": True},
                {"label": "B", "text": "确认菜品", "is_correct": True},
                {"label": "C", "text": "在客人小票上划单", "is_correct": True},
                {"label": "D", "text": "立即离开", "is_correct": False}
            ],
            "explanation": "传菜到客人桌上后应报菜名、确认菜品并在客人小票上划单。"
        },
        {
            "text": "无传菜工作时，传菜员应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "value_collaboration",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "一直站在传菜档口等", "is_correct": False},
                {"label": "B", "text": "巡场撤走客人空盘，配合服务部完成收台", "is_correct": True},
                {"label": "C", "text": "玩手机休息", "is_correct": False},
                {"label": "D", "text": "聊天", "is_correct": False}
            ],
            "explanation": "无传菜工作时不要一直站在传菜档口等，应巡场撤走客人空盘，配合服务部完成收台，体现高效协作。"
        },
        {
            "text": "撤空盘时的标准用语是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "我拿走了", "is_correct": False},
                {"label": "B", "text": "您好，帮您撤走一下空盘", "is_correct": True},
                {"label": "C", "text": "空盘撤了", "is_correct": False},
                {"label": "D", "text": "不需要说话直接拿走", "is_correct": False}
            ],
            "explanation": "撤空盘标准用语：您好，帮您撤走一下空盘。"
        },
        {
            "text": "传菜员上菜时手指可以触碰菜品吗？",
            "question_type": QuestionType.TRUE_FALSE,
            "category": "skill",
            "difficulty": "easy",
            "correct_answer": "错误",
            "explanation": "上菜标准明确要求手指不能触碰菜品。"
        },

        # 保洁专员 - 收复台标准（10道）
        {
            "text": "小桌收台的标准时长是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "1分钟", "is_correct": False},
                {"label": "B", "text": "3分钟", "is_correct": True},
                {"label": "C", "text": "5分钟", "is_correct": False},
                {"label": "D", "text": "10分钟", "is_correct": False}
            ],
            "explanation": "收台时长：小桌3分钟，大桌5分钟。"
        },
        {
            "text": "大桌收台的标准时长是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "3分钟", "is_correct": False},
                {"label": "B", "text": "5分钟", "is_correct": True},
                {"label": "C", "text": "10分钟", "is_correct": False},
                {"label": "D", "text": "15分钟", "is_correct": False}
            ],
            "explanation": "收台时长：小桌3分钟，大桌5分钟。"
        },
        {
            "text": "收台的第一步应该做什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "收餐具", "is_correct": False},
                {"label": "B", "text": "关火并检查炉具", "is_correct": True},
                {"label": "C", "text": "擦桌子", "is_correct": False},
                {"label": "D", "text": "倒垃圾", "is_correct": False}
            ],
            "explanation": "收台顺序第1步：关火并检查炉具。"
        },
        {
            "text": "建议的收台餐具顺序是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "玻璃器皿→茶杯→菜盘→筷子/汤漏勺→油碟碗→锅底", "is_correct": True},
                {"label": "B", "text": "锅底→油碟碗→菜盘→茶杯→玻璃器皿", "is_correct": False},
                {"label": "C", "text": "随意顺序", "is_correct": False},
                {"label": "D", "text": "筷子→碗→盘子→锅底", "is_correct": False}
            ],
            "explanation": "建议收台顺序：玻璃器皿→茶杯→菜盘→筷子/汤漏勺→油碟碗→锅底。"
        },
        {
            "text": "收台时应遵循什么原则？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "快拿、快放、快端", "is_correct": False},
                {"label": "B", "text": "轻拿、轻放、轻端", "is_correct": True},
                {"label": "C", "text": "用力拿、用力放", "is_correct": False},
                {"label": "D", "text": "随意即可", "is_correct": False}
            ],
            "explanation": "收台原则：轻拿、轻放、轻端（三轻）。"
        },
        {
            "text": "擦台的5个步骤中，第一步是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "用毛巾擦拭", "is_correct": False},
                {"label": "B", "text": "用刮刀将桌面残渣刮入垃圾桶", "is_correct": True},
                {"label": "C", "text": "喷洒清洁剂", "is_correct": False},
                {"label": "D", "text": "用水冲洗", "is_correct": False}
            ],
            "explanation": "擦台5步骤第1步：用刮刀将桌面残渣刮入垃圾桶。"
        },
        {
            "text": "擦台使用的清洁剂标准配比是多少？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "medium",
            "options": [
                {"label": "A", "text": "洗洁精:水=1:5", "is_correct": False},
                {"label": "B", "text": "洗洁精:水=1:9或2:8", "is_correct": True},
                {"label": "C", "text": "洗洁精:水=1:10", "is_correct": False},
                {"label": "D", "text": "纯洗洁精", "is_correct": False}
            ],
            "explanation": "用喷壶将清洁剂均匀喷洒在桌面（洗洁精:水=1:9或2:8）。"
        },
        {
            "text": "擦台时应使用哪些颜色的毛巾，分别用于什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "hard",
            "options": [
                {"label": "A", "text": "蓝色去污、紫色抛光、绿色擦椅凳", "is_correct": True},
                {"label": "B", "text": "绿色去污、蓝色抛光、紫色擦椅凳", "is_correct": False},
                {"label": "C", "text": "紫色去污、绿色抛光、蓝色擦椅凳", "is_correct": False},
                {"label": "D", "text": "所有颜色通用", "is_correct": False}
            ],
            "explanation": "用蓝色毛巾折叠成长条状擦拭（去除油污和污渍），用紫色毛巾二次擦拭、抛光（去除水渍，使桌面光亮），用绿色毛巾擦拭椅凳。"
        },
        {
            "text": "洗手间高峰期应多久清洁一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "15分钟", "is_correct": False},
                {"label": "B", "text": "半小时", "is_correct": True},
                {"label": "C", "text": "1小时", "is_correct": False},
                {"label": "D", "text": "2小时", "is_correct": False}
            ],
            "explanation": "洗手间清洁频次：高峰期每半小时，平峰期每1小时。"
        },
        {
            "text": "洗手间平峰期应多久清洁一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "category": "skill",
            "difficulty": "easy",
            "options": [
                {"label": "A", "text": "半小时", "is_correct": False},
                {"label": "B", "text": "1小时", "is_correct": True},
                {"label": "C", "text": "2小时", "is_correct": False},
                {"label": "D", "text": "3小时", "is_correct": False}
            ],
            "explanation": "洗手间清洁频次：高峰期每半小时，平峰期每1小时。"
        },
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
