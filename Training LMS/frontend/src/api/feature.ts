/**
 * 辅助功能相关API
 * 包括：通知、笔记、错题本、证书、排行榜、搜索、个人资料
 */
import { apiClient } from './client';

// ========== 类型定义 ==========
export interface Notification {
  id: number;
  type: 'system' | 'exam' | 'training' | 'achievement';
  title: string;
  content: string;
  is_read: boolean;
  created_at: string;
  read_at?: string;
}

export interface Note {
  id: number;
  title: string;
  content: string;
  course_id?: number;
  chapter_id?: number;
  created_at: string;
  updated_at: string;
}

export interface NoteCreate {
  title: string;
  content: string;
  course_id?: number;
  chapter_id?: number;
}

export interface WrongQuestion {
  id: number;
  question_id: number;
  course_name: string;
  question_type: 'single_choice' | 'multiple_choice' | 'true_false';
  content: string;
  options: Record<string, string>;
  my_answer: string;
  correct_answer: string;
  explanation: string;
  wrong_count: number;
  last_wrong_date: string;
  mastered: boolean;
}

export interface Certificate {
  id: number;
  certificate_number: string;
  title: string;
  course_id?: number;
  exam_record_id?: number;
  score: number;
  issued_at: string;
  issuer: string;
}

export interface LeaderboardEntry {
  user_id: number;
  username: string;
  full_name: string;
  role: string;
  exam_count: number;
  average_score: number;
  certificate_count: number;
  rank: number;
}

export interface SearchResult {
  courses: Array<{
    id: number;
    title: string;
    description: string;
    type: 'course';
  }>;
  notes: Array<{
    id: number;
    title: string;
    content: string;
    type: 'note';
  }>;
  questions: Array<{
    id: number;
    content: string;
    type: 'question';
  }>;
}

export interface ProfileUpdate {
  full_name?: string;
  phone?: string;
}

// ========== 通知系统API ==========
export const notificationAPI = {
  // 获取通知列表
  getList: async (params?: { type?: string; is_read?: boolean }): Promise<Notification[]> => {
    const response = await apiClient.get<Notification[]>('/api/features/notifications', {
      params,
    });
    return response.data;
  },

  // 标记单个通知为已读
  markAsRead: async (id: number): Promise<void> => {
    await apiClient.put(`/api/features/notifications/${id}/read`);
  },

  // 全部标记为已读
  markAllAsRead: async (): Promise<void> => {
    await apiClient.put('/api/features/notifications/read-all');
  },
};

// ========== 学习笔记API ==========
export const noteAPI = {
  // 获取笔记列表
  getList: async (params?: { course_id?: number; search?: string }): Promise<Note[]> => {
    const response = await apiClient.get<Note[]>('/api/features/notes', { params });
    return response.data;
  },

  // 创建笔记
  create: async (data: NoteCreate): Promise<Note> => {
    const response = await apiClient.post<Note>('/api/features/notes', data);
    return response.data;
  },

  // 更新笔记
  update: async (id: number, data: Partial<NoteCreate>): Promise<Note> => {
    const response = await apiClient.put<Note>(`/api/features/notes/${id}`, data);
    return response.data;
  },

  // 删除笔记
  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/features/notes/${id}`);
  },
};

// ========== 错题本API ==========
export const wrongQuestionAPI = {
  // 获取错题列表
  getList: async (params?: {
    course_id?: number;
    show_mastered?: boolean;
  }): Promise<WrongQuestion[]> => {
    const response = await apiClient.get<WrongQuestion[]>('/api/features/wrong-questions', {
      params,
    });
    return response.data;
  },

  // 标记为已掌握
  markAsMastered: async (id: number): Promise<void> => {
    await apiClient.put(`/api/features/wrong-questions/${id}/master`);
  },
};

// ========== 证书API ==========
export const certificateAPI = {
  // 获取证书列表
  getList: async (): Promise<Certificate[]> => {
    const response = await apiClient.get<Certificate[]>('/api/features/certificates');
    return response.data;
  },
};

// ========== 排行榜API ==========
export const leaderboardAPI = {
  // 获取排行榜
  getList: async (params?: { period?: 'week' | 'month' | 'all' }): Promise<LeaderboardEntry[]> => {
    const response = await apiClient.get<LeaderboardEntry[]>('/api/features/leaderboard', {
      params,
    });
    return response.data;
  },
};

// ========== 全局搜索API ==========
export const searchAPI = {
  // 搜索
  search: async (query: string): Promise<SearchResult> => {
    const response = await apiClient.get<SearchResult>('/api/features/search', {
      params: { q: query },
    });
    return response.data;
  },
};

// ========== 个人资料API ==========
export const profileAPI = {
  // 获取个人资料
  get: async (): Promise<any> => {
    const response = await apiClient.get('/api/features/profile');
    return response.data;
  },

  // 更新个人资料
  update: async (data: ProfileUpdate): Promise<any> => {
    const response = await apiClient.put('/api/features/profile', data);
    return response.data;
  },
};

// 统一导出
export const featureAPI = {
  notification: notificationAPI,
  note: noteAPI,
  wrongQuestion: wrongQuestionAPI,
  certificate: certificateAPI,
  leaderboard: leaderboardAPI,
  search: searchAPI,
  profile: profileAPI,
};
