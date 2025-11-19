import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { leaderboardAPI, type LeaderboardEntry } from '../api/feature';

const LeaderboardPage: React.FC = () => {
  const [timeRange, setTimeRange] = useState<'week' | 'month' | 'all'>('month');
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, [timeRange]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await leaderboardAPI.getList({ period: timeRange });
      setLeaderboard(data);
    } catch (error) {
      console.error('Failed to load leaderboard:', error);
      setLeaderboard([]);
    } finally {
      setLoading(false);
    }
  };

  const getAvatar = (name: string) => name.charAt(0);

  const getRankColor = (rank: number) => {
    if (rank === 1) return '#fbbf24';
    if (rank === 2) return '#94a3b8';
    if (rank === 3) return '#fb923c';
    return '#e5e7eb';
  };

  return (
    <Layout>
      <div className="leaderboard-page">
        <div className="page-header">
          <h1>学习排行榜</h1>
          <p>努力学习，争创佳绩</p>
        </div>

        <div className="filters">
          <div className="filter-group">
            <button
              className={`filter-btn ${timeRange === 'week' ? 'active' : ''}`}
              onClick={() => setTimeRange('week')}
            >
              本周
            </button>
            <button
              className={`filter-btn ${timeRange === 'month' ? 'active' : ''}`}
              onClick={() => setTimeRange('month')}
            >
              本月
            </button>
            <button
              className={`filter-btn ${timeRange === 'all' ? 'active' : ''}`}
              onClick={() => setTimeRange('all')}
            >
              全部
            </button>
          </div>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px', background: '#fff', borderRadius: '12px' }}>
            加载中...
          </div>
        ) : leaderboard.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '60px', background: '#fff', borderRadius: '12px' }}>
            暂无排行榜数据
          </div>
        ) : (
          <>
            <div className="podium">
              {leaderboard.slice(0, 3).sort((a, b) => [2, 1, 3].indexOf(a.rank) - [2, 1, 3].indexOf(b.rank)).map(item => (
                <div key={item.rank} className={`podium-item rank-${item.rank}`}>
                  <div className="podium-rank">
                    <span className="rank-badge" style={{ background: getRankColor(item.rank) }}>
                      {item.rank}
                    </span>
                  </div>
                  <div className="podium-avatar">{getAvatar(item.full_name)}</div>
                  <div className="podium-name">{item.full_name}</div>
                  <div className="podium-value">{item.average_score}分</div>
                </div>
              ))}
            </div>

            <div className="rank-list">
              {leaderboard.slice(3).map(item => (
                <div key={item.user_id} className="rank-item">
                  <div className="rank-number">{item.rank}</div>
                  <div className="rank-avatar">{getAvatar(item.full_name)}</div>
                  <div className="rank-info">
                    <div className="rank-name">{item.full_name}</div>
                    <div className="rank-dept">{item.role} · 考试{item.exam_count}次 · 证书{item.certificate_count}个</div>
                  </div>
                  <div className="rank-value">{item.average_score}分</div>
                </div>
              ))}
            </div>
          </>
        )}

        <style>{`
          .leaderboard-page { padding: 24px; background: #f5f5f5; min-height: 100vh; }
          .page-header { margin-bottom: 24px; }
          .page-header h1 { font-size: 28px; margin: 0 0 8px 0; }
          .page-header p { color: #666; margin: 0; }
          .filters { display: flex; justify-content: space-between; margin-bottom: 32px; flex-wrap: wrap; gap: 12px; }
          .filter-group { display: flex; gap: 8px; }
          .filter-btn { padding: 8px 16px; border: 1px solid #d1d5db; background: #fff; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
          .filter-btn:hover { border-color: #3b82f6; }
          .filter-btn.active { background: #3b82f6; color: #fff; border-color: #3b82f6; }

          .podium { display: flex; justify-content: center; align-items: flex-end; gap: 24px; margin-bottom: 32px; padding: 32px; background: #fff; border-radius: 12px; }
          .podium-item { display: flex; flex-direction: column; align-items: center; width: 140px; }
          .podium-item.rank-1 { order: 2; }
          .podium-item.rank-2 { order: 1; }
          .podium-item.rank-3 { order: 3; }
          .podium-rank { margin-bottom: 12px; }
          .rank-badge { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-weight: 600; font-size: 18px; }
          .podium-avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 600; margin-bottom: 12px; }
          .rank-1 .podium-avatar { width: 100px; height: 100px; font-size: 40px; }
          .podium-name { font-size: 16px; font-weight: 600; margin-bottom: 4px; }
          .podium-value { font-size: 18px; color: #3b82f6; font-weight: 600; }

          .rank-list { background: #fff; border-radius: 12px; overflow: hidden; }
          .rank-item { display: flex; align-items: center; padding: 16px 24px; border-bottom: 1px solid #f3f4f6; }
          .rank-item:last-child { border-bottom: none; }
          .rank-number { width: 40px; font-size: 18px; font-weight: 600; color: #6b7280; }
          .rank-avatar { width: 48px; height: 48px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; display: flex; align-items: center; justify-content: center; font-size: 20px; font-weight: 600; margin-right: 16px; }
          .rank-info { flex: 1; }
          .rank-name { font-size: 16px; font-weight: 500; margin-bottom: 4px; }
          .rank-dept { font-size: 13px; color: #6b7280; }
          .rank-value { font-size: 18px; color: #3b82f6; font-weight: 600; }

          @media (max-width: 768px) {
            .podium { flex-direction: column; align-items: center; }
            .podium-item { order: initial !important; width: 100%; }
            .filters { flex-direction: column; }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default LeaderboardPage;
