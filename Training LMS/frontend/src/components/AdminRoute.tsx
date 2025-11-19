/**
 * 管理后台路由保护组件
 * 仅允许L4及以上职级（主管、店长、区域经理、运营负责人）访问
 */
import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface AdminRouteProps {
  children: React.ReactNode;
}

// 允许访问管理后台的角色
const ADMIN_ROLES = ['L4', 'L5', 'L5+'];

const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const { user, loading, isAuthenticated } = useAuth();

  // 等待认证状态加载
  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        fontSize: '16px',
        color: '#6b7280'
      }}>
        加载中...
      </div>
    );
  }

  // 未登录，重定向到登录页
  if (!isAuthenticated || !user) {
    return <Navigate to="/login" replace />;
  }

  // 检查权限
  if (!ADMIN_ROLES.includes(user.role)) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        padding: '20px',
        textAlign: 'center'
      }}>
        <div style={{
          maxWidth: '600px',
          background: '#ffffff',
          border: '1px solid #e5e7eb',
          borderRadius: '8px',
          padding: '40px',
        }}>
          <div style={{
            fontSize: '48px',
            marginBottom: '20px'
          }}>
            🚫
          </div>
          <h1 style={{
            fontSize: '24px',
            fontWeight: 600,
            color: '#111827',
            marginBottom: '12px'
          }}>
            无访问权限
          </h1>
          <p style={{
            fontSize: '16px',
            color: '#6b7280',
            marginBottom: '24px',
            lineHeight: '1.6'
          }}>
            管理后台仅限L4及以上职级（主管、店长、区域经理、运营负责人）访问。
            <br />
            您当前的职级为：<strong>{user.role}</strong>
          </p>
          <button
            onClick={() => window.location.href = '/courses'}
            style={{
              backgroundColor: '#0066cc',
              color: 'white',
              border: 'none',
              padding: '12px 32px',
              borderRadius: '6px',
              fontSize: '16px',
              fontWeight: 500,
              cursor: 'pointer'
            }}
          >
            返回课程中心
          </button>
        </div>
      </div>
    );
  }

  // 有权限，渲染子组件
  return <>{children}</>;
};

export default AdminRoute;
