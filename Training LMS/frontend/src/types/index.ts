/**
 * TypeScript类型定义
 */

// ========== 用户相关 ==========
export interface User {
  id: number;
  username: string;
  full_name: string;
  phone: string;
  role: string;
  department_type: string;
  position_id: number | null;
  store_id: number | null;
  region_id: number | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// ========== 课程相关 ==========
export interface Course {
  id: number;
  title: string;
  code: string;
  description: string | null;
  department_type: string;
  category: string;
  is_mandatory: boolean;
  version: string;
  is_published: boolean;
  is_active: boolean;
  created_at: string;
  chapters?: Chapter[];
}

export interface Chapter {
  id: number;
  course_id: number;
  title: string;
  description: string | null;
  order: number;
  estimated_duration: number | null;
  has_quiz: boolean;
  is_active: boolean;
  contents?: Content[];
}

export interface Content {
  id: number;
  chapter_id: number;
  title: string;
  content_type: 'video' | 'document' | 'image' | 'audio';
  order: number;
  file_url: string | null;
  duration: number | null;
  text_content: string | null;
  is_active: boolean;
}

// ========== 考试相关 ==========
export interface Exam {
  id: number;
  title: string;
  exam_type: string;
  total_questions: number;
  pass_score: number;
  time_limit: number | null;
  allow_retake: boolean;
  max_attempts: number;
  retake_cooldown_days: number;
  is_published: boolean;
  is_active: boolean;
}

export interface Question {
  id: number;
  content: string;
  question_type: 'single_choice' | 'multiple_choice' | 'true_false' | 'short_answer';
  options: QuestionOption[];
  correct_answer: string | null;
  explanation: string | null;
  category: string;
}

export interface QuestionOption {
  label: string;
  content: string;
  is_correct?: boolean;
}

export interface AnswerSubmit {
  question_id: number;
  user_answer: string;
}

export interface ExamSubmit {
  exam_id: number;
  answers: AnswerSubmit[];
  time_spent?: number;
}

export interface ExamResult {
  exam_record_id: number;
  exam_id: number;
  exam_title: string;
  score: number;
  passed: boolean;
  attempt_number: number;
  max_attempts: number;
  can_retake: boolean;
  next_retake_at: string | null;
  correct_count: number;
  total_questions: number;
  time_spent?: number;
}

// ========== 学习进度相关 ==========
export interface CourseProgress {
  id: number;
  user_id: number;
  course_id: number;
  status: 'not_started' | 'in_progress' | 'completed';
  total_chapters: number;
  completed_chapters: number;
  progress_percentage: number;
  started_at: string | null;
  completed_at: string | null;
  last_accessed_at: string | null;
}

export interface ChapterProgress {
  id: number;
  user_id: number;
  chapter_id: number;
  course_id: number;
  status: 'not_started' | 'in_progress' | 'completed';
  total_contents: number;
  completed_contents: number;
  quiz_passed: boolean;
  started_at: string | null;
  completed_at: string | null;
}

export interface LearningStats {
  total_courses: number;
  completed_courses: number;
  in_progress_courses: number;
  total_chapters: number;
  completed_chapters: number;
  overall_progress: number;
}

export interface ExamRecord {
  id: number;
  user_id: number;
  exam_id: number;
  attempt_number: number;
  status: string;
  score: number | null;
  correct_answers: number | null;
  total_questions: number;
  started_at: string;
  submitted_at: string | null;
  can_retake: boolean;
  next_retake_at: string | null;
}
