import React from 'react';
import type { RiskItem } from '../types';

interface RiskTableProps {
  risks: RiskItem[];
}

const severityConfig: Record<string, { label: string; cls: string }> = {
  high: { label: '高', cls: 'bg-red-100 text-red-700' },
  medium: { label: '中', cls: 'bg-amber-100 text-amber-700' },
  low: { label: '低', cls: 'bg-green-100 text-green-700' },
};

export default function RiskTable({ risks }: RiskTableProps) {
  if (!risks.length) return <div className="text-sm text-gray-400 py-4">暂无风险数据</div>;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-gray-50">
            <th className="text-left py-2 px-3 font-medium text-gray-600">风险项</th>
            <th className="text-left py-2 px-3 font-medium text-gray-600">类型</th>
            <th className="text-center py-2 px-3 font-medium text-gray-600">等级</th>
            <th className="text-left py-2 px-3 font-medium text-gray-600">处理建议</th>
          </tr>
        </thead>
        <tbody>
          {risks.map((r, i) => {
            const cfg = severityConfig[r.severity] || severityConfig.medium;
            return (
              <tr key={i} className="border-b hover:bg-gray-50">
                <td className="py-2 px-3 max-w-xs">{r.risk}</td>
                <td className="py-2 px-3 text-gray-500">{r.risk_type}</td>
                <td className="py-2 px-3 text-center">
                  <span className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${cfg.cls}`}>
                    {cfg.label}
                  </span>
                </td>
                <td className="py-2 px-3 text-gray-500 max-w-xs">{r.action}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
