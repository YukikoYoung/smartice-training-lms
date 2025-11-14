import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { courseAPI } from '../api';
import { Course } from '../types';
import './CoursesPage.css';

const CoursesPage: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'mandatory' | 'optional'>('all');

  useEffect(() => {
    loadCourses();
  }, []);

  const loadCourses = async () => {
    try {
      setLoading(true);
      setError('');
      const data = await courseAPI.getList();
      setCourses(data);
    } catch (err: any) {
      console.error('加载课程失败:', err);
      setError(err.message || '加载课程失败');
    } finally {
      setLoading(false);
    }
  };

  const filteredCourses = courses.filter((course) => {
    if (filter === 'mandatory') return course.is_mandatory;
    if (filter === 'optional') return !course.is_mandatory;
    return true;
  });

  const getDepartmentLabel = (dept: string) => {
    const labels: Record<string, string> = {
      FRONT_HOUSE: '前厅',
      KITCHEN: '厨房',
      HEADQUARTERS: '总部',
    };
    return labels[dept] || dept;
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>加载课程中...</p>
      </div>
    );
  }

  return (
    <div className="courses-page">
      <div className="page-header">
        <h1>课程中心</h1>
        <p>选择课程开始学习</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={loadCourses} className="btn-retry">
            重试
          </button>
        </div>
      )}

      <div className="filter-tabs">
        <button
          className={`filter-tab ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          全部课程 ({courses.length})
        </button>
        <button
          className={`filter-tab ${filter === 'mandatory' ? 'active' : ''}`}
          onClick={() => setFilter('mandatory')}
        >
          必修课程 ({courses.filter((c) => c.is_mandatory).length})
        </button>
        <button
          className={`filter-tab ${filter === 'optional' ? 'active' : ''}`}
          onClick={() => setFilter('optional')}
        >
          选修课程 ({courses.filter((c) => !c.is_mandatory).length})
        </button>
      </div>

      <div className="courses-grid">
        {filteredCourses.length === 0 ? (
          <div className="empty-state">
            <p>暂无课程</p>
          </div>
        ) : (
          filteredCourses.map((course) => (
            <Link
              key={course.id}
              to={`/courses/${course.id}`}
              className="course-card"
            >
              <div className="course-header">
                <h3 className="course-title">{course.title}</h3>
                <div className="course-badges">
                  {course.is_mandatory && (
                    <span className="badge badge-mandatory">必修</span>
                  )}
                  <span className="badge badge-dept">
                    {getDepartmentLabel(course.department_type)}
                  </span>
                </div>
              </div>

              <p className="course-description">
                {course.description || '暂无描述'}
              </p>

              <div className="course-footer">
                <span className="course-code">{course.code}</span>
                <span className="course-version">v{course.version}</span>
              </div>
            </Link>
          ))
        )}
      </div>
    </div>
  );
};

export default CoursesPage;
