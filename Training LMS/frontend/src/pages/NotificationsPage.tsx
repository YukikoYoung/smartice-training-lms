import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Modal } from '../components/common';
import { notificationAPI, type Notification } from '../api/feature';

/**
 * 消息通知页面
 *
 * 功能：
 * - 查看所有通知消息
 * - 按类型筛选消息
 * - 标记已读/未读
 * - 查看消息详情
 * - 全部标记为已读
 *
 * 数据来源：localStorage（Mock数据）
 */
const NotificationsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filteredNotifications, setFilteredNotifications] = useState<Notification[]>([]);
  const [filterType, setFilterType] = useState<'all' | 'unread' | 'read'>('all');
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [selectedNotification, setSelectedNotification] = useState<Notification | null>(null);
  const [showDetailModal, setShowDetailModal] = useState(false);

  // 加载通知数据
  useEffect(() => {
    const loadNotifications = async () => {
      try {
        const data = await notificationAPI.getList();
        setNotifications(data);
      } catch (error) {
        console.error('Failed to load notifications:', error);
        // 如果加载失败，显示空列表
        setNotifications([]);
      }
    };

    loadNotifications();
  }, []);

  // 筛选通知
  useEffect(() => {
    let filtered = [...notifications];

    // 按已读/未读筛选
    if (filterType === 'unread') {
      filtered = filtered.filter(n => !n.is_read);
    } else if (filterType === 'read') {
      filtered = filtered.filter(n => n.is_read);
    }

    // 按类型筛选
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(n => n.type === categoryFilter);
    }

    setFilteredNotifications(filtered);
  }, [notifications, filterType, categoryFilter]);

  // 标记为已读
  const markAsRead = async (id: number) => {
    try {
      await notificationAPI.markAsRead(id);
      // 更新本地状态
      const updated = notifications.map(n =>
        n.id === id ? { ...n, is_read: true } : n
      );
      setNotifications(updated);
    } catch (error) {
      console.error('Failed to mark as read:', error);
    }
  };

  // 全部标记为已读
  const markAllAsRead = async () => {
    try {
      await notificationAPI.markAllAsRead();
      // 更新本地状态
      const updated = notifications.map(n => ({ ...n, is_read: true }));
      setNotifications(updated);
    } catch (error) {
      console.error('Failed to mark all as read:', error);
    }
  };

  // 查看详情
  const viewDetail = (notification: Notification) => {
    setSelectedNotification(notification);
    setShowDetailModal(true);
    if (!notification.is_read) {
      markAsRead(notification.id);
    }
  };

  // 格式化时间
  const formatTime = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now.getTime() - date.getTime();

    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return '刚刚';
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    if (days < 7) return `${days}天前`;

    return date.toLocaleDateString('zh-CN');
  };

  // 类型图标和颜色
  const getTypeConfig = (type: string) => {
    const configs: Record<string, { icon: string; color: string; label: string }> = {
      system: { icon: '🔔', color: '#3b82f6', label: '系统通知' },
      exam: { icon: '📝', color: '#f59e0b', label: '考试提醒' },
      training: { icon: '📚', color: '#10b981', label: '培训通知' },
      achievement: { icon: '🎉', color: '#8b5cf6', label: '成就通知' },
    };
    return configs[type] || configs.system;
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  return (
    <Layout>
      <div className="notifications-page">
        <div className="page-header">
          <div className="header-title">
            <h1>消息通知</h1>
            <span className="unread-badge">{unreadCount} 条未读</span>
          </div>
          {unreadCount > 0 && (
            <button className="btn btn-secondary" onClick={markAllAsRead}>
              全部标记为已读
            </button>
          )}
        </div>

        {/* 筛选栏 */}
        <div className="filter-bar">
          <div className="filter-tabs">
            <button
              className={`filter-tab ${filterType === 'all' ? 'active' : ''}`}
              onClick={() => setFilterType('all')}
            >
              全部
            </button>
            <button
              className={`filter-tab ${filterType === 'unread' ? 'active' : ''}`}
              onClick={() => setFilterType('unread')}
            >
              未读 ({notifications.filter(n => !n.is_read).length})
            </button>
            <button
              className={`filter-tab ${filterType === 'read' ? 'active' : ''}`}
              onClick={() => setFilterType('read')}
            >
              已读 ({notifications.filter(n => n.is_read).length})
            </button>
          </div>

          <div className="category-filter">
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="filter-select"
            >
              <option value="all">全部类型</option>
              <option value="system">系统通知</option>
              <option value="exam">考试提醒</option>
              <option value="training">培训通知</option>
              <option value="achievement">成就通知</option>
            </select>
          </div>
        </div>

        {/* 消息列表 */}
        <div className="notifications-list">
          {filteredNotifications.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📭</div>
              <p>暂无消息</p>
            </div>
          ) : (
            filteredNotifications.map(notification => {
              const typeConfig = getTypeConfig(notification.type);
              return (
                <div
                  key={notification.id}
                  className={`notification-item ${!notification.is_read ? 'unread' : ''}`}
                  onClick={() => viewDetail(notification)}
                >
                  <div className="notification-icon" style={{ background: typeConfig.color }}>
                    <span>{typeConfig.icon}</span>
                  </div>

                  <div className="notification-content">
                    <div className="notification-header">
                      <h3 className="notification-title">{notification.title}</h3>
                      <span className="notification-time">{formatTime(notification.created_at)}</span>
                    </div>

                    <p className="notification-preview">{notification.content}</p>

                    <div className="notification-footer">
                      <span className="notification-type" style={{ color: typeConfig.color }}>
                        {typeConfig.label}
                      </span>
                      {!notification.is_read && <span className="unread-dot"></span>}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* 详情弹窗 */}
        <Modal
          visible={showDetailModal}
          title={selectedNotification ? getTypeConfig(selectedNotification.type).label : ''}
          onClose={() => {
            setShowDetailModal(false);
            setSelectedNotification(null);
          }}
          footer={null}
          width="600px"
        >
          {selectedNotification && (
            <div className="notification-detail">
              <h2>{selectedNotification.title}</h2>
              <div className="detail-time">{formatTime(selectedNotification.created_at)}</div>
              <div className="detail-content">{selectedNotification.content}</div>
            </div>
          )}
        </Modal>

        <style>{`
          .notifications-page {
            min-height: 100vh;
            background: #f5f5f5;
            padding: 24px;
          }

          .page-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
          }

          .header-title {
            display: flex;
            align-items: center;
            gap: 12px;
          }

          .header-title h1 {
            font-size: 28px;
            font-weight: 600;
            color: #333;
            margin: 0;
          }

          .unread-badge {
            padding: 4px 12px;
            background: #fee2e2;
            color: #dc2626;
            border-radius: 12px;
            font-size: 13px;
            font-weight: 500;
          }

          .filter-bar {
            background: #fff;
            padding: 16px 24px;
            border-radius: 12px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
          }

          .filter-tabs {
            display: flex;
            gap: 8px;
          }

          .filter-tab {
            padding: 8px 16px;
            border: none;
            background: transparent;
            color: #666;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s;
          }

          .filter-tab:hover {
            background: #f3f4f6;
          }

          .filter-tab.active {
            background: #3b82f6;
            color: #fff;
          }

          .filter-select {
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            color: #333;
            cursor: pointer;
          }

          .notifications-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
          }

          .notification-item {
            display: flex;
            gap: 16px;
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            position: relative;
          }

          .notification-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
          }

          .notification-item.unread {
            background: #f0f9ff;
          }

          .notification-icon {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
          }

          .notification-content {
            flex: 1;
            min-width: 0;
          }

          .notification-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 8px;
          }

          .notification-title {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin: 0;
          }

          .notification-time {
            font-size: 13px;
            color: #9ca3af;
            flex-shrink: 0;
          }

          .notification-preview {
            color: #666;
            font-size: 14px;
            line-height: 1.6;
            margin: 0 0 12px 0;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
          }

          .notification-footer {
            display: flex;
            align-items: center;
            gap: 8px;
          }

          .notification-type {
            font-size: 12px;
            font-weight: 500;
          }

          .unread-dot {
            width: 8px;
            height: 8px;
            background: #ef4444;
            border-radius: 50%;
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

          .empty-state p {
            color: #9ca3af;
            font-size: 14px;
          }

          .notification-detail h2 {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin: 0 0 8px 0;
          }

          .detail-time {
            color: #9ca3af;
            font-size: 13px;
            margin-bottom: 16px;
          }

          .detail-content {
            color: #4b5563;
            font-size: 15px;
            line-height: 1.8;
          }

          .btn {
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
          }

          .btn-secondary {
            background: #fff;
            color: #333;
            border: 1px solid #d1d5db;
          }

          .btn-secondary:hover {
            background: #f9fafb;
          }

          /* 移动端优化 */
          @media (max-width: 768px) {
            .notifications-page {
              padding: 16px;
            }

            .page-header {
              flex-direction: column;
              align-items: flex-start;
              gap: 12px;
            }

            .filter-bar {
              flex-direction: column;
              align-items: stretch;
              gap: 12px;
            }

            .filter-tabs {
              justify-content: space-between;
            }

            .notification-item {
              padding: 16px;
            }

            .notification-icon {
              width: 40px;
              height: 40px;
              font-size: 20px;
            }

            .notification-title {
              font-size: 15px;
            }

            .notification-preview {
              -webkit-line-clamp: 1;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default NotificationsPage;
