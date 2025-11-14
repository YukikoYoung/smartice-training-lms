/**
 * Axios客户端配置
 */
import axios from 'axios';

// 创建axios实例
export const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器 - 自动添加Token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // 401未授权 - 跳转到登录页
      if (error.response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
      }

      // 返回错误信息
      return Promise.reject({
        status: error.response.status,
        message: error.response.data?.detail || '请求失败',
        data: error.response.data,
      });
    }

    // 网络错误
    return Promise.reject({
      status: 0,
      message: '网络连接失败，请检查网络',
    });
  }
);
