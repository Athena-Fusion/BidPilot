import React, { useEffect, useState } from 'react';
import type { AnalysisResult } from '../types';
import ReportViewer from '../components/ReportViewer';
import ResponseTableComp from '../components/ResponseTable';
import { api } from '../api/client';
import { FileText, Download } from 'lucide-react';
import { getStoredAnalysisResult } from '../utils/storage';
import EmptyState from '../components/EmptyState';

export default function DocumentWriter() {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [exporting, setExporting] = useState(false);
  const [exportMessage, setExportMessage] = useState('');
  const [exportError, setExportError] = useState('');

  useEffect(() => {
    const stored = getStoredAnalysisResult();
    if (stored) setResult(stored);
  }, []);

  const handleExport = async () => {
    if (!result) return;
    setExporting(true);
    setExportMessage('');
    setExportError('');
    try {
      await api.exportMarkdown(result.task_id);
      setExportMessage('Markdown 报告已导出到 backend/data/outputs/' + result.task_id);
    } catch (e) {
      setExportError(e instanceof Error ? e.message : '导出失败');
    } finally {
      setExporting(false);
    }
  };

  if (!result) {
    return (
      <div className="max-w-6xl mx-auto">
        <h2 className="text-xl font-bold text-gray-900 mb-4">标书生成</h2>
        <EmptyState title="暂无标书初稿" description="完成招标分析后，将在这里展示技术方案、商务响应、响应表和偏离表。" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-900 flex items-center gap-2"><FileText size={20} /> 标书生成</h2>
        <button onClick={handleExport} disabled={exporting} className="flex items-center gap-1 text-sm bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700 disabled:opacity-50">
          <Download size={14} /> {exporting ? '导出中...' : '导出Markdown'}
        </button>
      </div>

      {exportMessage && (
        <div className="mb-4 rounded border border-green-200 bg-green-50 px-3 py-2 text-sm text-green-700">{exportMessage}</div>
      )}
      {exportError && (
        <div className="mb-4 rounded border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">{exportError}</div>
      )}

      {/* 技术方案 */}
      <div className="bg-white rounded-lg border p-4 mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">技术方案初稿（{result.solution.sections.length}章节，约{result.solution.total_words}字）</h3>
        <div className="space-y-3">
          {result.solution.sections.map((s, i) => (
            <div key={i} className="border-l-2 border-primary-200 pl-3">
              <h4 className="text-sm font-medium text-gray-800">{s.title}</h4>
              <p className="text-xs text-gray-500 mt-1 whitespace-pre-line">{s.content}</p>
              {s.needs_review && <span className="text-xs text-amber-600 italic">（需人工确认）</span>}
            </div>
          ))}
        </div>
      </div>

      {/* 商务响应 */}
      <div className="bg-white rounded-lg border p-4 mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">商务响应（{result.business_response.items.length}项）</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead><tr className="border-b bg-gray-50">
              <th className="text-left py-2 px-3 font-medium text-gray-600">条款</th>
              <th className="text-left py-2 px-3 font-medium text-gray-600">要求</th>
              <th className="text-left py-2 px-3 font-medium text-gray-600">响应</th>
            </tr></thead>
            <tbody>
              {result.business_response.items.map((item, i) => (
                <tr key={i} className="border-b hover:bg-gray-50">
                  <td className="py-2 px-3 font-medium">{item.clause}</td>
                  <td className="py-2 px-3 text-gray-500">{item.requirement}</td>
                  <td className="py-2 px-3 text-gray-600">{item.response}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* 响应表 */}
      <div className="bg-white rounded-lg border p-4 mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">技术响应表</h3>
        <ResponseTableComp rows={result.response_tables.technical_response} />
        {result.response_tables.business_response.length > 0 && (
          <>
            <h3 className="text-sm font-semibold text-gray-700 mt-4 mb-3">商务响应表</h3>
            <ResponseTableComp rows={result.response_tables.business_response} />
          </>
        )}
      </div>

      {/* 报告预览 */}
      <div className="mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">报告预览</h3>
        <ReportViewer reports={result.reports.files} onExport={handleExport} />
      </div>

      <div className="text-xs text-gray-400 mt-4">
        标书内容为AI辅助生成初稿，需人工确认和完善。不确定内容已标注"需人工确认"。
      </div>
    </div>
  );
}
