import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { Modal, FormInput } from '../components/common';
import { noteAPI } from '../api/feature';

interface Note {
  id: number;
  course_id: number;
  course_name: string;
  chapter_id?: number;
  chapter_name?: string;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
}

const NotesPage: React.FC = () => {
  const [notes, setNotes] = useState<Note[]>([]);
  const [filteredNotes, setFilteredNotes] = useState<Note[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [editingNote, setEditingNote] = useState<Note | null>(null);
  const [searchKeyword, setSearchKeyword] = useState('');

  const [formData, setFormData] = useState({
    title: '',
    content: '',
    courseId: 0,
    courseName: '',
  });

  useEffect(() => {
    loadNotes();
  }, []);

  const loadNotes = async () => {
    try {
      const data = await noteAPI.getList();
      setNotes(data);
    } catch (error) {
      console.error('Failed to load notes:', error);
      setNotes([]);
    }
  };

  useEffect(() => {
    let filtered = [...notes];

    if (searchKeyword.trim()) {
      filtered = filtered.filter(note =>
        note.title.toLowerCase().includes(searchKeyword.toLowerCase()) ||
        note.content.toLowerCase().includes(searchKeyword.toLowerCase())
      );
    }

    setFilteredNotes(filtered);
  }, [notes, searchKeyword]);

  const handleCreate = () => {
    setEditingNote(null);
    setFormData({ title: '', content: '', courseId: 1, courseName: '前厅服务基础' });
    setShowModal(true);
  };

  const handleEdit = (note: Note) => {
    setEditingNote(note);
    setFormData({
      title: note.title,
      content: note.content,
      courseId: note.course_id,
      courseName: note.course_name,
    });
    setShowModal(true);
  };

  const handleSave = async () => {
    if (!formData.title.trim() || !formData.content.trim()) {
      alert('请填写标题和内容');
      return;
    }

    try {
      if (editingNote) {
        await noteAPI.update(editingNote.id, {
          title: formData.title,
          content: formData.content,
        });
      } else {
        await noteAPI.create({
          title: formData.title,
          content: formData.content,
          course_id: formData.courseId,
        });
      }

      // 重新加载笔记列表
      await loadNotes();
      setShowModal(false);
    } catch (error) {
      console.error('Failed to save note:', error);
      alert('保存失败，请重试');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('确定要删除这条笔记吗？')) return;

    try {
      await noteAPI.delete(id);
      // 重新加载笔记列表
      await loadNotes();
    } catch (error) {
      console.error('Failed to delete note:', error);
      alert('删除失败，请重试');
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Layout>
      <div className="notes-page">
        <div className="page-header">
          <div>
            <h1>学习笔记</h1>
            <p>记录学习心得，巩固知识要点</p>
          </div>
          <button className="btn btn-primary" onClick={handleCreate}>
            新建笔记
          </button>
        </div>

        <div className="search-bar">
          <input
            type="text"
            className="search-input"
            placeholder="搜索笔记标题或内容..."
            value={searchKeyword}
            onChange={(e) => setSearchKeyword(e.target.value)}
          />
          <span className="notes-count">共 {filteredNotes.length} 条笔记</span>
        </div>

        <div className="notes-grid">
          {filteredNotes.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">📝</div>
              <p>{searchKeyword ? '未找到匹配的笔记' : '暂无笔记，点击"新建笔记"开始记录'}</p>
            </div>
          ) : (
            filteredNotes.map(note => (
              <div key={note.id} className="note-card">
                <div className="note-header">
                  <h3>{note.title}</h3>
                  <div className="note-actions">
                    <button className="btn-icon" onClick={() => handleEdit(note)}>✏️</button>
                    <button className="btn-icon" onClick={() => handleDelete(note.id)}>🗑️</button>
                  </div>
                </div>

                <div className="note-meta">
                  <span className="course-tag">{note.course_name}</span>
                  {note.chapter_name && <span className="chapter-tag">{note.chapter_name}</span>}
                </div>

                <div className="note-content">
                  {note.content}
                </div>

                <div className="note-footer">
                  <span className="note-date">
                    {note.updated_at !== note.created_at ? '编辑于 ' : '创建于 '}
                    {formatDate(note.updated_at)}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>

        <Modal
          visible={showModal}
          title={editingNote ? '编辑笔记' : '新建笔记'}
          onClose={() => setShowModal(false)}
          onConfirm={handleSave}
          confirmText="保存"
          width="700px"
        >
          <div className="note-form">
            <FormInput
              label="笔记标题"
              name="title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              placeholder="输入笔记标题"
              required
            />

            <div className="form-group">
              <label className="form-label">
                笔记内容 <span className="required-mark">*</span>
              </label>
              <textarea
                className="note-textarea"
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                placeholder="记录学习心得、知识要点、疑问等..."
                rows={10}
              />
            </div>
          </div>
        </Modal>

        <style>{`
          .notes-page {
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

          .search-bar {
            display: flex;
            gap: 16px;
            align-items: center;
            margin-bottom: 24px;
          }

          .search-input {
            flex: 1;
            padding: 10px 16px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
          }

          .notes-count {
            color: #666;
            font-size: 14px;
            white-space: nowrap;
          }

          .notes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 20px;
          }

          .note-card {
            background: #fff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s;
          }

          .note-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
          }

          .note-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
          }

          .note-header h3 {
            font-size: 18px;
            margin: 0;
            color: #333;
            flex: 1;
          }

          .note-actions {
            display: flex;
            gap: 4px;
          }

          .btn-icon {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 16px;
            padding: 4px;
            opacity: 0.6;
            transition: opacity 0.2s;
          }

          .btn-icon:hover {
            opacity: 1;
          }

          .note-meta {
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
          }

          .course-tag, .chapter-tag {
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 500;
          }

          .course-tag {
            background: #dbeafe;
            color: #1e40af;
          }

          .chapter-tag {
            background: #f3f4f6;
            color: #6b7280;
          }

          .note-content {
            color: #4b5563;
            font-size: 14px;
            line-height: 1.8;
            margin-bottom: 16px;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
            flex: 1;
          }

          .note-footer {
            padding-top: 12px;
            border-top: 1px solid #e5e7eb;
          }

          .note-date {
            font-size: 13px;
            color: #9ca3af;
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

          .empty-state {
            grid-column: 1 / -1;
            text-align: center;
            padding: 60px 20px;
            background: #fff;
            border-radius: 12px;
          }

          .empty-icon {
            font-size: 64px;
            margin-bottom: 16px;
          }

          .note-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
          }

          .form-group {
            margin-bottom: 20px;
          }

          .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            font-size: 14px;
            color: #333;
          }

          .required-mark {
            color: #e53e3e;
            margin-left: 4px;
          }

          .note-textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            line-height: 1.6;
            font-family: inherit;
            resize: vertical;
          }

          .note-textarea:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
          }

          @media (max-width: 768px) {
            .notes-grid {
              grid-template-columns: 1fr;
            }

            .page-header {
              flex-direction: column;
              align-items: flex-start;
              gap: 16px;
            }

            .search-bar {
              flex-direction: column;
              align-items: stretch;
            }
          }
        `}</style>
      </div>
    </Layout>
  );
};

export default NotesPage;
