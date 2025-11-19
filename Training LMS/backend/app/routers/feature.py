"""
辅助功能API路由
包含: 通知、笔记、错题本、证书、排行榜、搜索、个人资料
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, or_
from typing import List, Optional
from datetime import datetime

from ..core.database import get_db
from ..core.security import get_current_user
from ..models import (
    User, Notification, NotificationType, Note, WrongQuestion,
    Certificate, Question, Course, Chapter, ExamRecord
)

router = APIRouter(prefix="/api/features", tags=["辅助功能"])


# ============= 1. 消息通知 API =============

@router.get("/notifications", summary="获取用户通知列表")
def get_notifications(
    filter_type: Optional[str] = Query("all", description="all/unread/read"),
    category: Optional[str] = Query("all", description="all/system/exam/training/achievement"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的通知列表"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    # 按已读状态筛选
    if filter_type == "unread":
        query = query.filter(Notification.is_read == False)
    elif filter_type == "read":
        query = query.filter(Notification.is_read == True)

    # 按类型筛选
    if category != "all":
        try:
            notification_type = NotificationType(category)
            query = query.filter(Notification.type == notification_type)
        except ValueError:
            pass

    notifications = query.order_by(desc(Notification.created_at)).all()

    # 直接返回数组，字段名使用蛇形命名（与其他API保持一致）
    return [
        {
            "id": n.id,
            "type": n.type.value,
            "title": n.title,
            "content": n.content,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "read_at": n.read_at.isoformat() if n.read_at else None
        }
        for n in notifications
    ]


@router.put("/notifications/{notification_id}/read", summary="标记通知为已读")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """标记指定通知为已读"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="通知不存在")

    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()

    return {"message": "已标记为已读"}


@router.put("/notifications/read-all", summary="全部标记为已读")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """将所有未读通知标记为已读"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True, "read_at": datetime.utcnow()})

    db.commit()
    return {"message": "已全部标记为已读"}


# ============= 2. 学习笔记 API =============

@router.get("/notes", summary="获取用户笔记列表")
def get_notes(
    course_id: Optional[int] = Query(None, description="按课程筛选"),
    search: Optional[str] = Query(None, description="关键词搜索"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的笔记列表"""
    query = db.query(Note).filter(Note.user_id == current_user.id)

    if course_id:
        query = query.filter(Note.course_id == course_id)

    if search:
        query = query.filter(
            or_(
                Note.title.like(f"%{search}%"),
                Note.content.like(f"%{search}%")
            )
        )

    notes = query.order_by(desc(Note.updated_at)).all()

    # 直接返回数组，使用蛇形命名
    return [
        {
            "id": n.id,
            "course_id": n.course_id,
            "course_name": n.course.title if n.course else "",
            "chapter_id": n.chapter_id,
            "chapter_name": n.chapter.title if n.chapter else None,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None
        }
        for n in notes
    ]


@router.post("/notes", summary="创建笔记")
def create_note(
    title: str,
    content: str,
    course_id: int,
    chapter_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新笔记"""
    note = Note(
        user_id=current_user.id,
        course_id=course_id,
        chapter_id=chapter_id,
        title=title,
        content=content
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    return {"message": "笔记创建成功", "note_id": note.id}


@router.put("/notes/{note_id}", summary="更新笔记")
def update_note(
    note_id: int,
    title: str,
    content: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新笔记"""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")

    note.title = title
    note.content = content
    note.updated_at = datetime.utcnow()
    db.commit()

    return {"message": "笔记更新成功"}


@router.delete("/notes/{note_id}", summary="删除笔记")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除笔记"""
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="笔记不存在")

    db.delete(note)
    db.commit()

    return {"message": "笔记删除成功"}


# ============= 3. 错题本 API =============

@router.get("/wrong-questions", summary="获取错题列表")
def get_wrong_questions(
    course_id: Optional[int] = Query(None, description="按课程筛选"),
    show_mastered: bool = Query(False, description="是否显示已掌握"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的错题列表"""
    query = db.query(WrongQuestion).filter(WrongQuestion.user_id == current_user.id)

    if course_id:
        # 通过question的course_id筛选
        query = query.join(Question).filter(Question.course_id == course_id)

    if not show_mastered:
        query = query.filter(WrongQuestion.mastered == False)

    wrong_questions = query.order_by(desc(WrongQuestion.last_wrong_date)).all()

    # 直接返回数组，使用蛇形命名，包含完整的显示信息
    return [
        {
            "id": wq.id,
            "question_id": wq.question_id,
            "course_name": wq.question.course.title if wq.question and wq.question.course else "",
            "question_type": wq.question.question_type.value if wq.question else "",
            "content": wq.question.content if wq.question else "",
            "options": wq.question.options if wq.question and wq.question.options else {},
            "my_answer": wq.my_answer,
            "correct_answer": wq.question.correct_answer if wq.question else "",
            "explanation": wq.question.explanation if wq.question else "",
            "wrong_count": wq.wrong_count,
            "last_wrong_date": wq.last_wrong_date.isoformat() if wq.last_wrong_date else None,
            "mastered": wq.mastered
        }
        for wq in wrong_questions
    ]


@router.put("/wrong-questions/{wrong_question_id}/master", summary="标记错题为已掌握")
def mark_wrong_question_mastered(
    wrong_question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """标记错题为已掌握"""
    wq = db.query(WrongQuestion).filter(
        WrongQuestion.id == wrong_question_id,
        WrongQuestion.user_id == current_user.id
    ).first()

    if not wq:
        raise HTTPException(status_code=404, detail="错题记录不存在")

    wq.mastered = True
    wq.mastered_at = datetime.utcnow()
    db.commit()

    return {"message": "已标记为掌握"}


# ============= 4. 证书 API =============

@router.get("/certificates", summary="获取用户证书列表")
def get_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的证书列表"""
    certificates = db.query(Certificate).filter(
        Certificate.user_id == current_user.id
    ).order_by(desc(Certificate.issued_at)).all()

    # 直接返回数组，使用蛇形命名
    return [
        {
            "id": cert.id,
            "certificate_number": cert.certificate_number,
            "title": cert.title,
            "score": cert.score,
            "issued_at": cert.issued_at.isoformat() if cert.issued_at else None,
            "issuer": cert.issuer
        }
        for cert in certificates
    ]


# ============= 5. 排行榜 API =============

@router.get("/leaderboard", summary="获取学习排行榜")
def get_leaderboard(
    period: str = Query("month", description="week/month/all"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取学习排行榜"""
    # 计算每个用户的学习统计
    user_stats = db.query(
        User.id,
        User.username,
        User.full_name,
        User.role,
        func.count(ExamRecord.id).label("exam_count"),
        func.avg(ExamRecord.score).label("average_score"),
        func.count(Certificate.id).label("certificate_count")
    ).outerjoin(ExamRecord, User.id == ExamRecord.user_id)\
     .outerjoin(Certificate, User.id == Certificate.user_id)\
     .group_by(User.id)\
     .order_by(desc("average_score"))\
     .limit(50)\
     .all()

    # 直接返回数组，使用蛇形命名
    return [
        {
            "rank": idx + 1,
            "user_id": stat.id,
            "username": stat.username,
            "full_name": stat.full_name,
            "role": stat.role.value,
            "exam_count": stat.exam_count or 0,
            "average_score": round(stat.average_score, 1) if stat.average_score else 0,
            "certificate_count": stat.certificate_count or 0
        }
        for idx, stat in enumerate(user_stats)
    ]


# ============= 6. 搜索 API =============

@router.get("/search", summary="全局搜索")
def global_search(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """全局搜索课程、笔记、题目"""
    results = {
        "courses": [],
        "notes": [],
        "questions": []
    }

    # 搜索课程
    courses = db.query(Course).filter(
        or_(
            Course.title.like(f"%{q}%"),
            Course.description.like(f"%{q}%")
        ),
        Course.is_published == True
    ).limit(10).all()

    results["courses"] = [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "type": "course"
        }
        for c in courses
    ]

    # 搜索用户笔记
    notes = db.query(Note).filter(
        Note.user_id == current_user.id,
        or_(
            Note.title.like(f"%{q}%"),
            Note.content.like(f"%{q}%")
        )
    ).limit(10).all()

    results["notes"] = [
        {
            "id": n.id,
            "title": n.title,
            "content": n.content[:100] + "..." if len(n.content) > 100 else n.content,
            "type": "note"
        }
        for n in notes
    ]

    # 搜索题目
    questions = db.query(Question).filter(
        or_(
            Question.content.like(f"%{q}%"),
            Question.explanation.like(f"%{q}%")
        )
    ).limit(10).all()

    results["questions"] = [
        {
            "id": que.id,
            "content": que.content,
            "type": "question"
        }
        for que in questions
    ]

    return results


# ============= 7. 个人资料 API =============

@router.get("/profile", summary="获取个人资料")
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的个人资料 - 使用蛇形命名"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "phone": current_user.phone,
        "role": current_user.role.value,
        "department_type": current_user.department_type.value if current_user.department_type else None,
        "position": current_user.position.name if current_user.position else None,
        "store": current_user.store.name if current_user.store else None,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }


@router.put("/profile", summary="更新个人资料")
def update_profile(
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新个人资料（仅允许修改姓名和电话）"""
    if full_name:
        current_user.full_name = full_name

    if phone:
        # 检查手机号是否已被使用
        existing_user = db.query(User).filter(
            User.phone == phone,
            User.id != current_user.id
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="该手机号已被使用")

        current_user.phone = phone

    db.commit()

    return {"message": "个人资料更新成功"}
