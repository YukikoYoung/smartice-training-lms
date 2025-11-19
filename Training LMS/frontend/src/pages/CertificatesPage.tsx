import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { DataTable, type Column } from '../components/common';
import { certificateAPI, type Certificate } from '../api/feature';

/**
 * 我的证书页面
 *
 * 功能：
 * - 查看已获得的证书列表
 * - 按课程筛选证书
 * - 下载证书（PDF/图片）
 * - 分享证书
 *
 * 数据来源：localStorage（Mock数据）
 */
const CertificatesPage: React.FC = () => {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [loading, setLoading] = useState(true);

  // 加载证书数据
  useEffect(() => {
    loadCertificates();
  }, []);

  const loadCertificates = async () => {
    try {
      setLoading(true);
      const data = await certificateAPI.getList();
      setCertificates(data);
    } catch (error) {
      console.error('加载证书失败:', error);
      setCertificates([]);
    } finally {
      setLoading(false);
    }
  };

  // 下载证书
  const downloadCertificate = (cert: Certificate) => {
    alert(`正在下载证书: ${cert.title}\n证书编号: ${cert.certificate_number}\n\n功能开发中，敬请期待！`);
  };

  // 分享证书
  const shareCertificate = (cert: Certificate) => {
    const shareUrl = `${window.location.origin}/certificates/${cert.id}`;
    navigator.clipboard.writeText(shareUrl);
    alert('证书链接已复制到剪贴板！');
  };

  // 表格列配置
  const columns: Column<Certificate>[] = [
    {
      key: 'title',
      title: '证书名称',
      dataIndex: 'title',
      width: '30%',
      render: (value) => <strong>{value}</strong>,
    },
    {
      key: 'certificate_number',
      title: '证书编号',
      dataIndex: 'certificate_number',
      width: '25%',
    },
    {
      key: 'score',
      title: '成绩',
      dataIndex: 'score',
      width: '10%',
      align: 'center',
      render: (value) => <span style={{ color: value >= 90 ? '#10b981' : '#3b82f6', fontWeight: 600 }}>{value}分</span>,
    },
    {
      key: 'issued_at',
      title: '颁发日期',
      dataIndex: 'issued_at',
      width: '15%',
      render: (value) => value ? new Date(value).toLocaleDateString('zh-CN') : '-',
    },
    {
      key: 'actions',
      title: '操作',
      width: '20%',
      align: 'center',
      render: (_, record) => (
        <div style={{ display: 'flex', gap: '8px', justifyContent: 'center' }}>
          <button className="btn-link" onClick={() => downloadCertificate(record)}>下载</button>
          <button className="btn-link" onClick={() => shareCertificate(record)}>分享</button>
        </div>
      ),
    },
  ];

  return (
    <Layout>
      <div className="certificates-page">
        <div className="page-header">
          <div>
            <h1>我的证书</h1>
            <p>查看和管理您获得的所有证书</p>
          </div>
          <div className="stats-summary">
            <div className="stat-item">
              <span className="stat-value">{certificates.length}</span>
              <span className="stat-label">总证书数</span>
            </div>
            <div className="stat-item">
              <span className="stat-value">{certificates.filter(c => c.score >= 90).length}</span>
              <span className="stat-label">优秀证书</span>
            </div>
          </div>
        </div>

        <DataTable
          columns={columns}
          dataSource={certificates}
          loading={loading}
          rowKey="id"
          emptyText="暂无证书，完成课程学习并通过考试即可获得证书"
        />

        <style>{`
          .certificates-page {
            padding: 24px;
            background: #f5f5f5;
            min-height: 100vh;
          }

          .page-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 24px;
          }

          .page-header h1 {
            font-size: 28px;
            font-weight: 600;
            margin: 0 0 8px 0;
            color: #333;
          }

          .page-header p {
            color: #666;
            margin: 0;
          }

          .stats-summary {
            display: flex;
            gap: 32px;
          }

          .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
          }

          .stat-value {
            font-size: 32px;
            font-weight: 600;
            color: #3b82f6;
          }

          .stat-label {
            font-size: 13px;
            color: #666;
            margin-top: 4px;
          }

          .btn-link {
            background: none;
            border: none;
            color: #3b82f6;
            cursor: pointer;
            font-size: 14px;
            padding: 4px 8px;
          }

          .btn-link:hover {
            text-decoration: underline;
          }

          @media (max-width: 768px) {
            .page-header {
              flex-direction: column;
              gap: 16px;
            }

            .stats-summary {
              width: 100%;
              justify-content: space-around;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default CertificatesPage;
