import React from 'react';
import type { ScoringItem } from '../types';

interface ScoreTableProps {
  items: ScoringItem[];
  highValueItems?: ScoringItem[];
}

export default function ScoreTable({ items, highValueItems = [] }: ScoreTableProps) {
  if (!items.length) return <div className="text-sm text-gray-400 py-4">暂无评分数据</div>;

  const highNames = new Set(highValueItems.map((h) => h.item));

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b bg-gray-50">
            <th className="text-left py-2 px-3 font-medium text-gray-600">评分项</th>
            <th className="text-center py-2 px-3 font-medium text-gray-600">分值</th>
            <th className="text-center py-2 px-3 font-medium text-gray-600">权重</th>
            <th className="text-left py-2 px-3 font-medium text-gray-600">得分策略</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item, i) => (
            <tr key={i} className={`border-b hover:bg-gray-50 ${highNames.has(item.item) ? 'bg-blue-50/50' : ''}`}>
              <td className="py-2 px-3">
                {highNames.has(item.item) && <span className="text-amber-500 mr-1">★</span>}
                {item.item}
              </td>
              <td className="py-2 px-3 text-center font-medium">{item.score}</td>
              <td className="py-2 px-3 text-center">
                <span className={`px-1.5 py-0.5 rounded text-xs ${
                  item.weight === '高' ? 'bg-red-100 text-red-700' : item.weight === '中' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-600'
                }`}>
                  {item.weight}
                </span>
              </td>
              <td className="py-2 px-3 text-gray-500 max-w-xs">{item.strategy || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
