import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Layout.css';

const Layout: React.FC = () => {
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
            </nav>

            <div className="user-menu">
              <div className="user-info">
                <span className="user-name">{user?.full_name || user?.username}</span>
                <span className="user-role">{user?.role}</span>
              </div>
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
          <Outlet />
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
