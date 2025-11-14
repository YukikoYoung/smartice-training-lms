import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { learningAPI } from '../api';
import { examAPI } from '../api';
import { CourseProgress, ExamRecord, LearningStats } from '../types';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [courseProgress, setCourseProgress] = useState<CourseProgress[]>([]);
  const [examRecords, setExamRecords] = useState<ExamRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');

      const [statsData, progressData, recordsData] = await Promise.all([
        learningAPI.getStats(),
        learningAPI.getCourseProgress(), // 不传参数获取所有课程进度
        examAPI.getRecords(),
      ]);

      setStats(statsData);
      setCourseProgress(progressData);
      setExamRecords(recordsData);
    } catch (err: any) {
      console.error('加载学习数据失败:', err);
      setError(err.message || '加载学习数据失败');
    } finally {
      setLoading(false);
    }
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      not_started: '未开始',
      in_progress: '学习中',
      completed: '已完成',
    };
    return labels[status] || status;
  };

  const getStatusClass = (status: string) => {
    const classes: Record<string, string> = {
      not_started: 'status-not-started',
      in_progress: 'status-in-progress',
      completed: 'status-completed',
    };
    return classes[status] || '';
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>加载学习数据中...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>学习看板</h1>
        <p>查看学习进度和考试记录</p>
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
          <button onClick={loadDashboardData} className="btn-retry">
            重试
          </button>
        </div>
      )}

      {/* 学习统计卡片 */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">📚</div>
            <div className="stat-content">
              <div className="stat-value">{stats.total_courses}</div>
              <div className="stat-label">总课程数</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <div className="stat-value">{stats.completed_courses}</div>
              <div className="stat-label">已完成课程</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📖</div>
            <div className="stat-content">
              <div className="stat-value">{stats.in_progress_courses}</div>
              <div className="stat-label">学习中课程</div>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-content">
              <div className="stat-value">{Math.round(stats.overall_progress)}%</div>
              <div className="stat-label">总体进度</div>
            </div>
          </div>
        </div>
      )}

      {/* 课程学习进度 */}
      <div className="section">
        <h2 className="section-title">课程学习进度</h2>

        {courseProgress.length === 0 ? (
          <div className="empty-state">
            <p>暂无学习记录</p>
            <Link to="/courses" className="btn-primary">
              开始学习
            </Link>
          </div>
        ) : (
          <div className="progress-list">
            {courseProgress.map((progress) => (
              <Link
                key={progress.id}
                to={`/courses/${progress.course_id}`}
                className="progress-card"
              >
                <div className="progress-header">
                  <h3 className="progress-title">课程 #{progress.course_id}</h3>
                  <span className={`status-badge ${getStatusClass(progress.status)}`}>
                    {getStatusLabel(progress.status)}
                  </span>
                </div>

                <div className="progress-bar-container">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${progress.progress_percentage}%` }}
                  ></div>
                </div>

                <div className="progress-details">
                  <span>
                    {progress.completed_chapters} / {progress.total_chapters} 章节
                  </span>
                  <span>{Math.round(progress.progress_percentage)}%</span>
                </div>

                {progress.last_accessed_at && (
                  <div className="progress-meta">
                    最后学习：{new Date(progress.last_accessed_at).toLocaleDateString()}
                  </div>
                )}
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* 考试记录 */}
      <div className="section">
        <h2 className="section-title">考试记录</h2>

        {examRecords.length === 0 ? (
          <div className="empty-state">
            <p>暂无考试记录</p>
          </div>
        ) : (
          <div className="exam-records-table">
            <table>
              <thead>
                <tr>
                  <th>考试ID</th>
                  <th>尝试次数</th>
                  <th>状态</th>
                  <th>分数</th>
                  <th>正确率</th>
                  <th>提交时间</th>
                </tr>
              </thead>
              <tbody>
                {examRecords.map((record) => (
                  <tr key={record.id}>
                    <td>#{record.exam_id}</td>
                    <td>第 {record.attempt_number} 次</td>
                    <td>
                      <span className={`status-badge ${record.status === 'passed' ? 'status-completed' : record.status === 'failed' ? 'status-failed' : ''}`}>
                        {record.status === 'passed' && '通过'}
                        {record.status === 'failed' && '未通过'}
                        {record.status === 'in_progress' && '进行中'}
                      </span>
                    </td>
                    <td>
                      {record.score !== null ? (
                        <span className="score-value">{record.score}分</span>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td>
                      {record.correct_answers !== null ? (
                        <span>
                          {record.correct_answers} / {record.total_questions}
                          {' '}
                          ({Math.round((record.correct_answers / record.total_questions) * 100)}%)
                        </span>
                      ) : (
                        '-'
                      )}
                    </td>
                    <td>
                      {record.submitted_at
                        ? new Date(record.submitted_at).toLocaleString()
                        : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
