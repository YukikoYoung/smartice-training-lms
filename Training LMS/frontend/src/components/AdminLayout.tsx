import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './AdminLayout.css';

interface AdminLayoutProps {
  children: React.ReactNode;
}

const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const menuItems = [
    { path: '/admin/dashboard', label: '数据看板', icon: '📊' },
    { path: '/admin/users', label: '用户管理', icon: '👥' },
    { path: '/admin/courses', label: '课程管理', icon: '📚' },
    { path: '/admin/questions', label: '题库管理', icon: '📝' },
    { path: '/admin/exams', label: '考试管理', icon: '✍️' },
  ];

  return (
    <div className="admin-layout">
      {/* 侧边栏 */}
      <aside className="admin-sidebar">
        <div className="admin-header">
          <h2>SmartIce 管理后台</h2>
          <p className="admin-user">
            <span className="user-icon">👤</span>
            {user?.username}
          </p>
        </div>

        <nav className="admin-nav">
          {menuItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="admin-footer">
          <button onClick={() => navigate('/courses')} className="btn-secondary">
            返回学员端
          </button>
          <button onClick={handleLogout} className="btn-logout">
            退出登录
          </button>
        </div>
      </aside>

      {/* 主内容区 */}
      <main className="admin-main">
        {children}
      </main>
    </div>
  );
};

export default AdminLayout;
