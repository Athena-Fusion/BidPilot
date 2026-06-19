import React, { useState } from 'react';
import type { ReportFile } from '../types';
import { FileText, Download, ChevronDown, ChevronUp } from 'lucide-react';

interface ReportViewerProps {
  reports: ReportFile[];
  onExport?: () => void;
}

export default function ReportViewer({ reports, onExport }: ReportViewerProps) {
  const [activeIdx, setActiveIdx] = useState(0);
  const [expanded, setExpanded] = useState(true);

  if (!reports.length) return <div className="text-sm text-gray-400 py-4">暂无报告</div>;

  return (
    <div className="bg-white rounded-lg border">
      <div className="flex items-center justify-between p-3 border-b">
        <div className="flex items-center gap-2">
          <FileText size={16} className="text-gray-500" />
          <span className="text-sm font-medium text-gray-700">{reports[activeIdx]?.name || '报告'}</span>
          <button onClick={() => setExpanded(!expanded)} className="text-gray-400 hover:text-gray-600">
            {expanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
          </button>
        </div>
        <div className="flex items-center gap-2">
          <select value={activeIdx} onChange={(e) => setActiveIdx(Number(e.target.value))} className="text-xs border rounded px-2 py-1">
            {reports.map((r, i) => (<option key={i} value={i}>{r.name}</option>))}
          </select>
          {onExport && (
            <button onClick={onExport} className="flex items-center gap-1 text-xs bg-primary-600 text-white px-3 py-1.5 rounded hover:bg-primary-700">
              <Download size={14} /> 导出
            </button>
          )}
        </div>
      </div>
      {expanded && reports[activeIdx] && (
        <div className="p-4 max-h-[600px] overflow-auto">
          <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono leading-relaxed">{reports[activeIdx].content}</pre>
        </div>
      )}
    </div>
  );
}
