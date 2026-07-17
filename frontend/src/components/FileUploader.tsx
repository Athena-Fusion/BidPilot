import React, { useRef } from 'react';
import { Upload, FileText, ShieldCheck } from 'lucide-react';

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
    <button
      type="button"
      className="group w-full border-2 border-dashed border-slate-200 bg-slate-50/70 rounded-2xl p-7 text-center hover:border-primary-400 hover:bg-primary-50/60 transition-all cursor-pointer focus-ring"
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
    >
      <input ref={inputRef} type="file" accept={accept} onChange={handleChange} className="hidden" />
      <div className="mx-auto mb-3 h-11 w-11 rounded-xl bg-white border border-slate-200 shadow-sm grid place-items-center group-hover:scale-105 group-hover:border-primary-200 transition-all">
        <Upload className="text-primary-600" size={20} />
      </div>
      <p className="text-sm font-semibold text-slate-700">上传招标文件</p>
      <p className="text-xs text-slate-500 mt-1">点击选择或直接拖拽到此处</p>
      <div className="mt-4 flex items-center justify-center gap-3 text-[11px] text-slate-400">
        <span className="inline-flex items-center gap-1"><FileText size={12} /> txt · md · docx · pdf</span>
        <span className="inline-flex items-center gap-1"><ShieldCheck size={12} /> 最大 {Math.floor(maxSizeBytes / 1024 / 1024)} MB</span>
      </div>
    </button>
  );
}
