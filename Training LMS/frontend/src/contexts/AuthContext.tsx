/**
 * 用户认证Context
 */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { authAPI } from '../api';
import type { User, LoginRequest } from '../types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 初始化时检查是否已登录
    const initAuth = async () => {
      if (authAPI.isAuthenticated()) {
        try {
          const cachedUser = authAPI.getCachedUser();
          if (cachedUser) {
            setUser(cachedUser);
          } else {
            // 从服务器获取最新用户信息
            const currentUser = await authAPI.getCurrentUser();
            setUser(currentUser);
          }
        } catch (error) {
          console.error('获取用户信息失败:', error);
          authAPI.logout();
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authAPI.login({ username, password });
    setUser(response.user);
  };

  const logout = () => {
    authAPI.logout();
    setUser(null);
  };

  const value = {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
