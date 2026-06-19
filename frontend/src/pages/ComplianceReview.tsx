import React, { useEffect, useState } from 'react';
import type { ComplianceResult } from '../types';
import { CheckSquare, AlertTriangle, AlertCircle, Info } from 'lucide-react';
import { getStoredAnalysisResult } from '../utils/storage';
import EmptyState from '../components/EmptyState';

export default function ComplianceReview() {
  const [compliance, setCompliance] = useState<ComplianceResult | null>(null);

  useEffect(() => {
    const data = getStoredAnalysisResult();
    if (data?.compliance) setCompliance(data.compliance);
  }, []);

  if (!compliance) {
    return (
      <div className="max-w-6xl mx-auto">
        <h2 className="text-xl font-bold text-gray-900 mb-4">合规审查</h2>
        <EmptyState title="暂无合规审查" description="完成招标分析后，将在这里展示高风险问题、警告项和人工确认清单。" />
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2"><CheckSquare size={20} /> 合规审查</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
        <div className={`rounded-lg border p-4 ${
          compliance.overall_status.includes('高风险') ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'
        }`}>
          <div className="text-sm font-semibold">总体状态</div>
          <div className={`text-lg font-bold mt-1 ${
            compliance.overall_status.includes('高风险') ? 'text-red-700' : 'text-green-700'
          }`}>{compliance.overall_status}</div>
        </div>
        <div className="bg-white rounded-lg border p-4">
          <div className="text-sm font-semibold">通过率</div>
          <div className="text-lg font-bold mt-1 text-gray-800">{compliance.pass_rate}</div>
        </div>
      </div>

      {compliance.critical_issues.length > 0 && (
        <div className="bg-white rounded-lg border p-4 mb-4">
          <h3 className="text-sm font-semibold text-red-700 mb-3 flex items-center gap-1"><AlertCircle size={16} /> 致命问题（{compliance.critical_issues.length}项）</h3>
          <div className="space-y-2">
            {compliance.critical_issues.map((c, i) => (
              <div key={i} className="flex items-start gap-2 text-sm border-l-2 border-red-300 pl-3">
                <div>
                  <span className="font-medium text-gray-800">{c.item}</span>
                  <p className="text-gray-500 text-xs mt-0.5">{c.suggestion}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {compliance.warnings.length > 0 && (
        <div className="bg-white rounded-lg border p-4 mb-4">
          <h3 className="text-sm font-semibold text-amber-700 mb-3 flex items-center gap-1"><AlertTriangle size={16} /> 警告（{compliance.warnings.length}项）</h3>
          <div className="space-y-2">
            {compliance.warnings.map((w, i) => (
              <div key={i} className="flex items-start gap-2 text-sm border-l-2 border-amber-300 pl-3">
                <div>
                  <span className="font-medium text-gray-800">{w.item}</span>
                  <p className="text-gray-500 text-xs mt-0.5">{w.suggestion}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {compliance.manual_review_items.length > 0 && (
        <div className="bg-white rounded-lg border p-4 mb-4">
          <h3 className="text-sm font-semibold text-blue-700 mb-3 flex items-center gap-1"><Info size={16} /> 待人工确认项</h3>
          <div className="space-y-1">
            {compliance.manual_review_items.map((m, i) => (
              <div key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-blue-400">-</span> {m}
              </div>
            ))}
          </div>
        </div>
      )}

      {compliance.suggestions.length > 0 && (
        <div className="bg-white rounded-lg border p-4 mb-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">修改建议</h3>
          <div className="space-y-1">
            {compliance.suggestions.map((s, i) => (
              <div key={i} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-primary-500">{i + 1}.</span> {s}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-gray-50 rounded-lg border p-4 text-xs text-gray-500">
        <strong>免责声明：</strong>{compliance.disclaimer}
      </div>
    </div>
  );
}
