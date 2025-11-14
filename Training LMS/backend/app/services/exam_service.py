"""
考试系统业务逻辑（含补考逻辑）
"""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from ..models.exam import Exam, Question
from ..models.learning import ExamRecord, ExamStatus
from ..schemas.exam import (
    ExamCreate, ExamUpdate,
    QuestionCreate, QuestionUpdate,
    ExamSubmit, AnswerSubmit
)


# ========== Exam CRUD ==========

def create_exam(db: Session, exam_data: ExamCreate, creator_id: int) -> Exam:
    """创建考试"""
    exam = Exam(
        **exam_data.model_dump(),
        created_by=creator_id
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def get_exam_by_id(db: Session, exam_id: int) -> Optional[Exam]:
    """根据ID获取考试"""
    return db.query(Exam).filter(Exam.id == exam_id).first()


def get_exams(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    is_active: Optional[bool] = None,
    is_published: Optional[bool] = None,
    exam_type: Optional[str] = None,
    course_id: Optional[int] = None
) -> List[Exam]:
    """获取考试列表"""
    query = db.query(Exam)

    if is_active is not None:
        query = query.filter(Exam.is_active == is_active)
    if is_published is not None:
        query = query.filter(Exam.is_published == is_published)
    if exam_type:
        query = query.filter(Exam.exam_type == exam_type)
    if course_id:
        query = query.filter(Exam.course_id == course_id)

    return query.offset(skip).limit(limit).all()


def update_exam(db: Session, exam_id: int, exam_data: ExamUpdate) -> Exam:
    """更新考试"""
    exam = get_exam_by_id(db, exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考试 ID {exam_id} 不存在"
        )

    for field, value in exam_data.model_dump(exclude_unset=True).items():
        setattr(exam, field, value)

    db.commit()
    db.refresh(exam)
    return exam


def delete_exam(db: Session, exam_id: int) -> bool:
    """删除考试"""
    exam = get_exam_by_id(db, exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考试 ID {exam_id} 不存在"
        )

    db.delete(exam)
    db.commit()
    return True


def publish_exam(db: Session, exam_id: int) -> Exam:
    """发布考试"""
    exam = get_exam_by_id(db, exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考试 ID {exam_id} 不存在"
        )

    if exam.is_published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="考试已发布"
        )

    exam.is_published = True
    exam.published_at = datetime.utcnow()
    db.commit()
    db.refresh(exam)
    return exam


# ========== Question CRUD ==========

def create_question(db: Session, question_data: QuestionCreate, creator_id: int) -> Question:
    """创建题目"""
    question = Question(
        **question_data.model_dump(),
        created_by=creator_id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question_by_id(db: Session, question_id: int) -> Optional[Question]:
    """根据ID获取题目"""
    return db.query(Question).filter(Question.id == question_id).first()


def get_questions(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    question_type: Optional[str] = None,
    category: Optional[str] = None,
    course_id: Optional[int] = None,
    chapter_id: Optional[int] = None
) -> List[Question]:
    """获取题目列表"""
    query = db.query(Question).filter(Question.is_active == True)

    if question_type:
        query = query.filter(Question.question_type == question_type)
    if category:
        query = query.filter(Question.category == category)
    if course_id:
        query = query.filter(Question.course_id == course_id)
    if chapter_id:
        query = query.filter(Question.chapter_id == chapter_id)

    return query.offset(skip).limit(limit).all()


def update_question(db: Session, question_id: int, question_data: QuestionUpdate) -> Question:
    """更新题目"""
    question = get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"题目 ID {question_id} 不存在"
        )

    for field, value in question_data.model_dump(exclude_unset=True).items():
        setattr(question, field, value)

    db.commit()
    db.refresh(question)
    return question


def delete_question(db: Session, question_id: int) -> bool:
    """删除题目"""
    question = get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"题目 ID {question_id} 不存在"
        )

    db.delete(question)
    db.commit()
    return True


# ========== 考试答题相关 ==========

def start_exam(db: Session, user_id: int, exam_id: int) -> ExamRecord:
    """开始考试"""
    exam = get_exam_by_id(db, exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考试 ID {exam_id} 不存在"
        )

    if not exam.is_published or not exam.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="考试未发布或已禁用"
        )

    # 检查用户是否可以参加考试
    existing_records = db.query(ExamRecord).filter(
        ExamRecord.user_id == user_id,
        ExamRecord.exam_id == exam_id
    ).order_by(ExamRecord.attempt_number.desc()).all()

    # 计算当前是第几次考试
    attempt_number = len(existing_records) + 1

    # 检查是否超过最大尝试次数
    if attempt_number > exam.max_attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"已达到最大考试次数 {exam.max_attempts}"
        )

    # 检查是否在补考冷却期内
    if existing_records:
        last_record = existing_records[0]
        if last_record.next_retake_at and last_record.next_retake_at > datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"补考冷却期未过，下次可考时间：{last_record.next_retake_at}"
            )

    # 创建考试记录
    exam_record = ExamRecord(
        user_id=user_id,
        exam_id=exam_id,
        attempt_number=attempt_number,
        status=ExamStatus.IN_PROGRESS,
        total_questions=exam.total_questions,
        started_at=datetime.utcnow()
    )
    db.add(exam_record)
    db.commit()
    db.refresh(exam_record)
    return exam_record


def submit_exam(db: Session, user_id: int, exam_submit: ExamSubmit) -> Dict[str, Any]:
    """提交考试并自动判分（含补考逻辑）"""
    exam = get_exam_by_id(db, exam_submit.exam_id)
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"考试 ID {exam_submit.exam_id} 不存在"
        )

    # 获取当前考试记录
    exam_record = db.query(ExamRecord).filter(
        ExamRecord.user_id == user_id,
        ExamRecord.exam_id == exam_submit.exam_id,
        ExamRecord.status == ExamStatus.IN_PROGRESS
    ).order_by(ExamRecord.attempt_number.desc()).first()

    if not exam_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未找到进行中的考试记录"
        )

    # 自动判分
    correct_count = 0
    answer_details = []

    for answer in exam_submit.answers:
        question = get_question_by_id(db, answer.question_id)
        if not question:
            continue

        is_correct = check_answer(question, answer.user_answer)
        if is_correct:
            correct_count += 1

        answer_details.append({
            "question_id": answer.question_id,
            "user_answer": answer.user_answer,
            "is_correct": is_correct
        })

    # 计算成绩
    score = (correct_count / exam.total_questions) * 100 if exam.total_questions > 0 else 0
    passed = score >= exam.pass_score

    # 更新考试记录
    exam_record.score = score
    exam_record.correct_answers = correct_count
    exam_record.answers = answer_details
    exam_record.submitted_at = datetime.utcnow()
    exam_record.graded_at = datetime.utcnow()
    exam_record.status = ExamStatus.PASSED if passed else ExamStatus.FAILED

    # ========== 补考逻辑 ==========
    if not passed and exam.allow_retake:
        # 检查是否还有补考机会
        if exam_record.attempt_number < exam.max_attempts:
            exam_record.can_retake = True
            # 计算下次可补考时间 = 当前时间 + 冷却期
            exam_record.next_retake_at = datetime.utcnow() + timedelta(days=exam.retake_cooldown_days)
            exam_record.status = ExamStatus.PENDING_RETAKE
        else:
            exam_record.can_retake = False
            exam_record.next_retake_at = None
    else:
        exam_record.can_retake = False
        exam_record.next_retake_at = None

    db.commit()
    db.refresh(exam_record)

    return {
        "exam_record_id": exam_record.id,
        "exam_id": exam.id,
        "exam_title": exam.title,
        "score": score,
        "passed": passed,
        "attempt_number": exam_record.attempt_number,
        "max_attempts": exam.max_attempts,
        "can_retake": exam_record.can_retake,
        "next_retake_at": exam_record.next_retake_at,
        "correct_count": correct_count,
        "total_questions": exam.total_questions,
        "time_spent": exam_submit.time_spent
    }


def check_answer(question: Question, user_answer: str) -> bool:
    """检查答案是否正确"""
    if question.question_type.value == "single_choice":
        # 单选题：从options中找正确答案
        if question.options:
            for option in question.options:
                if option.get("is_correct") and option.get("label") == user_answer:
                    return True
        return False

    elif question.question_type.value == "multiple_choice":
        # 多选题：用户答案需要完全匹配所有正确选项
        if question.options:
            correct_labels = [opt["label"] for opt in question.options if opt.get("is_correct")]
            user_labels = sorted(user_answer.split(","))
            return sorted(correct_labels) == user_labels
        return False

    elif question.question_type.value == "true_false":
        # 判断题：使用correct_answer字段
        return question.correct_answer == user_answer

    else:
        # 简答题暂不支持自动判分
        return False


def get_exam_records(db: Session, user_id: int, exam_id: Optional[int] = None) -> List[ExamRecord]:
    """获取用户的考试记录"""
    query = db.query(ExamRecord).filter(ExamRecord.user_id == user_id)

    if exam_id:
        query = query.filter(ExamRecord.exam_id == exam_id)

    return query.order_by(ExamRecord.created_at.desc()).all()
