import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Layout.css';

const Layout: React.FC<{ children?: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="layout">
      {/* 顶部导航栏 */}
      <header className="header">
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <h1>SmartIce 培训系统</h1>
            </div>

            <nav className="nav">
              <Link to="/courses" className="nav-link">课程中心</Link>
              <Link to="/dashboard" className="nav-link">学习看板</Link>
              <Link to="/search" className="nav-link">课程搜索</Link>
              <Link to="/certificates" className="nav-link">我的证书</Link>
              <Link to="/wrong-questions" className="nav-link">错题本</Link>
              <Link to="/notes" className="nav-link">学习笔记</Link>
              <Link to="/leaderboard" className="nav-link">排行榜</Link>
              <Link to="/notifications" className="nav-link">消息通知</Link>
            </nav>

            <div className="user-menu">
              <div className="user-info">
                <span className="user-name">{user?.full_name || user?.username}</span>
                <span className="user-role">{user?.role}</span>
              </div>
              {/* 管理后台入口 - 仅管理员可见 */}
              {(user?.role === 'L5+' || user?.username === 'admin') && (
                <button
                  onClick={() => navigate('/admin/dashboard')}
                  className="btn-admin"
                  style={{
                    padding: '8px 16px',
                    backgroundColor: '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    fontSize: '14px',
                    fontWeight: '500',
                    marginRight: '12px',
                    transition: 'background-color 0.2s'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#059669'}
                  onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#10b981'}
                >
                  🎛️ 管理后台
                </button>
              )}
              <button onClick={handleLogout} className="btn-logout">
                退出登录
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* 主要内容区域 */}
      <main className="main-content">
        <div className="container">
          {children || <Outlet />}
        </div>
      </main>

      {/* 页脚 */}
      <footer className="footer">
        <div className="container">
          <p>© 2025 SmartIce 培训系统 - 餐饮运营数字化培训平台</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
