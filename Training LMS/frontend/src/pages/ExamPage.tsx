import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { examAPI } from '../api';
import { Exam, Question, AnswerSubmit, ExamResult } from '../types';
import './ExamPage.css';

const ExamPage: React.FC = () => {
  const { examId } = useParams<{ examId: string }>();
  const navigate = useNavigate();

  const [exam, setExam] = useState<Exam | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [examStarted, setExamStarted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<ExamResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);

  useEffect(() => {
    if (examId) {
      loadExamInfo();
    }
  }, [examId]);

  // 倒计时
  useEffect(() => {
    if (examStarted && timeRemaining !== null && timeRemaining > 0) {
      const timer = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev === null || prev <= 1) {
            clearInterval(timer);
            handleAutoSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [examStarted, timeRemaining]);

  const loadExamInfo = async () => {
    if (!examId) return;

    try {
      setLoading(true);
      setError('');

      const examData = await examAPI.getDetail(parseInt(examId));
      setExam(examData);
    } catch (err: any) {
      console.error('加载考试信息失败:', err);
      setError(err.message || '加载考试信息失败');
    } finally {
      setLoading(false);
    }
  };

  const handleStartExam = async () => {
    if (!examId) return;

    try {
      setError('');

      const data = await examAPI.start(parseInt(examId));
      setQuestions(data.questions);
      setExamStarted(true);

      // 设置倒计时
      if (exam?.time_limit) {
        setTimeRemaining(exam.time_limit * 60);
      }
    } catch (err: any) {
      console.error('开始考试失败:', err);
      setError(err.message || '开始考试失败');
    }
  };

  const handleAnswerChange = (questionId: number, answer: string) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const handleSubmit = async () => {
    if (!examId) return;

    // 检查是否所有题目都已回答
    const unansweredCount = questions.length - Object.keys(answers).length;
    if (unansweredCount > 0) {
      if (!confirm(`还有 ${unansweredCount} 题未作答，确定要提交吗？`)) {
        return;
      }
    }

    try {
      setSubmitting(true);
      setError('');

      const answerList: AnswerSubmit[] = questions.map((q) => ({
        question_id: q.id,
        user_answer: answers[q.id] || '',
      }));

      const timeSpent = exam?.time_limit && timeRemaining !== null
        ? (exam.time_limit * 60 - timeRemaining)
        : undefined;

      const resultData = await examAPI.submit({
        exam_id: parseInt(examId),
        answers: answerList,
        time_spent: timeSpent,
      });

      setResult(resultData);
    } catch (err: any) {
      console.error('提交考试失败:', err);
      setError(err.message || '提交考试失败');
    } finally {
      setSubmitting(false);
    }
  };

  const handleAutoSubmit = () => {
    alert('考试时间已到，系统将自动提交！');
    handleSubmit();
  };

  const formatTime = (seconds: number) => {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>加载考试信息中...</p>
      </div>
    );
  }

  if (error && !exam) {
    return (
      <div className="page-error">
        <div className="alert alert-error">
          {error}
        </div>
        <button onClick={() => navigate('/courses')} className="btn-secondary">
          返回课程列表
        </button>
      </div>
    );
  }

  if (!exam) {
    return (
      <div className="page-error">
        <p>考试不存在</p>
        <button onClick={() => navigate('/courses')} className="btn-secondary">
          返回课程列表
        </button>
      </div>
    );
  }

  // 显示考试结果
  if (result) {
    return (
      <div className="exam-result-page">
        <div className="result-card">
          <div className={`result-header ${result.passed ? 'passed' : 'failed'}`}>
            <h1>{result.passed ? '恭喜通过！' : '未通过考试'}</h1>
            <div className="result-score">{result.score}分</div>
          </div>

          <div className="result-details">
            <div className="result-item">
              <span className="label">考试名称：</span>
              <span className="value">{result.exam_title}</span>
            </div>
            <div className="result-item">
              <span className="label">正确题数：</span>
              <span className="value">
                {result.correct_count} / {result.total_questions}
              </span>
            </div>
            <div className="result-item">
              <span className="label">尝试次数：</span>
              <span className="value">
                {result.attempt_number} / {result.max_attempts}
              </span>
            </div>
            {result.time_spent && (
              <div className="result-item">
                <span className="label">用时：</span>
                <span className="value">{formatTime(result.time_spent)}</span>
              </div>
            )}
          </div>

          {!result.passed && result.can_retake && (
            <div className="retake-info">
              <p>
                {result.next_retake_at
                  ? `可在 ${new Date(result.next_retake_at).toLocaleDateString()} 后重新考试`
                  : '可以重新考试'}
              </p>
            </div>
          )}

          <div className="result-actions">
            <button onClick={() => navigate('/courses')} className="btn-primary">
              返回课程列表
            </button>
            {result.can_retake && (
              <button
                onClick={() => {
                  setResult(null);
                  setExamStarted(false);
                  setAnswers({});
                }}
                className="btn-secondary"
              >
                重新考试
              </button>
            )}
          </div>
        </div>
      </div>
    );
  }

  // 考试开始前的信息页
  if (!examStarted) {
    return (
      <div className="exam-info-page">
        <div className="exam-info-card">
          <h1 className="exam-title">{exam.title}</h1>

          {error && (
            <div className="alert alert-error">
              {error}
            </div>
          )}

          <div className="exam-details">
            <div className="detail-item">
              <span className="label">题目数量：</span>
              <span className="value">{exam.total_questions} 题</span>
            </div>
            <div className="detail-item">
              <span className="label">及格分数：</span>
              <span className="value">{exam.pass_score} 分</span>
            </div>
            {exam.time_limit && (
              <div className="detail-item">
                <span className="label">考试时长：</span>
                <span className="value">{exam.time_limit} 分钟</span>
              </div>
            )}
            <div className="detail-item">
              <span className="label">允许重考：</span>
              <span className="value">
                {exam.allow_retake ? `是（最多${exam.max_attempts}次）` : '否'}
              </span>
            </div>
          </div>

          <div className="exam-rules">
            <h3>考试须知：</h3>
            <ul>
              <li>请认真阅读每道题目，仔细作答</li>
              {exam.time_limit && <li>考试有时间限制，请合理安排答题时间</li>}
              <li>提交后不可修改答案，请检查后再提交</li>
              {exam.allow_retake && (
                <li>本考试允许重考，每次重考有{exam.retake_cooldown_days}天冷却期</li>
              )}
            </ul>
          </div>

          <button onClick={handleStartExam} className="btn-primary btn-large">
            开始考试
          </button>
        </div>
      </div>
    );
  }

  // 答题页面
  return (
    <div className="exam-page">
      <div className="exam-header">
        <h1 className="exam-title">{exam.title}</h1>
        {timeRemaining !== null && (
          <div className={`time-remaining ${timeRemaining < 300 ? 'warning' : ''}`}>
            剩余时间：{formatTime(timeRemaining)}
          </div>
        )}
      </div>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      <div className="questions-container">
        {questions.map((question, index) => (
          <div key={question.id} className="question-card">
            <div className="question-header">
              <span className="question-number">第 {index + 1} 题</span>
              <span className="question-type">
                {question.question_type === 'single_choice' && '单选题'}
                {question.question_type === 'multiple_choice' && '多选题'}
                {question.question_type === 'true_false' && '判断题'}
                {question.question_type === 'short_answer' && '简答题'}
              </span>
            </div>

            <div className="question-content">{question.content}</div>

            <div className="question-options">
              {question.question_type === 'true_false' ? (
                <>
                  <label className="option-label">
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value="true"
                      checked={answers[question.id] === 'true'}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    />
                    <span>正确</span>
                  </label>
                  <label className="option-label">
                    <input
                      type="radio"
                      name={`question-${question.id}`}
                      value="false"
                      checked={answers[question.id] === 'false'}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                    />
                    <span>错误</span>
                  </label>
                </>
              ) : question.question_type === 'short_answer' ? (
                <textarea
                  className="answer-textarea"
                  value={answers[question.id] || ''}
                  onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                  placeholder="请输入答案..."
                  rows={4}
                />
              ) : (
                question.options.map((option) => (
                  <label key={option.label} className="option-label">
                    <input
                      type={question.question_type === 'multiple_choice' ? 'checkbox' : 'radio'}
                      name={`question-${question.id}`}
                      value={option.label}
                      checked={
                        question.question_type === 'multiple_choice'
                          ? (answers[question.id] || '').includes(option.label)
                          : answers[question.id] === option.label
                      }
                      onChange={(e) => {
                        if (question.question_type === 'multiple_choice') {
                          const current = answers[question.id] || '';
                          const newValue = e.target.checked
                            ? current + option.label
                            : current.replace(option.label, '');
                          handleAnswerChange(question.id, newValue);
                        } else {
                          handleAnswerChange(question.id, e.target.value);
                        }
                      }}
                    />
                    <span>
                      {option.label}. {option.content}
                    </span>
                  </label>
                ))
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="exam-footer">
        <div className="answer-progress">
          已答 {Object.keys(answers).length} / {questions.length} 题
        </div>
        <button
          onClick={handleSubmit}
          className="btn-primary btn-large"
          disabled={submitting}
        >
          {submitting ? '提交中...' : '提交考试'}
        </button>
      </div>
    </div>
  );
};

export default ExamPage;
