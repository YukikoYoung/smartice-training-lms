import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { courseAPI, learningAPI } from '../api';
import { Chapter, Content, ChapterProgress } from '../types';
import config from '../config/env';
import './StudyPage.css';

const StudyPage: React.FC = () => {
  const { courseId, chapterId } = useParams<{ courseId: string; chapterId: string }>();
  const navigate = useNavigate();

  const [chapter, setChapter] = useState<Chapter | null>(null);
  const [contents, setContents] = useState<Content[]>([]);
  const [progress, setProgress] = useState<ChapterProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);
  const [error, setError] = useState('');
  // 存储每个文档内容的Markdown文本，key为content.id
  const [documentContents, setDocumentContents] = useState<Record<number, string>>({});

  useEffect(() => {
    if (courseId && chapterId) {
      loadChapterData();
    }
  }, [courseId, chapterId]);

  // 当contents加载完成后，加载所有document类型的文件内容
  useEffect(() => {
    if (contents.length > 0) {
      loadAllDocumentContents();
    }
  }, [contents]);

  const loadChapterData = async () => {
    if (!courseId || !chapterId) return;

    try {
      setLoading(true);
      setError('');

      // 并行加载章节信息、内容列表、进度信息
      const [chapterData, contentsData, progressData] = await Promise.all([
        courseAPI.getChapter(parseInt(chapterId)),
        courseAPI.getContents(parseInt(chapterId)),
        learningAPI.getChapterProgress(parseInt(courseId)).catch(() => []),
      ]);

      setChapter(chapterData);
      setContents(contentsData);

      // 找到当前章节的进度
      const currentProgress = progressData.find(
        (p) => p.chapter_id === parseInt(chapterId)
      );
      setProgress(currentProgress || null);

      // 如果章节还未开始，自动开始学习
      if (!currentProgress || currentProgress.status === 'not_started') {
        await learningAPI.startChapter(parseInt(chapterId));
        // 重新加载进度
        const updatedProgress = await learningAPI.getChapterProgress(parseInt(courseId));
        const newProgress = updatedProgress.find(
          (p) => p.chapter_id === parseInt(chapterId)
        );
        setProgress(newProgress || null);
      }
    } catch (err: any) {
      console.error('加载章节数据失败:', err);
      setError(err.message || '加载章节数据失败');
    } finally {
      setLoading(false);
    }
  };

  // 加载所有文档类型内容的Markdown文件
  const loadAllDocumentContents = async () => {
    const documentContentsList = contents.filter(
      (c) => c.content_type === 'document' && c.file_url
    );

    for (const content of documentContentsList) {
      try {
        // 从后端加载Markdown文件
        // file_url格式: "/content/fronthall/ch1/service-etiquette.md"
        // 如果file_url以/开头，直接拼接；否则添加/
        const url = content.file_url.startsWith('/')
          ? `${config.apiBaseUrl}${content.file_url}`
          : `${config.apiBaseUrl}/${content.file_url}`;
        const response = await fetch(url);
        if (response.ok) {
          const text = await response.text();
          setDocumentContents((prev) => ({ ...prev, [content.id]: text }));
        } else {
          console.error(`加载文档失败: ${content.file_url}`, response.status);
          setDocumentContents((prev) => ({
            ...prev,
            [content.id]: '# 文档加载失败\n\n无法从服务器加载此文档内容。',
          }));
        }
      } catch (err) {
        console.error(`加载文档失败: ${content.file_url}`, err);
        setDocumentContents((prev) => ({
          ...prev,
          [content.id]: '# 文档加载失败\n\n网络错误，请检查连接。',
        }));
      }
    }
  };

  const handleCompleteChapter = async () => {
    if (!chapterId) return;

    try {
      setCompleting(true);
      setError('');

      await learningAPI.completeChapter(parseInt(chapterId));

      alert('恭喜！章节已完成');
      // 返回课程详情页
      navigate(`/courses/${courseId}`);
    } catch (err: any) {
      console.error('完成章节失败:', err);
      setError(err.message || '完成章节失败');
    } finally {
      setCompleting(false);
    }
  };

  const renderContent = (content: Content) => {
    switch (content.content_type) {
      case 'document':
        return (
          <div className="content-document">
            {documentContents[content.id] ? (
              <div className="content-text markdown-body">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {documentContents[content.id]}
                </ReactMarkdown>
              </div>
            ) : content.file_url ? (
              <div className="content-loading">
                <div className="spinner"></div>
                <p>加载文档中...</p>
              </div>
            ) : content.text_content ? (
              <div
                className="content-text"
                dangerouslySetInnerHTML={{ __html: content.text_content }}
              />
            ) : (
              <p className="content-placeholder">文档内容待加载</p>
            )}
          </div>
        );

      case 'video':
        return (
          <div className="content-video">
            {content.file_url ? (
              <video controls className="video-player">
                <source src={content.file_url} type="video/mp4" />
                您的浏览器不支持视频播放
              </video>
            ) : (
              <p className="content-placeholder">视频文件待上传</p>
            )}
            {content.duration && (
              <p className="content-duration">时长：{content.duration} 分钟</p>
            )}
          </div>
        );

      case 'image':
        return (
          <div className="content-image">
            {content.file_url ? (
              <img src={content.file_url} alt={content.title} className="content-img" />
            ) : (
              <p className="content-placeholder">图片待上传</p>
            )}
          </div>
        );

      case 'audio':
        return (
          <div className="content-audio">
            {content.file_url ? (
              <audio controls className="audio-player">
                <source src={content.file_url} type="audio/mpeg" />
                您的浏览器不支持音频播放
              </audio>
            ) : (
              <p className="content-placeholder">音频文件待上传</p>
            )}
          </div>
        );

      default:
        return <p className="content-placeholder">未知内容类型</p>;
    }
  };

  if (loading) {
    return (
      <div className="page-loading">
        <div className="spinner"></div>
        <p>加载章节内容中...</p>
      </div>
    );
  }

  if (error && !chapter) {
    return (
      <div className="page-error">
        <div className="alert alert-error">
          {error}
          <button onClick={loadChapterData} className="btn-retry">
            重试
          </button>
        </div>
        <button onClick={() => navigate(`/courses/${courseId}`)} className="btn-secondary">
          返回课程详情
        </button>
      </div>
    );
  }

  if (!chapter) {
    return (
      <div className="page-error">
        <p>章节不存在</p>
        <button onClick={() => navigate(`/courses/${courseId}`)} className="btn-secondary">
          返回课程详情
        </button>
      </div>
    );
  }

  return (
    <div className="study-page">
      <button
        onClick={() => navigate(`/courses/${courseId}`)}
        className="btn-back"
      >
        ← 返回课程详情
      </button>

      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {/* 章节头部 */}
      <div className="chapter-header">
        <h1 className="chapter-title">{chapter.title}</h1>
        {chapter.description && (
          <p className="chapter-description">{chapter.description}</p>
        )}

        {/* 进度信息 */}
        {progress && (
          <div className="progress-info">
            <div className="progress-status">
              {progress.status === 'completed' ? (
                <span className="status-badge status-completed">已完成</span>
              ) : progress.status === 'in_progress' ? (
                <span className="status-badge status-in-progress">学习中</span>
              ) : (
                <span className="status-badge status-not-started">未开始</span>
              )}
            </div>
            {chapter.estimated_duration && (
              <span className="chapter-duration">
                预计学习时间：{chapter.estimated_duration} 分钟
              </span>
            )}
          </div>
        )}
      </div>

      {/* 学习内容 */}
      <div className="study-content">
        {contents.length === 0 ? (
          <div className="empty-state">
            <p>暂无学习内容</p>
          </div>
        ) : (
          <div className="contents-list">
            {contents.map((content, index) => (
              <div key={content.id} className="content-item">
                <div className="content-header">
                  <h3 className="content-title">
                    {index + 1}. {content.title}
                  </h3>
                  <span className="content-type-tag">{getContentTypeLabel(content.content_type)}</span>
                </div>
                <div className="content-body">{renderContent(content)}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 完成章节按钮 */}
      {progress?.status !== 'completed' && (
        <div className="action-footer">
          <button
            onClick={handleCompleteChapter}
            className="btn-primary btn-large"
            disabled={completing}
          >
            {completing ? '提交中...' : '完成本章节'}
          </button>
          <p className="action-hint">
            完成后可以继续学习下一章节或参加测验
          </p>
        </div>
      )}

      {progress?.status === 'completed' && (
        <div className="completed-message">
          <p className="completed-text">✅ 您已完成本章节的学习</p>
          <button
            onClick={() => navigate(`/courses/${courseId}`)}
            className="btn-primary"
          >
            返回课程继续学习
          </button>
        </div>
      )}
    </div>
  );
};

// 辅助函数：获取内容类型标签
const getContentTypeLabel = (type: string): string => {
  const labels: Record<string, string> = {
    document: '文档',
    video: '视频',
    image: '图片',
    audio: '音频',
  };
  return labels[type] || type;
};

export default StudyPage;
