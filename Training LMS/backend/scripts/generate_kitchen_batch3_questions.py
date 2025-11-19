#!/usr/bin/env python3
"""
生成厨房题目批次3
生成60道题目，涵盖安全操作、设备使用、烹饪标准和价值观实践
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.core.database import SessionLocal
from app.models.exam import Question, QuestionType

def create_questions():
    """创建厨房批次3题目（60道）"""
    db = SessionLocal()

    questions = [
        # === 食品安全与卫生（15道）===
        {
            "text": "食品留样的正确做法是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "每个品种留样不少于125g", "is_correct": True},
                {"label": "B", "text": "留样保存48小时以上", "is_correct": True},
                {"label": "C", "text": "使用专用留样盒并标注日期", "is_correct": True},
                {"label": "D", "text": "留样可以随意放置", "is_correct": False}
            ]
        },
        {
            "text": "冷藏食材的储存温度应该控制在多少度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "0-4°C", "is_correct": True},
                {"label": "B", "text": "5-10°C", "is_correct": False},
                {"label": "C", "text": "10-15°C", "is_correct": False},
                {"label": "D", "text": "-5-0°C", "is_correct": False}
            ]
        },
        {
            "text": "生熟食材存放的原则是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "生熟分开存放", "is_correct": True},
                {"label": "B", "text": "使用不同的刀具和砧板", "is_correct": True},
                {"label": "C", "text": "熟食放在上层，生食放在下层", "is_correct": True},
                {"label": "D", "text": "可以混放节省空间", "is_correct": False}
            ]
        },
        {
            "text": "发现食材有异味或变质，正确的处理方式是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即丢弃并上报主管", "is_correct": True},
                {"label": "B", "text": "洗洗还能用", "is_correct": False},
                {"label": "C", "text": "烹饪时多加调料掩盖", "is_correct": False},
                {"label": "D", "text": "混在其他食材里用掉", "is_correct": False}
            ]
        },
        {
            "text": "厨房工作人员的个人卫生要求包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "工作前洗手消毒", "is_correct": True},
                {"label": "B", "text": "穿戴整洁的工作服和工作帽", "is_correct": True},
                {"label": "C", "text": "不戴首饰，指甲保持短且干净", "is_correct": True},
                {"label": "D", "text": "可以在工作区域吸烟", "is_correct": False}
            ]
        },
        {
            "text": "厨房垃圾应该如何处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "及时清理，不过夜堆积", "is_correct": True},
                {"label": "B", "text": "分类投放（干湿垃圾）", "is_correct": True},
                {"label": "C", "text": "使用加盖的垃圾桶", "is_correct": True},
                {"label": "D", "text": "随便扔在角落", "is_correct": False}
            ]
        },
        {
            "text": "厨房地面有油渍或水渍时，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即清理，防止滑倒", "is_correct": True},
                {"label": "B", "text": "等下班后再清理", "is_correct": False},
                {"label": "C", "text": "让其他人小心点就行", "is_correct": False},
                {"label": "D", "text": "不用管", "is_correct": False}
            ]
        },
        {
            "text": "食材验收时，应该检查哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "生产日期和保质期", "is_correct": True},
                {"label": "B", "text": "包装是否完整无破损", "is_correct": True},
                {"label": "C", "text": "食材的新鲜度和品质", "is_correct": True},
                {"label": "D", "text": "只看价格就行", "is_correct": False}
            ]
        },
        {
            "text": "厨房用抹布和毛巾应该如何管理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "生熟分开使用不同颜色", "is_correct": True},
                {"label": "B", "text": "每日清洗消毒", "is_correct": True},
                {"label": "C", "text": "定期更换", "is_correct": True},
                {"label": "D", "text": "一条抹布用到底", "is_correct": False}
            ]
        },
        {
            "text": "刀具使用完毕后，正确的做法是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即清洗消毒并归位", "is_correct": True},
                {"label": "B", "text": "随便放在台面上", "is_correct": False},
                {"label": "C", "text": "等下班一起洗", "is_correct": False},
                {"label": "D", "text": "扔在水池里", "is_correct": False}
            ]
        },
        {
            "text": "厨房消毒的正确频率是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "每日至少一次，营业结束后全面消毒", "is_correct": True},
                {"label": "B", "text": "每周一次", "is_correct": False},
                {"label": "C", "text": "想起来就做", "is_correct": False},
                {"label": "D", "text": "不需要消毒", "is_correct": False}
            ]
        },
        {
            "text": "发现厨房有老鼠或蟑螂，应该怎么处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即上报主管", "is_correct": True},
                {"label": "B", "text": "检查并封堵可能的进入通道", "is_correct": True},
                {"label": "C", "text": "联系专业除虫公司", "is_correct": True},
                {"label": "D", "text": "视而不见继续工作", "is_correct": False}
            ]
        },
        {
            "text": "食材先进先出（FIFO）原则的目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "确保食材新鲜，避免过期浪费", "is_correct": True},
                {"label": "B", "text": "方便库存管理", "is_correct": False},
                {"label": "C", "text": "节省时间", "is_correct": False},
                {"label": "D", "text": "没有特别原因", "is_correct": False}
            ]
        },
        {
            "text": "厨房灭火器应该如何管理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "放置在明显易取的位置", "is_correct": True},
                {"label": "B", "text": "定期检查压力和有效期", "is_correct": True},
                {"label": "C", "text": "所有员工都会使用", "is_correct": True},
                {"label": "D", "text": "放在储物间不碍事", "is_correct": False}
            ]
        },
        {
            "text": "厨房工作人员如果生病（感冒、腹泻等），应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "主动上报并请假，避免传染", "is_correct": True},
                {"label": "B", "text": "戴口罩继续工作", "is_correct": False},
                {"label": "C", "text": "坚持上班不请假", "is_correct": False},
                {"label": "D", "text": "吃点药就继续干活", "is_correct": False}
            ]
        },

        # === 设备操作与维护（15道）===
        {
            "text": "使用燃气灶前，应该先检查什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "燃气阀门是否正常", "is_correct": True},
                {"label": "B", "text": "是否有燃气泄漏的气味", "is_correct": True},
                {"label": "C", "text": "点火装置是否正常", "is_correct": True},
                {"label": "D", "text": "不需要检查直接使用", "is_correct": False}
            ]
        },
        {
            "text": "发现燃气泄漏时，正确的应急处理是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即关闭燃气总阀", "is_correct": True},
                {"label": "B", "text": "打开门窗通风", "is_correct": True},
                {"label": "C", "text": "严禁使用明火和电器开关", "is_correct": True},
                {"label": "D", "text": "立即开灯查看", "is_correct": False}
            ]
        },
        {
            "text": "油炸设备使用时的安全注意事项包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "油温不超过安全范围", "is_correct": True},
                {"label": "B", "text": "投料时避免溅油", "is_correct": True},
                {"label": "C", "text": "定期更换食用油", "is_correct": True},
                {"label": "D", "text": "可以离开去做其他事", "is_correct": False}
            ]
        },
        {
            "text": "蒸箱使用完毕后，应该如何操作？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "关闭电源", "is_correct": True},
                {"label": "B", "text": "待冷却后清洁内部", "is_correct": True},
                {"label": "C", "text": "排空余水", "is_correct": True},
                {"label": "D", "text": "直接关门就行", "is_correct": False}
            ]
        },
        {
            "text": "切片机使用时，应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "使用护手器，不直接用手推料", "is_correct": True},
                {"label": "B", "text": "清洁前必须断电", "is_correct": True},
                {"label": "C", "text": "刀片保持锋利，定期维护", "is_correct": True},
                {"label": "D", "text": "可以边聊天边操作", "is_correct": False}
            ]
        },
        {
            "text": "冰箱温度异常升高时，应该怎么处理？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即检查门封条是否完好", "is_correct": True},
                {"label": "B", "text": "上报维修人员", "is_correct": True},
                {"label": "C", "text": "将食材转移到正常冰箱", "is_correct": True},
                {"label": "D", "text": "继续使用没关系", "is_correct": False}
            ]
        },
        {
            "text": "消毒柜的正确使用方法是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "餐具清洗干净后放入", "is_correct": True},
                {"label": "B", "text": "不要过度堆积，保证通风", "is_correct": True},
                {"label": "C", "text": "按规定时间消毒", "is_correct": True},
                {"label": "D", "text": "带水的餐具也可以直接放入", "is_correct": False}
            ]
        },
        {
            "text": "排油烟机应该多久清洁一次？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "每周至少一次", "is_correct": True},
                {"label": "B", "text": "每月一次", "is_correct": False},
                {"label": "C", "text": "每季度一次", "is_correct": False},
                {"label": "D", "text": "看心情", "is_correct": False}
            ]
        },
        {
            "text": "厨房地漏堵塞时，正确的处理方式是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即清理并上报，避免积水", "is_correct": True},
                {"label": "B", "text": "等下班后处理", "is_correct": False},
                {"label": "C", "text": "让水自己流走", "is_correct": False},
                {"label": "D", "text": "不用管", "is_correct": False}
            ]
        },
        {
            "text": "使用高压锅时，必须遵守的安全规则包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "检查排气阀是否畅通", "is_correct": True},
                {"label": "B", "text": "食物不超过容量的2/3", "is_correct": True},
                {"label": "C", "text": "泄压后才能开盖", "is_correct": True},
                {"label": "D", "text": "可以强行开盖", "is_correct": False}
            ]
        },
        {
            "text": "电器设备出现故障时，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "立即断电并上报维修", "is_correct": True},
                {"label": "B", "text": "自己拆开修理", "is_correct": False},
                {"label": "C", "text": "继续使用观察", "is_correct": False},
                {"label": "D", "text": "关机重启试试", "is_correct": False}
            ]
        },
        {
            "text": "厨房设备每日维护应该包括哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "清洁设备表面和内部", "is_correct": True},
                {"label": "B", "text": "检查设备运行是否正常", "is_correct": True},
                {"label": "C", "text": "记录设备使用情况", "is_correct": True},
                {"label": "D", "text": "不需要每日维护", "is_correct": False}
            ]
        },
        {
            "text": "使用烤箱时，应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "预热后再放入食物", "is_correct": True},
                {"label": "B", "text": "使用隔热手套取放烤盘", "is_correct": True},
                {"label": "C", "text": "定期清理油渍和残渣", "is_correct": True},
                {"label": "D", "text": "可以把手伸进去取食物", "is_correct": False}
            ]
        },
        {
            "text": "洗碗机使用时的注意事项包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "先冲洗掉大块残渣", "is_correct": True},
                {"label": "B", "text": "按规定添加清洁剂", "is_correct": True},
                {"label": "C", "text": "定期清理过滤网", "is_correct": True},
                {"label": "D", "text": "可以超量堆放餐具", "is_correct": False}
            ]
        },
        {
            "text": "厨房用电安全的基本原则是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "湿手不触碰电器开关", "is_correct": True},
                {"label": "B", "text": "定期检查线路和插座", "is_correct": True},
                {"label": "C", "text": "不私拉乱接电线", "is_correct": True},
                {"label": "D", "text": "可以用湿布擦拭通电设备", "is_correct": False}
            ]
        },

        # === 烹饪标准与流程（15道）===
        {
            "text": "炒菜时控制火候的基本原则是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "根据食材特性和菜品要求调整火力", "is_correct": True},
                {"label": "B", "text": "一直用大火最快", "is_correct": False},
                {"label": "C", "text": "全程小火慢炖", "is_correct": False},
                {"label": "D", "text": "随意调节", "is_correct": False}
            ]
        },
        {
            "text": "肉类食材应该煮到什么程度才安全？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "中心温度达到75°C以上", "is_correct": True},
                {"label": "B", "text": "表面变色就可以", "is_correct": False},
                {"label": "C", "text": "看起来熟了就行", "is_correct": False},
                {"label": "D", "text": "客人要几分熟就几分熟", "is_correct": False}
            ]
        },
        {
            "text": "蔬菜清洗的正确步骤是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "先浸泡10分钟，再流水冲洗3次", "is_correct": True},
                {"label": "B", "text": "直接用水冲一下", "is_correct": False},
                {"label": "C", "text": "不用洗直接炒", "is_correct": False},
                {"label": "D", "text": "只泡水不冲洗", "is_correct": False}
            ]
        },
        {
            "text": "调味的基本原则是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "少量多次，逐步调整", "is_correct": True},
                {"label": "B", "text": "先尝后调，确保口味", "is_correct": True},
                {"label": "C", "text": "遵循菜品标准配方", "is_correct": True},
                {"label": "D", "text": "凭感觉随便放", "is_correct": False}
            ]
        },
        {
            "text": "出餐前应该检查哪些内容？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "菜品温度是否适宜", "is_correct": True},
                {"label": "B", "text": "摆盘是否美观", "is_correct": True},
                {"label": "C", "text": "分量是否足够", "is_correct": True},
                {"label": "D", "text": "不需要检查直接出", "is_correct": False}
            ]
        },
        {
            "text": "汤品制作时，应该注意什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "水量充足，避免中途加水", "is_correct": True},
                {"label": "B", "text": "文火慢炖，保持小滚", "is_correct": True},
                {"label": "C", "text": "适时撇去浮沫", "is_correct": True},
                {"label": "D", "text": "大火猛煮最快", "is_correct": False}
            ]
        },
        {
            "text": "刀工处理食材时的安全要点包括哪些？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "刀具锋利，砧板稳固", "is_correct": True},
                {"label": "B", "text": "手指要蜷曲，避免切到", "is_correct": True},
                {"label": "C", "text": "注意力集中，不分心", "is_correct": True},
                {"label": "D", "text": "可以边聊天边切菜", "is_correct": False}
            ]
        },
        {
            "text": "煎炸食品时，如何避免油温过高引发火灾？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "hard",
            "category": "skill",
            "options": [
                {"label": "A", "text": "使用温度计监控油温", "is_correct": True},
                {"label": "B", "text": "不离开灶台", "is_correct": True},
                {"label": "C", "text": "准备好锅盖随时灭火", "is_correct": True},
                {"label": "D", "text": "油温冒烟再投料", "is_correct": False}
            ]
        },
        {
            "text": "菜品备料时的先后顺序应该如何安排？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "先处理不易变质的，再处理易变质的", "is_correct": True},
                {"label": "B", "text": "随便处理", "is_correct": False},
                {"label": "C", "text": "先易后难", "is_correct": False},
                {"label": "D", "text": "先难后易", "is_correct": False}
            ]
        },
        {
            "text": "烹饪过程中试味时，正确的做法是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "skill",
            "options": [
                {"label": "A", "text": "使用专用试味勺，用后清洗", "is_correct": True},
                {"label": "B", "text": "直接用炒勺尝", "is_correct": False},
                {"label": "C", "text": "用手指蘸一点", "is_correct": False},
                {"label": "D", "text": "不需要试味", "is_correct": False}
            ]
        },
        {
            "text": "面点制作时，发酵的温度和湿度控制很重要。理想条件是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "温度28-30°C，湿度75-80%", "is_correct": True},
                {"label": "B", "text": "温度40-50°C，湿度50%", "is_correct": False},
                {"label": "C", "text": "温度15-20°C，湿度90%", "is_correct": False},
                {"label": "D", "text": "随便什么温度湿度", "is_correct": False}
            ]
        },
        {
            "text": "炖煮菜品时，应该什么时候加盐？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "出锅前调味，保持食材鲜嫩", "is_correct": True},
                {"label": "B", "text": "一开始就加", "is_correct": False},
                {"label": "C", "text": "中途加", "is_correct": False},
                {"label": "D", "text": "不用加盐", "is_correct": False}
            ]
        },
        {
            "text": "凉拌菜制作时，最重要的食品安全要求是什么？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "所有食材必须清洗干净", "is_correct": True},
                {"label": "B", "text": "使用专用凉菜间和工具", "is_correct": True},
                {"label": "C", "text": "现做现吃，不长时间存放", "is_correct": True},
                {"label": "D", "text": "可以提前一天做好", "is_correct": False}
            ]
        },
        {
            "text": "菜品出锅后多久内必须送到客人桌上？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "3-5分钟内", "is_correct": True},
                {"label": "B", "text": "10分钟内", "is_correct": False},
                {"label": "C", "text": "15分钟内", "is_correct": False},
                {"label": "D", "text": "什么时候都可以", "is_correct": False}
            ]
        },
        {
            "text": "厨房标准化操作的核心目的是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "skill",
            "options": [
                {"label": "A", "text": "确保每道菜品质稳定，口味一致", "is_correct": True},
                {"label": "B", "text": "限制厨师发挥", "is_correct": False},
                {"label": "C", "text": "节省成本", "is_correct": False},
                {"label": "D", "text": "提高工作难度", "is_correct": False}
            ]
        },

        # === 价值观实践（15道）===
        {
            "text": "厨师长发现员工切菜手法不规范容易受伤，主动停下来示范正确做法。这体现了什么价值观？",
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
            "text": '以下哪些行为体现了"以勤劳者为本"的价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "主动承担重活累活", "is_correct": True},
                {"label": "B", "text": "工作时间认真负责，不偷懒", "is_correct": True},
                {"label": "C", "text": "主动学习新菜品和技能", "is_correct": True},
                {"label": "D", "text": "能躲就躲，少干活", "is_correct": False}
            ]
        },
        {
            "text": "备菜员发现食材有问题，立即停止使用并上报，避免了食品安全事故。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "帮助顾客", "is_correct": True},
                {"label": "B", "text": "以勤劳者为本", "is_correct": False},
                {"label": "C", "text": "高效协作", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '关于"帮助顾客"价值观，厨房员工应该如何践行？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "严格把控食品安全和卫生", "is_correct": True},
                {"label": "B", "text": "确保菜品质量稳定可口", "is_correct": True},
                {"label": "C", "text": "快速出餐，不让客人久等", "is_correct": True},
                {"label": "D", "text": "随便做做能吃就行", "is_correct": False}
            ]
        },
        {
            "text": "高峰期，洗碗员主动帮助传菜和清理后厨。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "高效协作", "is_correct": True},
                {"label": "B", "text": "帮助顾客", "is_correct": False},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": '以下哪些行为违背了"高效协作"的价值观？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "各岗位各干各的，互不配合", "is_correct": True},
                {"label": "B", "text": "用完公共工具不清洁不归位", "is_correct": True},
                {"label": "C", "text": "交接班时不交代重要信息", "is_correct": True},
                {"label": "D", "text": "主动帮助其他岗位", "is_correct": False}
            ]
        },
        {
            "text": "老员工耐心教导新员工刀工技巧和安全注意事项。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": False},
                {"label": "C", "text": "以勤劳者为本", "is_correct": False},
                {"label": "D", "text": "帮助顾客", "is_correct": False}
            ]
        },
        {
            "text": '关于"平等透明"价值观，以下哪些做法是正确的？',
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "对新老员工一视同仁", "is_correct": True},
                {"label": "B", "text": "发现问题及时沟通，不隐瞒", "is_correct": True},
                {"label": "C", "text": "勇于承认错误并改正", "is_correct": True},
                {"label": "D", "text": "拉帮结派，排挤他人", "is_correct": False}
            ]
        },
        {
            "text": "厨师不小心做错了菜，主动承认并重新制作。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "平等透明", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": False},
                {"label": "C", "text": "帮助顾客", "is_correct": False},
                {"label": "D", "text": "以勤劳者为本", "is_correct": False}
            ]
        },
        {
            "text": "厨房工作中，团队精神最重要的体现是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_collaboration",
            "options": [
                {"label": "A", "text": "各岗位紧密配合，确保出餐顺畅", "is_correct": True},
                {"label": "B", "text": "只管自己的事", "is_correct": False},
                {"label": "C", "text": "互相推卸责任", "is_correct": False},
                {"label": "D", "text": "各自为战", "is_correct": False}
            ]
        },
        {
            "text": "发现同事操作不当可能引发安全隐患，应该怎么做？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_transparency",
            "options": [
                {"label": "A", "text": "立即制止并友善提醒正确做法", "is_correct": True},
                {"label": "B", "text": "视而不见", "is_correct": False},
                {"label": "C", "text": "背后向领导打小报告", "is_correct": False},
                {"label": "D", "text": "嘲笑同事不专业", "is_correct": False}
            ]
        },
        {
            "text": "面对客人的特殊饮食要求（如过敏、忌口），厨房应该持什么态度？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "认真对待，严格按要求制作", "is_correct": True},
                {"label": "B", "text": "觉得麻烦就拒绝", "is_correct": False},
                {"label": "C", "text": "随便做做", "is_correct": False},
                {"label": "D", "text": "不当回事", "is_correct": False}
            ]
        },
        {
            "text": "厨房主管分配工作时，小张主动要求做最累的备菜工作。这体现了什么价值观？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "easy",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "以勤劳者为本", "is_correct": True},
                {"label": "B", "text": "高效协作", "is_correct": False},
                {"label": "C", "text": "帮助顾客", "is_correct": False},
                {"label": "D", "text": "平等透明", "is_correct": False}
            ]
        },
        {
            "text": "一个优秀的厨房员工应该具备哪些品质？",
            "question_type": QuestionType.MULTIPLE_CHOICE,
            "difficulty": "medium",
            "category": "value_diligence",
            "options": [
                {"label": "A", "text": "勤奋敬业，不怕脏累", "is_correct": True},
                {"label": "B", "text": "食品安全意识强", "is_correct": True},
                {"label": "C", "text": "团队协作精神好", "is_correct": True},
                {"label": "D", "text": "只求完成任务不求质量", "is_correct": False}
            ]
        },
        {
            "text": "厨房工作的核心使命是什么？",
            "question_type": QuestionType.SINGLE_CHOICE,
            "difficulty": "medium",
            "category": "value_customer",
            "options": [
                {"label": "A", "text": "为客人提供安全、美味、满意的菜品", "is_correct": True},
                {"label": "B", "text": "完成工作任务", "is_correct": False},
                {"label": "C", "text": "听从领导安排", "is_correct": False},
                {"label": "D", "text": "挣钱养家", "is_correct": False}
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
            print(f"[{i}/{len(questions)}] 已插入题目：{q_data['content'][:40]}...")

        print(f"\n✅ 成功插入 {inserted_count} 道厨房批次3题目！")

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
        print(f"- 简单：{easy}道")
        print(f"- 中等：{medium}道")
        print(f"- 困难：{hard}道")
        print(f"\n类别分布：")
        print(f"- 技能类：{skill}道")
        print(f"- 价值观（勤劳）：{value_diligence}道")
        print(f"- 价值观（顾客）：{value_customer}道")
        print(f"- 价值观（协作）：{value_collaboration}道")
        print(f"- 价值观（透明）：{value_transparency}道")

    except Exception as e:
        db.rollback()
        print(f"❌ 插入题目失败：{str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("开始生成厨房批次3题目（60道）...")
    create_questions()
    print("\n厨房批次3题目生成完成！")
