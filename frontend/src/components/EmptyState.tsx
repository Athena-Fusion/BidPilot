import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FileSearch } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
}

export default function EmptyState({
  title = '暂无分析结果',
  description = '请先选择示例招标文件并执行一键分析。',
}: EmptyStateProps) {
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg border p-8 text-center">
      <div className="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-primary-50 text-primary-600">
        <FileSearch size={18} />
      </div>
      <div className="text-sm font-medium text-gray-700">{title}</div>
      <p className="mt-1 text-sm text-gray-400">{description}</p>
      <button
        onClick={() => navigate('/analysis')}
        className="mt-4 inline-flex items-center gap-1 rounded bg-primary-600 px-4 py-2 text-sm text-white hover:bg-primary-700"
      >
        <FileSearch size={14} />
        去招标分析
      </button>
    </div>
  );
}
