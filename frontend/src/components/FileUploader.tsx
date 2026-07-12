import React, { useRef } from 'react';
import { Upload, FileText } from 'lucide-react';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  onValidationError?: (message: string) => void;
  accept?: string;
  maxSizeBytes?: number;
}

export default function FileUploader({
  onFileSelect,
  onValidationError,
  accept = '.txt,.md,.docx,.pdf',
  maxSizeBytes = 10 * 1024 * 1024,
}: FileUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndSelect = (file: File) => {
    const extension = `.${file.name.split('.').pop()?.toLowerCase() || ''}`;
    const acceptedExtensions = accept.split(',').map((item) => item.trim().toLowerCase());
    if (!acceptedExtensions.includes(extension)) {
      onValidationError?.('仅支持 .txt、.md、.docx、.pdf 格式的招标文件');
      return;
    }
    if (file.size > maxSizeBytes) {
      onValidationError?.(`文件不能超过 ${Math.floor(maxSizeBytes / 1024 / 1024)} MB`);
      return;
    }
    onFileSelect(file);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) validateAndSelect(file);
    e.target.value = '';
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) validateAndSelect(file);
  };

  return (
    <div
      className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors cursor-pointer"
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <input ref={inputRef} type="file" accept={accept} onChange={handleChange} className="hidden" />
      <Upload className="mx-auto text-gray-400 mb-3" size={32} />
      <p className="text-sm text-gray-600">点击或拖拽上传招标文件</p>
      <p className="text-xs text-gray-400 mt-1">支持 .txt .md .docx .pdf，最大 {Math.floor(maxSizeBytes / 1024 / 1024)} MB</p>
    </div>
  );
}
