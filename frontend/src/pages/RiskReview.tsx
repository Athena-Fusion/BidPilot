import React, { useState } from 'react';
import type { RiskItem } from '../types';
import RiskTable from '../components/RiskTable';
import { ShieldAlert } from 'lucide-react';
import { getStoredAnalysisResult } from '../utils/storage';
import EmptyState from '../components/EmptyState';

interface RiskReviewProps {
  risks?: RiskItem[];
}

export default function RiskReview({ risks = [] }: RiskReviewProps) {
  const [filter, setFilter] = useState<string>('all');

  // 从 sessionStorage 恢复分析结果
  const storedResult = getStoredAnalysisResult();
  const resultRisks: RiskItem[] = risks.length > 0 ? risks : storedResult?.risks || [];
  const filtered = filter === 'all' ? resultRisks : resultRisks.filter((r) => r.severity === filter);

  const highCount = resultRisks.filter((r) => r.severity === 'high').length;
  const medCount = resultRisks.filter((r) => r.severity === 'medium').length;
  const lowCount = resultRisks.filter((r) => r.severity === 'low').length;

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <ShieldAlert size={20} /> 风险审查
      </h2>

      {resultRisks.length > 0 && (
      <div className="flex gap-3 mb-4">
        <button onClick={() => setFilter('all')} className={`px-3 py-1.5 rounded text-xs font-medium ${filter === 'all' ? 'bg-primary-600 text-white' : 'bg-white border text-gray-600'}`}>
          全部（{resultRisks.length}）
        </button>
        <button onClick={() => setFilter('high')} className={`px-3 py-1.5 rounded text-xs font-medium ${filter === 'high' ? 'bg-red-600 text-white' : 'bg-white border text-gray-600'}`}>
          高风险（{highCount}）
        </button>
        <button onClick={() => setFilter('medium')} className={`px-3 py-1.5 rounded text-xs font-medium ${filter === 'medium' ? 'bg-amber-600 text-white' : 'bg-white border text-gray-600'}`}>
          中风险（{medCount}）
        </button>
        <button onClick={() => setFilter('low')} className={`px-3 py-1.5 rounded text-xs font-medium ${filter === 'low' ? 'bg-green-600 text-white' : 'bg-white border text-gray-600'}`}>
          低风险（{lowCount}）
        </button>
      </div>
      )}

      {resultRisks.length > 0 ? (
        <div className="bg-white rounded-lg border p-4">
          <RiskTable risks={filtered} />
        </div>
      ) : (
        <EmptyState title="暂无风险清单" description="完成招标分析后，将在这里展示废标风险、商务风险和技术风险。" />
      )}

      <div className="mt-4 text-xs text-gray-400">
        风险识别为辅助审查，需人工复核确认。
      </div>
    </div>
  );
}
