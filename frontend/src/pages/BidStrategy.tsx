import React, { useEffect, useState } from 'react';
import type { StrategyResult } from '../types';
import { Target, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import { getStoredAnalysisResult } from '../utils/storage';
import EmptyState from '../components/EmptyState';

export default function BidStrategy() {
  const [strategy, setStrategy] = useState<StrategyResult | null>(null);

  useEffect(() => {
    const data = getStoredAnalysisResult();
    if (data?.strategy) setStrategy(data.strategy);
  }, []);

  if (!strategy) {
    return (
      <div className="max-w-6xl mx-auto">
        <h2 className="text-xl font-bold text-gray-900 mb-4">投标策略</h2>
        <EmptyState title="暂无投标策略" description="完成招标分析后，将在这里展示投标建议、胜算评估和材料清单。" />
      </div>
    );
  }

  const recColor = strategy.recommendation.includes('不建议') ? 'red' : strategy.recommendation.includes('谨慎') ? 'amber' : 'green';
  const recBg: Record<string, string> = { red: 'bg-red-50 border-red-200 text-red-700', amber: 'bg-amber-50 border-amber-200 text-amber-700', green: 'bg-green-50 border-green-200 text-green-700' };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2"><Target size={20} /> 投标策略</h2>

      <div className={`rounded-lg border p-4 mb-4 ${recBg[recColor] || recBg.green}`}>
        <div className="flex items-center gap-2 font-semibold">
          {recColor === 'red' ? <AlertTriangle size={18} /> : <CheckCircle size={18} />}
          投标建议：{strategy.recommendation}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className="bg-white rounded-lg border p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-1"><TrendingUp size={14} /> 胜算评估</h3>
          <p className="text-sm text-gray-600">{strategy.win_assessment}</p>
        </div>
        <div className="bg-white rounded-lg border p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">报价建议</h3>
          <p className="text-sm text-gray-600">{strategy.price_suggestion}</p>
        </div>
      </div>

      <div className="bg-white rounded-lg border p-4 mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">核心得分策略</h3>
        <div className="space-y-2">
          {strategy.score_strategy.map((s, i) => (
            <div key={i} className="flex items-start gap-2 text-sm">
              <span className="text-primary-600 font-bold flex-shrink-0">{i + 1}.</span>
              <span className="text-gray-600">{s}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg border p-4 mb-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-3">材料准备清单</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {strategy.material_checklist.map((m, i) => (
            <div key={i} className="flex items-center gap-2 text-sm">
              <input type="checkbox" className="rounded" />
              <span className="text-gray-600">{m}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg border p-4">
        <h3 className="text-sm font-semibold text-gray-700 mb-2">管理层摘要</h3>
        <p className="text-sm text-gray-600">{strategy.management_summary}</p>
      </div>

      <div className="mt-4 text-xs text-gray-400">
        策略建议仅作为投标辅助参考，最终决策需由投标负责人确认。不涉及围标、串标、控标建议。
      </div>
    </div>
  );
}
