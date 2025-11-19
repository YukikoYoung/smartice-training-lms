import { lazy, Suspense } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import AdminRoute from './components/AdminRoute';
import Layout from './components/Layout';
import { Loading } from './components/common';
import './App.css';

// ============================================================
// 代码分割：使用React.lazy实现按需加载
// 优势：减少初始加载包体积，提升首屏加载速度
// ============================================================

// 公开页面 - 立即加载
import LoginPage from './pages/LoginPage';

// 员工端页面 - 懒加载
const CoursesPage = lazy(() => import('./pages/CoursesPage'));
const CourseDetailPage = lazy(() => import('./pages/CourseDetailPage'));
const StudyPage = lazy(() => import('./pages/StudyPage'));
const ExamPage = lazy(() => import('./pages/ExamPage'));
const DashboardPage = lazy(() => import('./pages/DashboardPage'));
const ProfilePage = lazy(() => import('./pages/ProfilePage'));
const NotificationsPage = lazy(() => import('./pages/NotificationsPage'));
const CertificatesPage = lazy(() => import('./pages/CertificatesPage'));
const WrongQuestionsPage = lazy(() => import('./pages/WrongQuestionsPage'));
const NotesPage = lazy(() => import('./pages/NotesPage'));
const SearchPage = lazy(() => import('./pages/SearchPage'));
const LeaderboardPage = lazy(() => import('./pages/LeaderboardPage'));

// 管理后台页面 - 懒加载
const AdminDashboardPage = lazy(() => import('./pages/AdminDashboardPage'));
const UserManagementPage = lazy(() => import('./pages/UserManagementPage'));
const CourseManagementPage = lazy(() => import('./pages/CourseManagementPage'));
const QuestionManagementPage = lazy(() => import('./pages/QuestionManagementPage'));
const ExamManagementPage = lazy(() => import('./pages/ExamManagementPage'));

// 受保护的路由
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <Loading fullscreen text="验证身份中..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Suspense fallback={<Loading fullscreen text="页面加载中..." />}>
          <Routes>
          {/* 公开路由 */}
          <Route path="/login" element={<LoginPage />} />

          {/* 全屏页面（无导航栏） */}
          <Route
            path="/courses/:courseId/chapters/:chapterId/study"
            element={
              <ProtectedRoute>
                <StudyPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/exams/:id"
            element={
              <ProtectedRoute>
                <ExamPage />
              </ProtectedRoute>
            }
          />

          {/* 带导航栏的页面 - 使用Layout包裹 */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <Layout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/courses" replace />} />
            <Route path="courses" element={<CoursesPage />} />
            <Route path="courses/:id" element={<CourseDetailPage />} />
            <Route path="dashboard" element={<DashboardPage />} />
            <Route path="profile" element={<ProfilePage />} />
            <Route path="notifications" element={<NotificationsPage />} />
            <Route path="certificates" element={<CertificatesPage />} />
            <Route path="wrong-questions" element={<WrongQuestionsPage />} />
            <Route path="notes" element={<NotesPage />} />
            <Route path="search" element={<SearchPage />} />
            <Route path="leaderboard" element={<LeaderboardPage />} />

            {/* 管理后台路由 - 需要L4及以上权限 */}
            <Route path="admin/dashboard" element={<AdminRoute><AdminDashboardPage /></AdminRoute>} />
            <Route path="admin/users" element={<AdminRoute><UserManagementPage /></AdminRoute>} />
            <Route path="admin/courses" element={<AdminRoute><CourseManagementPage /></AdminRoute>} />
            <Route path="admin/questions" element={<AdminRoute><QuestionManagementPage /></AdminRoute>} />
            <Route path="admin/exams" element={<AdminRoute><ExamManagementPage /></AdminRoute>} />
          </Route>

          {/* 404页面 */}
          <Route path="*" element={<Navigate to="/courses" replace />} />
          </Routes>
        </Suspense>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
