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
    limit: int = Query(20, ge=1, le=100),
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


@router.get("/questions", response_model=List[QuestionResponse])
def get_questions_api(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
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


@router.get("/records", response_model=List)
def get_my_exam_records_api(
    exam_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取我的考试记录

    - **exam_id**: 考试ID（可选，不传则返回所有考试记录）
    """
    from ..schemas.learning import ExamRecordResponse
    records = exam_service.get_exam_records(db, current_user.id, exam_id)
    return records
