import React from 'react';
import type { ResponseTableRow } from '../types';

interface ResponseTableProps {
  rows: ResponseTableRow[];
  title?: string;
}

const deviationConfig: Record<string, string> = {
  '正偏离': 'bg-green-100 text-green-700',
  '负偏离': 'bg-red-100 text-red-700',
  '无偏离': 'bg-gray-100 text-gray-600',
};

export default function ResponseTable({ rows, title }: ResponseTableProps) {
  if (!rows.length) return <div className="text-sm text-gray-400 py-4">暂无响应表数据</div>;

  return (
    <div>
      {title && <h4 className="text-sm font-medium text-gray-700 mb-2">{title}</h4>}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b bg-gray-50">
              <th className="text-center py-2 px-2 font-medium text-gray-600 w-10">序号</th>
              <th className="text-left py-2 px-2 font-medium text-gray-600">招标要求</th>
              <th className="text-left py-2 px-2 font-medium text-gray-600">响应内容</th>
              <th className="text-center py-2 px-2 font-medium text-gray-600">偏离</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr key={r.id} className="border-b hover:bg-gray-50">
                <td className="py-2 px-2 text-center text-gray-400">{r.id}</td>
                <td className="py-2 px-2 max-w-xs">{r.tender_requirement}</td>
                <td className="py-2 px-2 text-gray-600 max-w-xs">{r.response}</td>
                <td className="py-2 px-2 text-center">
                  <span className={`inline-block px-2 py-0.5 rounded text-xs ${deviationConfig[r.deviation] || 'bg-gray-100 text-gray-600'}`}>
                    {r.deviation || '-'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
