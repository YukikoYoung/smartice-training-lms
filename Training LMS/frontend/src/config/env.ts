/**
 * 环境变量配置
 *
 * Vite环境变量必须以VITE_开头才能被暴露到客户端代码
 * 开发环境读取.env文件
 * 生产环境读取.env.production文件
 */

export const config = {
  // API基础地址
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',

  // API前缀
  apiPrefix: '/api',

  // 完整的API URL
  get apiUrl() {
    return `${this.apiBaseUrl}${this.apiPrefix}`;
  },

  // 环境模式
  isDevelopment: import.meta.env.DEV,
  isProduction: import.meta.env.PROD,
  mode: import.meta.env.MODE,
};

export default config;
