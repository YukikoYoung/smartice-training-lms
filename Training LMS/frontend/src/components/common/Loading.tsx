import React from 'react';

export interface LoadingProps {
  size?: 'small' | 'medium' | 'large';
  text?: string;
  fullscreen?: boolean;
  overlay?: boolean;
  className?: string;
}

/**
 * 统一的Loading加载组件
 *
 * @example
 * // 基础用法
 * <Loading text="加载中..." />
 *
 * // 全屏Loading
 * <Loading fullscreen text="数据加载中..." />
 *
 * // 局部遮罩Loading
 * <div style={{ position: 'relative', height: '400px' }}>
 *   <Loading overlay text="处理中..." />
 * </div>
 */
export const Loading: React.FC<LoadingProps> = ({
  size = 'medium',
  text,
  fullscreen = false,
  overlay = false,
  className = '',
}) => {
  const sizeMap = {
    small: 24,
    medium: 40,
    large: 56,
  };

  const spinnerSize = sizeMap[size];

  const content = (
    <div className={`loading-content ${size}`}>
      <div className="spinner" style={{ width: spinnerSize, height: spinnerSize }}></div>
      {text && <p className="loading-text">{text}</p>}

      <style>{`
        .loading-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .loading-wrapper.fullscreen {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.9);
          z-index: 9999;
          backdrop-filter: blur(4px);
        }

        .loading-wrapper.overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(255, 255, 255, 0.85);
          z-index: 100;
          backdrop-filter: blur(2px);
        }

        .loading-content {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .loading-content.small {
          gap: 8px;
        }

        .loading-content.medium {
          gap: 12px;
        }

        .loading-content.large {
          gap: 16px;
        }

        .spinner {
          border: 3px solid #e5e7eb;
          border-top-color: #3b82f6;
          border-radius: 50%;
          animation: spin 0.8s linear infinite;
        }

        .loading-content.small .spinner {
          border-width: 2px;
        }

        .loading-content.large .spinner {
          border-width: 4px;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .loading-text {
          margin: 0;
          color: #6b7280;
          font-size: 14px;
          font-weight: 500;
        }

        .loading-content.small .loading-text {
          font-size: 12px;
        }

        .loading-content.large .loading-text {
          font-size: 16px;
        }

        /* 呼吸动画 */
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.6;
          }
        }

        .loading-text {
          animation: pulse 1.5s ease-in-out infinite;
        }
      `}</style>
    </div>
  );

  if (fullscreen || overlay) {
    return (
      <div className={`loading-wrapper ${fullscreen ? 'fullscreen' : 'overlay'} ${className}`}>
        {content}
      </div>
    );
  }

  return <div className={`loading-wrapper ${className}`}>{content}</div>;
};

/**
 * Skeleton骨架屏组件
 * 用于内容加载时的占位显示
 */
export interface SkeletonProps {
  rows?: number;
  avatar?: boolean;
  title?: boolean;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  rows = 3,
  avatar = false,
  title = false,
  className = '',
}) => {
  return (
    <div className={`skeleton ${className}`}>
      {avatar && <div className="skeleton-avatar"></div>}

      <div className="skeleton-content">
        {title && <div className="skeleton-title"></div>}
        {Array.from({ length: rows }).map((_, index) => (
          <div
            key={index}
            className="skeleton-row"
            style={{
              width: index === rows - 1 ? '60%' : '100%',
            }}
          ></div>
        ))}
      </div>

      <style>{`
        .skeleton {
          display: flex;
          gap: 16px;
          padding: 16px;
          animation: fadeIn 0.3s ease-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .skeleton-avatar {
          width: 64px;
          height: 64px;
          border-radius: 50%;
          background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s infinite;
          flex-shrink: 0;
        }

        .skeleton-content {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 12px;
        }

        .skeleton-title {
          width: 40%;
          height: 20px;
          border-radius: 4px;
          background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s infinite;
        }

        .skeleton-row {
          height: 16px;
          border-radius: 4px;
          background: linear-gradient(90deg, #f3f4f6 25%, #e5e7eb 50%, #f3f4f6 75%);
          background-size: 200% 100%;
          animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
          0% {
            background-position: 200% 0;
          }
          100% {
            background-position: -200% 0;
          }
        }
      `}</style>
    </div>
  );
};

export default Loading;
