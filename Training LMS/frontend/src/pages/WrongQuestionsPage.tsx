import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Modal } from '../components/common';
import { wrongQuestionAPI, type WrongQuestion } from '../api/feature';

const WrongQuestionsPage: React.FC = () => {
  const [questions, setQuestions] = useState<WrongQuestion[]>([]);
  const [filteredQuestions, setFilteredQuestions] = useState<WrongQuestion[]>([]);
  const [courseFilter, setCourseFilter] = useState<string | 'all'>('all');
  const [showMastered, setShowMastered] = useState(false);
  const [selectedQuestion, setSelectedQuestion] = useState<WrongQuestion | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);

  useEffect(() => {
    loadWrongQuestions();
  }, []);

  const loadWrongQuestions = async () => {
    try {
      const data = await wrongQuestionAPI.getList();
      setQuestions(data);
    } catch (error) {
      console.error('Failed to load wrong questions:', error);
      setQuestions([]);
    }
  };

  useEffect(() => {
    let filtered = [...questions];

    if (courseFilter !== 'all') {
      filtered = filtered.filter(q => q.course_name === courseFilter);
    }

    if (!showMastered) {
      filtered = filtered.filter(q => !q.mastered);
    }

    setFilteredQuestions(filtered);
  }, [questions, courseFilter, showMastered]);

  const markAsMastered = async (id: number) => {
    try {
      await wrongQuestionAPI.markAsMastered(id);
      // 重新加载错题列表
      await loadWrongQuestions();
    } catch (error) {
      console.error('Failed to mark as mastered:', error);
      alert('操作失败，请重试');
    }
  };

  const viewDetail = (question: WrongQuestion) => {
    setSelectedQuestion(question);
    setShowDetailModal(true);
  };

  const startPractice = () => {
    const unmasteredQuestions = questions.filter(q => !q.mastered);
    if (unmasteredQuestions.length === 0) {
      alert('暂无需要练习的错题');
      return;
    }
    alert(`准备开始错题练习模式！\n题目数量：${unmasteredQuestions.length}道\n\n功能开发中，敬请期待！`);
  };

  const getQuestionTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      single_choice: '单选题',
      multiple_choice: '多选题',
      true_false: '判断题',
    };
    return labels[type] || type;
  };

  const uniqueCourses = Array.from(new Set(questions.map(q => q.course_name)));

  return (
    <Layout>
      <div className="wrong-questions-page">
        <div className="page-header">
          <div>
            <h1>错题本</h1>
            <p>回顾错题，查缺补漏，巩固知识</p>
          </div>
          <button className="btn btn-primary" onClick={startPractice}>
            开始练习
          </button>
        </div>

        <div className="stats-cards">
          <div className="stat-card">
            <div className="stat-value">{questions.length}</div>
            <div className="stat-label">总错题数</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{questions.filter(q => !q.mastered).length}</div>
            <div className="stat-label">待掌握</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{questions.filter(q => q.mastered).length}</div>
            <div className="stat-label">已掌握</div>
          </div>
        </div>

        <div className="filters">
          <select
            className="filter-select"
            value={courseFilter}
            onChange={(e) => setCourseFilter(e.target.value)}
          >
            <option value="all">全部课程</option>
            {uniqueCourses.map(courseName => (
              <option key={courseName} value={courseName}>{courseName}</option>
            ))}
          </select>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={showMastered}
              onChange={(e) => setShowMastered(e.target.checked)}
            />
            显示已掌握
          </label>
        </div>

        <div className="questions-list">
          {filteredQuestions.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🎉</div>
              <p>{showMastered ? '暂无错题' : '暂无待掌握的错题'}</p>
            </div>
          ) : (
            filteredQuestions.map(question => (
              <div key={question.id} className={`question-card ${question.mastered ? 'mastered' : ''}`}>
                <div className="question-header">
                  <div className="question-meta">
                    <span className="question-type">{getQuestionTypeLabel(question.question_type)}</span>
                    <span className="course-name">{question.course_name}</span>
                  </div>
                  <span className="wrong-count">错误{question.wrong_count}次</span>
                </div>

                <div className="question-content">
                  <h3>{question.content}</h3>
                  {question.options && (
                    <div className="options">
                      {Object.entries(question.options).map(([key, value]) => (
                        <div
                          key={key}
                          className={`option ${
                            question.correct_answer.split(',').includes(key) ? 'correct' :
                            question.my_answer.split(',').includes(key) ? 'wrong' : ''
                          }`}
                        >
                          <span className="option-key">{key}.</span>
                          <span className="option-value">{value}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="question-footer">
                  <button className="btn-link" onClick={() => viewDetail(question)}>
                    查看解析
                  </button>
                  {!question.mastered && (
                    <button className="btn-link" onClick={() => markAsMastered(question.id)}>
                      标记为已掌握
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        <Modal
          visible={showDetailModal}
          title="题目详情"
          onClose={() => setShowDetailModal(false)}
          footer={null}
          width="700px"
        >
          {selectedQuestion && (
            <div className="question-detail">
              <h3>{selectedQuestion.content}</h3>

              {selectedQuestion.options && (
                <div className="detail-options">
                  {Object.entries(selectedQuestion.options).map(([key, value]) => (
                    <div key={key} className="detail-option">
                      <span className="option-key">{key}.</span> {value}
                    </div>
                  ))}
                </div>
              )}

              <div className="answer-section">
                <div className="answer-item wrong">
                  <strong>我的答案：</strong>{selectedQuestion.my_answer}
                </div>
                <div className="answer-item correct">
                  <strong>正确答案：</strong>{selectedQuestion.correct_answer}
                </div>
              </div>

              <div className="explanation">
                <strong>解析：</strong>
                <p>{selectedQuestion.explanation}</p>
              </div>
            </div>
          )}
        </Modal>

        <style>{`
          .wrong-questions-page {
            padding: 24px;
            background: #f5f5f5;
            min-height: 100vh;
          }

          .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
          }

          .page-header h1 {
            font-size: 28px;
            font-weight: 600;
            margin: 0 0 8px 0;
          }

          .page-header p {
            color: #666;
            margin: 0;
          }

          .stats-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
          }

          .stat-card {
            background: #fff;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
          }

          .stat-value {
            font-size: 36px;
            font-weight: 600;
            color: #3b82f6;
          }

          .stat-label {
            font-size: 14px;
            color: #666;
            margin-top: 8px;
          }

          .filters {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-bottom: 20px;
          }

          .filter-select {
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
          }

          .checkbox-label {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            cursor: pointer;
          }

          .questions-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
          }

          .question-card {
            background: #fff;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid #ef4444;
          }

          .question-card.mastered {
            border-left-color: #10b981;
            opacity: 0.7;
          }

          .question-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 16px;
          }

          .question-meta {
            display: flex;
            gap: 12px;
          }

          .question-type {
            padding: 4px 12px;
            background: #f3f4f6;
            border-radius: 4px;
            font-size: 13px;
            color: #666;
          }

          .course-name {
            font-size: 14px;
            color: #666;
          }

          .wrong-count {
            color: #ef4444;
            font-size: 14px;
            font-weight: 500;
          }

          .question-content h3 {
            font-size: 16px;
            margin: 0 0 16px 0;
            color: #333;
          }

          .options {
            display: flex;
            flex-direction: column;
            gap: 8px;
          }

          .option {
            padding: 12px;
            background: #f9fafb;
            border-radius: 6px;
            border: 2px solid transparent;
          }

          .option.correct {
            background: #d1fae5;
            border-color: #10b981;
          }

          .option.wrong {
            background: #fee2e2;
            border-color: #ef4444;
          }

          .option-key {
            font-weight: 600;
            margin-right: 8px;
          }

          .question-footer {
            display: flex;
            gap: 16px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid #e5e7eb;
          }

          .btn {
            padding: 8px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            border: none;
            cursor: pointer;
          }

          .btn-primary {
            background: #3b82f6;
            color: #fff;
          }

          .btn-link {
            background: none;
            border: none;
            color: #3b82f6;
            cursor: pointer;
            font-size: 14px;
          }

          .btn-link:hover {
            text-decoration: underline;
          }

          .empty-state {
            text-align: center;
            padding: 60px 20px;
            background: #fff;
            border-radius: 12px;
          }

          .empty-icon {
            font-size: 64px;
            margin-bottom: 16px;
          }

          .question-detail h3 {
            font-size: 18px;
            margin-bottom: 16px;
          }

          .detail-options {
            margin: 16px 0;
          }

          .detail-option {
            padding: 10px;
            margin-bottom: 8px;
            background: #f9fafb;
            border-radius: 6px;
          }

          .answer-section {
            margin: 24px 0;
            display: flex;
            flex-direction: column;
            gap: 12px;
          }

          .answer-item {
            padding: 12px;
            border-radius: 6px;
          }

          .answer-item.wrong {
            background: #fee2e2;
            color: #991b1b;
          }

          .answer-item.correct {
            background: #d1fae5;
            color: #065f46;
          }

          .explanation {
            padding: 16px;
            background: #f0f9ff;
            border-radius: 6px;
          }

          .explanation p {
            margin: 8px 0 0 0;
            line-height: 1.6;
          }

          @media (max-width: 768px) {
            .stats-cards {
              grid-template-columns: 1fr;
            }

            .page-header {
              flex-direction: column;
              align-items: flex-start;
              gap: 16px;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default WrongQuestionsPage;
