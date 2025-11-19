import React from 'react';

export interface Column<T> {
  key: string;
  title: string;
  dataIndex?: keyof T;
  render?: (value: any, record: T, index: number) => React.ReactNode;
  width?: string;
  align?: 'left' | 'center' | 'right';
  sorter?: boolean;
}

export interface DataTableProps<T> {
  columns: Column<T>[];
  dataSource: T[];
  loading?: boolean;
  rowKey?: keyof T | ((record: T) => string | number);
  emptyText?: string;
  onRow?: (record: T, index: number) => React.HTMLAttributes<HTMLTableRowElement>;
  className?: string;
  striped?: boolean;
  hover?: boolean;
  bordered?: boolean;
}

/**
 * 通用数据表格组件
 *
 * @example
 * <DataTable
 *   columns={[
 *     { key: 'name', title: '姓名', dataIndex: 'name' },
 *     { key: 'age', title: '年龄', dataIndex: 'age', align: 'center' },
 *     { key: 'action', title: '操作', render: (_, record) => <button>编辑</button> },
 *   ]}
 *   dataSource={users}
 *   rowKey="id"
 *   loading={isLoading}
 * />
 */
export function DataTable<T extends Record<string, any>>({
  columns,
  dataSource,
  loading = false,
  rowKey = 'id' as keyof T,
  emptyText = '暂无数据',
  onRow,
  className = '',
  striped = true,
  hover = true,
  bordered = false,
}: DataTableProps<T>) {
  const getRowKey = (record: T, index: number): string | number => {
    if (typeof rowKey === 'function') {
      return rowKey(record);
    }
    return record[rowKey] ?? index;
  };

  const getCellValue = (column: Column<T>, record: T, index: number) => {
    if (column.render) {
      return column.render(column.dataIndex ? record[column.dataIndex] : undefined, record, index);
    }
    return column.dataIndex ? record[column.dataIndex] : null;
  };

  if (loading) {
    return (
      <div className="table-loading">
        <div className="spinner"></div>
        <span>加载中...</span>

        <style>{`
          .table-loading {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px 20px;
            color: #6b7280;
          }

          .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid #e5e7eb;
            border-top-color: #3b82f6;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 12px;
          }

          @keyframes spin {
            to {
              transform: rotate(360deg);
            }
          }
        `}</style>
      </div>
    );
  }

  if (!dataSource || dataSource.length === 0) {
    return (
      <div className="table-empty">
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" className="empty-icon">
          <circle cx="32" cy="32" r="30" stroke="#e5e7eb" strokeWidth="2" />
          <path d="M32 20v24M20 32h24" stroke="#d1d5db" strokeWidth="2" strokeLinecap="round" />
        </svg>
        <p>{emptyText}</p>

        <style>{`
          .table-empty {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 60px 20px;
            color: #9ca3af;
          }

          .empty-icon {
            margin-bottom: 16px;
            opacity: 0.5;
          }

          .table-empty p {
            margin: 0;
            font-size: 14px;
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className={`data-table-wrapper ${className}`}>
      <div className="table-container">
        <table className={`data-table ${striped ? 'striped' : ''} ${hover ? 'hover' : ''} ${bordered ? 'bordered' : ''}`}>
          <thead>
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  style={{
                    width: column.width,
                    textAlign: column.align || 'left',
                  }}
                >
                  {column.title}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {dataSource.map((record, index) => {
              const key = getRowKey(record, index);
              const rowProps = onRow ? onRow(record, index) : {};

              return (
                <tr key={key} {...rowProps}>
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      style={{
                        textAlign: column.align || 'left',
                      }}
                    >
                      {getCellValue(column, record, index)}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <style>{`
        .data-table-wrapper {
          width: 100%;
          overflow: hidden;
          background: #fff;
          border-radius: 8px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .table-container {
          width: 100%;
          overflow-x: auto;
        }

        .data-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 14px;
        }

        .data-table thead {
          background-color: #f9fafb;
          border-bottom: 2px solid #e5e7eb;
        }

        .data-table th {
          padding: 12px 16px;
          font-weight: 600;
          color: #374151;
          white-space: nowrap;
        }

        .data-table td {
          padding: 12px 16px;
          color: #4b5563;
          border-bottom: 1px solid #f3f4f6;
        }

        .data-table.striped tbody tr:nth-child(even) {
          background-color: #fafafa;
        }

        .data-table.hover tbody tr:hover {
          background-color: #f3f4f6;
          transition: background-color 0.15s;
        }

        .data-table.bordered {
          border: 1px solid #e5e7eb;
        }

        .data-table.bordered th,
        .data-table.bordered td {
          border-right: 1px solid #e5e7eb;
        }

        .data-table.bordered th:last-child,
        .data-table.bordered td:last-child {
          border-right: none;
        }

        /* 移动端优化 */
        @media (max-width: 768px) {
          .table-container {
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          }

          .data-table {
            font-size: 13px;
          }

          .data-table th,
          .data-table td {
            padding: 10px 12px;
          }
        }

        /* 小屏手机优化 */
        @media (max-width: 480px) {
          .data-table {
            font-size: 12px;
          }

          .data-table th,
          .data-table td {
            padding: 8px 10px;
          }
        }
      `}</style>
    </div>
  );
}

export default DataTable;
