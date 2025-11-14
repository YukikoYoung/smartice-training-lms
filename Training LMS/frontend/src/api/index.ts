/**
 * API服务层统一导出
 */
import { apiClient } from './client';
import type {
  Course,
  Chapter,
  Content,
  Exam,
  Question,
  ExamSubmit,
  ExamResult,
  CourseProgress,
  ChapterProgress,
  LearningStats,
  ExamRecord,
} from '../types';

// ========== 课程相关API ==========
export const courseAPI = {
  // 获取课程列表
  getList: async (): Promise<Course[]> => {
    const response = await apiClient.get<Course[]>('/api/courses/');
    return response.data;
  },

  // 获取课程详情
  getDetail: async (courseId: number): Promise<Course> => {
    const response = await apiClient.get<Course>(`/api/courses/${courseId}`);
    return response.data;
  },

  // 获取课程的章节列表
  getChapters: async (courseId: number): Promise<Chapter[]> => {
    const response = await apiClient.get<Chapter[]>(`/api/courses/${courseId}/chapters`);
    return response.data;
  },

  // 获取章节详情
  getChapter: async (chapterId: number): Promise<Chapter> => {
    const response = await apiClient.get<Chapter>(`/api/courses/chapters/${chapterId}`);
    return response.data;
  },

  // 获取章节的内容列表
  getContents: async (chapterId: number): Promise<Content[]> => {
    const response = await apiClient.get<Content[]>(
      `/api/courses/chapters/${chapterId}/contents`
    );
    return response.data;
  },
};

// ========== 考试相关API ==========
export const examAPI = {
  // 获取考试列表
  getList: async (): Promise<Exam[]> => {
    const response = await apiClient.get<Exam[]>('/api/exams/');
    return response.data;
  },

  // 获取考试详情
  getDetail: async (examId: number): Promise<Exam> => {
    const response = await apiClient.get<Exam>(`/api/exams/${examId}`);
    return response.data;
  },

  // 获取题目列表
  getQuestions: async (params?: { exam_id?: number }): Promise<Question[]> => {
    const response = await apiClient.get<Question[]>('/api/exams/questions', { params });
    return response.data;
  },

  // 开始考试
  start: async (examId: number): Promise<any> => {
    const response = await apiClient.post(`/api/exams/${examId}/start`);
    return response.data;
  },

  // 提交考试
  submit: async (data: ExamSubmit): Promise<ExamResult> => {
    const response = await apiClient.post<ExamResult>('/api/exams/submit', data);
    return response.data;
  },

  // 获取考试记录
  getRecords: async (examId?: number): Promise<ExamRecord[]> => {
    const params = examId ? { exam_id: examId } : undefined;
    const response = await apiClient.get<ExamRecord[]>('/api/exams/records', { params });
    return response.data;
  },
};

// ========== 学习进度相关API ==========
export const learningAPI = {
  // 开始学习课程
  startCourse: async (courseId: number): Promise<CourseProgress> => {
    const response = await apiClient.post<CourseProgress>(
      `/api/learning/courses/${courseId}/start`
    );
    return response.data;
  },

  // 获取课程学习进度
  getCourseProgress: async (courseId?: number): Promise<CourseProgress[]> => {
    const params = courseId ? { course_id: courseId } : undefined;
    const response = await apiClient.get<CourseProgress[]>(
      '/api/learning/courses/progress',
      { params }
    );
    return response.data;
  },

  // 开始学习章节
  startChapter: async (chapterId: number): Promise<ChapterProgress> => {
    const response = await apiClient.post<ChapterProgress>(
      `/api/learning/chapters/${chapterId}/start`
    );
    return response.data;
  },

  // 完成章节
  completeChapter: async (chapterId: number): Promise<ChapterProgress> => {
    const response = await apiClient.post<ChapterProgress>(
      `/api/learning/chapters/${chapterId}/complete`
    );
    return response.data;
  },

  // 获取章节学习进度
  getChapterProgress: async (courseId?: number): Promise<ChapterProgress[]> => {
    const params = courseId ? { course_id: courseId } : undefined;
    const response = await apiClient.get<ChapterProgress[]>(
      '/api/learning/chapters/progress',
      { params }
    );
    return response.data;
  },

  // 获取学习统计
  getStats: async (): Promise<LearningStats> => {
    const response = await apiClient.get<LearningStats>('/api/learning/stats');
    return response.data;
  },
};

// 统一导出
export { authAPI } from './auth';
