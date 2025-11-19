import React, { useEffect, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiClient } from '../api/client';

interface Question {
  id: number;
  content: string;
  question_type: 'single_choice' | 'multiple_choice' | 'true_false' | 'short_answer';
  difficulty: 'easy' | 'medium' | 'hard';
  category: 'skill' | 'value_diligence' | 'value_customer' | 'value_collaboration' | 'value_transparency';
  options?: any[];
  correct_answer?: string;
  explanation?: string;
  is_active: boolean;
  created_at: string;
}

interface QuestionFormData {
  content: string;
  question_type: 'single_choice' | 'multiple_choice' | 'true_false' | 'short_answer';
  category: string;
  difficulty: string;
  options: { label: string; content: string; is_correct: boolean }[];
  correct_answer?: string;
  explanation?: string;
  is_active: boolean;
}

const QuestionManagementPage: React.FC = () => {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // 弹窗状态
  const [showModal, setShowModal] = useState(false);
  const [editingQuestion, setEditingQuestion] = useState<Question | null>(null);
  const [formData, setFormData] = useState<QuestionFormData>({
    content: '',
    question_type: 'single_choice',
    category: 'skill',
    difficulty: 'medium',
    options: [
      { label: 'A', content: '', is_correct: false },
      { label: 'B', content: '', is_correct: false },
      { label: 'C', content: '', is_correct: false },
      { label: 'D', content: '', is_correct: false }
    ],
    correct_answer: '',
    explanation: '',
    is_active: true
  });

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const response = await apiClient.get('/api/exams/questions', {
        params: { limit: 500 }  // 增加到500以显示所有题目（当前421道）
      });
      setQuestions(response.data || []);
    } catch (error) {
      console.error('获取题目列表失败:', error);
      alert('获取题目列表失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteQuestion = async (questionId: number) => {
    if (!confirm('确定要删除该题目吗？此操作不可恢复！')) return;

    try {
      await apiClient.delete(`/api/exams/questions/${questionId}`);
      alert('题目删除成功');
      fetchQuestions();
    } catch (error) {
      console.error('删除题目失败:', error);
      alert('删除失败，请重试');
    }
  };

  const handleOpenModal = (question?: Question) => {
    if (question) {
      // 编辑模式
      setEditingQuestion(question);
      setFormData({
        content: question.content,
        question_type: question.question_type,
        category: question.category,
        difficulty: question.difficulty || 'medium',
        options: question.options || [
          { label: 'A', content: '', is_correct: false },
          { label: 'B', content: '', is_correct: false },
          { label: 'C', content: '', is_correct: false },
          { label: 'D', content: '', is_correct: false }
        ],
        correct_answer: question.correct_answer || '',
        explanation: question.explanation || '',
        is_active: question.is_active
      });
    } else {
      // 新增模式
      setEditingQuestion(null);
      setFormData({
        content: '',
        question_type: 'single_choice',
        category: 'skill',
        difficulty: 'medium',
        options: [
          { label: 'A', content: '', is_correct: false },
          { label: 'B', content: '', is_correct: false },
          { label: 'C', content: '', is_correct: false },
          { label: 'D', content: '', is_correct: false }
        ],
        correct_answer: '',
        explanation: '',
        is_active: true
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingQuestion(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // 验证表单
    if (!formData.content.trim()) {
      alert('请输入题目内容');
      return;
    }

    // 选择题验证选项
    if (formData.question_type !== 'true_false' && formData.question_type !== 'short_answer') {
      const hasCorrectAnswer = formData.options.some(opt => opt.is_correct && opt.content.trim());
      if (!hasCorrectAnswer) {
        alert('请至少选择一个正确答案并填写选项内容');
        return;
      }
      const emptyOptions = formData.options.filter(opt => opt.content.trim() === '');
      if (emptyOptions.length > 0) {
        alert('请填写所有选项内容');
        return;
      }
    }

    // 判断题验证答案
    if (formData.question_type === 'true_false' && !formData.correct_answer) {
      alert('请选择正确答案');
      return;
    }

    try {
      const submitData: any = {
        content: formData.content,
        question_type: formData.question_type,
        category: formData.category,
        difficulty: formData.difficulty,
        explanation: formData.explanation || undefined,
        is_active: formData.is_active
      };

      // 根据题型添加不同字段
      if (formData.question_type === 'true_false') {
        submitData.correct_answer = formData.correct_answer;
      } else if (formData.question_type === 'short_answer') {
        submitData.correct_answer = formData.correct_answer || undefined;
      } else {
        // 选择题:只保留有内容的选项
        submitData.options = formData.options
          .filter(opt => opt.content.trim())
          .map(opt => ({
            label: opt.label,
            content: opt.content,
            is_correct: opt.is_correct
          }));
      }

      if (editingQuestion) {
        // 更新题目
        await apiClient.put(`/api/exams/questions/${editingQuestion.id}`, submitData);
        alert('题目更新成功');
      } else {
        // 创建题目
        await apiClient.post('/api/exams/questions', submitData);
        alert('题目创建成功');
      }

      handleCloseModal();
      fetchQuestions();
    } catch (error: any) {
      console.error('保存题目失败:', error);
      alert(`保存失败: ${error.response?.data?.detail || '请重试'}`);
    }
  };

  const handleOptionChange = (index: number, field: 'content' | 'is_correct', value: string | boolean) => {
    const newOptions = [...formData.options];
    if (field === 'is_correct') {
      // 单选题只能选一个正确答案
      if (formData.question_type === 'single_choice' && value === true) {
        newOptions.forEach((opt, i) => {
          opt.is_correct = i === index;
        });
      } else {
        newOptions[index].is_correct = value as boolean;
      }
    } else {
      newOptions[index].content = value as string;
    }
    setFormData({ ...formData, options: newOptions });
  };

  const addOption = () => {
    const nextLabel = String.fromCharCode(65 + formData.options.length); // A,B,C,D...
    setFormData({
      ...formData,
      options: [...formData.options, { label: nextLabel, content: '', is_correct: false }]
    });
  };

  const removeOption = (index: number) => {
    if (formData.options.length <= 2) {
      alert('至少保留2个选项');
      return;
    }
    const newOptions = formData.options.filter((_, i) => i !== index);
    setFormData({ ...formData, options: newOptions });
  };

  const filteredQuestions = questions.filter(question => {
    const matchesSearch = question.content.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedType === 'all' || question.question_type === selectedType;
    const matchesDifficulty = selectedDifficulty === 'all' || question.difficulty === selectedDifficulty;
    const matchesCategory = selectedCategory === 'all' || question.category === selectedCategory;

    return matchesSearch && matchesType && matchesDifficulty && matchesCategory;
  });

  const getTypeBadge = (type: string) => {
    const typeMap: Record<string, { label: string; className: string }> = {
      single_choice: { label: '单选', className: 'badge-info' },
      multiple_choice: { label: '多选', className: 'badge-warning' },
      true_false: { label: '判断', className: 'badge-success' },
      short_answer: { label: '简答', className: 'badge-danger' },
    };
    const config = typeMap[type] || { label: type, className: 'badge-info' };
    return <span className={`badge ${config.className}`}>{config.label}</span>;
  };

  const getDifficultyBadge = (difficulty: string) => {
    const difficultyMap: Record<string, { label: string; className: string }> = {
      easy: { label: '简单', className: 'badge-success' },
      medium: { label: '中等', className: 'badge-warning' },
      hard: { label: '困难', className: 'badge-danger' },
    };
    const config = difficultyMap[difficulty] || { label: difficulty, className: 'badge-info' };
    return <span className={`badge ${config.className}`}>{config.label}</span>;
  };

  const getCategoryLabel = (category: string) => {
    const categoryMap: Record<string, string> = {
      skill: '技能',
      value_diligence: '勤劳者为本',
      value_customer: '帮助顾客',
      value_collaboration: '高效协作',
      value_transparency: '平等透明',
    };
    return categoryMap[category] || category;
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
        <h1 className="page-title">题库管理</h1>
        <p className="page-subtitle">管理考试题目、选项和答案</p>
      </div>

      {/* 工具栏 */}
      <div className="toolbar">
        <div className="toolbar-left">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="搜索题目内容..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            className="form-select"
            style={{ width: '130px' }}
            value={selectedType}
            onChange={(e) => setSelectedType(e.target.value)}
          >
            <option value="all">全部题型</option>
            <option value="single_choice">单选</option>
            <option value="multiple_choice">多选</option>
            <option value="true_false">判断</option>
            <option value="short_answer">简答</option>
          </select>
          <select
            className="form-select"
            style={{ width: '120px' }}
            value={selectedDifficulty}
            onChange={(e) => setSelectedDifficulty(e.target.value)}
          >
            <option value="all">全部难度</option>
            <option value="easy">简单</option>
            <option value="medium">中等</option>
            <option value="hard">困难</option>
          </select>
          <select
            className="form-select"
            style={{ width: '150px' }}
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="all">全部类别</option>
            <option value="skill">技能</option>
            <option value="value_diligence">勤劳者为本</option>
            <option value="value_customer">帮助顾客</option>
            <option value="value_collaboration">高效协作</option>
            <option value="value_transparency">平等透明</option>
          </select>
        </div>
        <div className="toolbar-right">
          <button
            className="btn btn-outline"
            onClick={() => alert('批量导入功能开发中')}
          >
            📤 批量导入
          </button>
          <button className="btn btn-primary" onClick={() => handleOpenModal()}>
            ➕ 新增题目
          </button>
        </div>
      </div>

      {/* 题目列表 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">题目列表 ({filteredQuestions.length})</h3>
        </div>
        <div className="table-container">
          {filteredQuestions.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📝</div>
              <h3 className="empty-state-title">暂无题目</h3>
              <p className="empty-state-text">没有找到符合条件的题目</p>
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>题目内容</th>
                  <th>题型</th>
                  <th>难度</th>
                  <th>类别</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredQuestions.map((question) => (
                  <tr key={question.id}>
                    <td>{question.id}</td>
                    <td style={{ maxWidth: '400px' }}>
                      <div style={{
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap'
                      }}>
                        {question.content}
                      </div>
                    </td>
                    <td>{getTypeBadge(question.question_type)}</td>
                    <td>{getDifficultyBadge(question.difficulty)}</td>
                    <td style={{ fontSize: '13px' }}>
                      {getCategoryLabel(question.category)}
                    </td>
                    <td>{new Date(question.created_at).toLocaleDateString()}</td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px' }}>
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleOpenModal(question)}
                        >
                          ✏️ 编辑
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleDeleteQuestion(question.id)}
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

      {/* 题目表单弹窗 */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '700px', maxHeight: '90vh', overflow: 'auto' }}>
            <div className="modal-header">
              <h2>{editingQuestion ? '编辑题目' : '新增题目'}</h2>
              <button className="modal-close" onClick={handleCloseModal}>✕</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {/* 题目内容 */}
                <div className="form-group">
                  <label className="form-label required">题目内容</label>
                  <textarea
                    className="form-control"
                    rows={4}
                    value={formData.content}
                    onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                    placeholder="请输入题目内容..."
                    required
                  />
                </div>

                {/* 题型选择 */}
                <div className="form-row">
                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label required">题型</label>
                    <select
                      className="form-control"
                      value={formData.question_type}
                      onChange={(e) => setFormData({ ...formData, question_type: e.target.value as any })}
                      required
                    >
                      <option value="single_choice">单选题</option>
                      <option value="multiple_choice">多选题</option>
                      <option value="true_false">判断题</option>
                      <option value="short_answer">简答题</option>
                    </select>
                  </div>

                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label required">难度</label>
                    <select
                      className="form-control"
                      value={formData.difficulty}
                      onChange={(e) => setFormData({ ...formData, difficulty: e.target.value })}
                      required
                    >
                      <option value="easy">简单</option>
                      <option value="medium">中等</option>
                      <option value="hard">困难</option>
                    </select>
                  </div>

                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label required">类别</label>
                    <select
                      className="form-control"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      required
                    >
                      <option value="skill">技能</option>
                      <option value="value_diligence">勤劳者为本</option>
                      <option value="value_customer">帮助顾客</option>
                      <option value="value_collaboration">高效协作</option>
                      <option value="value_transparency">平等透明</option>
                    </select>
                  </div>
                </div>

                {/* 选择题选项 */}
                {(formData.question_type === 'single_choice' || formData.question_type === 'multiple_choice') && (
                  <div className="form-group">
                    <label className="form-label required">选项（{formData.question_type === 'single_choice' ? '单选' : '可多选'}）</label>
                    {formData.options.map((option, index) => (
                      <div key={index} style={{ display: 'flex', gap: '8px', marginBottom: '8px', alignItems: 'center' }}>
                        <input
                          type={formData.question_type === 'single_choice' ? 'radio' : 'checkbox'}
                          name="correct_answer"
                          checked={option.is_correct}
                          onChange={(e) => handleOptionChange(index, 'is_correct', e.target.checked)}
                          style={{ width: '20px', height: '20px' }}
                        />
                        <span style={{ minWidth: '30px', fontWeight: 600 }}>{option.label}.</span>
                        <input
                          type="text"
                          className="form-control"
                          value={option.content}
                          onChange={(e) => handleOptionChange(index, 'content', e.target.value)}
                          placeholder={`选项${option.label}内容...`}
                          style={{ flex: 1 }}
                        />
                        {formData.options.length > 2 && (
                          <button
                            type="button"
                            className="btn btn-danger"
                            onClick={() => removeOption(index)}
                            style={{ padding: '6px 12px' }}
                          >
                            删除
                          </button>
                        )}
                      </div>
                    ))}
                    {formData.options.length < 8 && (
                      <button
                        type="button"
                        className="btn btn-outline"
                        onClick={addOption}
                        style={{ marginTop: '8px' }}
                      >
                        ➕ 添加选项
                      </button>
                    )}
                  </div>
                )}

                {/* 判断题答案 */}
                {formData.question_type === 'true_false' && (
                  <div className="form-group">
                    <label className="form-label required">正确答案</label>
                    <div style={{ display: 'flex', gap: '16px' }}>
                      <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                        <input
                          type="radio"
                          name="true_false_answer"
                          value="true"
                          checked={formData.correct_answer === 'true'}
                          onChange={(e) => setFormData({ ...formData, correct_answer: e.target.value })}
                          style={{ width: '20px', height: '20px' }}
                        />
                        <span>正确</span>
                      </label>
                      <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                        <input
                          type="radio"
                          name="true_false_answer"
                          value="false"
                          checked={formData.correct_answer === 'false'}
                          onChange={(e) => setFormData({ ...formData, correct_answer: e.target.value })}
                          style={{ width: '20px', height: '20px' }}
                        />
                        <span>错误</span>
                      </label>
                    </div>
                  </div>
                )}

                {/* 简答题参考答案 */}
                {formData.question_type === 'short_answer' && (
                  <div className="form-group">
                    <label className="form-label">参考答案（可选）</label>
                    <textarea
                      className="form-control"
                      rows={3}
                      value={formData.correct_answer}
                      onChange={(e) => setFormData({ ...formData, correct_answer: e.target.value })}
                      placeholder="请输入参考答案..."
                    />
                  </div>
                )}

                {/* 答案解析 */}
                <div className="form-group">
                  <label className="form-label">答案解析（可选）</label>
                  <textarea
                    className="form-control"
                    rows={3}
                    value={formData.explanation}
                    onChange={(e) => setFormData({ ...formData, explanation: e.target.value })}
                    placeholder="请输入答案解析..."
                  />
                </div>

                {/* 是否启用 */}
                <div className="form-group">
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      style={{ width: '20px', height: '20px' }}
                    />
                    <span>启用该题目</span>
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={handleCloseModal}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingQuestion ? '保存修改' : '创建题目'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <style>{`
        /* Modal样式 */
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
          box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
          width: 100%;
          animation: modalSlideIn 0.3s ease-out;
        }
        @keyframes modalSlideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 20px 24px;
          border-bottom: 1px solid #e5e7eb;
        }
        .modal-header h2 {
          margin: 0;
          font-size: 20px;
          font-weight: 600;
          color: #333;
        }
        .modal-close {
          background: none;
          border: none;
          font-size: 24px;
          color: #666;
          cursor: pointer;
          padding: 0;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 4px;
        }
        .modal-close:hover {
          background: #f3f4f6;
          color: #333;
        }
        .modal-body {
          padding: 24px;
          max-height: calc(90vh - 160px);
          overflow-y: auto;
        }
        .modal-footer {
          display: flex;
          justify-content: flex-end;
          gap: 12px;
          padding: 16px 24px;
          border-top: 1px solid #e5e7eb;
        }

        /* Form样式 */
        .form-row {
          display: flex;
          gap: 16px;
        }
        .form-group {
          margin-bottom: 20px;
        }
        .form-label {
          display: block;
          margin-bottom: 8px;
          font-weight: 500;
          color: #333;
          font-size: 14px;
        }
        .form-label.required::after {
          content: '*';
          color: #ef4444;
          margin-left: 4px;
        }
        .form-control {
          width: 100%;
          padding: 10px 12px;
          border: 1px solid #d1d5db;
          border-radius: 6px;
          font-size: 14px;
          transition: border-color 0.2s;
        }
        .form-control:focus {
          outline: none;
          border-color: #3b82f6;
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        textarea.form-control {
          resize: vertical;
          font-family: inherit;
        }
      `}</style>
    </AdminLayout>
  );
};

export default QuestionManagementPage;
