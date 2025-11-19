import React, { useEffect } from 'react';

export interface ModalProps {
  visible: boolean;
  title?: string;
  children: React.ReactNode;
  onClose: () => void;
  onConfirm?: () => void;
  onCancel?: () => void;
  confirmText?: string;
  cancelText?: string;
  width?: string;
  footer?: React.ReactNode | null;
  closable?: boolean;
  maskClosable?: boolean;
  confirmLoading?: boolean;
  className?: string;
}

/**
 * 通用弹窗组件
 *
 * @example
 * <Modal
 *   visible={isOpen}
 *   title="确认删除"
 *   onClose={() => setIsOpen(false)}
 *   onConfirm={handleDelete}
 *   confirmText="删除"
 *   cancelText="取消"
 * >
 *   <p>确定要删除这条记录吗？</p>
 * </Modal>
 */
export const Modal: React.FC<ModalProps> = ({
  visible,
  title,
  children,
  onClose,
  onConfirm,
  onCancel,
  confirmText = '确定',
  cancelText = '取消',
  width = '520px',
  footer,
  closable = true,
  maskClosable = true,
  confirmLoading = false,
  className = '',
}) => {
  // 阻止背景滚动
  useEffect(() => {
    if (visible) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [visible]);

  // ESC键关闭
  useEffect(() => {
    const handleEsc = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && visible && closable) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEsc);
    return () => document.removeEventListener('keydown', handleEsc);
  }, [visible, closable, onClose]);

  if (!visible) {
    return null;
  }

  const handleMaskClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget && maskClosable) {
      onClose();
    }
  };

  const handleCancelClick = () => {
    if (onCancel) {
      onCancel();
    } else {
      onClose();
    }
  };

  const renderFooter = () => {
    if (footer === null) {
      return null;
    }

    if (footer) {
      return <div className="modal-footer">{footer}</div>;
    }

    return (
      <div className="modal-footer">
        <button className="btn btn-secondary" onClick={handleCancelClick} disabled={confirmLoading}>
          {cancelText}
        </button>
        {onConfirm && (
          <button className="btn btn-primary" onClick={onConfirm} disabled={confirmLoading}>
            {confirmLoading ? '处理中...' : confirmText}
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="modal-mask" onClick={handleMaskClick}>
      <div className="modal-wrapper">
        <div className={`modal-container ${className}`} style={{ width }}>
          {/* Header */}
          {(title || closable) && (
            <div className="modal-header">
              {title && <h3 className="modal-title">{title}</h3>}
              {closable && (
                <button className="modal-close" onClick={onClose} aria-label="关闭">
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path
                      d="M1 1L13 13M1 13L13 1"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                    />
                  </svg>
                </button>
              )}
            </div>
          )}

          {/* Body */}
          <div className="modal-body">{children}</div>

          {/* Footer */}
          {renderFooter()}
        </div>
      </div>

      <style>{`
        .modal-mask {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(0, 0, 0, 0.45);
          z-index: 1000;
          display: flex;
          align-items: center;
          justify-content: center;
          animation: fadeIn 0.2s ease-out;
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
          }
          to {
            opacity: 1;
          }
        }

        .modal-wrapper {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 100%;
          height: 100%;
          padding: 20px;
          overflow-y: auto;
        }

        .modal-container {
          position: relative;
          background: #fff;
          border-radius: 8px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
          max-width: 100%;
          max-height: calc(100vh - 40px);
          display: flex;
          flex-direction: column;
          animation: slideUp 0.3s ease-out;
        }

        @keyframes slideUp {
          from {
            transform: translateY(20px);
            opacity: 0;
          }
          to {
            transform: translateY(0);
            opacity: 1;
          }
        }

        .modal-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 16px 24px;
          border-bottom: 1px solid #e5e7eb;
        }

        .modal-title {
          margin: 0;
          font-size: 18px;
          font-weight: 600;
          color: #111827;
        }

        .modal-close {
          padding: 4px;
          background: none;
          border: none;
          cursor: pointer;
          color: #6b7280;
          transition: color 0.2s;
          line-height: 1;
        }

        .modal-close:hover {
          color: #111827;
        }

        .modal-body {
          padding: 24px;
          flex: 1;
          overflow-y: auto;
          color: #374151;
          font-size: 14px;
          line-height: 1.6;
        }

        .modal-footer {
          display: flex;
          align-items: center;
          justify-content: flex-end;
          gap: 12px;
          padding: 12px 24px;
          border-top: 1px solid #e5e7eb;
        }

        .btn {
          padding: 8px 16px;
          font-size: 14px;
          font-weight: 500;
          border-radius: 6px;
          border: 1px solid transparent;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-secondary {
          color: #374151;
          background: #fff;
          border-color: #d1d5db;
        }

        .btn-secondary:hover:not(:disabled) {
          background: #f9fafb;
          border-color: #9ca3af;
        }

        .btn-primary {
          color: #fff;
          background: #3b82f6;
          border-color: #3b82f6;
        }

        .btn-primary:hover:not(:disabled) {
          background: #2563eb;
          border-color: #2563eb;
        }

        /* 移动端优化 */
        @media (max-width: 640px) {
          .modal-wrapper {
            padding: 10px;
          }

          .modal-container {
            max-height: calc(100vh - 20px);
          }

          .modal-header {
            padding: 12px 16px;
          }

          .modal-title {
            font-size: 16px;
          }

          .modal-body {
            padding: 16px;
          }

          .modal-footer {
            padding: 10px 16px;
            flex-direction: column-reverse;
            gap: 8px;
          }

          .modal-footer .btn {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default Modal;
