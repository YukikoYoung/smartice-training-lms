import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { courseAPI } from '../api';
import { learningAPI } from '../api';
import { Course, CourseProgress } from '../types';
import './CourseDetailPage.css';

const CourseDetailPage: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();

  const [course, setCourse] = useState<Course | null>(null);
  const [progress, setProgress] = useState<CourseProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (courseId) {
      loadCourseDetail();
    }
  }, [courseId]);

  const loadCourseDetail = async () => {
    if (!courseId) return;

    try {
      setLoading(true);
      setError('');

      const [courseData, progressData] = await Promise.all([
        courseAPI.getDetail(parseInt(courseId)),
        learningAPI.getCourseProgress(parseInt(courseId)).catch(() => null),
      ]);

      setCourse(courseData);
      setProgress(progressData);
    } catch (err: any) {
      console.error('加载课程详情失败:', err);
      setError(err.message || '加载课程详情失败');
    } finally {
      setLoading(false);
    }
  };

  const handleStartCourse = async () => {
    if (!courseId) return;

    try {
      setStarting(true);
      setError('');

      await learningAPI.startCourse(parseInt(courseId));

      // 重新加载进度数据
      await loadCourseDetail();

      alert('课程已开始！可以点击章节开始学习');
    } catch (err: any) {
      console.error('开始课程失败:', err);
      setError(err.message || '开始课程失败');
    } finally {
      setStarting(false);
    }
  };

  const handleChapterClick = (chapterId: number) => {
    // TODO: 实现章节学习页面跳转
    alert(`章节 ${chapterId} 学习功能开发中...`);
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>加载课程详情中...</p>
      </div>
    );
  }

  if (error && !course) {
    return (
      <div className="page-error">
        <div className="alert alert-error">
          {error}
          <button onClick={loadCourseDetail} className="btn-retry">
            重试
          </button>
        </div>
        <button onClick={() => navigate('/courses')} className="btn-secondary">
          返回课程列表
        </button>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="page-error">
        <p>课程不存在</p>
        <button onClick={() => navigate('/courses')} className="btn-secondary">
          返回课程列表
        </button>
      </div>
    );
  }

  return (
    <div className="course-detail-page">
      <button onClick={() => navigate('/courses')} className="btn-back">
        ← 返回课程列表
      </button>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="course-info-card">
        <div className="course-info-header">
          <div>
            <h1 className="course-info-title">{course.title}</h1>
            <div className="course-meta">
              <span className="course-code">{course.code}</span>
              <span className="separator">•</span>
              <span>v{course.version}</span>
              {course.is_mandatory && (
                <>
                  <span className="separator">•</span>
                  <span className="mandatory-tag">必修课程</span>
                </>
              )}
            </div>
          </div>

          {!progress || progress.status === 'not_started' ? (
            <button
              onClick={handleStartCourse}
              className="btn-primary btn-large"
              disabled={starting}
            >
              {starting ? '开始中...' : '开始学习'}
            </button>
          ) : (
            <div className="progress-summary">
              <div className="progress-bar-container">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${progress.progress_percentage}%` }}
                ></div>
              </div>
              <p className="progress-text">
                已完成 {progress.completed_chapters}/{progress.total_chapters} 章节
                ({Math.round(progress.progress_percentage)}%)
              </p>
            </div>
          )}
        </div>

        {course.description && (
          <p className="course-description">{course.description}</p>
        )}
      </div>

      <div className="chapters-section">
        <h2 className="section-title">课程章节</h2>

        {!course.chapters || course.chapters.length === 0 ? (
          <div className="empty-state">
            <p>暂无章节内容</p>
          </div>
        ) : (
          <div className="chapters-list">
            {course.chapters.map((chapter, index) => (
              <div
                key={chapter.id}
                className="chapter-card"
                onClick={() => handleChapterClick(chapter.id)}
              >
                <div className="chapter-number">{index + 1}</div>
                <div className="chapter-content">
                  <h3 className="chapter-title">{chapter.title}</h3>
                  {chapter.description && (
                    <p className="chapter-description">{chapter.description}</p>
                  )}
                  <div className="chapter-meta">
                    {chapter.estimated_duration && (
                      <span>预计 {chapter.estimated_duration} 分钟</span>
                    )}
                    {chapter.has_quiz && (
                      <>
                        <span className="separator">•</span>
                        <span className="quiz-tag">包含测验</span>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CourseDetailPage;
