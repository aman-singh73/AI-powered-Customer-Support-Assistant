import { useState } from 'react';

export default function Sidebar() {
  const [isDragging, setIsDragging] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploadStatus, setUploadStatus] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFiles(Array.from(e.dataTransfer.files));
    }
  };

  const handleFileSelect = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setIsUploading(true);
    setUploadStatus('Uploading...');

    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    try {
      const response = await fetch('/documents/upload', {
        method: 'POST',
        body: formData,
      });
      if (response.ok) {
        setUploadStatus('Upload successful!');
        setFiles([]);
        setTimeout(() => setUploadStatus(''), 3000);
      } else {
        setUploadStatus('Upload failed.');
      }
    } catch (error) {
      setUploadStatus('Error connecting to server.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="glass-panel sidebar">
      <h2>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/>
        </svg>
        Knowledge Base
      </h2>
      
      <div 
        className={`upload-zone ${isDragging ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => document.getElementById('file-upload').click()}
      >
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-secondary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <p>Drag & drop documents here or click to browse</p>
        <input 
          id="file-upload" 
          type="file" 
          multiple 
          accept=".pdf,.txt,.docx"
          onChange={handleFileSelect}
          style={{ display: 'none' }} 
        />
      </div>

      {files.length > 0 && (
        <div style={{ fontSize: '0.875rem' }}>
          <strong>Selected Files:</strong>
          <ul style={{ listStyleType: 'none', paddingLeft: 0, marginTop: '0.5rem', color: 'var(--text-secondary)' }}>
            {files.map((file, i) => <li key={i}>{file.name}</li>)}
          </ul>
          <button 
            className="upload-btn" 
            onClick={handleUpload}
            disabled={isUploading}
            style={{ width: '100%' }}
          >
            {isUploading ? 'Uploading...' : 'Upload to Knowledge Base'}
          </button>
        </div>
      )}

      {uploadStatus && <div className="upload-status">{uploadStatus}</div>}
    </div>
  );
}
