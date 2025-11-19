#!/usr/bin/env python3
"""
生成综合性题目批次
生成76道题目，涵盖前后厅协作、管理知识、应急处理、服务综合、价值观综合应用
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType

def create_questions():
    """创建综合性题目（76道）"""
    db = SessionLocal()

    questions = [
        # === 前后厅协作（15道）===
        {
            "text": "高峰期，前厅服务员发现某道菜出餐延迟超过10分钟，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即到厨房确认进度和预计时间", "is_correct": True},
                {"label": "B", "text": "主动告知客人并致歉", "is_correct": True},
                {"label": "C", "text": "提供饮品或小食安抚客人", "is_correct": True},
                {"label": "D", "text": "假装不知道等客人催", "is_correct": False}
            ]
        },
        {
            "text": "客人投诉菜品口味不对，服务员应该如何协调前后厅？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "先向客人致歉并询问具体问题", "is_correct": True},
                {"label": "B", "text": "将菜品带回厨房，向厨师说明情况", "is_correct": True},
                {"label": "C", "text": "询问客人是否需要重做或更换", "is_correct": True},
                {"label": "D", "text": "责怪厨房做错了", "is_correct": False}
            ]
        },
        {
            "text": "传菜员发现出餐台上有准备好的菜品，但不确定是哪桌的，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即询问厨房或核对订单单据", "is_correct": True},
                {"label": "B", "text": "随便端给一桌", "is_correct": False},
                {"label": "C", "text": "放在那里不管", "is_correct": False},
                {"label": "D", "text": "等服务员来问", "is_correct": False}
            ]
        },
        {
            "text": "厨房备料发现食材不足，可能影响出餐，应该如何通知前厅？",
            "question_type": "MULTIPLE_CHOICE",
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "第一时间通知前厅主管或店长", "is_correct": True},
                {"label": "B", "text": "告知哪些菜品受影响", "is_correct": True},
                {"label": "C", "text": "说明预计何时恢复供应", "is_correct": True},
                {"label": "D", "text": "等客人点了再说", "is_correct": False}
            ]
        },
        {
            "text": "前厅接到客人大单预定（20人），需要与厨房协调哪些事项？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "提前告知厨房用餐时间和人数", "is_correct": True},
                {"label": "B", "text": "沟通菜单需求，确认厨房能否准备", "is_correct": True},
                {"label": "C", "text": "协商备料和出餐时间安排", "is_correct": True},
                {"label": "D", "text": "不需要提前通知厨房", "is_correct": False}
            ]
        },
        {
            "text": "客人要求菜品加辣或少盐，服务员应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "详细记录需求并明确传达给厨房", "is_correct": True},
                {"label": "B", "text": "告诉客人不能调整", "is_correct": False},
                {"label": "C", "text": "随口说说不记录", "is_correct": False},
                {"label": "D", "text": "不告诉厨房", "is_correct": False}
            ]
        },
        {
            "text": "厨房设备突然故障无法制作某类菜品，应该如何与前厅协作？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即通知前厅停止接受相关菜品订单", "is_correct": True},
                {"label": "B", "text": "说明故障原因和预计修复时间", "is_correct": True},
                {"label": "C", "text": "建议前厅向客人推荐替代菜品", "is_correct": True},
                {"label": "D", "text": "继续接单慢慢想办法", "is_correct": False}
            ]
        },
        {
            "text": "交接班时，前后厅应该沟通哪些重要信息？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "当前在制菜品和待出菜品情况", "is_correct": True},
                {"label": "B", "text": "食材库存和特殊情况", "is_correct": True},
                {"label": "C", "text": "客人特殊要求和投诉处理进度", "is_correct": True},
                {"label": "D", "text": "同事之间的矛盾和抱怨", "is_correct": False}
            ]
        },
        {
            "text": "客人要求菜品退换，服务员和厨房应该如何配合？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "服务员了解原因后与厨房沟通，共同确定解决方案", "is_correct": True},
                {"label": "B", "text": "服务员直接决定退换", "is_correct": False},
                {"label": "C", "text": "让客人自己去厨房说", "is_correct": False},
                {"label": "D", "text": "拒绝客人要求", "is_correct": False}
            ]
        },
        {
            "text": "前厅发现厨房出餐速度较慢，应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "先了解原因，主动提供帮助或协调资源", "is_correct": True},
                {"label": "B", "text": "抱怨厨房效率低", "is_correct": False},
                {"label": "C", "text": "不管不问", "is_correct": False},
                {"label": "D", "text": "催促厨房快点", "is_correct": False}
            ]
        },
        {
            "text": "厨房人手不足时，前厅员工可以提供哪些支持？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "帮助传菜和清理出餐台", "is_correct": True},
                {"label": "B", "text": "协助简单的备料工作", "is_correct": True},
                {"label": "C", "text": "配合厨房调整菜单推荐", "is_correct": True},
                {"label": "D", "text": "无视厨房的困难", "is_correct": False}
            ]
        },
        {
            "text": "服务员发现传菜员送错菜品到桌上，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即礼貌地撤回菜品", "is_correct": True},
                {"label": "B", "text": "核对正确的台号并送达", "is_correct": True},
                {"label": "C", "text": "向客人致歉", "is_correct": True},
                {"label": "D", "text": "当众责怪传菜员", "is_correct": False}
            ]
        },
        {
            "text": "前后厅沟通的基本原则包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "信息准确、及时、清晰", "is_correct": True},
                {"label": "B", "text": "态度礼貌、互相尊重", "is_correct": True},
                {"label": "C", "text": "以解决问题为导向", "is_correct": True},
                {"label": "D", "text": "互相指责推卸责任", "is_correct": False}
            ]
        },
        {
            "text": "客人赶时间需要快速出餐，前后厅应该如何配合？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "服务员立即告知厨房客人的紧急需求", "is_correct": True},
                {"label": "B", "text": "推荐制作时间短的菜品", "is_correct": True},
                {"label": "C", "text": "厨房优先安排制作", "is_correct": True},
                {"label": "D", "text": "告诉客人我们很忙", "is_correct": False}
            ]
        },
        {
            "text": "前后厅高效协作的核心价值是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "共同为客人提供优质服务体验", "is_correct": True},
                {"label": "B", "text": "各干各的互不干涉", "is_correct": False},
                {"label": "C", "text": "前厅管点菜厨房管做菜", "is_correct": False},
                {"label": "D", "text": "互相监督检查", "is_correct": False}
            ]
        },

        # === 管理知识（15道）===
        {
            "text": "作为店长，每天营业前应该检查哪些事项？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "员工出勤情况和仪容仪表", "is_correct": True},
                {"label": "B", "text": "设备运行状态和安全隐患", "is_correct": True},
                {"label": "C", "text": "食材库存和当日备料计划", "is_correct": True},
                {"label": "D", "text": "只需要看看有没有员工迟到", "is_correct": False}
            ]
        },
        {
            "text": "主管发现员工服务态度不佳，应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "私下沟通了解原因，耐心引导改正", "is_correct": True},
                {"label": "B", "text": "当着客人的面批评", "is_correct": False},
                {"label": "C", "text": "不管不问", "is_correct": False},
                {"label": "D", "text": "直接扣工资", "is_correct": False}
            ]
        },
        {
            "text": "店长每日工作的核心职责是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "确保门店正常运营和服务质量", "is_correct": True},
                {"label": "B", "text": "管理和激励团队成员", "is_correct": True},
                {"label": "C", "text": "控制成本和提升营业额", "is_correct": True},
                {"label": "D", "text": "只负责看着员工干活", "is_correct": False}
            ]
        },
        {
            "text": "新员工培训期间，主管应该关注哪些方面？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "基础服务流程和标准掌握情况", "is_correct": True},
                {"label": "B", "text": "安全操作规范的学习", "is_correct": True},
                {"label": "C", "text": "企业文化和价值观的理解", "is_correct": True},
                {"label": "D", "text": "只要能干活就行", "is_correct": False}
            ]
        },
        {
            "text": "高峰期员工突然请假，店长应该如何应对？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "快速调配现有人员补位", "is_correct": True},
                {"label": "B", "text": "联系其他门店或备用人员支援", "is_correct": True},
                {"label": "C", "text": "必要时管理层亲自上岗", "is_correct": True},
                {"label": "D", "text": "让其他员工硬扛", "is_correct": False}
            ]
        },
        {
            "text": "主管在团队管理中，最重要的能力是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "激励团队、协调资源、解决问题", "is_correct": True},
                {"label": "B", "text": "批评指责员工", "is_correct": False},
                {"label": "C", "text": "只会下命令", "is_correct": False},
                {"label": "D", "text": "什么都自己做", "is_correct": False}
            ]
        },
        {
            "text": "店长发现门店库存管理混乱，应该采取哪些措施？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "建立库存盘点制度", "is_correct": True},
                {"label": "B", "text": "落实先进先出(FIFO)原则", "is_correct": True},
                {"label": "C", "text": "培训员工正确的库存管理方法", "is_correct": True},
                {"label": "D", "text": "继续混乱管理", "is_correct": False}
            ]
        },
        {
            "text": "主管在处理员工投诉时，正确的做法是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "认真倾听、公正调查、妥善解决", "is_correct": True},
                {"label": "B", "text": "偏袒某一方", "is_correct": False},
                {"label": "C", "text": "压制投诉", "is_correct": False},
                {"label": "D", "text": "不理不睬", "is_correct": False}
            ]
        },
        {
            "text": "店长如何激励表现优秀的员工？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "公开表扬和认可", "is_correct": True},
                {"label": "B", "text": "提供晋升和发展机会", "is_correct": True},
                {"label": "C", "text": "物质奖励和精神激励结合", "is_correct": True},
                {"label": "D", "text": "觉得是应该的不表扬", "is_correct": False}
            ]
        },
        {
            "text": "主管发现员工工作态度消极，应该如何引导？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "私下谈话了解原因，帮助解决困难", "is_correct": True},
                {"label": "B", "text": "当众批评", "is_correct": False},
                {"label": "C", "text": "不管不问", "is_correct": False},
                {"label": "D", "text": "直接辞退", "is_correct": False}
            ]
        },
        {
            "text": "门店营业额持续下滑，店长应该如何分析和应对？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "分析客流、菜品、服务等各方面原因", "is_correct": True},
                {"label": "B", "text": "征求员工意见和建议", "is_correct": True},
                {"label": "C", "text": "制定改进计划并跟踪执行", "is_correct": True},
                {"label": "D", "text": "责怪员工不努力", "is_correct": False}
            ]
        },
        {
            "text": "主管在排班时，应该考虑哪些因素？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "营业时段和客流预测", "is_correct": True},
                {"label": "B", "text": "员工技能和经验匹配", "is_correct": True},
                {"label": "C", "text": "劳动法规和员工休息需求", "is_correct": True},
                {"label": "D", "text": "随便排就行", "is_correct": False}
            ]
        },
        {
            "text": "店长如何有效开展员工晨会？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "总结昨日工作和表扬优秀表现", "is_correct": True},
                {"label": "B", "text": "部署当日任务和注意事项", "is_correct": True},
                {"label": "C", "text": "传达公司政策和激励团队士气", "is_correct": True},
                {"label": "D", "text": "开会就是批评人", "is_correct": False}
            ]
        },
        {
            "text": "管理者的核心价值观应该是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以身作则，带领团队共同成长", "is_correct": True},
                {"label": "B", "text": "只会指挥不干活", "is_correct": False},
                {"label": "C", "text": "只为完成业绩指标", "is_correct": False},
                {"label": "D", "text": "压榨员工劳动力", "is_correct": False}
            ]
        },
        {
            "text": "主管如何平衡业绩目标和员工关怀？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "在追求业绩的同时关注员工成长和福祉，实现双赢", "is_correct": True},
                {"label": "B", "text": "只看业绩不管员工", "is_correct": False},
                {"label": "C", "text": "只关心员工不管业绩", "is_correct": False},
                {"label": "D", "text": "二者无法兼顾", "is_correct": False}
            ]
        },

        # === 应急处理（12道）===
        {
            "text": "客人在用餐时突然晕倒，应该立即采取哪些措施？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即拨打120急救电话", "is_correct": True},
                {"label": "B", "text": "将客人转移到安全通风处", "is_correct": True},
                {"label": "C", "text": "安抚其他客人情绪", "is_correct": True},
                {"label": "D", "text": "假装没看见", "is_correct": False}
            ]
        },
        {
            "text": "发现厨房起火，正确的应急处理流程是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即切断电源和燃气", "is_correct": True},
                {"label": "B", "text": "使用灭火器或灭火毯扑灭", "is_correct": True},
                {"label": "C", "text": "火势无法控制时立即疏散并报警", "is_correct": True},
                {"label": "D", "text": "用水直接浇灭油锅火", "is_correct": False}
            ]
        },
        {
            "text": "客人投诉食物中有异物，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即道歉并撤下菜品", "is_correct": True},
                {"label": "B", "text": "保留异物作为证据", "is_correct": True},
                {"label": "C", "text": "向上级汇报并商讨赔偿方案", "is_correct": True},
                {"label": "D", "text": "争辩说不可能", "is_correct": False}
            ]
        },
        {
            "text": "发现燃气泄漏，最优先的处理措施是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即关闭燃气总阀并疏散人员", "is_correct": True},
                {"label": "B", "text": "开灯查看泄漏点", "is_correct": False},
                {"label": "C", "text": "用打火机测试", "is_correct": False},
                {"label": "D", "text": "继续营业", "is_correct": False}
            ]
        },
        {
            "text": "客人之间发生争执甚至打斗，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即制止并隔离双方", "is_correct": True},
                {"label": "B", "text": "通知店长或主管处理", "is_correct": True},
                {"label": "C", "text": "必要时报警", "is_correct": True},
                {"label": "D", "text": "围观看热闹", "is_correct": False}
            ]
        },
        {
            "text": "员工在工作中被烫伤或割伤，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即用冷水冲洗伤口", "is_correct": True},
                {"label": "B", "text": "进行简单包扎消毒", "is_correct": True},
                {"label": "C", "text": "严重时送医院并上报", "is_correct": True},
                {"label": "D", "text": "忍一忍继续工作", "is_correct": False}
            ]
        },
        {
            "text": "突然停电，餐厅应该如何应对？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "启动应急照明设备", "is_correct": True},
                {"label": "B", "text": "安抚客人情绪并说明情况", "is_correct": True},
                {"label": "C", "text": "检查食材保存情况", "is_correct": True},
                {"label": "D", "text": "让客人自己离开", "is_correct": False}
            ]
        },
        {
            "text": "客人醉酒闹事，应该如何妥善处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "礼貌劝阻并停止供应酒水", "is_correct": True},
                {"label": "B", "text": "联系客人同伴协助控制", "is_correct": True},
                {"label": "C", "text": "影响其他客人时请保安或报警", "is_correct": True},
                {"label": "D", "text": "和醉酒客人对骂", "is_correct": False}
            ]
        },
        {
            "text": "发现疑似食物中毒情况，应该立即采取哪些措施？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即送医并报告卫生部门", "is_correct": True},
                {"label": "B", "text": "封存可疑食品和留样", "is_correct": True},
                {"label": "C", "text": "停止供应相关菜品", "is_correct": True},
                {"label": "D", "text": "隐瞒事实", "is_correct": False}
            ]
        },
        {
            "text": "地震发生时，餐厅员工应该如何引导客人？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "保持冷静，指挥客人有序疏散", "is_correct": True},
                {"label": "B", "text": "引导到空旷安全区域", "is_correct": True},
                {"label": "C", "text": "检查是否有受伤人员", "is_correct": True},
                {"label": "D", "text": "自己先跑", "is_correct": False}
            ]
        },
        {
            "text": "发现未成年人单独饮酒，服务员应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "礼貌拒绝并说明法律规定", "is_correct": True},
                {"label": "B", "text": "只要给钱就卖", "is_correct": False},
                {"label": "C", "text": "假装没看见", "is_correct": False},
                {"label": "D", "text": "劝他们偷偷喝", "is_correct": False}
            ]
        },
        {
            "text": "应急处理的核心原则是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "生命安全第一，快速反应，妥善处理", "is_correct": True},
                {"label": "B", "text": "保护公司利益", "is_correct": False},
                {"label": "C", "text": "推卸责任", "is_correct": False},
                {"label": "D", "text": "大事化小小事化了", "is_correct": False}
            ]
        },

        # === 服务综合（15道）===
        {
            "text": "优质服务的核心要素包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "主动热情、细致周到", "is_correct": True},
                {"label": "B", "text": "专业高效、准确无误", "is_correct": True},
                {"label": "C", "text": "真诚待客、换位思考", "is_correct": True},
                {"label": "D", "text": "只要完成任务就行", "is_correct": False}
            ]
        },
        {
            "text": "如何提升客户满意度？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "超越客人期待，提供惊喜服务", "is_correct": True},
                {"label": "B", "text": "及时响应客人需求", "is_correct": True},
                {"label": "C", "text": "主动发现并解决问题", "is_correct": True},
                {"label": "D", "text": "客人不说就不管", "is_correct": False}
            ]
        },
        {
            "text": "客人带老人和小孩用餐，服务员可以提供哪些贴心服务？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "安排安静舒适的座位", "is_correct": True},
                {"label": "B", "text": "提供儿童座椅和老人坐垫", "is_correct": True},
                {"label": "C", "text": "推荐适合老人和儿童的菜品", "is_correct": True},
                {"label": "D", "text": "不需要特别照顾", "is_correct": False}
            ]
        },
        {
            "text": "客人对账单有疑问时,服务员应该如何处理？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "耐心核对每一项，如有错误立即更正并致歉", "is_correct": True},
                {"label": "B", "text": "坚持账单没错", "is_correct": False},
                {"label": "C", "text": "让客人自己去前台", "is_correct": False},
                {"label": "D", "text": "随便改改数字", "is_correct": False}
            ]
        },
        {
            "text": "雨天客人到店，服务员可以提供哪些周到服务？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "提供雨伞架或雨伞袋", "is_correct": True},
                {"label": "B", "text": "提供毛巾擦拭", "is_correct": True},
                {"label": "C", "text": "引导到干燥的座位", "is_correct": True},
                {"label": "D", "text": "嫌弃客人弄湿地面", "is_correct": False}
            ]
        },
        {
            "text": "客人表示对某道菜过敏，服务员应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "详细记录过敏信息", "is_correct": True},
                {"label": "B", "text": "推荐安全的替代菜品", "is_correct": True},
                {"label": "C", "text": "与厨房明确沟通避免交叉污染", "is_correct": True},
                {"label": "D", "text": "觉得麻烦就不理", "is_correct": False}
            ]
        },
        {
            "text": "如何处理客人的不合理要求？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "礼貌解释原因，寻求替代方案，维护双方利益", "is_correct": True},
                {"label": "B", "text": "直接拒绝", "is_correct": False},
                {"label": "C", "text": "无条件答应", "is_correct": False},
                {"label": "D", "text": "和客人争吵", "is_correct": False}
            ]
        },
        {
            "text": "客人提出要见厨师当面感谢，应该如何安排？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "征得厨师同意后安排合适时间见面", "is_correct": True},
                {"label": "B", "text": "拒绝客人要求", "is_correct": False},
                {"label": "C", "text": "让客人自己去厨房", "is_correct": False},
                {"label": "D", "text": "不理会", "is_correct": False}
            ]
        },
        {
            "text": "如何营造良好的用餐氛围？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "保持环境整洁舒适", "is_correct": True},
                {"label": "B", "text": "控制音乐和噪音适度", "is_correct": True},
                {"label": "C", "text": "服务自然不过度打扰", "is_correct": True},
                {"label": "D", "text": "大声喧哗聊天", "is_correct": False}
            ]
        },
        {
            "text": "常客再次到店，服务员应该如何提供个性化服务？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "主动问候并表示欢迎", "is_correct": True},
                {"label": "B", "text": "记住客人的口味偏好", "is_correct": True},
                {"label": "C", "text": "推荐新品或客人喜欢的菜", "is_correct": True},
                {"label": "D", "text": "当作新客人对待", "is_correct": False}
            ]
        },
        {
            "text": "客人用餐后留下好评，应该如何回应？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "真诚感谢并表示期待下次光临", "is_correct": True},
                {"label": "B", "text": "觉得理所当然", "is_correct": False},
                {"label": "C", "text": "不回应", "is_correct": False},
                {"label": "D", "text": "过度吹嘘", "is_correct": False}
            ]
        },
        {
            "text": "如何平衡多桌客人的服务需求？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "合理规划动线，分清主次，确保每桌都得到关注", "is_correct": True},
                {"label": "B", "text": "只服务一桌", "is_correct": False},
                {"label": "C", "text": "忽视部分客人", "is_correct": False},
                {"label": "D", "text": "手忙脚乱", "is_correct": False}
            ]
        },
        {
            "text": "客人对菜品提出改进建议，应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "真诚感谢客人的建议", "is_correct": True},
                {"label": "B", "text": "详细记录反馈内容", "is_correct": True},
                {"label": "C", "text": "转达给厨房和管理层", "is_correct": True},
                {"label": "D", "text": "觉得客人多事", "is_correct": False}
            ]
        },
        {
            "text": "服务中的'细节决定成败'体现在哪些方面？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "观察客人需求并主动提供", "is_correct": True},
                {"label": "B", "text": "确保餐具茶水随时充足", "is_correct": True},
                {"label": "C", "text": "及时清理桌面保持整洁", "is_correct": True},
                {"label": "D", "text": "做完基本工作就够了", "is_correct": False}
            ]
        },
        {
            "text": "餐饮服务的最终目标是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "让每位客人满意而归，成为回头客", "is_correct": True},
                {"label": "B", "text": "完成工作任务", "is_correct": False},
                {"label": "C", "text": "挣钱", "is_correct": False},
                {"label": "D", "text": "应付了事", "is_correct": False}
            ]
        },

        # === 价值观综合应用（19道）===
        {
            "text": "高峰期，老员工小李主动放弃休息时间帮助新员工，还耐心指导服务技巧。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "平等透明", "is_correct": True},
                {"label": "D", "text": "只体现勤劳", "is_correct": False}
            ]
        },
        {
            "text": "服务员发现客人遗落贵重物品，立即上交并主动联系失主归还。这体现了哪些价值观？",
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
            "text": "厨房发现食材有问题，主动停止使用并告知前厅，避免了食品安全事故。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "平等透明", "is_correct": True},
                {"label": "D", "text": "只为了完成工作", "is_correct": False}
            ]
        },
        {
            "text": "员工小王发现同事操作不规范有安全隐患，立即友善提醒并示范正确做法。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "高效协作", "is_correct": True},
                {"label": "B", "text": "平等透明", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": "主管在分配任务时，公平公正，不偏袒任何人，并愿意倾听员工意见。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "以勤劳者为本", "is_correct": False}
            ]
        },
        {
            "text": "客人点了可能引发过敏的菜品，服务员主动提醒并建议更换，还与厨房沟通避免交叉污染。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": "在餐饮工作中，四大价值观之间的关系是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "相互支撑、缺一不可、共同构成企业文化核心", "is_correct": True},
                {"label": "B", "text": "互相矛盾", "is_correct": False},
                {"label": "C", "text": "可以选择性遵守", "is_correct": False},
                {"label": "D", "text": "只是口号", "is_correct": False}
            ]
        },
        {
            "text": "员工在工作中犯了错，主动承认并提出改进方案。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "以勤劳者为本", "is_correct": False}
            ]
        },
        {
            "text": "团队成员相互支持，忙时互帮，闲时分享经验，共同提升服务水平。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "高效协作", "is_correct": True},
                {"label": "B", "text": "以勤劳者为本", "is_correct": True},
                {"label": "C", "text": "平等透明", "is_correct": True},
                {"label": "D", "text": "只体现协作", "is_correct": False}
            ]
        },
        {
            "text": "服务员观察到客人不停地看手机查时间，主动询问是否赶时间并协调厨房加快出餐。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": "新员工小张工作很努力但方法不对效率低，老员工主动分享经验帮助改进。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "高效协作", "is_correct": True},
                {"label": "B", "text": "平等透明", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": "员工下班后主动留下来帮助清洁未完成的区域，确保第二天营业环境整洁。这体现了什么价值观？",
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
            "text": "店长发现员工家里有困难影响工作，主动关心并协调解决。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": "厨房和前厅因沟通不畅发生误会，双方主动坐下来坦诚交流解决问题。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": "一个优秀的餐饮团队，最重要的文化基因是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "四大价值观深入人心并体现在日常工作中", "is_correct": True},
                {"label": "B", "text": "业绩好就行", "is_correct": False},
                {"label": "C", "text": "听话服从", "is_correct": False},
                {"label": "D", "text": "各干各的", "is_correct": False}
            ]
        },
        {
            "text": "面对客人的无理要求，员工礼貌拒绝并解释原因，维护了公司原则也保持了服务态度。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": True},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "高效协作", "is_correct": False}
            ]
        },
        {
            "text": "员工在工作中不断学习提升技能，主动分享经验帮助新人成长。这体现了哪些价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": True},
                {"label": "C", "text": "平等透明", "is_correct": True},
                {"label": "D", "text": "只为自己", "is_correct": False}
            ]
        },
        {
            "text": "如何在日常工作中践行四大价值观？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "勤奋工作，主动承担", "is_correct": True},
                {"label": "B", "text": "真诚待客，用心服务", "is_correct": True},
                {"label": "C", "text": "团队协作，互相支持", "is_correct": True},
                {"label": "D", "text": "只说不做", "is_correct": False}
            ]
        },
        {
            "text": "餐饮行业从业者的职业自豪感应该来自哪里？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "通过专业服务为客人创造价值，获得认可和尊重", "is_correct": True},
                {"label": "B", "text": "挣钱多", "is_correct": False},
                {"label": "C", "text": "工作轻松", "is_correct": False},
                {"label": "D", "text": "没有自豪感", "is_correct": False}
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

            inserted_count += 1
            print(f"[{i}/{len(questions)}] 已插入题目：{q_data['content'][:40]}...")

        print(f"\n✅ 成功插入 {inserted_count} 道综合性题目！")

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
        print(f"- 简单：{easy}道 ({easy/len(questions)*100:.1f}%)")
        print(f"- 中等：{medium}道 ({medium/len(questions)*100:.1f}%)")
        print(f"- 困难：{hard}道 ({hard/len(questions)*100:.1f}%)")
        print(f"\n类别分布：")
        print(f"- 技能类：{skill}道 ({skill/len(questions)*100:.1f}%)")
        print(f"- 价值观（勤劳）：{value_diligence}道")
        print(f"- 价值观（顾客）：{value_customer}道")
        print(f"- 价值观（协作）：{value_collaboration}道")
        print(f"- 价值观（透明）：{value_transparency}道")
        print(f"- 价值观总计：{value_diligence + value_customer + value_collaboration + value_transparency}道 ({(value_diligence + value_customer + value_collaboration + value_transparency)/len(questions)*100:.1f}%)")

    except Exception as e:
        db.rollback()
        print(f"❌ 插入题目失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始生成综合性题目（76道）...")
    create_questions()
    print("\n综合性题目生成完成！")
