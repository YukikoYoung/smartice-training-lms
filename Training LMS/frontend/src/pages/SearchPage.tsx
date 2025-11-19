import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { searchAPI, type SearchResult } from '../api/feature';

const SearchPage: React.FC = () => {
  const navigate = useNavigate();
  const [keyword, setKeyword] = useState('');
  const [results, setResults] = useState<SearchResult | null>(null);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!keyword.trim()) {
      alert('请输入搜索关键词');
      return;
    }

    try {
      setSearching(true);
      const data = await searchAPI.search(keyword);
      setResults(data);
    } catch (error) {
      console.error('Search failed:', error);
      alert('搜索失败，请重试');
    } finally {
      setSearching(false);
    }
  };

  return (
    <Layout>
      <div className="search-page">
        <h1>课程搜索</h1>

        <div className="search-box">
          <input
            type="text"
            placeholder="搜索课程、笔记、题目..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
          />
          <button className="btn btn-primary" onClick={handleSearch} disabled={searching}>
            {searching ? '搜索中...' : '搜索'}
          </button>
        </div>

        {results && (
          <div className="results">
            {results.courses.length > 0 && (
              <div className="result-section">
                <h2>课程 ({results.courses.length})</h2>
                <div className="result-list">
                  {results.courses.map(item => (
                    <div key={item.id} className="result-item" onClick={() => navigate(`/courses/${item.id}`)}>
                      <div className="result-type">📚</div>
                      <div className="result-content">
                        <div className="result-title">{item.title}</div>
                        <div className="result-desc">{item.description}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {results.notes.length > 0 && (
              <div className="result-section">
                <h2>笔记 ({results.notes.length})</h2>
                <div className="result-list">
                  {results.notes.map(item => (
                    <div key={item.id} className="result-item" onClick={() => navigate('/notes')}>
                      <div className="result-type">📝</div>
                      <div className="result-content">
                        <div className="result-title">{item.title}</div>
                        <div className="result-desc">{item.content}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {results.questions.length > 0 && (
              <div className="result-section">
                <h2>题目 ({results.questions.length})</h2>
                <div className="result-list">
                  {results.questions.map(item => (
                    <div key={item.id} className="result-item">
                      <div className="result-type">❓</div>
                      <div className="result-content">
                        <div className="result-title">{item.content}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {results.courses.length === 0 && results.notes.length === 0 && results.questions.length === 0 && (
              <div className="empty-state">
                <div style={{ fontSize: '48px', marginBottom: '16px' }}>🔍</div>
                <p>未找到相关内容</p>
              </div>
            )}
          </div>
        )}

        <style>{`
          .search-page { padding: 24px; background: #f5f5f5; min-height: 100vh; }
          .search-page h1 { font-size: 28px; margin-bottom: 24px; }
          .search-box { display: flex; gap: 12px; margin-bottom: 32px; }
          .search-input { flex: 1; padding: 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; }
          .btn { padding: 10px 24px; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; }
          .btn-primary { background: #3b82f6; color: #fff; }
          .btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

          .results { display: flex; flex-direction: column; gap: 24px; }
          .result-section { background: #fff; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
          .result-section h2 { margin: 0 0 16px 0; font-size: 18px; color: #333; }
          .result-list { display: flex; flex-direction: column; gap: 12px; }
          .result-item { display: flex; gap: 16px; padding: 16px; background: #f9fafb; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
          .result-item:hover { background: #f3f4f6; transform: translateX(4px); }
          .result-type { font-size: 24px; flex-shrink: 0; }
          .result-content { flex: 1; min-width: 0; }
          .result-title { font-weight: 500; margin-bottom: 4px; color: #333; }
          .result-desc { font-size: 13px; color: #666; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

          .empty-state { text-align: center; padding: 60px 20px; background: #fff; border-radius: 12px; }
          .empty-state p { color: #9ca3af; margin: 0; }
        `}</style>
      </div>
    </Layout>
  );
};

export default SearchPage;
