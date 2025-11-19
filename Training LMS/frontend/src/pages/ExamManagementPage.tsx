import React, { useEffect, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiClient } from '../api/client';

interface Exam {
  id: number;
  title: string;
  exam_type: string;
  description?: string;
  course_id?: number;
  chapter_id?: number;
  total_questions: number;
  pass_score: number;
  time_limit?: number;
  question_distribution?: Record<string, number>;
  question_ids?: number[];
  allow_retake: boolean;
  max_attempts: number;
  retake_cooldown_days: number;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
}

interface ExamFormData {
  title: string;
  exam_type: string;
  description: string;
  course_id: string;
  chapter_id: string;
  total_questions: string;
  pass_score: string;
  time_limit: string;
  allow_retake: boolean;
  max_attempts: string;
  retake_cooldown_days: string;
  is_active: boolean;
}

const ExamManagementPage: React.FC = () => {
  const [exams, setExams] = useState<Exam[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingExam, setEditingExam] = useState<Exam | null>(null);
  const [formData, setFormData] = useState<ExamFormData>({
    title: '',
    exam_type: 'chapter_quiz',
    description: '',
    course_id: '',
    chapter_id: '',
    total_questions: '10',
    pass_score: '70',
    time_limit: '30',
    allow_retake: true,
    max_attempts: '3',
    retake_cooldown_days: '3',
    is_active: true
  });

  useEffect(() => {
    fetchExams();
  }, []);

  const fetchExams = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/exams', {
        params: { limit: 200 }
      });
      setExams(response.data);
    } catch (error) {
      console.error('获取考试列表失败:', error);
      alert('获取考试列表失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (exam?: Exam) => {
    if (exam) {
      setEditingExam(exam);
      setFormData({
        title: exam.title,
        exam_type: exam.exam_type,
        description: exam.description || '',
        course_id: exam.course_id?.toString() || '',
        chapter_id: exam.chapter_id?.toString() || '',
        total_questions: exam.total_questions?.toString() || '10',
        pass_score: exam.pass_score?.toString() || '70',
        time_limit: exam.time_limit?.toString() || '',
        allow_retake: exam.allow_retake ?? true,
        max_attempts: exam.max_attempts?.toString() || '3',
        retake_cooldown_days: exam.retake_cooldown_days?.toString() || '3',
        is_active: exam.is_active ?? true
      });
    } else {
      setEditingExam(null);
      setFormData({
        title: '',
        exam_type: 'chapter_quiz',
        description: '',
        course_id: '',
        chapter_id: '',
        total_questions: '10',
        pass_score: '70',
        time_limit: '30',
        allow_retake: true,
        max_attempts: '3',
        retake_cooldown_days: '3',
        is_active: true
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingExam(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 验证必填字段
    if (!formData.title.trim()) {
      alert('请填写考试标题');
      return;
    }

    if (!formData.total_questions || parseInt(formData.total_questions) <= 0) {
      alert('总题数必须大于0');
      return;
    }

    // 构建提交数据
    const submitData: any = {
      title: formData.title.trim(),
      exam_type: formData.exam_type,
      description: formData.description.trim() || undefined,
      course_id: formData.course_id ? parseInt(formData.course_id) : undefined,
      chapter_id: formData.chapter_id ? parseInt(formData.chapter_id) : undefined,
      total_questions: parseInt(formData.total_questions),
      pass_score: parseFloat(formData.pass_score),
      time_limit: formData.time_limit ? parseInt(formData.time_limit) : undefined,
      allow_retake: formData.allow_retake,
      max_attempts: parseInt(formData.max_attempts),
      retake_cooldown_days: parseInt(formData.retake_cooldown_days),
      is_active: formData.is_active
    };

    try {
      if (editingExam) {
        await apiClient.put(`/api/exams/${editingExam.id}`, submitData);
        alert('考试更新成功');
      } else {
        await apiClient.post('/api/exams', submitData);
        alert('考试创建成功');
      }
      handleCloseModal();
      fetchExams();
    } catch (error: any) {
      console.error('提交失败:', error);
      alert(error.response?.data?.detail || '操作失败，请重试');
    }
  };

  const handleDelete = async (exam: Exam) => {
    if (!confirm(`确定要删除考试"${exam.title}"吗？此操作不可恢复！`)) return;

    try {
      await apiClient.delete(`/api/exams/${exam.id}`);
      alert('考试删除成功');
      fetchExams();
    } catch (error: any) {
      console.error('删除失败:', error);
      alert(error.response?.data?.detail || '删除失败，请重试');
    }
  };

  const handlePublish = async (exam: Exam) => {
    if (!confirm(`确定要发布考试"${exam.title}"吗？发布后学员即可参加考试。`)) return;

    try {
      await apiClient.post(`/api/exams/${exam.id}/publish`);
      alert('考试发布成功');
      fetchExams();
    } catch (error: any) {
      console.error('发布失败:', error);
      alert(error.response?.data?.detail || '发布失败，请重试');
    }
  };

  const handleToggleStatus = async (exam: Exam) => {
    if (!confirm(`确定要${exam.is_active ? '禁用' : '启用'}该考试吗？`)) return;

    try {
      await apiClient.put(`/api/exams/${exam.id}`, {
        is_active: !exam.is_active
      });
      fetchExams();
    } catch (error: any) {
      console.error('更新状态失败:', error);
      alert(error.response?.data?.detail || '操作失败，请重试');
    }
  };

  const handleExportResults = async (exam: Exam) => {
    try {
      const response = await apiClient.get(`/api/exams/${exam.id}/results`);

      const results = response.data;
      if (!results || results.length === 0) {
        alert('该考试暂无成绩数据');
        return;
      }

      const csvContent = [
        ['考试名称', '学员姓名', '分数', '及格状态', '考试时间'].join(','),
        ...results.map((r: any) => [
          exam.title,
          r.username || '未知',
          r.score,
          r.score >= exam.pass_score ? '及格' : '不及格',
          new Date(r.created_at).toLocaleString()
        ].join(','))
      ].join('\n');

      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${exam.title}_成绩_${new Date().toLocaleDateString()}.csv`;
      link.click();
    } catch (error) {
      console.error('导出成绩失败:', error);
      alert('导出失败，请重试');
    }
  };

  const filteredExams = exams.filter(exam =>
    exam.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (exam.description && exam.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const getExamTypeName = (type: string) => {
    const typeMap: Record<string, string> = {
      'chapter_quiz': '章节测验',
      'course_exam': '课程考试',
      'final_exam': '总结性考试',
      'daily_quiz': '每日一题',
      'value_assessment': '价值观评估'
    };
    return typeMap[type] || type;
  };

  if (loading) {
    return (
      <AdminLayout>
        <div style={{ textAlign: 'center', padding: '60px' }}>加载中...</div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      <div className="page-header">
        <h1 className="page-title">考试管理</h1>
        <p className="page-subtitle">管理考试试卷、成绩和统计数据</p>
      </div>

      {/* 工具栏 */}
      <div className="toolbar">
        <div className="toolbar-left">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="搜索考试名称、描述..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>
        <div className="toolbar-right">
          <button className="btn btn-primary" onClick={() => handleOpenModal()}>
            ➕ 新增考试
          </button>
        </div>
      </div>

      {/* 考试列表 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">考试列表 ({filteredExams.length})</h3>
        </div>
        <div className="table-container">
          {filteredExams.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">✍️</div>
              <h3 className="empty-state-title">暂无考试</h3>
              <p className="empty-state-text">没有找到符合条件的考试</p>
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>考试名称</th>
                  <th>类型</th>
                  <th>总题数</th>
                  <th>考试时长</th>
                  <th>及格分</th>
                  <th>最大尝试</th>
                  <th>发布状态</th>
                  <th>启用状态</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredExams.map((exam) => (
                  <tr key={exam.id}>
                    <td>{exam.id}</td>
                    <td style={{ fontWeight: 500 }}>{exam.title}</td>
                    <td>{getExamTypeName(exam.exam_type)}</td>
                    <td>{exam.total_questions} 题</td>
                    <td>{exam.time_limit ? `${exam.time_limit} 分钟` : '不限时'}</td>
                    <td>{exam.pass_score} 分</td>
                    <td>{exam.max_attempts} 次</td>
                    <td>
                      {exam.is_published ? (
                        <span className="badge badge-success">已发布</span>
                      ) : (
                        <span className="badge badge-warning">未发布</span>
                      )}
                    </td>
                    <td>
                      {exam.is_active ? (
                        <span className="badge badge-success">已启用</span>
                      ) : (
                        <span className="badge badge-danger">已禁用</span>
                      )}
                    </td>
                    <td>{new Date(exam.created_at).toLocaleDateString()}</td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleOpenModal(exam)}
                        >
                          ✏️ 编辑
                        </button>
                        {!exam.is_published && (
                          <button
                            className="btn btn-primary"
                            style={{ padding: '6px 12px', fontSize: '13px' }}
                            onClick={() => handlePublish(exam)}
                          >
                            📢 发布
                          </button>
                        )}
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleExportResults(exam)}
                        >
                          📥 导出
                        </button>
                        <button
                          className={`btn ${exam.is_active ? 'btn-danger' : 'btn-success'}`}
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleToggleStatus(exam)}
                        >
                          {exam.is_active ? '🚫 禁用' : '✅ 启用'}
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleDelete(exam)}
                        >
                          🗑️ 删除
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* 新增/编辑模态框 */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingExam ? '编辑考试' : '新增考试'}</h2>
              <button className="modal-close" onClick={handleCloseModal}>✕</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                <div className="form-row">
                  <div className="form-group" style={{ flex: 2 }}>
                    <label className="form-label">考试标题 *</label>
                    <input
                      type="text"
                      className="form-input"
                      value={formData.title}
                      onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                      placeholder="请输入考试标题"
                      required
                    />
                  </div>

                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label">考试类型 *</label>
                    <select
                      className="form-input"
                      value={formData.exam_type}
                      onChange={(e) => setFormData({ ...formData, exam_type: e.target.value })}
                      required
                    >
                      <option value="chapter_quiz">章节测验</option>
                      <option value="course_exam">课程考试</option>
                      <option value="final_exam">总结性考试</option>
                      <option value="daily_quiz">每日一题</option>
                      <option value="value_assessment">价值观评估</option>
                    </select>
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">考试说明</label>
                  <textarea
                    className="form-input"
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="请输入考试说明"
                    rows={3}
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">关联课程ID</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.course_id}
                      onChange={(e) => setFormData({ ...formData, course_id: e.target.value })}
                      placeholder="可选"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">关联章节ID</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.chapter_id}
                      onChange={(e) => setFormData({ ...formData, chapter_id: e.target.value })}
                      placeholder="可选"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">总题数 *</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.total_questions}
                      onChange={(e) => setFormData({ ...formData, total_questions: e.target.value })}
                      min="1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">及格分数 *</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.pass_score}
                      onChange={(e) => setFormData({ ...formData, pass_score: e.target.value })}
                      min="0"
                      max="100"
                      step="0.1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">考试时长（分钟）</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.time_limit}
                      onChange={(e) => setFormData({ ...formData, time_limit: e.target.value })}
                      min="1"
                      placeholder="不填表示不限时"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">最大尝试次数 *</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.max_attempts}
                      onChange={(e) => setFormData({ ...formData, max_attempts: e.target.value })}
                      min="1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">补考冷却期（天）*</label>
                    <input
                      type="number"
                      className="form-input"
                      value={formData.retake_cooldown_days}
                      onChange={(e) => setFormData({ ...formData, retake_cooldown_days: e.target.value })}
                      min="0"
                      required
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={formData.allow_retake}
                        onChange={(e) => setFormData({ ...formData, allow_retake: e.target.checked })}
                      />
                      <span>允许补考</span>
                    </label>
                  </div>

                  <div className="form-group">
                    <label className="checkbox-label">
                      <input
                        type="checkbox"
                        checked={formData.is_active}
                        onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      />
                      <span>启用该考试</span>
                    </label>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={handleCloseModal}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingExam ? '保存' : '创建'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
          padding: 20px;
        }

        .modal-content {
          background: #fff;
          border-radius: 12px;
          width: 100%;
          max-width: 800px;
          max-height: 90vh;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .modal-content > form {
          display: flex;
          flex-direction: column;
          flex: 1;
          overflow: hidden;
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 24px;
          border-bottom: 1px solid #e5e7eb;
        }

        .modal-header h2 {
          margin: 0;
          font-size: 20px;
          font-weight: 600;
        }

        .modal-close {
          background: none;
          border: none;
          font-size: 24px;
          cursor: pointer;
          color: #9ca3af;
          padding: 0;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 6px;
        }

        .modal-close:hover {
          background: #f3f4f6;
          color: #374151;
        }

        .modal-body {
          padding: 24px;
          overflow-y: auto;
          flex: 1;
        }

        .modal-footer {
          display: flex;
          justify-content: flex-end;
          gap: 12px;
          padding: 16px 24px;
          border-top: 1px solid #e5e7eb;
          background: #f9fafb;
        }

        .form-row {
          display: flex;
          gap: 16px;
          margin-bottom: 16px;
        }

        .form-group {
          flex: 1;
          display: flex;
          flex-direction: column;
        }

        .form-label {
          font-size: 14px;
          font-weight: 500;
          color: #374151;
          margin-bottom: 8px;
        }

        .form-input {
          padding: 10px 12px;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          font-size: 14px;
          transition: border-color 0.2s;
        }

        .form-input:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }

        .form-input::placeholder {
          color: #9ca3af;
        }

        textarea.form-input {
          resize: vertical;
          font-family: inherit;
        }

        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          user-select: none;
        }

        .checkbox-label input[type="checkbox"] {
          width: 18px;
          height: 18px;
          cursor: pointer;
        }

        .checkbox-label span {
          font-size: 14px;
          color: #374151;
        }
      `}</style>
    </AdminLayout>
  );
};

export default ExamManagementPage;
