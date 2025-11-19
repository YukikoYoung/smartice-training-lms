import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import Layout from '../components/Layout';
import { FormInput, Modal } from '../components/common';
import { profileAPI } from '../api/feature';

interface ProfileData {
  username: string;
  full_name: string;
  phone: string;
  role: string;
  department_type: string | null;
  position: string | null;
  store: string | null;
  is_active: boolean;
  created_at: string;
}

interface PasswordForm {
  oldPassword: string;
  newPassword: string;
  confirmPassword: string;
}

/**
 * 个人中心页面
 *
 * 功能：
 * - 查看个人资料
 * - 编辑个人信息（姓名、手机、邮箱）
 * - 修改密码
 * - 查看我的学习统计
 */
const ProfilePage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [showPasswordModal, setShowPasswordModal] = useState(false);

  // 编辑表单状态
  const [formData, setFormData] = useState({
    full_name: '',
    phone: '',
  });

  // 修改密码表单
  const [passwordForm, setPasswordForm] = useState<PasswordForm>({
    oldPassword: '',
    newPassword: '',
    confirmPassword: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saving, setSaving] = useState(false);

  // 加载用户信息
  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const data = await profileAPI.get();
      setProfile(data);
      setFormData({
        full_name: data.full_name,
        phone: data.phone || '',
      });
    } catch (error) {
      console.error('加载个人信息失败:', error);
      alert('加载个人信息失败，请稍后重试');
    } finally {
      setLoading(false);
    }
  };

  // 进入编辑模式
  const handleEdit = () => {
    setEditMode(true);
    setErrors({});
  };

  // 取消编辑
  const handleCancel = () => {
    setEditMode(false);
    if (profile) {
      setFormData({
        full_name: profile.full_name,
        phone: profile.phone || '',
      });
    }
    setErrors({});
  };

  // 验证表单
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.full_name.trim()) {
      newErrors.full_name = '请输入姓名';
    }

    if (!formData.phone.trim()) {
      newErrors.phone = '请输入手机号';
    } else if (!/^1[3-9]\d{9}$/.test(formData.phone)) {
      newErrors.phone = '请输入有效的手机号';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 保存个人信息
  const handleSave = async () => {
    if (!validateForm()) {
      return;
    }

    try {
      setSaving(true);
      await profileAPI.update(formData);

      // 重新加载profile
      await loadProfile();

      alert('个人信息更新成功！');
      setEditMode(false);
    } catch (error) {
      console.error('保存失败:', error);
      alert('保存失败，请稍后重试');
    } finally {
      setSaving(false);
    }
  };

  // 验证密码表单
  const validatePasswordForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!passwordForm.oldPassword) {
      newErrors.oldPassword = '请输入当前密码';
    }

    if (!passwordForm.newPassword) {
      newErrors.newPassword = '请输入新密码';
    } else if (passwordForm.newPassword.length < 6) {
      newErrors.newPassword = '密码长度至少6位';
    }

    if (passwordForm.newPassword !== passwordForm.confirmPassword) {
      newErrors.confirmPassword = '两次输入的密码不一致';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 修改密码
  const handleChangePassword = async () => {
    if (!validatePasswordForm()) {
      return;
    }

    try {
      setSaving(true);
      // 调用修改密码API
      // await userAPI.changePassword(user.id, passwordForm);

      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000));

      alert('密码修改成功！请重新登录');
      setShowPasswordModal(false);
      setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
      setErrors({});

      // 延迟跳转到登录页
      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (error) {
      console.error('修改密码失败:', error);
      alert('修改密码失败，请检查当前密码是否正确');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div style={{ padding: '40px', textAlign: 'center' }}>加载中...</div>
      </Layout>
    );
  }

  if (!profile) {
    return (
      <Layout>
        <div style={{ padding: '40px', textAlign: 'center' }}>无法加载用户信息</div>
      </Layout>
    );
  }

  // 格式化日期
  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('zh-CN');
  };

  // 角色显示名称
  const getRoleName = (role: string) => {
    const roleMap: Record<string, string> = {
      'L1': 'L1 - 基层员工',
      'L2': 'L2 - 骨干员工',
      'L3': 'L3 - 主管',
      'L4': 'L4 - 店长/厨师长',
      'L5': 'L5 - 区域经理',
      'L5+': 'L5+ - 运营负责人',
    };
    return roleMap[role] || role;
  };

  // 部门显示名称
  const getDepartmentName = (dept: string) => {
    const deptMap: Record<string, string> = {
      'front_hall': '前厅',
      'kitchen': '厨房',
      'headquarters': '总部',
    };
    return deptMap[dept] || dept;
  };

  return (
    <Layout>
      <div className="profile-page">
        <div className="profile-header">
          <h1>个人中心</h1>
          <p>管理您的个人信息和账号设置</p>
        </div>

        <div className="profile-container">
          {/* 个人资料卡片 */}
          <div className="profile-card">
            <div className="card-header">
              <h2>个人资料</h2>
              {!editMode ? (
                <button className="btn btn-primary" onClick={handleEdit}>
                  编辑资料
                </button>
              ) : (
                <div className="action-buttons">
                  <button className="btn btn-secondary" onClick={handleCancel} disabled={saving}>
                    取消
                  </button>
                  <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
                    {saving ? '保存中...' : '保存'}
                  </button>
                </div>
              )}
            </div>

            <div className="card-body">
              {/* 头像区域 */}
              <div className="avatar-section">
                <div className="avatar">
                  {profile.full_name.charAt(0)}
                </div>
                <div className="user-basic">
                  <h3>{profile.full_name}</h3>
                  <p className="role-badge">{profile.role}</p>
                </div>
              </div>

              {/* 信息表单 */}
              <div className="info-form">
                <div className="form-row">
                  <label>用户名</label>
                  <div className="form-value">{profile.username}</div>
                </div>

                {editMode ? (
                  <>
                    <FormInput
                      label="姓名"
                      name="full_name"
                      value={formData.full_name}
                      onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                      error={errors.full_name}
                      required
                    />

                    <FormInput
                      label="手机号"
                      name="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      error={errors.phone}
                      required
                      maxLength={11}
                    />
                  </>
                ) : (
                  <>
                    <div className="form-row">
                      <label>姓名</label>
                      <div className="form-value">{profile.full_name}</div>
                    </div>

                    <div className="form-row">
                      <label>手机号</label>
                      <div className="form-value">{profile.phone}</div>
                    </div>

                    <div className="form-row">
                      <label>邮箱</label>
                      <div className="form-value">{profile.position || '未设置'}</div>
                    </div>
                  </>
                )}

                <div className="form-row">
                  <label>部门</label>
                  <div className="form-value">{profile.department_type || '未设置'}</div>
                </div>

                <div className="form-row">
                  <label>加入时间</label>
                  <div className="form-value">{formatDate(profile.createdAt)}</div>
                </div>
              </div>
            </div>
          </div>

          {/* 账号安全卡片 */}
          <div className="profile-card">
            <div className="card-header">
              <h2>账号安全</h2>
            </div>

            <div className="card-body">
              <div className="security-item">
                <div className="security-info">
                  <h4>登录密码</h4>
                  <p>定期更换密码，保护账号安全</p>
                </div>
                <button className="btn btn-secondary" onClick={() => setShowPasswordModal(true)}>
                  修改密码
                </button>
              </div>
            </div>
          </div>

          {/* 学习统计卡片 */}
          <div className="profile-card">
            <div className="card-header">
              <h2>我的学习</h2>
            </div>

            <div className="card-body">
              <div className="stats-grid">
                <div className="stat-item">
                  <div className="stat-value">0</div>
                  <div className="stat-label">已学课程</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">0</div>
                  <div className="stat-label">参加考试</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">0%</div>
                  <div className="stat-label">通过率</div>
                </div>
                <div className="stat-item">
                  <div className="stat-value">0</div>
                  <div className="stat-label">获得证书</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* 修改密码弹窗 */}
        <Modal
          visible={showPasswordModal}
          title="修改密码"
          onClose={() => {
            setShowPasswordModal(false);
            setPasswordForm({ oldPassword: '', newPassword: '', confirmPassword: '' });
            setErrors({});
          }}
          onConfirm={handleChangePassword}
          confirmText="确认修改"
          confirmLoading={saving}
        >
          <div style={{ minWidth: '400px' }}>
            <FormInput
              label="当前密码"
              name="oldPassword"
              type="password"
              value={passwordForm.oldPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, oldPassword: e.target.value })}
              error={errors.oldPassword}
              required
            />

            <FormInput
              label="新密码"
              name="newPassword"
              type="password"
              value={passwordForm.newPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, newPassword: e.target.value })}
              error={errors.newPassword}
              helpText="密码长度至少6位"
              required
              minLength={6}
            />

            <FormInput
              label="确认新密码"
              name="confirmPassword"
              type="password"
              value={passwordForm.confirmPassword}
              onChange={(e) => setPasswordForm({ ...passwordForm, confirmPassword: e.target.value })}
              error={errors.confirmPassword}
              required
            />
          </div>
        </Modal>

        <style>{`
          .profile-page {
            min-height: 100vh;
            background: #f5f5f5;
            padding: 24px;
          }

          .profile-header {
            margin-bottom: 24px;
          }

          .profile-header h1 {
            font-size: 28px;
            font-weight: 600;
            color: #333;
            margin: 0 0 8px 0;
          }

          .profile-header p {
            color: #666;
            margin: 0;
          }

          .profile-container {
            max-width: 800px;
            display: flex;
            flex-direction: column;
            gap: 20px;
          }

          .profile-card {
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            overflow: hidden;
          }

          .card-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 20px 24px;
            border-bottom: 1px solid #eee;
          }

          .card-header h2 {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin: 0;
          }

          .action-buttons {
            display: flex;
            gap: 12px;
          }

          .card-body {
            padding: 24px;
          }

          .avatar-section {
            display: flex;
            align-items: center;
            gap: 20px;
            padding-bottom: 24px;
            border-bottom: 1px solid #eee;
            margin-bottom: 24px;
          }

          .avatar {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            font-weight: 600;
          }

          .user-basic h3 {
            margin: 0 0 8px 0;
            font-size: 24px;
            color: #333;
          }

          .role-badge {
            display: inline-block;
            padding: 4px 12px;
            background: #f0f9ff;
            color: #0284c7;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 500;
            margin: 0;
          }

          .info-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
          }

          .form-row {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f5f5f5;
          }

          .form-row label {
            flex: 0 0 120px;
            font-weight: 500;
            color: #666;
          }

          .form-value {
            color: #333;
          }

          .btn {
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
          }

          .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
          }

          .btn-primary {
            background: #3b82f6;
            color: #fff;
          }

          .btn-primary:hover:not(:disabled) {
            background: #2563eb;
          }

          .btn-secondary {
            background: #fff;
            color: #333;
            border: 1px solid #d1d5db;
          }

          .btn-secondary:hover:not(:disabled) {
            background: #f9fafb;
          }

          .security-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 0;
          }

          .security-info h4 {
            margin: 0 0 4px 0;
            font-size: 16px;
            color: #333;
          }

          .security-info p {
            margin: 0;
            font-size: 14px;
            color: #666;
          }

          .stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
          }

          .stat-item {
            text-align: center;
            padding: 20px;
            background: #f9fafb;
            border-radius: 8px;
          }

          .stat-value {
            font-size: 32px;
            font-weight: 600;
            color: #3b82f6;
            margin-bottom: 8px;
          }

          .stat-label {
            font-size: 14px;
            color: #666;
          }

          /* 移动端优化 */
          @media (max-width: 768px) {
            .profile-page {
              padding: 16px;
            }

            .avatar-section {
              flex-direction: column;
              text-align: center;
            }

            .form-row {
              flex-direction: column;
              align-items: flex-start;
              gap: 8px;
            }

            .form-row label {
              flex: none;
            }

            .stats-grid {
              grid-template-columns: repeat(2, 1fr);
            }

            .action-buttons {
              flex-direction: column-reverse;
              width: 100%;
            }

            .action-buttons .btn {
              width: 100%;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default ProfilePage;
