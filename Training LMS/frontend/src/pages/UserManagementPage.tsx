import React, { useEffect, useState } from 'react';
import AdminLayout from '../components/AdminLayout';
import { apiClient } from '../api/client';

interface User {
  id: number;
  username: string;
  full_name: string;
  email?: string;
  phone?: string;
  role: string;
  department_type: string;
  position_id?: number;
  store_id?: number;
  region_id?: number;
  created_at: string;
  is_active: boolean;
}

interface NewUserData {
  username: string;
  password: string;
  full_name: string;
  email: string;
  phone: string;
  role: string;
  department_type: string;
}

const UserManagementPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRole, setSelectedRole] = useState<string>('all');
  const [selectedDepartment, setSelectedDepartment] = useState<string>('all');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newUser, setNewUser] = useState<NewUserData>({
    username: '',
    password: '',
    full_name: '',
    email: '',
    phone: '',
    role: 'L1',
    department_type: 'front_hall',
  });

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/users/', {
        params: { limit: 200 }
      });
      setUsers(response.data);
    } catch (error) {
      console.error('获取用户列表失败:', error);
      alert('获取用户列表失败，请重试');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (user: User) => {
    if (!confirm(`确定要${user.is_active ? '禁用' : '启用'}用户"${user.full_name}"吗？`)) return;

    try {
      await apiClient.patch(`/api/users/${user.id}/toggle-status`);
      alert(`用户已${user.is_active ? '禁用' : '启用'}`);
      fetchUsers();
    } catch (error: any) {
      console.error('更新用户状态失败:', error);
      alert(error.response?.data?.detail || '操作失败，请重试');
    }
  };

  const handleResetPassword = async (user: User) => {
    if (!confirm(`确定要重置用户 ${user.full_name}(${user.username}) 的密码吗？`)) return;

    try {
      const response = await apiClient.post(`/api/users/${user.id}/reset-password`);
      alert(`密码已重置为：${response.data.new_password}\n\n请及时通知用户修改密码！`);
    } catch (error: any) {
      console.error('重置密码失败:', error);
      alert(error.response?.data?.detail || '操作失败，请重试');
    }
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();

    // 验证必填字段
    if (!newUser.username.trim() || !newUser.password || !newUser.full_name.trim()) {
      alert('请填写所有必填字段（用户名、密码、真实姓名）');
      return;
    }

    if (newUser.password.length < 6) {
      alert('密码长度至少为6位');
      return;
    }

    try {
      const submitData = {
        username: newUser.username.trim(),
        password: newUser.password,
        full_name: newUser.full_name.trim(),
        email: newUser.email.trim() || undefined,
        phone: newUser.phone.trim() || undefined,
        role: newUser.role,
        department_type: newUser.department_type
      };

      await apiClient.post('/api/auth/register', submitData);
      alert('用户创建成功！');
      setShowCreateModal(false);
      setNewUser({
        username: '',
        password: '',
        full_name: '',
        email: '',
        phone: '',
        role: 'L1',
        department_type: 'front_hall',
      });
      fetchUsers();
    } catch (error: any) {
      console.error('创建用户失败:', error);
      alert(error.response?.data?.detail || '创建失败，请重试');
    }
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch =
      user.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (user.email && user.email.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (user.phone && user.phone.includes(searchTerm));

    const matchesRole = selectedRole === 'all' || user.role === selectedRole;
    const matchesDepartment = selectedDepartment === 'all' || user.department_type === selectedDepartment;

    return matchesSearch && matchesRole && matchesDepartment;
  });

  const getRoleName = (role: string) => {
    const roleMap: Record<string, string> = {
      'L1': 'L1-基层员工',
      'L2': 'L2-骨干员工',
      'L3': 'L3-主管',
      'L4': 'L4-店长/厨师长',
      'L5': 'L5-区域经理',
      'L5+': 'L5+-运营负责人',
      'admin': '系统管理员'
    };
    return roleMap[role] || role;
  };

  const getDepartmentName = (dept: string) => {
    const deptMap: Record<string, string> = {
      'front_hall': '前厅',
      'kitchen': '厨房',
      'headquarters': '总部',
      'all_departments': '全部门'
    };
    return deptMap[dept] || dept;
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
        <h1 className="page-title">用户管理</h1>
        <p className="page-subtitle">管理系统用户账号、权限和状态</p>
      </div>

      {/* 工具栏 */}
      <div className="toolbar">
        <div className="toolbar-left">
          <div className="search-box">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="搜索用户名、姓名、邮箱、手机..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <select
            className="form-select"
            style={{ width: '150px' }}
            value={selectedRole}
            onChange={(e) => setSelectedRole(e.target.value)}
          >
            <option value="all">全部职级</option>
            <option value="L1">L1-基层员工</option>
            <option value="L2">L2-骨干员工</option>
            <option value="L3">L3-主管</option>
            <option value="L4">L4-店长/厨师长</option>
            <option value="L5">L5-区域经理</option>
            <option value="L5+">L5+-运营负责人</option>
          </select>
          <select
            className="form-select"
            style={{ width: '130px' }}
            value={selectedDepartment}
            onChange={(e) => setSelectedDepartment(e.target.value)}
          >
            <option value="all">全部部门</option>
            <option value="front_hall">前厅</option>
            <option value="kitchen">厨房</option>
            <option value="headquarters">总部</option>
          </select>
        </div>
        <div className="toolbar-right">
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            ➕ 新增用户
          </button>
        </div>
      </div>

      {/* 用户列表 */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">用户列表 ({filteredUsers.length})</h3>
        </div>
        <div className="table-container">
          {filteredUsers.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">👥</div>
              <h3 className="empty-state-title">暂无用户</h3>
              <p className="empty-state-text">没有找到符合条件的用户</p>
            </div>
          ) : (
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>用户名</th>
                  <th>真实姓名</th>
                  <th>邮箱</th>
                  <th>手机</th>
                  <th>职级</th>
                  <th>部门</th>
                  <th>状态</th>
                  <th>注册时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {filteredUsers.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td style={{ fontWeight: 500 }}>{user.username}</td>
                    <td>{user.full_name}</td>
                    <td style={{ fontSize: '13px' }}>{user.email || '-'}</td>
                    <td>{user.phone || '-'}</td>
                    <td>
                      <span className="badge badge-info">{getRoleName(user.role)}</span>
                    </td>
                    <td>{getDepartmentName(user.department_type)}</td>
                    <td>
                      {user.is_active ? (
                        <span className="badge badge-success">正常</span>
                      ) : (
                        <span className="badge badge-danger">禁用</span>
                      )}
                    </td>
                    <td>{new Date(user.created_at).toLocaleDateString()}</td>
                    <td>
                      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                        <button
                          className="btn btn-outline"
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleResetPassword(user)}
                        >
                          🔑 重置密码
                        </button>
                        <button
                          className={`btn ${user.is_active ? 'btn-danger' : 'btn-success'}`}
                          style={{ padding: '6px 12px', fontSize: '13px' }}
                          onClick={() => handleToggleStatus(user)}
                        >
                          {user.is_active ? '🚫 禁用' : '✅ 启用'}
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

      {/* 创建用户模态框 */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>创建新用户</h2>
              <button className="modal-close" onClick={() => setShowCreateModal(false)}>✕</button>
            </div>

            <form onSubmit={handleCreateUser}>
              <div className="modal-body">
                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">用户名 *</label>
                    <input
                      type="text"
                      className="form-input"
                      value={newUser.username}
                      onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                      placeholder="请输入用户名"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">密码 *</label>
                    <input
                      type="password"
                      className="form-input"
                      value={newUser.password}
                      onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                      placeholder="至少6位字符"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label className="form-label">真实姓名 *</label>
                  <input
                    type="text"
                    className="form-input"
                    value={newUser.full_name}
                    onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                    placeholder="请输入真实姓名"
                    required
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">邮箱</label>
                    <input
                      type="email"
                      className="form-input"
                      value={newUser.email}
                      onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                      placeholder="可选"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">手机号</label>
                    <input
                      type="tel"
                      className="form-input"
                      value={newUser.phone}
                      onChange={(e) => setNewUser({ ...newUser, phone: e.target.value })}
                      placeholder="可选"
                    />
                  </div>
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label className="form-label">职级 *</label>
                    <select
                      className="form-input"
                      value={newUser.role}
                      onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                      required
                    >
                      <option value="L1">L1 - 基层员工</option>
                      <option value="L2">L2 - 骨干员工</option>
                      <option value="L3">L3 - 主管</option>
                      <option value="L4">L4 - 店长/厨师长</option>
                      <option value="L5">L5 - 区域经理</option>
                      <option value="L5+">L5+ - 运营负责人</option>
                    </select>
                  </div>

                  <div className="form-group">
                    <label className="form-label">部门 *</label>
                    <select
                      className="form-input"
                      value={newUser.department_type}
                      onChange={(e) => setNewUser({ ...newUser, department_type: e.target.value })}
                      required
                    >
                      <option value="front_hall">前厅</option>
                      <option value="kitchen">厨房</option>
                      <option value="headquarters">总部</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-outline" onClick={() => setShowCreateModal(false)}>
                  取消
                </button>
                <button type="submit" className="btn btn-primary">
                  创建用户
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
          max-width: 650px;
          max-height: 90vh;
          overflow: hidden;
          display: flex;
          flex-direction: column;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
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
      `}</style>
    </AdminLayout>
  );
};

export default UserManagementPage;
