import React, { useEffect, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiClient } from '../api/client';

interface Course {
  id: number;
  title: string;
  code: string;
  description?: string;
  department_type: string;
  category: string;
  is_mandatory: boolean;
  is_active: boolean;
  is_published: boolean;
  created_at: string;
  chapters_count?: number;
}

interface CourseFormData {
  title: string;
  code: string;
  description: string;
  department_type: string;
  category: string;
  is_mandatory: boolean;
  is_active: boolean;
}

const CourseManagementPage: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // Modal状态
  const [showModal, setShowModal] = useState(false);
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
  const [formData, setFormData] = useState<CourseFormData>({
    title: '',
    code: '',
    description: '',
    department_type: 'front_hall',
    category: 'skill',
    is_mandatory: false,
    is_active: true
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await apiClient.get('/api/courses', {
        params: { limit: 100 }
      });
      setCourses(response.data || []);
    } catch (error) {
      console.error('获取课程列表失败:', error);
      alert('获取课程列表失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleOpenModal = (course?: Course) => {
    if (course) {
      setEditingCourse(course);
      setFormData({
        title: course.title,
        code: course.code,
        description: course.description || '',
        department_type: course.department_type,
        category: course.category,
        is_mandatory: course.is_mandatory,
        is_active: course.is_active
      });
    } else {
      setEditingCourse(null);
      setFormData({
        title: '',
        code: '',
        description: '',
        department_type: 'front_hall',
        category: 'skill',
        is_mandatory: false,
        is_active: true
      });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingCourse(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.title.trim() || !formData.code.trim()) {
      alert('请填写课程标题和编码');
      return;
    }

    try {
      const submitData = {
        ...formData,
        description: formData.description || undefined
      };

      if (editingCourse) {
        await apiClient.put(`/api/courses/${editingCourse.id}`, submitData);
        alert('课程更新成功');
      } else {
        await apiClient.post('/api/courses', submitData);
        alert('课程创建成功');
      }

      handleCloseModal();
      fetchCourses();
    } catch (error: any) {
      console.error('保存课程失败:', error);
      alert(`保存失败: ${error.response?.data?.detail || '请重试'}`);
    }
  };

  const handleDelete = async (courseId: number, courseTitle: string) => {
    if (!confirm(`确定要删除课程"${courseTitle}"吗？此操作不可恢复！`)) return;

    try {
      await apiClient.delete(`/api/courses/${courseId}`);
      alert('课程删除成功');
      fetchCourses();
    } catch (error) {
      console.error('删除课程失败:', error);
      alert('删除失败，请重试');
    }
  };

  const handlePublish = async (courseId: number) => {
    try {
      await apiClient.post(`/api/courses/${courseId}/publish`);
      alert('课程发布成功');
      fetchCourses();
    } catch (error) {
      console.error('发布课程失败:', error);
      alert('发布失败，请重试');
    }
  };

  const filteredCourses = courses.filter(course => {
    const matchesSearch =
      course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (course.description && course.description.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getCategoryBadge = (category: string) => {
    const categoryMap: Record<string, { label: string; className: string }> = {
      skill: { label: '技能', className: 'badge-info' },
      management: { label: '管理', className: 'badge-success' },
      safety: { label: '安全', className: 'badge-warning' },
      value: { label: '价值观', className: 'badge-danger' },
    };
    const config = categoryMap[category] || { label: category, className: 'badge-info' };
    return <span className={`badge ${config.className}`}>{config.label}</span>;
  };

  const getDepartmentLabel = (dept: string) => {
    const map: Record<string, string> = {
      front_hall: '前厅',
      kitchen: '厨房',
      management: '管理层',
      all: '全部门'
    };
    return map[dept] || dept;
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
        <h1 className="page-title">课程管理</h1>
        <p className="page-subtitle">管理培训课程、章节和学习内容</p>
      </div>

      {/* 工具栏 */}
      <div className="toolbar">
        <div className="toolbar-left">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="搜索课程名称、描述..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            className="form-select"
            style={{ width: '150px' }}
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
          >
            <option value="all">全部分类</option>
            <option value="skill">技能</option>
            <option value="management">管理</option>
            <option value="safety">安全</option>
            <option value="value">价值观</option>
          </select>
        </div>
        <div className="toolbar-right">
          <button className="btn btn-primary" onClick={() => handleOpenModal()}>
            ➕ 新增课程
          </button>
        </div>
      </div>

      {/* 课程列表 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">课程列表 ({filteredCourses.length})</h3>
        </div>
        <div className="table-container">
          {filteredCourses.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📚</div>
              <h3 className="empty-state-title">暂无课程</h3>
              <p className="empty-state-text">没有找到符合条件的课程</p>
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>课程名称</th>
                  <th>编码</th>
                  <th>分类</th>
                  <th>适用部门</th>
                  <th>状态</th>
                  <th>创建时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredCourses.map((course) => (
                  <tr key={course.id}>
                    <td>{course.id}</td>
                    <td style={{ fontWeight: 500 }}>{course.title}</td>
                    <td>{course.code}</td>
                    <td>{getCategoryBadge(course.category)}</td>
                    <td style={{ fontSize: '13px' }}>{getDepartmentLabel(course.department_type)}</td>
                    <td>
                      {course.is_published ? (
                        <span className="badge badge-success">已发布</span>
                      ) : course.is_active ? (
                        <span className="badge badge-warning">草稿</span>
                      ) : (
                        <span className="badge badge-danger">已禁用</span>
                      )}
                      {course.is_mandatory && <span className="badge badge-info" style={{ marginLeft: '4px' }}>必修</span>}
                    </td>
                    <td>{new Date(course.created_at).toLocaleDateString()}</td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleOpenModal(course)}
                        >
                          ✏️ 编辑
                        </button>
                        {!course.is_published && (
                          <button
                            className="btn btn-primary"
                            style={{ padding: '6px 12px', fontSize: '13px' }}
                            onClick={() => handlePublish(course.id)}
                          >
                            📢 发布
                          </button>
                        )}
                        <button
                          className="btn btn-danger"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleDelete(course.id, course.title)}
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

      {/* 课程表单弹窗 */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '600px' }}>
            <div className="modal-header">
              <h2>{editingCourse ? '编辑课程' : '新增课程'}</h2>
              <button className="modal-close" onClick={handleCloseModal}>✕</button>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="modal-body">
                {/* 课程标题 */}
                <div className="form-group">
                  <label className="form-label required">课程标题</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    placeholder="请输入课程标题..."
                    required
                  />
                </div>

                {/* 课程编码 */}
                <div className="form-group">
                  <label className="form-label required">课程编码</label>
                  <input
                    type="text"
                    className="form-control"
                    value={formData.code}
                    onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                    placeholder="例如: FRONT-001"
                    required
                    disabled={!!editingCourse}
                  />
                  {editingCourse && (
                    <small style={{ color: '#666', fontSize: '12px' }}>编码创建后不可修改</small>
                  )}
                </div>

                {/* 课程描述 */}
                <div className="form-group">
                  <label className="form-label">课程描述</label>
                  <textarea
                    className="form-control"
                    rows={3}
                    value={formData.description}
                    onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                    placeholder="请输入课程描述..."
                  />
                </div>

                {/* 适用部门和分类 */}
                <div className="form-row">
                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label required">适用部门</label>
                    <select
                      className="form-control"
                      value={formData.department_type}
                      onChange={(e) => setFormData({ ...formData, department_type: e.target.value })}
                      required
                    >
                      <option value="front_hall">前厅</option>
                      <option value="kitchen">厨房</option>
                      <option value="management">管理层</option>
                      <option value="all">全部门</option>
                    </select>
                  </div>

                  <div className="form-group" style={{ flex: 1 }}>
                    <label className="form-label required">课程分类</label>
                    <select
                      className="form-control"
                      value={formData.category}
                      onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                      required
                    >
                      <option value="skill">技能培训</option>
                      <option value="management">管理培训</option>
                      <option value="safety">安全培训</option>
                      <option value="value">价值观培训</option>
                    </select>
                  </div>
                </div>

                {/* 是否必修和启用 */}
                <div className="form-group">
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', marginBottom: '8px' }}>
                    <input
                      type="checkbox"
                      checked={formData.is_mandatory}
                      onChange={(e) => setFormData({ ...formData, is_mandatory: e.target.checked })}
                      style={{ width: '20px', height: '20px' }}
                    />
                    <span>设为必修课程</span>
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={formData.is_active}
                      onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                      style={{ width: '20px', height: '20px' }}
                    />
                    <span>启用该课程</span>
                  </label>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={handleCloseModal}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingCourse ? '保存修改' : '创建课程'}
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
          max-height: 90vh;
          overflow-y: auto;
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
        .form-control:disabled {
          background: #f3f4f6;
          cursor: not-allowed;
        }
        textarea.form-control {
          resize: vertical;
          font-family: inherit;
        }
      `}</style>
    </AdminLayout>
  );
};

export default CourseManagementPage;
