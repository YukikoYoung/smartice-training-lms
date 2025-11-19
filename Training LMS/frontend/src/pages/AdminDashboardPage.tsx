import React, { useEffect, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiClient } from '../api/client';

interface DashboardStats {
  total_users: number;
  active_users: number;
  total_courses: number;
  total_exams: number;
  total_questions: number;
  completion_rate: number;
  average_score: number;
  new_users_this_week: number;
  completed_exams_this_week: number;
}

interface RoleCompletion {
  role: string;
  total_enrollments: number;
  completed: number;
  completion_rate: number;
}

interface CoursePopularity {
  title: string;
  category: string;
  enrollments: number;
  completed: number;
  completion_rate: number;
}

interface ExamPerformance {
  exam_title: string;
  pass_score: number;
  total_attempts: number;
  passed_count: number;
  pass_rate: number;
  average_score: number;
}

const AdminDashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [roleCompletion, setRoleCompletion] = useState<RoleCompletion[]>([]);
  const [coursePopularity, setCoursePopularity] = useState<CoursePopularity[]>([]);
  const [examPerformance, setExamPerformance] = useState<ExamPerformance[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAllStats();
  }, []);

  const fetchAllStats = async () => {
    try {
      setLoading(true);

      // 并行请求所有统计数据
      const [dashboardRes, learningRes, examRes] = await Promise.all([
        apiClient.get('/api/stats/dashboard'),
        apiClient.get('/api/stats/learning-overview').catch(() => ({ data: { role_completion: [], course_popularity: [] } })),
        apiClient.get('/api/stats/exam-performance').catch(() => ({ data: { exam_performance: [] } }))
      ]);

      setStats(dashboardRes.data);
      setRoleCompletion(learningRes.data.role_completion || []);
      setCoursePopularity(learningRes.data.course_popularity || []);
      setExamPerformance(examRes.data.exam_performance || []);
    } catch (error) {
      console.error('获取统计数据失败:', error);
      alert('获取统计数据失败，请刷新重试');
    } finally {
      setLoading(false);
    }
  };

  const getRoleName = (role: string) => {
    const roleMap: Record<string, string> = {
      'L1': 'L1-基层员工',
      'L2': 'L2-骨干员工',
      'L3': 'L3-主管',
      'L4': 'L4-店长/厨师长',
      'L5': 'L5-区域经理',
      'L5+': 'L5+-运营负责人'
    };
    return roleMap[role] || role;
  };

  if (loading) {
    return (
      <AdminLayout>
        <div style={{ textAlign: 'center', padding: '60px' }}>加载中...</div>
      </AdminLayout>
    );
  }

  if (!stats) {
    return (
      <AdminLayout>
        <div style={{ textAlign: 'center', padding: '60px' }}>加载失败，请刷新重试</div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="page-header">
        <h1 className="page-title">数据看板</h1>
        <p className="page-subtitle">系统整体运营数据概览</p>
      </div>

      {/* 核心统计卡片 */}
      <div className="stats-grid">
        <div className="stat-card stat-card-primary">
          <div className="stat-icon-large">👥</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_users}</div>
            <div className="stat-title">总用户数</div>
            <div className="stat-description">
              活跃用户: {stats.active_users} ({stats.total_users > 0 ? ((stats.active_users / stats.total_users) * 100).toFixed(0) : 0}%)
            </div>
          </div>
        </div>

        <div className="stat-card stat-card-success">
          <div className="stat-icon-large">📚</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_courses}</div>
            <div className="stat-title">课程总数</div>
            <div className="stat-description">前厅、厨房、价值观培训</div>
          </div>
        </div>

        <div className="stat-card stat-card-warning">
          <div className="stat-icon-large">✍️</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_exams}</div>
            <div className="stat-title">考试总数</div>
            <div className="stat-description">覆盖所有培训课程</div>
          </div>
        </div>

        <div className="stat-card stat-card-info">
          <div className="stat-icon-large">📝</div>
          <div className="stat-content">
            <div className="stat-value">{stats.total_questions}</div>
            <div className="stat-title">题库容量</div>
            <div className="stat-description">技能类和价值观类题目</div>
          </div>
        </div>
      </div>

      {/* 本周数据 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">📈 本周数据</h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '24px' }}>
            <div className="metric-box">
              <div className="metric-label">新增用户</div>
              <div className="metric-value">{stats.new_users_this_week}</div>
            </div>
            <div className="metric-box">
              <div className="metric-label">完成考试</div>
              <div className="metric-value">{stats.completed_exams_this_week}</div>
            </div>
            <div className="metric-box">
              <div className="metric-label">课程完成率</div>
              <div className="metric-value">{stats.completion_rate}%</div>
            </div>
            <div className="metric-box">
              <div className="metric-label">平均考试分数</div>
              <div className="metric-value">{stats.average_score}分</div>
            </div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))', gap: '24px' }}>
        {/* 各职级学习完成情况 */}
        {roleCompletion.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">👔 各职级学习完成情况</h3>
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>职级</th>
                    <th>总学习数</th>
                    <th>已完成</th>
                    <th>完成率</th>
                  </tr>
                </thead>
                <tbody>
                  {roleCompletion.map((item, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 500 }}>{getRoleName(item.role)}</td>
                      <td>{item.total_enrollments}</td>
                      <td>{item.completed}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div className="progress-bar" style={{ flex: 1 }}>
                            <div
                              className="progress-fill"
                              style={{
                                width: `${item.completion_rate}%`,
                                background: item.completion_rate >= 80 ? '#10b981' : item.completion_rate >= 50 ? '#f59e0b' : '#ef4444'
                              }}
                            />
                          </div>
                          <span style={{ fontSize: '13px', fontWeight: 500 }}>{item.completion_rate}%</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* 课程学习热度 */}
        {coursePopularity.length > 0 && (
          <div className="card">
            <div className="card-header">
              <h3 className="card-title">🔥 课程学习热度</h3>
            </div>
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>课程名称</th>
                    <th>学习人数</th>
                    <th>已完成</th>
                    <th>完成率</th>
                  </tr>
                </thead>
                <tbody>
                  {coursePopularity.slice(0, 8).map((item, idx) => (
                    <tr key={idx}>
                      <td style={{ fontWeight: 500 }}>{item.title}</td>
                      <td>{item.enrollments}</td>
                      <td>{item.completed}</td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div className="progress-bar" style={{ flex: 1 }}>
                            <div
                              className="progress-fill"
                              style={{
                                width: `${item.completion_rate}%`,
                                background: item.completion_rate >= 80 ? '#10b981' : item.completion_rate >= 50 ? '#f59e0b' : '#ef4444'
                              }}
                            />
                          </div>
                          <span style={{ fontSize: '13px', fontWeight: 500 }}>{item.completion_rate}%</span>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* 考试通过率统计 */}
      {examPerformance.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">🎯 考试通过率统计</h3>
          </div>
          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>考试名称</th>
                  <th>及格分</th>
                  <th>总考试次数</th>
                  <th>通过次数</th>
                  <th>通过率</th>
                  <th>平均分</th>
                </tr>
              </thead>
              <tbody>
                {examPerformance.map((item, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 500 }}>{item.exam_title}</td>
                    <td>{item.pass_score}分</td>
                    <td>{item.total_attempts}</td>
                    <td>{item.passed_count}</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div className="progress-bar" style={{ flex: 1 }}>
                          <div
                            className="progress-fill"
                            style={{
                              width: `${item.pass_rate}%`,
                              background: item.pass_rate >= 80 ? '#10b981' : item.pass_rate >= 50 ? '#f59e0b' : '#ef4444'
                            }}
                          />
                        </div>
                        <span style={{ fontSize: '13px', fontWeight: 500 }}>{item.pass_rate}%</span>
                      </div>
                    </td>
                    <td style={{ fontWeight: 500, color: item.average_score >= item.pass_score ? '#10b981' : '#ef4444' }}>
                      {item.average_score}分
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 快捷操作 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">⚡ 快捷操作</h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px' }}>
            <button className="quick-action-btn" onClick={() => window.location.href = '/admin/users'}>
              <span className="quick-action-icon">👥</span>
              <span className="quick-action-text">管理用户</span>
            </button>
            <button className="quick-action-btn" onClick={() => window.location.href = '/admin/courses'}>
              <span className="quick-action-icon">📚</span>
              <span className="quick-action-text">管理课程</span>
            </button>
            <button className="quick-action-btn" onClick={() => window.location.href = '/admin/questions'}>
              <span className="quick-action-icon">📝</span>
              <span className="quick-action-text">管理题库</span>
            </button>
            <button className="quick-action-btn" onClick={() => window.location.href = '/admin/exams'}>
              <span className="quick-action-icon">✍️</span>
              <span className="quick-action-text">管理考试</span>
            </button>
          </div>
        </div>
      </div>

      <style>{`
        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 24px;
          margin-bottom: 24px;
        }

        .stat-card {
          background: #fff;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          display: flex;
          align-items: center;
          gap: 20px;
          transition: all 0.3s;
        }

        .stat-card:hover {
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
          transform: translateY(-2px);
        }

        .stat-card-primary { border-left: 4px solid #3b82f6; }
        .stat-card-success { border-left: 4px solid #10b981; }
        .stat-card-warning { border-left: 4px solid #f59e0b; }
        .stat-card-info { border-left: 4px solid #8b5cf6; }

        .stat-icon-large {
          font-size: 48px;
          flex-shrink: 0;
        }

        .stat-content {
          flex: 1;
        }

        .stat-value {
          font-size: 36px;
          font-weight: 700;
          color: #1f2937;
          margin-bottom: 4px;
        }

        .stat-title {
          font-size: 14px;
          font-weight: 600;
          color: #6b7280;
          margin-bottom: 4px;
        }

        .stat-description {
          font-size: 13px;
          color: #9ca3af;
        }

        .metric-box {
          text-align: center;
          padding: 16px;
          background: #f9fafb;
          border-radius: 8px;
        }

        .metric-label {
          font-size: 14px;
          color: #6b7280;
          margin-bottom: 8px;
        }

        .metric-value {
          font-size: 28px;
          font-weight: 700;
          color: #1f2937;
        }

        .progress-bar {
          height: 8px;
          background: #e5e7eb;
          border-radius: 4px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          transition: width 0.3s ease;
          border-radius: 4px;
        }

        .quick-action-btn {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 16px 20px;
          background: #fff;
          border: 2px solid #e5e7eb;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .quick-action-btn:hover {
          border-color: #3b82f6;
          background: #eff6ff;
          transform: translateY(-2px);
        }

        .quick-action-icon {
          font-size: 24px;
        }

        .quick-action-text {
          font-size: 15px;
          font-weight: 500;
          color: #374151;
        }

        @media (max-width: 768px) {
          .stats-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </AdminLayout>
  );
};

export default AdminDashboardPage;
