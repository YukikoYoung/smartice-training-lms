"""
系统统计API路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from ..core.database import get_db
from ..core.security import get_current_user
from ..models.user import User
from ..models.course import Course
from ..models.exam import Exam
from ..models.learning import CourseProgress, ExamRecord, LearningStatus, ExamStatus

router = APIRouter(prefix="/api/stats", tags=["statistics"])


@router.get("/dashboard")
def get_dashboard_stats_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取管理后台仪表板统计数据

    返回:
    - total_users: 总用户数
    - active_users: 活跃用户数（最近7天有登录活动）
    - total_courses: 总课程数
    - total_exams: 总考试数
    - total_questions: 总题目数
    - completion_rate: 课程完成率（所有已完成课程 / 所有课程进度记录）
    - average_score: 平均考试分数（所有已完成考试的平均分）
    """
    from ..models.exam import Question

    # 总用户数
    total_users = db.query(User).count()

    # 活跃用户数（简化版：所有启用的用户）
    # TODO: 如果有last_login字段，可以改为最近7天登录的用户
    active_users = db.query(User).filter(User.is_active == True).count()

    # 总课程数
    total_courses = db.query(Course).count()

    # 总考试数
    total_exams = db.query(Exam).count()

    # 总题目数
    total_questions = db.query(Question).count()

    # 课程完成率
    total_progress_records = db.query(CourseProgress).count()
    if total_progress_records > 0:
        completed_courses = (
            db.query(CourseProgress)
            .filter(CourseProgress.status == LearningStatus.COMPLETED)
            .count()
        )
        completion_rate = round((completed_courses / total_progress_records) * 100, 1)
    else:
        completion_rate = 0.0

    # 平均考试分数（统计所有已提交的考试：passed, failed, pending_retake）
    avg_score_result = (
        db.query(func.avg(ExamRecord.score))
        .filter(
            ExamRecord.status.in_([ExamStatus.PASSED, ExamStatus.FAILED, ExamStatus.PENDING_RETAKE]),
            ExamRecord.score.isnot(None)
        )
        .scalar()
    )
    average_score = round(float(avg_score_result), 1) if avg_score_result else 0.0

    # 本周新增数据（奖励统计）
    week_ago = datetime.utcnow() - timedelta(days=7)

    new_users_this_week = (
        db.query(User).filter(User.created_at >= week_ago).count()
    )

    completed_exams_this_week = (
        db.query(ExamRecord)
        .filter(
            ExamRecord.status.in_([ExamStatus.PASSED, ExamStatus.FAILED, ExamStatus.PENDING_RETAKE]),
            ExamRecord.submitted_at >= week_ago
        )
        .count()
    )

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_courses": total_courses,
        "total_exams": total_exams,
        "total_questions": total_questions,
        "completion_rate": completion_rate,
        "average_score": average_score,
        "new_users_this_week": new_users_this_week,
        "completed_exams_this_week": completed_exams_this_week,
    }


@router.get("/learning-overview")
def get_learning_overview_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取学习概览统计

    返回各职级的学习完成情况、各课程的学习人数等
    """
    # 按职级统计学习进度
    role_stats = (
        db.query(
            User.role,
            func.count(CourseProgress.id).label("total_enrollments"),
        )
        .join(CourseProgress, User.id == CourseProgress.user_id)
        .group_by(User.role)
        .all()
    )

    role_completion = []
    for role, total in role_stats:
        # 统计该职级已完成的课程数
        completed = (
            db.query(func.count(CourseProgress.id))
            .join(User, CourseProgress.user_id == User.id)
            .filter(User.role == role)
            .filter(CourseProgress.status == LearningStatus.COMPLETED)
            .scalar()
        ) or 0

        role_completion.append({
            "role": role,
            "total_enrollments": total,
            "completed": completed,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 1),
        })

    # 按课程统计学习人数
    course_stats = (
        db.query(
            Course.id,
            Course.title,
            Course.category,
            func.count(CourseProgress.id).label("enrollments"),
        )
        .join(CourseProgress, Course.id == CourseProgress.course_id)
        .group_by(Course.id, Course.title, Course.category)
        .all()
    )

    course_popularity = []
    for course_id, title, category, enrollments in course_stats:
        # 统计该课程已完成的学习数
        completed = (
            db.query(func.count(CourseProgress.id))
            .filter(CourseProgress.course_id == course_id)
            .filter(CourseProgress.status == LearningStatus.COMPLETED)
            .scalar()
        ) or 0

        course_popularity.append({
            "title": title,
            "category": category,
            "enrollments": enrollments,
            "completed": completed,
            "completion_rate": round((completed / enrollments * 100) if enrollments > 0 else 0, 1),
        })

    return {
        "role_completion": role_completion,
        "course_popularity": course_popularity,
    }


@router.get("/exam-performance")
def get_exam_performance_api(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取考试表现统计

    返回各考试的通过率、平均分等
    """
    # 先获取每个考试的基本统计信息
    exam_stats = (
        db.query(
            Exam.id,
            Exam.title,
            Exam.pass_score,
            func.count(ExamRecord.id).label("total_attempts"),
            func.avg(ExamRecord.score).label("avg_score"),
        )
        .join(ExamRecord, Exam.id == ExamRecord.exam_id)
        .filter(ExamRecord.status.in_([ExamStatus.PASSED, ExamStatus.FAILED, ExamStatus.PENDING_RETAKE]))
        .group_by(Exam.id, Exam.title, Exam.pass_score)
        .all()
    )

    exam_performance = []
    for exam_id, title, pass_score, attempts, avg_score in exam_stats:
        # 单独统计该考试的通过次数
        passed_count = (
            db.query(func.count(ExamRecord.id))
            .filter(ExamRecord.exam_id == exam_id)
            .filter(ExamRecord.status == ExamStatus.PASSED)
            .scalar()
        ) or 0

        exam_performance.append({
            "exam_title": title,
            "pass_score": pass_score,
            "total_attempts": attempts,
            "passed_count": passed_count,
            "pass_rate": round((passed_count / attempts * 100) if attempts > 0 else 0, 1),
            "average_score": round(float(avg_score) if avg_score else 0, 1),
        })

    return {"exam_performance": exam_performance}
