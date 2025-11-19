"""
考试系统API路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..schemas.exam import (
    ExamCreate, ExamUpdate, ExamResponse, ExamListResponse,
    QuestionCreate, QuestionUpdate, QuestionResponse,
    ExamSubmit, ExamResult
)
from ..schemas.learning import ExamRecordResponse
from ..services import exam_service

router = APIRouter(prefix="/api/exams", tags=["exams"])


# ========== Exam API ==========

@router.post("/", response_model=ExamResponse, status_code=201)
def create_exam_api(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建考试

    - **title**: 考试标题
    - **exam_type**: 考试类型
    - **total_questions**: 总题数
    - **pass_score**: 及格分数
    - **allow_retake**: 是否允许补考
    - **max_attempts**: 最大考试次数
    - **retake_cooldown_days**: 补考冷却期（天）
    """
    return exam_service.create_exam(db, exam_data, current_user.id)


@router.get("/", response_model=List[ExamListResponse])
def get_exams_api(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=200),
    is_active: Optional[bool] = None,
    is_published: Optional[bool] = None,
    exam_type: Optional[str] = None,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取考试列表

    - **skip**: 跳过记录数
    - **limit**: 每页记录数
    - **is_active**: 是否启用
    - **is_published**: 是否已发布
    - **exam_type**: 考试类型筛选
    - **course_id**: 课程ID筛选
    """
    return exam_service.get_exams(db, skip, limit, is_active, is_published, exam_type, course_id)


@router.get("/records", response_model=List[ExamRecordResponse])
def get_my_exam_records_api(
    exam_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的考试记录

    - **exam_id**: 考试ID（可选，不传则返回所有考试记录）
    """
    records = exam_service.get_exam_records(db, current_user.id, exam_id)
    return records


# ========== Question API ==========

@router.post("/questions", response_model=QuestionResponse, status_code=201)
def create_question_api(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建题目

    - **content**: 题目内容
    - **question_type**: 题目类型（single_choice/multiple_choice/true_false/short_answer）
    - **category**: 题目分类（skill/value_*）
    - **options**: 选项列表（选择题必填）
    - **correct_answer**: 正确答案（判断题必填）
    - **explanation**: 答案解析
    """
    return exam_service.create_question(db, question_data, current_user.id)


@router.get("/questions/count")
def get_questions_count_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取题目总数
    """
    from ..models.exam import Question
    count = db.query(Question).count()
    return {"count": count}


@router.get("/questions", response_model=List[QuestionResponse])
def get_questions_api(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),  # 提高到1000以支持大题库
    question_type: Optional[str] = None,
    category: Optional[str] = None,
    course_id: Optional[int] = None,
    chapter_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取题目列表

    - **skip**: 跳过记录数
    - **limit**: 每页记录数
    - **question_type**: 题目类型筛选
    - **category**: 分类筛选
    - **course_id**: 课程ID筛选
    - **chapter_id**: 章节ID筛选
    """
    return exam_service.get_questions(db, skip, limit, question_type, category, course_id, chapter_id)


@router.get("/questions/{question_id}", response_model=QuestionResponse)
def get_question_api(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取题目详情

    - **question_id**: 题目ID
    """
    question = exam_service.get_question_by_id(db, question_id)
    if not question:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="题目不存在")
    return question


@router.put("/questions/{question_id}", response_model=QuestionResponse)
def update_question_api(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新题目

    - **question_id**: 题目ID
    """
    return exam_service.update_question(db, question_id, question_data)


@router.delete("/questions/{question_id}")
def delete_question_api(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除题目

    - **question_id**: 题目ID
    """
    exam_service.delete_question(db, question_id)
    return {"message": "题目删除成功"}


@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取考试详情

    - **exam_id**: 考试ID
    """
    exam = exam_service.get_exam_by_id(db, exam_id)
    if not exam:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="考试不存在")
    return exam


@router.put("/{exam_id}", response_model=ExamResponse)
def update_exam_api(
    exam_id: int,
    exam_data: ExamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新考试

    - **exam_id**: 考试ID
    """
    return exam_service.update_exam(db, exam_id, exam_data)


@router.delete("/{exam_id}")
def delete_exam_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除考试

    - **exam_id**: 考试ID
    """
    exam_service.delete_exam(db, exam_id)
    return {"message": "考试删除成功"}


@router.post("/{exam_id}/publish", response_model=ExamResponse)
def publish_exam_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    发布考试

    - **exam_id**: 考试ID
    """
    return exam_service.publish_exam(db, exam_id)



# ========== 考试答题API ==========

@router.post("/{exam_id}/start")
def start_exam_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    开始考试

    - 创建考试记录
    - 检查补考冷却期
    - 检查最大尝试次数
    - 返回题目列表

    - **exam_id**: 考试ID
    """
    exam_record = exam_service.start_exam(db, current_user.id, exam_id)

    # 获取考试对象
    exam = exam_service.get_exam_by_id(db, exam_id)

    # 获取题目列表
    questions = []
    if exam and exam.question_ids:
        from ..models.exam import Question
        questions = db.query(Question).filter(Question.id.in_(exam.question_ids)).all()

        # 转换 options 格式（从字典转为列表，并统一字段名）
        for q in questions:
            if q.options:
                if isinstance(q.options, dict):
                    # 字典格式: {'A': '选项内容', 'B': '...'}
                    # 转换为列表格式: [{"label": "A", "content": "选项内容", "is_correct": False}, ...]
                    q.options = [
                        {"label": key, "content": value, "is_correct": False}
                        for key, value in q.options.items()
                    ]
                elif isinstance(q.options, list):
                    # 统一字段名：将 "text" 改为 "content"
                    for option in q.options:
                        if "text" in option and "content" not in option:
                            option["content"] = option.pop("text")

        # 转换为响应格式
        from ..schemas.exam import QuestionResponse
        questions = [QuestionResponse.from_orm(q) for q in questions]

    return {
        "exam_record_id": exam_record.id,
        "exam_id": exam_record.exam_id,
        "attempt_number": exam_record.attempt_number,
        "started_at": exam_record.started_at,
        "questions": questions,
        "message": "考试已开始"
    }


@router.post("/submit", response_model=ExamResult)
def submit_exam_api(
    exam_submit: ExamSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    提交考试并自动判分

    - 自动判分
    - 计算成绩
    - 判断是否通过
    - **自动计算补考逻辑**：
      - 如果未通过且允许补考
      - 自动计算next_retake_at（当前时间 + 冷却期）
      - 判断是否还有补考机会

    - **exam_id**: 考试ID
    - **answers**: 答题列表
    - **time_spent**: 答题耗时（秒）
    """
    return exam_service.submit_exam(db, current_user.id, exam_submit)


@router.get("/{exam_id}/result")
def get_exam_result_detail_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的考试详细成绩（最近一次）

    返回详细的答题情况，包括：
    - 总分、得分、是否通过
    - 每道题的详细信息（题目、选项、用户答案、正确答案、是否正确、解析）

    - **exam_id**: 考试ID
    """
    from ..models.learning import ExamRecord
    from ..models.exam import Question, Exam
    from fastapi import HTTPException, status

    # 获取用户最近一次的考试记录
    record = (
        db.query(ExamRecord)
        .filter(
            ExamRecord.exam_id == exam_id,
            ExamRecord.user_id == current_user.id,
            ExamRecord.status == "completed"
        )
        .order_by(ExamRecord.completed_at.desc())
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="未找到该考试的成绩记录"
        )

    # 获取考试信息
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="考试不存在"
        )

    # 构建答题详情
    question_details = []
    if record.answers:
        for answer_item in record.answers:
            question_id = answer_item.get("question_id")
            question = db.query(Question).filter(Question.id == question_id).first()

            if question:
                question_details.append({
                    "question_id": question.id,
                    "content": question.content,
                    "question_type": question.question_type.value,
                    "options": question.options,
                    "user_answer": answer_item.get("user_answer"),
                    "correct_answer": question.correct_answer,
                    "is_correct": answer_item.get("is_correct", False),
                    "explanation": question.explanation,
                    "category": question.category,
                })

    return {
        "exam_id": exam.id,
        "exam_title": exam.title,
        "user_id": current_user.id,
        "username": current_user.username,
        "score": record.score,
        "total_score": exam.total_score,
        "passed": record.passed,
        "pass_score": exam.pass_score,
        "attempt_number": record.attempt_number,
        "total_questions": record.total_questions,
        "correct_answers": record.correct_answers,
        "started_at": record.started_at.isoformat() if record.started_at else None,
        "submitted_at": record.submitted_at.isoformat() if record.submitted_at else None,
        "time_spent_seconds": (
            int((record.submitted_at - record.started_at).total_seconds())
            if record.started_at and record.submitted_at
            else None
        ),
        "question_details": question_details,
        "can_retake": (
            record.attempt_number < exam.max_attempts
            if exam.allow_retake and exam.max_attempts
            else False
        ),
        "next_retake_at": (
            record.next_retake_at.isoformat() if record.next_retake_at else None
        ),
    }


@router.get("/{exam_id}/results")
def get_exam_results_api(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取考试成绩列表（用于管理后台导出）

    - **exam_id**: 考试ID
    """
    from ..models.learning import ExamRecord
    from ..models.user import User as UserModel

    records = db.query(ExamRecord).filter(ExamRecord.exam_id == exam_id).all()

    results = []
    for record in records:
        user = db.query(UserModel).filter(UserModel.id == record.user_id).first()
        results.append({
            "exam_id": record.exam_id,
            "user_id": record.user_id,
            "username": user.username if user else "Unknown",
            "score": record.score,
            "passed": record.passed,
            "attempt_number": record.attempt_number,
            "completed_at": record.completed_at.isoformat() if record.completed_at else None
        })

    return results
